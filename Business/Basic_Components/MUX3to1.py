from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Logic_Gates import AND_Gate
from Business.Basic_Components.Logic_Gates import OR_Gate
from Business.Basic_Components.Logic_Gates import NOT_Gate

class MUX3to1:
    """
    Multiplexor 3:1 con 2 bits de selección.
    Selecciona entre:
    00 -> Input_A (Aritmética)
    01 -> Input_B (Lógica)
    10 -> Input_C (Desplazamiento)
    11 -> 0 (no usado)
    """
    
    # Constructor
    def __init__(self):
        # Inputs
        self.__Input_A = Bit(0)
        self.__Input_B = Bit(0)
        self.__Input_C = Bit(0)
        
        # Señal de selección (2 bits: S1=MSB, S0=LSB)
        self.__Input_S = Bus(2)  
        
        # Output
        self.__Output = Bit(0)
        
        # Puertas NOT para las señales de control
        self.__Not_S0 = NOT_Gate()
        self.__Not_S1 = NOT_Gate()
        
        # Puertas AND para cada término
        self.__And_A1 = AND_Gate()  
        self.__And_A2 = AND_Gate()  
        
        self.__And_B1 = AND_Gate()  
        self.__And_B2 = AND_Gate()  
        
        self.__And_C1 = AND_Gate()  
        self.__And_C2 = AND_Gate() 
        
        # Puertas OR para combinar términos 
        self.__Or1 = OR_Gate()  
        self.__Or2 = OR_Gate()  
    
    # --- Getters ---
    def get_Input_A(self) -> Bit: 
        return self.__Input_A
    
    def get_Input_B(self) -> Bit: 
        return self.__Input_B
    
    def get_Input_C(self) -> Bit: 
        return self.__Input_C
    
    def get_Input_S(self) -> Bus: 
        return self.__Input_S
    
    def get_Output(self) -> Bit: 
        return self.__Output
    
    # --- Setters ---
    def set_Input_A(self, Input: Bit): 
        self.__Input_A = Input
    
    def set_Input_B(self, Input: Bit): 
        self.__Input_B = Input
    
    def set_Input_C(self, Input: Bit): 
        self.__Input_C = Input
    
    def set_Input_S(self, Input: Bus):
        if Input.width != 2:
            raise ValueError("El bus de selección debe ser de 2 bits")
        self.__Input_S = Input
    
    # --- Método Principal de Cálculo ---
    def Calculate(self) -> Bit:
        # Obtener bits de selección (índice 0 = MSB, índice 1 = LSB)
        S0 = self.__Input_S.get_Line_bit(1)  # LSB (índice 1)
        S1 = self.__Input_S.get_Line_bit(0)  # MSB (índice 0)
        
        # 1. Calcular negaciones de S0 y S1
        self.__Not_S0.connect_input(S0, 0)
        self.__Not_S1.connect_input(S1, 0)
        self.__Not_S0.calculate()
        self.__Not_S1.calculate()
        
        S0_not = self.__Not_S0.get_output()
        S1_not = self.__Not_S1.get_output()
        
        # 2. Calcular término A: S1'·S0'·A
        self.__And_A1.connect_input(S1_not, 0)
        self.__And_A1.connect_input(S0_not, 1)
        self.__And_A1.calculate()
        and_a1_out = self.__And_A1.get_output()
        
        self.__And_A2.connect_input(and_a1_out, 0)
        self.__And_A2.connect_input(self.__Input_A, 1)
        self.__And_A2.calculate()
        term_A = self.__And_A2.get_output()
        
        # 3. Calcular término B: S1'·S0·B
        self.__And_B1.connect_input(S1_not, 0)
        self.__And_B1.connect_input(S0, 1)
        self.__And_B1.calculate()
        and_b1_out = self.__And_B1.get_output()
        
        self.__And_B2.connect_input(and_b1_out, 0)
        self.__And_B2.connect_input(self.__Input_B, 1)
        self.__And_B2.calculate()
        term_B = self.__And_B2.get_output()
        
        # 4. Calcular término C: S1·S0'·C
        self.__And_C1.connect_input(S1, 0)
        self.__And_C1.connect_input(S0_not, 1)
        self.__And_C1.calculate()
        and_c1_out = self.__And_C1.get_output()
        
        self.__And_C2.connect_input(and_c1_out, 0)
        self.__And_C2.connect_input(self.__Input_C, 1)
        self.__And_C2.calculate()
        term_C = self.__And_C2.get_output()
        
        # 5. Combinar términos: term_A + term_B + term_C
        self.__Or1.connect_input(term_A, 0)
        self.__Or1.connect_input(term_B, 1)
        self.__Or1.calculate()
        or1_out = self.__Or1.get_output()
        
        self.__Or2.connect_input(or1_out, 0)
        self.__Or2.connect_input(term_C, 1)
        self.__Or2.calculate()
        self.__Output = self.__Or2.get_output()
        
        return self.__Output
    
    def __str__(self):
        return f"MUX3to1(A={self.__Input_A}, B={self.__Input_B}, C={self.__Input_C}, S={self.__Input_S.get_Binary_value()}, Out={self.__Output})"