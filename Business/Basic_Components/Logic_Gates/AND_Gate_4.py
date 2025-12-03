from Business.Basic_Components.Logic_Gate import Logic_Gate
from Business.Basic_Components.Bit import Bit

class AND_Gate_4(Logic_Gate):
    def __init__(self):
        super().__init__(n_inputs=4)
        self._set_output(Bit(0))
    
    def calculate(self):
        inputs = self._get_inputs()
        if len(inputs) >= 4:
            result = 1
            for i in range(4):
                if inputs[i] is None or inputs[i].get_value() == 0:
                    result = 0
                    break
            self._get_output().set_value(result)
        return self.get_output()