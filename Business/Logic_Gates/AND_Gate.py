from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Logic_Gate import Logic_Gate

class AND_Gate(Logic_Gate):
    def __init__(self, A, B):
        super().__init__(A, B)
    
    def Calculate(self):

        value_A = self._Input_A.get_value()
        value_B = self._Input_B.get_value()

        result = 1 if value_A == 1 and value_B == 1 else 0

        self._Output.set_value(result)

        return self._Output
