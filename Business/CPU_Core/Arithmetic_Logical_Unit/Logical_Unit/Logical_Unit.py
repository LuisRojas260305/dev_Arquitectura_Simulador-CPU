from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from .Logical_MUX import MUX
from Business.Basic_Components.Logic_Gates.AND_Gate import AND_Gate
from Business.Basic_Components.Logic_Gates.OR_Gate import OR_Gate
from Business.Basic_Components.Logic_Gates.XOR_Gate import XOR_Gate
from Business.Basic_Components.Logic_Gates.NOT_Gate import NOT_Gate

class Logical_Unit:
    
    def __init__(self):
        # Gates arrays (16 de cada una, una por bit)
        self.__AND_Gates = [AND_Gate() for _ in range(16)]
        self.__OR_Gates = [OR_Gate() for _ in range(16)]
        self.__XOR_Gates = [XOR_Gate() for _ in range(16)]
        self.__NOT_Gates = [NOT_Gate() for _ in range(16)]

        # Outputs intermedios
        self.__AND_Output = Bus(16)
        self.__OR_Output = Bus(16)
        self.__XOR_Output = Bus(16)
        self.__NOT_Output = Bus(16)

        # Output final
        self.__Output = Bus(16)

        # Inputs
        self.__Input_A = Bus(16)
        self.__Input_B = Bus(16)
        self.__Mode = Bus(2)  

        # Mux interno
        self.__MUX = MUX()
    
    # --- Setters ---
    def set_Input_A(self, Input: Bus):
        if Input.width != 16:
            raise ValueError("El bus de entrada A debe ser de 16 bits")
        self.__Input_A = Input
    
    def set_Input_B(self, Input: Bus):
        if Input.width != 16:
            raise ValueError("El bus de entrada B debe ser de 16 bits")
        self.__Input_B = Input
    
    def set_Mode(self, Input: Bus):
        if Input.width != 2:
            raise ValueError("El bus de modo debe ser de 2 bits")
        self.__Mode = Input
    
    # --- Getter ---
    def get_Output(self) -> Bus:
        return self.__Output

    # --- Método principal de cálculo ---
    def Calculate(self) -> Bus:
        # Calcular todas las operaciones en paralelo
        
        # Puertas AND (bit a bit)
        for i in range(16):
            # Conectar entradas
            self.__AND_Gates[i].connect_input(self.__Input_A.get_Line_bit(i), 0)
            self.__AND_Gates[i].connect_input(self.__Input_B.get_Line_bit(i), 1)
            # Calcular y guardar resultado
            self.__AND_Gates[i].calculate()
            self.__AND_Output.set_Line_bit(i, self.__AND_Gates[i].get_output())
        
        # Puertas OR (bit a bit)
        for i in range(16):
            self.__OR_Gates[i].connect_input(self.__Input_A.get_Line_bit(i), 0)
            self.__OR_Gates[i].connect_input(self.__Input_B.get_Line_bit(i), 1)
            self.__OR_Gates[i].calculate()
            self.__OR_Output.set_Line_bit(i, self.__OR_Gates[i].get_output())
        
        # Puertas XOR (bit a bit)
        for i in range(16):
            self.__XOR_Gates[i].connect_input(self.__Input_A.get_Line_bit(i), 0)
            self.__XOR_Gates[i].connect_input(self.__Input_B.get_Line_bit(i), 1)
            self.__XOR_Gates[i].calculate()
            self.__XOR_Output.set_Line_bit(i, self.__XOR_Gates[i].get_output())
        
        # Puertas NOT (operación unaria, solo usa Input_A)
        for i in range(16):
            self.__NOT_Gates[i].connect_input(self.__Input_A.get_Line_bit(i), 0)
            self.__NOT_Gates[i].calculate()
            self.__NOT_Output.set_Line_bit(i, self.__NOT_Gates[i].get_output())
        
        # Configurar el multiplexor interno
        self.__MUX.set_input_AND(self.__AND_Output)
        self.__MUX.set_input_OR(self.__OR_Output)
        self.__MUX.set_input_XOR(self.__XOR_Output)
        self.__MUX.set_input_NOT(self.__NOT_Output)
        self.__MUX.set_select(self.__Mode)
        
        # Obtener resultado seleccionado
        self.__Output = self.__MUX.calculate()

        return self.__Output
    
    def __str__(self):
        return f"Logical_Unit(Output={self.__Output.get_Hexadecimal_value()})"