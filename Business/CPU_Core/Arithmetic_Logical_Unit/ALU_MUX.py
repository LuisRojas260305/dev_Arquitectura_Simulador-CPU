# Business/CPU_Core/Arithmetic_Logical_Unit/ALU_Multiplexor.py
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.MUX3to1 import MUX3to1

class ALU_MUX:
    """
    Multiplexor principal de la ALU.
    Selecciona entre las 3 unidades según ALUop[0:1]
    Mapeo: 00=Aritmética, 01=Lógica, 10=Desplazamiento
    """
    
    def __init__(self):
        # Entradas de las tres unidades
        self.__Input_Aritmetica = Bus(16)      # Resultado Unidad Aritmética
        self.__Input_Logica = Bus(16)          # Resultado Unidad Lógica
        self.__Input_Desplazamiento = Bus(16)  # Resultado Unidad Desplazamiento
        
        # Señal de control (2 bits de ALUop)
        self.__Input_Select = Bus(2)  # ALUop[0:1]
        
        # Salida
        self.__Output = Bus(16)
        
        # 16 MUX3to1 (uno por cada bit del bus)
        self.__MUX_array = [MUX3to1() for _ in range(16)]
    
    # --- Setters para entradas ---
    def set_input_aritmetica(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus de Aritmética debe ser de 16 bits")
        self.__Input_Aritmetica = bus
    
    def set_input_logica(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus de Lógica debe ser de 16 bits")
        self.__Input_Logica = bus
    
    def set_input_desplazamiento(self, bus: Bus):
        if bus.width != 16:
            raise ValueError("El bus de Desplazamiento debe ser de 16 bits")
        self.__Input_Desplazamiento = bus
    
    def set_select(self, select_bus: Bus):
        if select_bus.width != 2:
            raise ValueError("El bus de selección debe ser de 2 bits")
        self.__Input_Select = select_bus
    
    # --- Getter para salida ---
    def get_output(self) -> Bus:
        return self.__Output
    
    # --- Método principal de cálculo ---
    def calculate(self) -> Bus:
        # Para cada bit del bus (0 a 15)
        for bit_index in range(16):
            # Obtener el MUX correspondiente a este bit
            current_mux = self.__MUX_array[bit_index]
            
            # Configurar las 3 entradas del MUX3to1
            current_mux.set_Input_A(self.__Input_Aritmetica.get_Line_bit(bit_index))
            current_mux.set_Input_B(self.__Input_Logica.get_Line_bit(bit_index))
            current_mux.set_Input_C(self.__Input_Desplazamiento.get_Line_bit(bit_index))
            
            # Configurar la selección (2 bits de ALUop)
            current_mux.set_Input_S(self.__Input_Select)
            
            # Calcular y obtener el bit de salida
            output_bit = current_mux.Calculate()
            
            # Asignar el bit de salida al bus de resultados
            self.__Output.set_Line_bit(bit_index, output_bit)
        
        return self.__Output
    
    def __str__(self):
        return f"ALU_Multiplexor(Output={self.__Output.get_Hexadecimal_value()})"