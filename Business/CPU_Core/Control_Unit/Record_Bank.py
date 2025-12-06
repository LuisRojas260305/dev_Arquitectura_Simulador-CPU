"""
Registros:
- PC (16 bits) - Program Counter
- IR (16 bits) - Instruction Register  
- AC (16 bits) - Accumulator
- MAR (12 bits) - Memory Address Register
- MDR (16 bits) - Memory Data Register
- Temp (16 bits) - Registro Temporal
"""

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
        self.__STATUS= Record(8)

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

    # HEX
    def get_PC_HEX(self): return self.__PC.get_Hexadecimal_value()
    def get_IR_HEX(self): return self.__IR.get_Hexadecimal_value()
    def get_AC_HEX(self): return self.__AC.get_Hexadecimal_value()
    def get_MAR_HEX(self): return self.__MAR.get_Hexadecimal_value()
    def get_MDR_HEX(self): return self.__MDR.get_Hexadecimal_value()
    def get_TEMP_HEX(self): return self.__TEMP.get_Hexadecimal_value()

    # Setters
    def set_PC(self, Input: Bus = Bus(16)): self.__PC = Input
    def set_IR(self, Input: Bus = Bus(16)): self.__IR = Input
    def set_AC(self, Input: Bus = Bus(16)): self.__AC = Input
    def set_MAR(self, Input: Bus = Bus(16)): self.__MAR = Input
    def set_MDR(self, Input: Bus = Bus(16)): self.__MDR = Input
    def set_TEMP(self, Input: Bus = Bus(16)): self.__TEMP = Input
    def set_FLAG_Z(self, Input: Bit): self.__FLAG_Z = Input
    