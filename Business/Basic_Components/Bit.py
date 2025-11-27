class Bit:
    # Constructor
    def __init__(self, value: int = 0):
        self.set_value(value)
    
    # Metodos

    def set_value(self, value):
        # Verificacion para que el valor del bit sea 1 o 0
        if value not in [0,1]:
            raise ValueError("El valor de un Bit debe ser 0 o 1.")
        self.__value = value
    
    def get_value(self):
        return self.__value
    
    def __str__(self):
        return f"Bit: {self.__value}"
    
    def toggle(self):
        self.set_value(1 - self.get_value())
    
    def __repr__(self):
        return f"Bit({self.__value})"
    
    def __eq__(self, other):
        if not isinstance(other, Bit):
            return False
        return self.__value == other.__value
