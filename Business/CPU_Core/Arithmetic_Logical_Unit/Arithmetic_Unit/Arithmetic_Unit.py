from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit  
from .Full_Adder import Full_Adder
from Business.Basic_Components.Logic_Gates.XOR_Gate import XOR_Gate
from typing import Tuple

class Arithmetic_Unit:
    
    def __init__(self):
        # Full Adders (16, uno por cada bit)
        self.__FAs = [Full_Adder() for _ in range(16)]
        
        # Inversores (XOR como inversor controlado)
        self.__Inverters = [XOR_Gate() for _ in range(16)]
        
        # Control Sub (para inversión en resta)
        self.__Control_SUB = Bit(0)
    
    def __invert_bus(self, input_bus: Bus, invert_control: Bit) -> Bus:
        """
        Invierte el bus si invert_control = 1 (para operación de resta).
        Usa XOR: B XOR 0 = B, B XOR 1 = NOT B
        """
        width = len(input_bus)
        result = Bus(width)
        
        for i in range(width):
            self.__Inverters[i].connect_input(input_bus.get_Line_bit(i), 0)
            self.__Inverters[i].connect_input(invert_control, 1)
            self.__Inverters[i].calculate()
            result.set_Line_bit(i, self.__Inverters[i].get_output())
        
        return result
    
    def __add(self, input_a: Bus, input_b: Bus, c_in: Bit) -> Tuple[Bus, Bit]:
        """Suma dos buses con acarreo inicial."""
        width = len(input_a)
        result = Bus(width)
        
        carry = c_in
        
        # Sumar de LSB a MSB (de 15 a 0 en tu representación Big-Endian)
        for i in range(width - 1, -1, -1):
            # Configurar el Full Adder
            self.__FAs[i].set_Input_A(input_a.get_Line_bit(i))
            self.__FAs[i].set_Input_B(input_b.get_Line_bit(i))
            self.__FAs[i].set_C_in(carry)
            
            # Calcular
            self.__FAs[i].calculate()
            
            # Obtener resultados
            result.set_Line_bit(i, self.__FAs[i].get_Output())
            carry = self.__FAs[i].get_C_out()
        
        return result, carry
    
    def calculate(self, input_a: Bus, input_b: Bus, c_in: Bit) -> Tuple[Bus, Bit]:
        """
        Ejecuta operación aritmética según c_in:
        - c_in = 0: ADD (A + B)
        - c_in = 1: SUB (A - B) = A + NOT B + 1
        """
        if not isinstance(c_in, Bit):
            raise TypeError(f"c_in debe ser Bit, no {type(c_in)}")
        
        if not isinstance(input_a, Bus) or not isinstance(input_b, Bus):
            raise TypeError("Los inputs deben ser Bus")
        
        if len(input_a) != 16 or len(input_b) != 16:
            raise ValueError("Los buses deben ser de 16 bits")
        
        if c_in.get_value() == 0:  # ADD
            return self.__add(input_a, input_b, Bit(0))
        else:  # SUB (A - B)
            # Invertir B y sumar 1 (c_in = 1)
            inverted_b = self.__invert_bus(input_b, Bit(1))
            return self.__add(input_a, inverted_b, Bit(1))
    
    def get_result(self) -> Bus:
        """Método auxiliar para compatibilidad."""
        # Nota: Este método sería útil si guardas el resultado como atributo
        pass
        
        width = len(Input_A) 
        result = Bus(width)

        Carry = C_in

        for i in range(width - 1, -1, -1):

            # Recogemos los bits a sumar
            A = Input_A.get_Line_bit(i)
            B = Input_B.get_Line_bit(i)

            # Ingresamos los valores en el adder
            self.__FAs[i].set_Input_A(A)
            self.__FAs[i].set_Input_B(B)
            self.__FAs[i].set_C_in(Carry)

            # Realizamos la suma
            self.__FAs[i].Calculate()

            # Guardamos el Carry
            Carry = self.__FAs[i].get_C_out()

            # Guardamos el resultado de la suma
            result.set_Line_bit(i, self.__FAs[i].get_Output())

        return result, Carry