from .ASR import ASR
from .LSL import LSL
from .LSR import LSR
from .ROL import ROL
from .ROR import ROR
from .Multiplex import Multiplex
from Business.Basic_Components.Bus import Bus

class Shift_Unit:
    
    # Constructor
    def __init__(self):
        # Inputs
        self.__Input_A = Bus(16)
        self.__Input_B = Bus(16)
        self.__Operation_Bus = Bus(3)

        # Motores de desplazamiento
        self.__ASR = ASR()
        self.__LSL = LSL()
        self.__LSR = LSR()
        self.__ROL = ROL()
        self.__ROR = ROR()
        
        # Multiplex
        self.__Multiplex = Multiplex()

        # Outputs
        self.__ASR_Output = Bus(16)
        self.__LSL_Output = Bus(16)
        self.__LSR_Output = Bus(16)
        self.__ROL_Output = Bus(16)
        self.__ROR_Output = Bus(16)
        self.__Output = Bus(16)

    # --- Setters para configurar ---
    def set_input_A(self, bus: Bus):
        self.__Input_A = bus
    
    def set_input_B(self, bus: Bus):
        self.__Input_B = bus
    
    def set_operation_bus(self, bus: Bus):
        if bus.width != 3:
            raise ValueError("El bus de operación debe ser de 3 bits")
        self.__Operation_Bus = bus
    
    # --- Getter para salida ---
    def get_output(self) -> Bus:
        return self.__Output
    
    # --- Método principal de cálculo ---
    def calculate(self) -> Bus:
        # Conectar Input A
        self.__ASR.set_Input_A(self.__Input_A)
        self.__LSL.set_Input_A(self.__Input_A)
        self.__LSR.set_Input_A(self.__Input_A)
        self.__ROL.set_Input_A(self.__Input_A)
        self.__ROR.set_Input_A(self.__Input_A)

        # Conectar Input B
        self.__ASR.set_Input_B(self.__Input_B)
        self.__LSL.set_Input_B(self.__Input_B)
        self.__LSR.set_Input_B(self.__Input_B)
        self.__ROL.set_Input_B(self.__Input_B)
        self.__ROR.set_Input_B(self.__Input_B)

        # Calcular todas las operaciones
        self.__ASR.Calculate()
        self.__LSL.Calculate()
        self.__LSR.Calculate()
        self.__ROL.Calculate()
        self.__ROR.Calculate()

        # Obtener Outputs
        self.__ASR_Output = self.__ASR.get_Output()
        self.__LSL_Output = self.__LSL.get_Output()
        self.__LSR_Output = self.__LSR.get_Output()
        self.__ROL_Output = self.__ROL.get_Output()
        self.__ROR_Output = self.__ROR.get_Output()

        # Configurar el multiplexor interno
        self.__Multiplex.set_input_ASR(self.__ASR_Output)
        self.__Multiplex.set_input_LSL(self.__LSL_Output)
        self.__Multiplex.set_input_LSR(self.__LSR_Output)
        self.__Multiplex.set_input_ROL(self.__ROL_Output)
        self.__Multiplex.set_input_ROR(self.__ROR_Output)
        self.__Multiplex.set_select(self.__Operation_Bus)

        # Calcular y obtener resultado final
        self.__Multiplex.calculate()
        self.__Output = self.__Multiplex.get_output()

        return self.__Output