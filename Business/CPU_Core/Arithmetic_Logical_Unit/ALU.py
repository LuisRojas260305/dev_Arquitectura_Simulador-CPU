# Business/CPU_Core/Arithmetic_Logical_Unit/ALU.py
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from .Arithmetic_Unit.Arithmetic_Unit import Arithmetic_Unit
from .Logical_Unit.Logical_Unit import Logical_Unit
from .Shift_Unit.Shift_Unit import Shift_Unit
from .MUX import ALU_MUX

class ALU:
    """
    Unidad Aritmético Lógica Principal.
    Orquesta las tres unidades y selecciona el resultado según ALUop.
    """
    
    def __init__(self):
        # Componentes internos
        self.__arithmetic_unit = Arithmetic_Unit()
        self.__logical_unit = Logical_Unit()
        self.__shift_unit = Shift_Unit()
        self.__output_mux = ALU_MUX()
        
        # Entradas
        self.__input_a = Bus(16)
        self.__input_b = Bus(16)
        self.__aluop = Bus(2)      # Selección de unidad (00, 01, 10)
        self.__modo_funcion = Bus(3)  # Operación específica
        
        # Salidas
        self.__output = Bus(16)
        self.__carry_out = Bit(0)
        self.__zero_flag = Bit(0)
        self.__negative_flag = Bit(0)
        
        # Resultados intermedios
        self.__arith_result = Bus(16)
        self.__logic_result = Bus(16)
        self.__shift_result = Bus(16)
    
    # --- Setters para configuración ---
    def set_input_a(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus A debe ser de 16 bits")
        self.__input_a = bus
    
    def set_input_b(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus B debe ser de 16 bits")
        self.__input_b = bus
    
    def set_aluop(self, bus: Bus):
        if bus.width != 2:
            raise ValueError("ALUop debe ser de 2 bits")
        self.__aluop = bus
    
    def set_modo_funcion(self, bus: Bus):
        if bus.width != 3:
            raise ValueError("ModoFunción debe ser de 3 bits")
        self.__modo_funcion = bus
    
    # --- Getters para resultados ---
    def get_output(self) -> Bus:
        return self.__output
    
    def get_carry_out(self) -> Bit:
        return self.__carry_out
    
    def get_zero_flag(self) -> Bit:
        return self.__zero_flag
    
    def get_negative_flag(self) -> Bit:
        return self.__negative_flag
    
    # --- Método principal de ejecución ---
    # Business/CPU_Core/Arithmetic_Logical_Unit/ALU.py (método execute corregido)
    def execute(self) -> Bus:
        """
        Ejecuta la operación completa según ALUop y ModoFunción.
        Actualiza flags y retorna el resultado.
        """
        # 1. Extraer señales de control
        # ModoFunción es un Bus de 3 bits: bit0=LSB (resta), bit1, bit2=MSB
        # En Bus: índice 0=MSB, índice 1, índice 2=LSB
        
        # Para aritmética: bit 0 de ModoFunción es C_in (1 para resta, 0 para suma)
        # En Bus de 3 bits: bit0 está en índice 2
        c_in_bit = self.__modo_funcion.get_Line_bit(2)  # LSB del ModoFunción
        
        # Para lógica: bits 0-1 de ModoFunción
        # 00=AND, 01=OR, 10=XOR, 11=NOT
        modo_logica = Bus(2)
        # Asignar: bit1 de ModoFunción (índice 1) -> MSB de modo_logica (índice 0)
        #          bit0 de ModoFunción (índice 2) -> LSB de modo_logica (índice 1)
        modo_logica.set_Line_bit(0, self.__modo_funcion.get_Line_bit(1))  # MSB
        modo_logica.set_Line_bit(1, self.__modo_funcion.get_Line_bit(2))  # LSB
        
        # Para desplazamiento: bits 0-2 de ModoFunción
        # Mapeo: 000=SLL, 001=SRA, 010=ROL, 011=ROR, 100=LSR
        modo_desplazamiento = Bus(3)
        # Mantener el mismo orden: MSB en índice 0, LSB en índice 2
        for i in range(3):
            modo_desplazamiento.set_Line_bit(i, self.__modo_funcion.get_Line_bit(i))
        
        # 2. Ejecutar todas las unidades en paralelo
        
        # Unidad Aritmética (ADD/SUB)
        self.__arith_result, self.__carry_out = self.__arithmetic_unit.calculate(
            self.__input_a, 
            self.__input_b, 
            c_in_bit
        )
        
        # Unidad Lógica (AND, OR, XOR, NOT)
        self.__logical_unit.set_Input_A(self.__input_a)
        self.__logical_unit.set_Input_B(self.__input_b)
        self.__logical_unit.set_Mode(modo_logica)
        self.__logic_result = self.__logical_unit.Calculate()
        
        # Unidad Desplazamiento
        self.__shift_unit.set_input_A(self.__input_a)
        self.__shift_unit.set_input_B(self.__input_b)
        self.__shift_unit.set_operation_bus(modo_desplazamiento)
        self.__shift_result = self.__shift_unit.calculate()
        
        # 3. Seleccionar resultado según ALUop
        self.__output_mux.set_input_aritmetica(self.__arith_result)
        self.__output_mux.set_input_logica(self.__logic_result)
        self.__output_mux.set_input_desplazamiento(self.__shift_result)
        self.__output_mux.set_select(self.__aluop)
        self.__output = self.__output_mux.calculate()
        
        # 4. Actualizar flags
        self.__update_flags()
        
        return self.__output
    
    def __update_flags(self):
        """Actualiza los flags de estado basados en el resultado."""
        
        # Flag Zero: ¿Resultado = 0?
        is_zero = True
        for i in range(16):
            if self.__output.get_Line_bit(i).get_value() == 1:
                is_zero = False
                break
        self.__zero_flag.set_value(1 if is_zero else 0)
        
        # Flag Negative: MSB = 1 (bit 0 en Big-Endian)
        self.__negative_flag.set_value(self.__output.get_Line_bit(0).get_value())
        
        # Flag Carry ya se actualizó en la unidad aritmética
    
    # --- Método conveniente para usar con señales directas ---
    def execute_with_signals(self, a: int, b: int, aluop: int, modo_funcion: int) -> int:
        """
        Método de conveniencia para pruebas.
        a, b: valores decimales (0-65535)
        aluop: 0-3 (00, 01, 10)
        modo_funcion: 0-7 (000-111)
        Retorna resultado decimal.
        """
        # Convertir a buses
        a_bus = Bus(16)
        b_bus = Bus(16)
        a_bus.set_Binary_value(a)
        b_bus.set_Binary_value(b)
        
        aluop_bus = Bus(2)
        modo_bus = Bus(3)
        aluop_bus.set_Binary_value(aluop)
        modo_bus.set_Binary_value(modo_funcion)
        
        # Configurar
        self.set_input_a(a_bus)
        self.set_input_b(b_bus)
        self.set_aluop(aluop_bus)
        self.set_modo_funcion(modo_bus)
        
        # Ejecutar
        self.execute()
        
        return self.__output.get_Decimal_value()
    
    def __str__(self):
        hex_output = self.__output.get_Hexadecimal_value()
        return f"ALU(Out={hex_output}, Z={self.__zero_flag}, C={self.__carry_out}, N={self.__negative_flag})"