from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Logic_Gates import AND_Gate
from Business.Basic_Components.Logic_Gates import OR_Gate
from Business.Basic_Components.Logic_Gates import NOT_Gate

class MUX4to1:
    
    # Constructor
    def __init__(self):
        # Inputs
        self.__Input_D0 = Bit(0)
        self.__Input_D1 = Bit(0)
        self.__Input_D2 = Bit(0)
        self.__Input_D3 = Bit(0)
        
        # Señal de selección (2 bits: S1=MSB, S0=LSB)
        self.__Input_S = Bus(2)
        
        # Output
        self.__Output = Bit(0)
        
        # Puertas NOT para las señales de control
        self.__Not_S0 = NOT_Gate()
        self.__Not_S1 = NOT_Gate()
        
        # Puertas AND para cada término (cascada de 2 ANDs por término)
        # Término D0: S1'·S0'·D0
        self.__And_D0_1 = AND_Gate()  # AND entre S1' y S0'
        self.__And_D0_2 = AND_Gate()  # AND entre (S1'·S0') y D0
        
        # Término D1: S1'·S0·D1
        self.__And_D1_1 = AND_Gate()  # AND entre S1' y S0
        self.__And_D1_2 = AND_Gate()  # AND entre (S1'·S0) y D1
        
        # Término D2: S1·S0'·D2
        self.__And_D2_1 = AND_Gate()  # AND entre S1 y S0'
        self.__And_D2_2 = AND_Gate()  # AND entre (S1·S0') y D2
        
        # Término D3: S1·S0·D3
        self.__And_D3_1 = AND_Gate()  # AND entre S1 y S0
        self.__And_D3_2 = AND_Gate()  # AND entre (S1·S0) y D3
        
        # Puertas OR en árbol para combinar los 4 términos
        self.__Or1 = OR_Gate()  # OR entre D0 y D1
        self.__Or2 = OR_Gate()  # OR entre D2 y D3
        self.__Or3 = OR_Gate()  # OR entre (D0+D1) y (D2+D3)
    
    # --- Getters ---
    def get_Input_D0(self) -> Bit: 
        return self.__Input_D0
    
    def get_Input_D1(self) -> Bit: 
        return self.__Input_D1
    
    def get_Input_D2(self) -> Bit: 
        return self.__Input_D2
    
    def get_Input_D3(self) -> Bit: 
        return self.__Input_D3
    
    def get_Input_S(self) -> Bus: 
        return self.__Input_S
    
    def get_Output(self) -> Bit: 
        return self.__Output
    
    # --- Setters ---
    def set_Input_D0(self, Input: Bit): 
        self.__Input_D0 = Input
    
    def set_Input_D1(self, Input: Bit): 
        self.__Input_D1 = Input
    
    def set_Input_D2(self, Input: Bit): 
        self.__Input_D2 = Input
    
    def set_Input_D3(self, Input: Bit): 
        self.__Input_D3 = Input
    
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
        
        # 2. Calcular término D0: S1'·S0'·D0
        self.__And_D0_1.connect_input(S1_not, 0)
        self.__And_D0_1.connect_input(S0_not, 1)
        self.__And_D0_1.calculate()
        and_d0_1_out = self.__And_D0_1.get_output()
        
        self.__And_D0_2.connect_input(and_d0_1_out, 0)
        self.__And_D0_2.connect_input(self.__Input_D0, 1)
        self.__And_D0_2.calculate()
        term_D0 = self.__And_D0_2.get_output()
        
        # 3. Calcular término D1: S1'·S0·D1
        self.__And_D1_1.connect_input(S1_not, 0)
        self.__And_D1_1.connect_input(S0, 1)
        self.__And_D1_1.calculate()
        and_d1_1_out = self.__And_D1_1.get_output()
        
        self.__And_D1_2.connect_input(and_d1_1_out, 0)
        self.__And_D1_2.connect_input(self.__Input_D1, 1)
        self.__And_D1_2.calculate()
        term_D1 = self.__And_D1_2.get_output()
        
        # 4. Calcular término D2: S1·S0'·D2
        self.__And_D2_1.connect_input(S1, 0)
        self.__And_D2_1.connect_input(S0_not, 1)
        self.__And_D2_1.calculate()
        and_d2_1_out = self.__And_D2_1.get_output()
        
        self.__And_D2_2.connect_input(and_d2_1_out, 0)
        self.__And_D2_2.connect_input(self.__Input_D2, 1)
        self.__And_D2_2.calculate()
        term_D2 = self.__And_D2_2.get_output()
        
        # 5. Calcular término D3: S1·S0·D3
        self.__And_D3_1.connect_input(S1, 0)
        self.__And_D3_1.connect_input(S0, 1)
        self.__And_D3_1.calculate()
        and_d3_1_out = self.__And_D3_1.get_output()
        
        self.__And_D3_2.connect_input(and_d3_1_out, 0)
        self.__And_D3_2.connect_input(self.__Input_D3, 1)
        self.__And_D3_2.calculate()
        term_D3 = self.__And_D3_2.get_output()
        
        # 6. Combinar términos en árbol: (D0 + D1) + (D2 + D3)
        self.__Or1.connect_input(term_D0, 0)
        self.__Or1.connect_input(term_D1, 1)
        self.__Or1.calculate()
        or1_out = self.__Or1.get_output()
        
        self.__Or2.connect_input(term_D2, 0)
        self.__Or2.connect_input(term_D3, 1)
        self.__Or2.calculate()
        or2_out = self.__Or2.get_output()
        
        self.__Or3.connect_input(or1_out, 0)
        self.__Or3.connect_input(or2_out, 1)
        self.__Or3.calculate()
        self.__Output = self.__Or3.get_output()
        
        return self.__Output
    
    def __str__(self):
        return f"MUX4to1(D0={self.__Input_D0}, D1={self.__Input_D1}, D2={self.__Input_D2}, D3={self.__Input_D3}, S={self.__Input_S.get_Binary_value()}, Out={self.__Output})"