from Business.Basic_Components.Logic_Gates.AND_Gate import AND_Gate
from Business.Basic_Components.Logic_Gates.NOT_Gate import NOT_Gate
from Business.Basic_Components.Logic_Gates.OR_Gate import OR_Gate
from Business.Basic_Components.Bit import Bit

class MUX2to1:
    # Constructor
    def __init__(self):
        # Inputs
        self.__Input_A = Bit(0)
        self.__Input_B = Bit(0)
        self.__S = Bit(0)

        # Output
        self.__Output = Bit(0)

        # Gates
        self.__And_A = AND_Gate()
        self.__And_B = AND_Gate()
        self.__Not = NOT_Gate()
        self.__Or = OR_Gate()
    
    # Setters
    def set_Input_A(self, value: Bit):
        self.__Input_A = value
    
    def set_Input_B(self, value: Bit):
        self.__Input_B = value
    
    def set_S(self, value: Bit):
        self.__S = value
    
    # Getters
    def get_Input_A(self) -> Bit:
        return self.__Input_A
    
    def get_Input_B(self) -> Bit:
        return self.__Input_B
    
    def get_S(self) -> Bit:
        return self.__S
    
    def get_Output(self) -> Bit:
        return self.__Output
    
    # Metodos
    def Calculate(self):
        
        # Output = (Sˉ⋅I0​)+(S⋅I1​)

        # Not S
        self.__Not.connect_input(self.__S, 0)
        self.__Not.calculate()

        # Primer AND
        self.__And_A.connect_input(self.__Input_A, 0)
        self.__And_A.connect_input(self.__Not.get_output(), 1)
        self.__And_A.calculate()

        # Segundo AND
        self.__And_B.connect_input(self.__Input_B, 0)
        self.__And_B.connect_input(self.__S, 1)
        self.__And_B.calculate()

        # Or
        self.__Or.connect_input(self.__And_A.get_output(), 0)
        self.__Or.connect_input(self.__And_B.get_output(), 1)
        self.__Or.calculate()

        # Output
        self.__Output = self.__Or.get_output()
    
    def __str__(self):
        return f"MUX2to1(A={self.__Input_A}, B={self.__Input_B}, S={self.__S}, Output={self.__Output})"
    
    def __repr__(self):
        return f"MUX2to1(Input_A={repr(self.__Input_A)}, Input_B={repr(self.__Input_B)}, S={repr(self.__S)})"