from Basic_Components.Bus import Bus
from Basic_Components.Bit import Bit
from Business.CPU_Core.Full_Adder import Full_Adder
from Business.Logic_Gates.NOT_Gate import NOT_Gate
from typing import List

class Arithmetic_Unit:
    # Constructor
    def __init__(self):
        # Full Adders
        self.__FAs: List[Full_Adder] = [Full_Adder() for _ in range(16)]

        # Inversiores
        self.__Inverters: List[NOT_Gate] = [NOT_Gate() for _ in range(16)]

        # Control Sub
        self.__Control_SUB = None
    
    def Inverter(self, Input_B: Bus) -> Bus:
        
        width = len(Input_B) 
        result = Bus(width)

        for i in range(width):
            
            self.__Inverters[i].connect_input(Input_B.get_Line_bit(i), 0)

            output_bit = self.__Inverters[i].calculate() 
            
            result.set_Line_bit(i, output_bit) 

        return result
    def Calculate(self, Input_A: Bus, Input_B: Bus, C_in: Bit) -> Bus:
        
        if not isinstance (C_in, Bit):
            raise TypeError(f"El C_in debe ser una instancia de la clase Bit, no {type(C_in).__name__}")

        if not isinstance (Input_A, Bus) or not isinstance (Input_B, Bus):
            raise TypeError("Los input deben ser de la clase Bus")
        Output = Bus(16)

        if C_in.get_value == 0:
            # Suma los inpunts (A + B + C_in = 0)
            Output, C_out = self.ADD(Input_A, Input_B, C_in)
            return Output, C_out
        else:
            # Resta los inputs (A - (~B) + C_in = 1)
            Output, C_out = self.ADD(Input_A, self.Inverter(Input_B), C_in)
            return Output, C_out
        
    def ADD (self, Input_A: Bus, Input_B: Bus, C_in: Bit) -> (Bus, Bit):
        
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