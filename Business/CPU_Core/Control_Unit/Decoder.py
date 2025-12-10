# Business/CPU_Core/Control_Unit/Decoder.py

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Logic_Gates.AND_Gate_4 import AND_Gate_4
from Business.Basic_Components.Logic_Gates.NOT_Gate import NOT_Gate

class Decoder:
    # Constructor
    def __init__(self):
        
        self.__Input = Bus(4)
        self.__Output = Bus(16, 0)  # Inicializar con 0

        self.__NOT_Gates = [NOT_Gate() for _ in range(4)]
        self.__AND_Gates = [AND_Gate_4() for _ in range(16)]

        self.__Inverted_Bits = [None, None, None, None]
        
        # Estado actual
        self.__current_instruction = Bus(16, 0)
        self.__opcode = 0
        self.__operand = 0
        self.__instruction_type = "UNKNOWN"

    # Método principal para decodificar instrucciones de 16 bits
    def set_instruction(self, instruction_bus: Bus):
        """Decodifica una instrucción de 16 bits (MSB en índice 0)"""
        if instruction_bus.width != 16:
            raise ValueError("La instrucción debe ser un bus de 16 bits")
        
        self.__current_instruction = instruction_bus
        
        # Extraer opcode (bits 15-12, índices 0-3 en MSB-first)
        opcode = 0
        for i in range(4):  # Bits 0-3 son opcode
            bit_val = instruction_bus.get_Line_bit(i).get_value()
            opcode = (opcode << 1) | bit_val
        
        self.__opcode = opcode
        
        # Extraer operando (bits 11-0, índices 4-15)
        operand = 0
        for i in range(4, 16):  # Bits 4-15 son operando
            bit_val = instruction_bus.get_Line_bit(i).get_value()
            operand = (operand << 1) | bit_val
        
        self.__operand = operand
        
        # Determinar tipo de instrucción basado en opcode (ISA ESTANDARIZADO)
        if opcode == 0x0:
            self.__instruction_type = "NOP"
        elif opcode == 0x1:
            self.__instruction_type = "LOAD"
        elif opcode == 0x2:
            self.__instruction_type = "STORE"
        elif opcode == 0x3:
            self.__instruction_type = "ADD"
        elif opcode == 0x4:
            self.__instruction_type = "SUB"
        elif opcode == 0x5:
            self.__instruction_type = "MULT"
        elif opcode == 0x6:
            self.__instruction_type = "DIV"
        elif opcode == 0x7:
            self.__instruction_type = "JUMP"
        elif opcode == 0x8:
            self.__instruction_type = "JZ"
        elif opcode == 0x9:
            self.__instruction_type = "LOADI"
        elif opcode == 0xA:
            self.__instruction_type = "AND"
        elif opcode == 0xB:
            self.__instruction_type = "OR"
        elif opcode == 0xC:
            self.__instruction_type = "XOR"
        elif opcode == 0xD:
            self.__instruction_type = "SHL"
        elif opcode == 0xE:
            self.__instruction_type = "SHR"
        elif opcode == 0xF:
            self.__instruction_type = "HALT"
        else:
            self.__instruction_type = "UNKNOWN"
    
    # Método para decodificador 4→16 (para otros usos)
    def decode(self, Input: Bus):
        """Decodificador genérico 4→16 bits"""
        if Input.width != 4:
            raise ValueError("Decoder requiere una entrada de 4 bits")

        self.__Input = Input

        # 1. Calcular bits invertidos
        for i in range(4):
            bit = self.__Input.get_Line_bit(i)
            self.__NOT_Gates[i].connect_input(bit, 0)
            self.__NOT_Gates[i].calculate()
            self.__Inverted_Bits[i] = self.__NOT_Gates[i].get_output()

        # 2. Para cada línea de salida (0-15)
        for output_line in range(16):
            
            and_gate = self.__AND_Gates[output_line]

            # Para cada posición del bit de entrada (0=MSB, 3=LSB)
            for bit_position in range(4):
                shift_amount = 3 - bit_position  # 3 para MSB, 0 para LSB
                bit_needed = (output_line >> shift_amount) & 1

                if bit_needed == 1:
                    # Conectar bit original
                    and_gate.connect_input(
                        self.__Input.get_Line_bit(bit_position),
                        bit_position
                    )
                else:
                    # Conectar bit invertido
                    and_gate.connect_input(
                        self.__Inverted_Bits[bit_position],
                        bit_position
                    )
            
            # Calcular la puerta AND para esta línea
            and_gate.calculate()
            output_bit = and_gate.get_output()
            
            # Establecer el bit en la salida
            self.__Output.set_Line_bit(output_line, output_bit)
    
        return self.__Output
    
    # Métodos getter
    def get_opcode(self):
        return self.__opcode
    
    def get_operand(self):
        return self.__operand
    
    def get_instruction_type(self):
        return self.__instruction_type
    
    def get_Output(self, line: int) -> Bit:
        if 0 <= line < 16:
            return self.__Output.get_Line_bit(line)
        raise ValueError(f"Línea {line} fuera de rango [0-15]")
    
    def get_all_outputs(self) -> Bus:
        return self.__Output
    
    def get_active_line(self) -> int:
        """Retorna el índice de la línea activa (-1 si ninguna)"""
        for i in range(16):
            if self.__Output.get_Line_bit(i).get_value() == 1:
                return i
        return -1
    
    # NUEVO MÉTODO: Reset del decoder
    def reset(self):
        """Resetea el decoder a estado inicial"""
        self.__Input = Bus(4)
        self.__Output = Bus(16, 0)
        self.__current_instruction = Bus(16, 0)
        self.__opcode = 0
        self.__operand = 0
        self.__instruction_type = "UNKNOWN"
    
    def __str__(self):
        return (f"Decoder(Inst={self.__current_instruction.get_Hexadecimal_value()}, "
                f"Opcode=0x{self.__opcode:X}, Type={self.__instruction_type}, "
                f"Operand=0x{self.__operand:03X})")