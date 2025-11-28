from abc import ABC, abstractmethod

class Logic_Gate(ABC):
    # Constructor    
    def __init__(self, n_inputs: int = 2):
        self.__inputs = []        
        self.__output = None       
        self.__n_inputs = n_inputs  
    
    
    def _get_inputs(self):
        return self.__inputs
    
    def _get_input(self, index: int):
        if 0 <= index < len(self.__inputs):
            return self.__inputs[index]
        return None
    
    def _get_output(self):
        return self.__output
    
    def _set_output(self, value):
        self.__output = value
    
    def _get_n_inputs(self):
        return self.__n_inputs
    
    # Métodos públicos
    def connect_input(self, input_gate, index: int = 0):
        # Validar índice
        if index < 0 or index >= self.__n_inputs:
            raise ValueError(f"Índice de entrada {index} fuera de rango. Debe estar entre 0 y {self.__n_inputs-1}.")
        
        # Extender la lista si es necesario
        if len(self.__inputs) <= index:
            self.__inputs.extend([None] * (index - len(self.__inputs) + 1))
        
        # Conectar la entrada
        self.__inputs[index] = input_gate
    
    def get_output(self):
        return self.__output
    
    @abstractmethod
    def calculate(self):
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}"