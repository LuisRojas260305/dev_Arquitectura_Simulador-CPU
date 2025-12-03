from Business.Basic_Components.Logic_Gate import Logic_Gate
from Business.Basic_Components.Bit import Bit

class OR_Gate_8(Logic_Gate):
    def __init__(self):
        super().__init__(n_inputs=8)
        self._set_output(Bit(0))
    
    def calculate(self):
        inputs = self._get_inputs()
        if len(inputs) >= 8:
            result = 0
            for i in range(8):
                if inputs[i] is not None and inputs[i].get_value() == 1:
                    result = 1
                    break
            self._get_output().set_value(result)
        return self.get_output()