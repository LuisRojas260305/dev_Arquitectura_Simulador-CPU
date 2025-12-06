from dataclasses import dataclass, field
from typing import List, ClassVar, Dict
from Business.Basic_Components.Bit import Bit

@dataclass
class Bus:

    # Atributos 
    width: int = 16
    initial_value: int = 0

    # Atributos post __init__
    __lines: List[Bit] = field(init = False, repr = False)

    # Constantes de clase
    DEFAULT_WIDTH: ClassVar[int] = 16
    MAX_WIDTH: ClassVar[int] = 64

    # Inicializacion post __init__
    def __post_init__(self):
        # Validaciones

        # Tamaño del bus
        if self.width <= 0 or self.width > self.MAX_WIDTH:
            raise ValueError(f"Ancho del bus debe estar dentro de los parametros [1 y {self.MAX_WIDTH}]")

        # Valor del bus
        if self.initial_value < 0 or self.initial_value >= (1 << self.width):
            raise ValueError(f"Valor inicial {self.initial_value} fuera del rando del bus")
        
        # Inicializacion de las lineas del bus
        self.__lines = [Bit(0) for _ in range(self.width)]
        self.set_Binary_value(self.initial_value)

    # Establece el valor del bus en binario
    def set_Binary_value(self, value: int):
        # Validacion
        if value < 0 or value >= (1 << self.width):
            raise ValueError(f"Valor {value} fuera del rango del bus {0, (1 << self.width)}")

        for i in range(self.width):
            bit_val = (value >> (self.width - 1 - i)) & 1
            self.__lines[i].set_value(bit_val)

    # Devuelve el valor del bus en decimal
    def get_Decimal_value(self) -> int:

        value = 0
        
        for i in range(self.width):
            value = (value << 1) | self.__lines[i].get_value()
        
        return value

    # Devuelve el valor del bus en binario
    def get_Binary_value(self) -> str:
        return ''.join(str(bit.get_value()) for bit in self.__lines)
    
    # Devuelve el valor del bus en hexadecimal
    def get_Hexadecimal_value(self) -> str:
        hex_digits = (self.width + 3) // 4
        return f"0x{self.get_Decimal_value():0{hex_digits}X}"
    
    # Devuelve un diccionario con todos los valores y sus indices
    def get_Lines_values(self) -> Dict[int, int]:
        return {i: self.__lines[i].get_value() for i in range(self.width)}
    
    # Devuelve un diccionario con todos los valores y sus indicies ordenados
    def get_Ordered_lines_values(self, msb_first: bool = True) -> Dict[int, int]:
        if msb_first:
            return {i: self.__lines[i].get_value() for i in range(self.width)}
        else:
            return {i: self.__lines[i].get_value() for i in range(self.width - 1, -1, -1)}
        
    # Devuelve el valor de una linea
    def get_Line_bit(self, index: int) -> Bit:
        if index < 0 or index >= self.width:
            raise ValueError(f"El indice debe estar dentro del rango [0, {self.width - 1}]")
        
        return self.__lines[index]
    
    def set_Line_bit(self, index: int, value: Bit):
        if index < 0 or index >= self.width:
            raise ValueError(f"El indice debe estar dentro del rango [0, {self.width - 1}]")
        
        if not isinstance(value, Bit):
            raise TypeError(f"El valor debe ser una instancia de la clase Bit, no {type(value).__name__}")
        
        self.__lines[index] = value
    
    def __str__(self):
        return f"Bus{self.width}({self.get_Hexadecimal_value()})"
    
    def __len__(self):
        return self.width