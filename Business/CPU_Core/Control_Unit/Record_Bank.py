from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Record import Record

class Record_Bank:
    
    # Constructor
    def __init__(self):
        
        # Registros base
        self.__PC = Record(16)
        self.__IR = Record(16)
        self.__AC = Record(16)
        self.__MAR = Record(16)
        self.__MDR = Record(16)
        self.__TEMP = Record(16)

        # Registros para operaciones secuenciales
        self.__HI = Record(16)
        self.__LO = Record(16)
        self.__MD_CNT = Record(4)
        self.__MD_STATE = Record(3)

        # Registros para control de microinstrucciones
        self.__STEP_CNT = Record(4)
        self.__OP_TYPE = Record(4)
        self.__STATUS = Record(8)

        # Banderas
        self.__FLAG_Z = Bit()
        self.__FLAG_C = Bit()
        self.__FLAG_N = Bit()

    # Getters

    # Flags
    def get_FLAG_Z(self): return self.__FLAG_Z
    def get_FLAG_C(self): return self.__FLAG_C
    def get_FLAG_N(self): return self.__FLAG_N

    # BUS
    def get_PC(self): return self.__PC
    def get_IR(self): return self.__IR
    def get_AC(self): return self.__AC
    def get_MAR(self): return self.__MAR
    def get_MDR(self): return self.__MDR
    def get_TEMP(self): return self.__TEMP
    def get_HI(self): return self.__HI
    def get_LO(self): return self.__LO
    def get_MD_CNT(self): return self.__MD_CNT
    def get_MD_STATE(self): return self.__MD_STATE
    def get_STEP_CNT(self): return self.__STEP_CNT
    def get_OP_TYPE(self): return self.__OP_TYPE
    def get_STATUS(self): return self.__STATUS

    # HEX (usando métodos de Record)
    def get_PC_HEX(self): return self.__PC.get_Hex_Value()
    def get_IR_HEX(self): return self.__IR.get_Hex_Value()
    def get_AC_HEX(self): return self.__AC.get_Hex_Value()
    def get_MAR_HEX(self): return self.__MAR.get_Hex_Value()
    def get_MDR_HEX(self): return self.__MDR.get_Hex_Value()
    def get_TEMP_HEX(self): return self.__TEMP.get_Hex_Value()
    def get_HI_HEX(self): return self.__HI.get_Hex_Value()
    def get_LO_HEX(self): return self.__LO.get_Hex_Value()
    def get_MD_CNT_HEX(self): return self.__MD_CNT.get_Hex_Value()
    def get_MD_STATE_HEX(self): return self.__MD_STATE.get_Hex_Value()
    def get_STEP_CNT_HEX(self): return self.__STEP_CNT.get_Hex_Value()
    def get_OP_TYPE_HEX(self): return self.__OP_TYPE.get_Hex_Value()
    def get_STATUS_HEX(self): return self.__STATUS.get_Hex_Value()

    # Setters (CORREGIDOS - dentro de la clase)
    def set_PC(self, Input: Bus):
        self.__PC.set_Value(Input)

    def set_IR(self, Input: Bus):
        self.__IR.set_Value(Input)

    def set_AC(self, Input: Bus):
        self.__AC.set_Value(Input)

    def set_MAR(self, Input: Bus):
        self.__MAR.set_Value(Input)

    def set_MDR(self, Input: Bus):
        self.__MDR.set_Value(Input)

    def set_TEMP(self, Input: Bus):
        self.__TEMP.set_Value(Input)

    def set_FLAG_Z(self, Input: Bit): 
        self.__FLAG_Z.set_value(Input.get_value())  

    def set_FLAG_C(self, Input: Bit): 
        self.__FLAG_C.set_value(Input.get_value())

    def set_FLAG_N(self, Input: Bit): 
        self.__FLAG_N.set_value(Input.get_value())

    def set_HI(self, Input: Bus): 
        self.__HI.set_Value(Input)

    def set_LO(self, Input: Bus): 
        self.__LO.set_Value(Input)

    def set_MD_CNT(self, Input: Bus): 
        self.__MD_CNT.set_Value(Input)

    def set_MD_STATE(self, Input: Bus): 
        self.__MD_STATE.set_Value(Input)

    def set_STEP_CNT(self, Input: Bus):
        self.__STEP_CNT.set_Value(Input)

    def set_OP_TYPE(self, Input: Bus):
        self.__OP_TYPE.set_Value(Input)

    def set_STATUS(self, Input: Bus):
        self.__STATUS.set_Value(Input)