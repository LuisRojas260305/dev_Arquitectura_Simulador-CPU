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

    # Métodos internos
    def decode(self, Input: Bus):
        
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
    
    def __str__(self):
        active = self.get_active_line()
        return f"Decoder(Input={self.__Input.get_Binary_value()}, ActiveLine={active})"