from Business.Basic_Components import Logic_Gate, Bit

class XOR_Gate(Logic_Gate):
    def __init__(self):
        super().__init__(n_inputs=2)
        self._set_output(Bit(0))  
    
    def calculate(self):
        inputs = self._get_inputs()  
        if len(inputs) >= 2 and all(inputs):
            value1 = inputs[0].get_value()
            value2 = inputs[1].get_value()
            
            result = 1 if value1 != value2 else 0
            self._get_output().set_value(result)  
        
        return self.get_output() 