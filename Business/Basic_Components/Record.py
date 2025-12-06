from .Bus import Bus

class Record:
    # Constructor
    def __init__(self, width: int = 16, initial_value: int = 0):

        self._width = width
        self._Value = Bus(width, initial_value)
    
    # Métodos internos básicos
    def set_Value(self, value: Bus):
        if value.width != self._width:
            raise ValueError(f"El Bus debe tener ancho {self._width}, no {value.width}")
        self._Value = value
    
    def set_Value_int(self, value: int):
        """Establece el valor del registro desde un entero"""
        self._Value.set_Binary_value(value)
    
    def get_Value(self) -> Bus:
        """Retorna el valor actual como Bus"""
        return self._Value
    
    def get_Hex_Value(self) -> str:
        """Retorna el valor en hexadecimal"""
        return self._Value.get_Hexadecimal_value()
    
    def get_Dec_Value(self) -> int:
        """Retorna el valor en decimal"""
        return self._Value.get_Decimal_value()
    
    def get_Bin_Value(self) -> str:
        """Retorna el valor en binario"""
        return self._Value.get_Binary_value()
    
    # Métodos para cambiar tamaño
    def resize(self, new_width: int, preserve_value: bool = True):
        """
        Cambia el tamaño del registro.
        
        Args:
            new_width: Nuevo ancho en bits
            preserve_value: Si True, intenta preservar el valor actual
            (truncando o extendiendo con ceros)
        """
        old_value = self.get_Dec_Value()
        self._width = new_width
        
        if preserve_value:
            # Si el nuevo ancho es mayor, extender con ceros
            # Si es menor, truncar (solo los bits menos significativos)
            if new_width >= 16:  # Si el nuevo ancho es suficiente para el valor
                self._Value = Bus(new_width, old_value)
            else:
                # Máscara para mantener solo los bits LSB
                mask = (1 << new_width) - 1
                self._Value = Bus(new_width, old_value & mask)
        else:
            self._Value = Bus(new_width, 0)
    
    def get_width(self) -> int:
        """Retorna el ancho actual del registro"""
        return self._width