from Business.Basic_Components.Logic_Gates.AND_Gate import AND_Gate
from Business.Basic_Components.Logic_Gates.NOT_Gate import NOT_Gate
from Business.Basic_Components.Logic_Gates.OR_Gate import OR_Gate
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from typing import List

class MUX8to1_1Bit:
    """
    Simula un Multiplexor 8x1 (de un solo bit) utilizando compuertas lógicas.
    Asume que AND_Gate y OR_Gate pueden manejar 4 y 8 entradas respectivamente.
    """
    
    # Constructor
    def __init__(self):
        
        # Inputs: Input se asume que es un Bus de 8 Bits (D0 a D7)
        self.__Input = Bus(8) # Corregido para ser un bus de 8 bits para D0-D7
        self.__S: List[Bit] = [Bit() for _ in range(3)] # [S0, S1, S2]

        # Compuertas NOT (Corregido para 3 NOT)
        self.__Not_S0 = NOT_Gate()
        self.__Not_S1 = NOT_Gate()
        self.__Not_S2 = NOT_Gate()

        # Compuertas AND (8 Minterms, cada una con 4 entradas)
        self.__And_Gates = [AND_Gate() for _ in range(8)]

        # Compuerta OR (Corregido: Añadida la compuerta OR de 8 entradas)
        self.__Or_Gate = OR_Gate() 
        
        # Output
        self.__Output = Bit()

    # --- Setters para las entradas de datos y control ---
    def set_Data_Inputs(self, input_bus: Bus):
        """Establece las 8 entradas de datos (D0-D7)."""
        if input_bus.width < 8:
            raise ValueError("El bus de entrada debe tener al menos 8 bits.")
        self.__Input = input_bus # Asume que D0=bit 0, D7=bit 7

    def set_Control_Inputs(self, S_bus: Bus):
        """Establece las 3 líneas de selección (S0-S2)."""
        if S_bus.width != 3:
            raise ValueError("El bus de control (S) debe ser de 3 bits.")
        self.__S[0] = S_bus.get_Line_bit(2) # S0 (LSB)
        self.__S[1] = S_bus.get_Line_bit(1) # S1
        self.__S[2] = S_bus.get_Line_bit(0) # S2 (MSB)
    
    # --- Método Principal de Cálculo ---
    def Calculate(self) -> Bit:
        
        # Bits de control
        S0 = self.__S[0]
        S1 = self.__S[1]
        S2 = self.__S[2]

        # 1. Compuertas NOT (Bits de control negados)
        self.__Not_S0.connect_input(S0, 0)
        self.__Not_S1.connect_input(S1, 0) # Corregido: Índice 0
        self.__Not_S2.connect_input(S2, 0) # Corregido: Índice 0

        self.__Not_S0.calculate()
        self.__Not_S1.calculate()
        self.__Not_S2.calculate()

        # Bits de control negados
        S0_Not = self.__Not_S0.get_output()
        S1_Not = self.__Not_S1.get_output()
        S2_Not = self.__Not_S2.get_output()

        # Lista de Minterms: (Dato, S2_term, S1_term, S0_term)
        minterm_inputs = [
            # D0 (000)
            (self.__Input.get_Line_bit(0), S2_Not, S1_Not, S0_Not), 
            # D1 (001)
            (self.__Input.get_Line_bit(1), S2_Not, S1_Not, S0),     
            # D2 (010)
            (self.__Input.get_Line_bit(2), S2_Not, S1, S0_Not),     
            # D3 (011)
            (self.__Input.get_Line_bit(3), S2_Not, S1, S0),         
            # D4 (100)
            (self.__Input.get_Line_bit(4), S2, S1_Not, S0_Not),     
            # D5 (101)
            (self.__Input.get_Line_bit(5), S2, S1_Not, S0),         
            # D6 (110)
            (self.__Input.get_Line_bit(6), S2, S1, S0_Not),         
            # D7 (111)
            (self.__Input.get_Line_bit(7), S2, S1, S0)              
        ]
        
        # 2. Compuertas AND (Minterms)
        minterm_outputs = []
        for i in range(8):
            D_i, S_C, S_B, S_A = minterm_inputs[i]
            
            # Conexiones: (Dato, S2_term, S1_term, S0_term)
            self.__And_Gates[i].connect_input(D_i, 0)
            self.__And_Gates[i].connect_input(S_C, 1)
            self.__And_Gates[i].connect_input(S_B, 2)
            self.__And_Gates[i].connect_input(S_A, 3)
            
            minterm_outputs.append(self.__And_Gates[i].calculate())

        # 3. Compuerta OR (Suma de Productos)
        for i in range(8):
            self.__Or_Gate.connect_input(minterm_outputs[i], i)
            
        self.__Output = self.__Or_Gate.calculate()
        return self.__Output

    def get_output(self) -> Bit:
        return self.__Output