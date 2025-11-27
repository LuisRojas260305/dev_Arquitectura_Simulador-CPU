from abc import ABC, abstractmethod
from Business.Basic_Components.Bit import Bit 

class Logic_Gate (ABC):

    def __init__(self, A: Bit, B: Bit):

        if not isinstance (A, Bit) or not isinstance (B, Bit):
            raise TypeError("Las entradas A y B deben ser instansias de la clase bit")
        
        self._Input_A = A
        self._Input_B = B
        
        self._Output = Bit(0)

    def get_Output(self) -> Bit:
        return self._Output

    @abstractmethod
    def Calculate(self):
        raise NotImplementedError("Las clases hijas deben implementar el metodo 'Calculate()'")
