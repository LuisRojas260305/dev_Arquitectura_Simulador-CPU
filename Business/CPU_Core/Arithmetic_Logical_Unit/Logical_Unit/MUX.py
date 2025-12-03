from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.MUX4to1 import MUX4to1

class MUX:

    def __init__(self):
        # Entradas de resultados de operaciones lógicas
        self.__Input_AND = Bus(16)   # AND gate results
        self.__Input_OR = Bus(16)    # OR gate results  
        self.__Input_XOR = Bus(16)   # XOR gate results
        self.__Input_NOT = Bus(16)   # NOT gate results
        
        # Señal de control (2 bits LSB de ModoFunción)
        self.__Input_Select = Bus(2)  # ModoFunción[0:1]
        
        # Salida
        self.__Output = Bus(16)
        
        # 16 MUX4to1 (uno por cada bit del bus)
        self.__MUX_array = [MUX4to1() for _ in range(16)]
    
    # --- Setters para entradas ---
    def set_input_AND(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus AND debe ser de 16 bits")
        self.__Input_AND = bus
    
    def set_input_OR(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus OR debe ser de 16 bits")
        self.__Input_OR = bus
    
    def set_input_XOR(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus XOR debe ser de 16 bits")
        self.__Input_XOR = bus
    
    def set_input_NOT(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus NOT debe ser de 16 bits")
        self.__Input_NOT = bus
    
    def set_select(self, select_bus: Bus):
        """
        Configura la selección (2 bits LSB de ModoFunción)
        00: AND, 01: OR, 10: XOR, 11: NOT
        """
        if select_bus.width != 2:
            raise ValueError("El bus de selección debe ser de 2 bits")
        self.__Input_Select = select_bus
    
    # --- Getter para salida ---
    def get_output(self) -> Bus:
        return self.__Output
    
    # --- Método principal de cálculo ---
    def calculate(self) -> Bus:
        """
        Calcula la salida seleccionando la operación lógica adecuada.
        Retorna un Bus de 16 bits con el resultado.
        """
        # Para cada bit del bus (0 a 15)
        for bit_index in range(16):
            # Obtener el MUX correspondiente a este bit
            current_mux = self.__MUX_array[bit_index]
            
            # Configurar las 4 entradas del MUX4to1
            # D0 = AND (ModoFunción 000 → 00)
            # D1 = OR  (ModoFunción 001 → 01)  
            # D2 = XOR (ModoFunción 010 → 10)
            # D3 = NOT (ModoFunción 011 → 11)
            current_mux.set_Input_D0(self.__Input_AND.get_Line_bit(bit_index))
            current_mux.set_Input_D1(self.__Input_OR.get_Line_bit(bit_index))
            current_mux.set_Input_D2(self.__Input_XOR.get_Line_bit(bit_index))
            current_mux.set_Input_D3(self.__Input_NOT.get_Line_bit(bit_index))
            
            # Configurar la selección (2 bits LSB de ModoFunción)
            current_mux.set_Input_S(self.__Input_Select)
            
            # Calcular y obtener el bit de salida
            output_bit = current_mux.Calculate()
            
            # Asignar el bit de salida al bus de resultados
            self.__Output.set_Line_bit(bit_index, output_bit)
        
        return self.__Output
    
    def __str__(self):
        return f"Logic_Unit_Multiplexor(Output={self.__Output.get_Hexadecimal_value()})"