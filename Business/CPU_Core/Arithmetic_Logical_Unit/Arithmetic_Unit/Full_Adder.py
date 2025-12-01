from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Logic_Gates.XOR_Gate import XOR_Gate
from Business.Basic_Components.Logic_Gates.AND_Gate import AND_Gate
from Business.Basic_Components.Logic_Gates.OR_Gate import OR_Gate

class Full_Adder:
    # Constructor
    def __init__(self):
        #Inputs 
        self.__Input_A = Bit(0)
        self.__Input_B = Bit(0)
        self.__C_in = Bit(0)
        
        #Outputs
        self.__Output = Bit(0)
        self.__C_out = Bit(0)

        #Gates
        self.__Xor_A = XOR_Gate()
        self.__Xor_B = XOR_Gate()
        self.__And_A = AND_Gate()
        self.__And_B = AND_Gate()
        self.__Or = OR_Gate()

    # Metodos
    def Calculate(self):
        
        # Output = A⊕B⊕Cin​
        # C_out​ = (A⋅B)+((A⊕B)⋅Cin​)

        # Primer XOR
        self.__Xor_A.connect_input(self.__Input_A, 0)
        self.__Xor_A.connect_input(self.__Input_B, 1)

        self.__Xor_A.calculate()

        # Primer AND
        self.__And_A.connect_input(self.__Input_A, 0)
        self.__And_A.connect_input(self.__Input_B, 1)

        self.__And_A.calculate()

        # Segundo AND
        self.__And_B.connect_input(self.__Xor_A.get_output(), 0)
        self.__And_B.connect_input(self.__C_in, 1)

        self.__And_B.calculate()

        # Calcular C_out
        self.__Or.connect_input(self.__And_B.get_output(), 0)
        self.__Or.connect_input(self.__And_A.get_output(), 1)

        self.__C_out = self.__Or.calculate()

        # Calcular Output
        self.__Xor_B.connect_input(self.__Xor_A.get_output(), 0)
        self.__Xor_B.connect_input(self.__C_in, 1)

        self.__Output = self.__Xor_B.calculate()
    
    def get_Output(self):
        return self.__Output
    
    def get_C_out(self):
        return self.__C_out
    
    def set_Input_A(self, value: Bit):
        self.__Input_A = value
    
    def set_Input_B(self, value: Bit):
        self.__Input_B = value
    
    def set_C_in(self, value: Bit):
        self.__C_in = value
    
    def __str__(self):
        return f"FullAdder(A={self.__Input_A}, B={self.__Input_B}, Cin={self.__C_in})"

