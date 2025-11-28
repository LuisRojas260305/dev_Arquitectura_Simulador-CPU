from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from typing import Tuple

class Shift_Unit:
    
    # Modos de operacion
    SLL = 0  # Izquierda/Multiplicacion
    SRA = 1  # Derecha/Division

    # Constructor
    def __init__(self, width: int = 16):
        self.__width = width
    
    # Desplazamiento a la izquierda
    def __SLL(self, Input: Bus, Shift_Amount: int) -> Tuple[Bus, Bit]:
        result = Bus(self.__width)
        carry_out = Bit(0)

        # En caso de no haber desplazamiento
        if Shift_Amount == 0:
            return Input, Bit(0)
        
        if Shift_Amount <= self.__width:
            carry_out = Input.get_Line_bit(Shift_Amount - 1)
        
        for i in range(self.__width):
            index = i + Shift_Amount

            if index < self.__width:
                bit = Input.get_Line_bit(index)
            else:
                bit = Bit(0)
            
            result.set_Line_bit(i, bit)
        
        return result, carry_out
    
    # Desplazamiento a la derecha
    def __SRA(self, Input: Bus, Shift_Amount: int) -> Tuple[Bus, Bit]:
        result = Bus(self.__width)
        carry_out = Bit(0)

        # En caso de no haber desplazamiento
        if Shift_Amount == 0:
            return Input, Bit(0)
        
        # Sign bit (MSB)
        sign_bit = Input.get_Line_bit(0)

        if Shift_Amount <= self.__width:
            carry_out = Input.get_Line_bit(self.__width - Shift_Amount)
        
        for i in range(self.__width):
            index = i - Shift_Amount

            if index >= 0:
                bit = Input.get_Line_bit(index)
            else:
                bit = sign_bit  # Extensión de signo
            
            result.set_Line_bit(i, bit)
        
        return result, carry_out
    
    def Calculate(self, Shift_Amount: int, Input: Bus, Mode: int) -> Tuple[Bus, Bit]:
        
        if Shift_Amount < 0 or Shift_Amount >= self.__width:
            raise ValueError(f"El Shift_Amount debe estar dentro del rango [0, {self.__width - 1}]")
        
        if not isinstance(Input, Bus):
            raise TypeError(f"El Input debe ser de la clase Bus, no de la clase {type(Input).__name__}")
        
        if not isinstance(Mode, int) or Mode not in [self.SLL, self.SRA]:
            raise ValueError("Modo de operación no válido. Use Shift_Unit.SLL o Shift_Unit.SRA.")
        
        if Mode == self.SLL:
            return self.__SLL(Input, Shift_Amount)
        elif Mode == self.SRA:
            return self.__SRA(Input, Shift_Amount)