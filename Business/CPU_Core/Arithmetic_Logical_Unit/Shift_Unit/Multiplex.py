from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.MUX8to1 import MUX8to1

class Multiplex:
    # Constructor
    def __init__(self):
        # Inputs
        self.__Input_ASR = Bus(16)
        self.__Input_LSL = Bus(16)
        self.__Input_LSR = Bus(16)
        self.__Input_ROL = Bus(16)
        self.__Input_ROR = Bus(16)
        
        self.__Input_Select = Bus(3)
        
        # Output
        self.__Output = Bus(16)

        # MUX8to1 
        self.__MUX = [MUX8to1() for _ in range(16)]
    
    # --- Setters para los buses de entrada ---
    def set_input_ASR(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus debe ser de 16 bits")
        self.__Input_ASR = bus
    
    def set_input_LSL(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus debe ser de 16 bits")
        self.__Input_LSL = bus

    def set_input_LSR(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus debe ser de 16 bits")
        self.__Input_LSR = bus

    def set_input_ROL(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus debe ser de 16 bits")
        self.__Input_ROL = bus

    def set_input_ROR(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus debe ser de 16 bits")
        self.__Input_ROR = bus

    def set_select(self, select_bus: Bus):
        if select_bus.width != 3:
            raise ValueError("El bus de selección debe ser de 3 bits")
        self.__Input_Select = select_bus
    
    # --- Getter para la salida ---
    def get_output(self) -> Bus:
        return self.__Output
    
    # --- Método de cálculo principal ---
    def calculate(self):
        
        for i in range(16):
            
            data_bus = Bus(8)
            
            # Conectar los bits de cada operación:
            data_bus.set_Line_bit(0, self.__Input_LSL.get_Line_bit(i))   # 000: LSL
            data_bus.set_Line_bit(1, self.__Input_ASR.get_Line_bit(i))   # 001: ASR
            data_bus.set_Line_bit(2, self.__Input_ROL.get_Line_bit(i))   # 010: ROL
            data_bus.set_Line_bit(3, self.__Input_ROR.get_Line_bit(i))   # 011: ROR
            data_bus.set_Line_bit(4, self.__Input_LSR.get_Line_bit(i))   # 100: LSR
            data_bus.set_Line_bit(5, Bit(0))
            data_bus.set_Line_bit(6, Bit(0))
            data_bus.set_Line_bit(7, Bit(0))
            
            # Configurar el MUX actual
            self.__MUX[i].set_Data_Inputs(data_bus)
            self.__MUX[i].set_Control_Inputs(self.__Input_Select)
            
            # Calcular y obtener la salida
            output_bit = self.__MUX[i].Calculate()
            
            # Establecer el bit de salida en el bus de salida
            self.__Output.set_Line_bit(i, output_bit)
    
    def __str__(self):
        return f"Multiplexor(Output={self.__Output.get_Hexadecimal_value()})"