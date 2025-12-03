from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from .MUX2to1 import MUX2to1

class ROL:
    
    def __init__(self, Input_A: Bus = None, Input_B: Bus = None):
        # MUX Stages
        self.__1bit__stage = [MUX2to1() for _ in range(16)]
        self.__2bit__stage = [MUX2to1() for _ in range(16)]
        self.__4bit__stage = [MUX2to1() for _ in range(16)]
        self.__8bit__stage = [MUX2to1() for _ in range(16)]

        self.__Input_A = Input_A if Input_A else Bus(16)
        self.__Input_B = Input_B if Input_B else Bus(16)
        self.__Stage_0, self.__Stage_1, self.__Stage_2, self.__Stage_3 = (None,)*4

    def set_Input_A(self, input_bus: Bus): self.__Input_A = input_bus
    def set_Input_B(self, shift_amount_bus: Bus): self.__Input_B = shift_amount_bus
    def get_Input_A(self) -> Bus: return self.__Input_A
    def get_Input_B(self) -> Bus: return self.__Input_B
    def get_Output(self) -> Bus: return self.__Stage_3
    
    def __Calculate_Stage_0(self, input: Bus, S_in: Bit) -> Bus:
        K = 1
        for i in range(16):
            self.__1bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__1bit__stage[i].set_S(S_in)
            
            if i >= 16 - K: 
                # Relleno ROL (K=1): Mapea Input_A[0] a Output[15]
                self.__1bit__stage[i].set_Input_B(self.__Input_A.get_Line_bit(i - (16 - K)))
            else:
                self.__1bit__stage[i].set_Input_B(input.get_Line_bit(i + K))
        
        for i in range(16): self.__1bit__stage[i].Calculate()
        
        Output = Bus(16)
        for i in range(16): Output.set_Line_bit(i, self.__1bit__stage[i].get_Output())
        return Output

    def __Calculate_Stage_1(self, input: Bus, S_in: Bit) -> Bus:
        K = 2
        for i in range(16):
            self.__2bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__2bit__stage[i].set_S(S_in)

            if i >= 16 - K:
                # Relleno ROL (K=2): Mapea Input_A[0, 1] a Output[14, 15]
                self.__2bit__stage[i].set_Input_B(self.__Input_A.get_Line_bit(i - (16 - K)))
            else:
                self.__2bit__stage[i].set_Input_B(input.get_Line_bit(i + K))
        
        for i in range(16): self.__2bit__stage[i].Calculate()
        
        Output = Bus(16)
        for i in range(16): Output.set_Line_bit(i, self.__2bit__stage[i].get_Output())
        return Output
    
    def __Calculate_Stage_2(self, input: Bus, S_in: Bit) -> Bus:
        K = 4
        for i in range(16):
            self.__4bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__4bit__stage[i].set_S(S_in)
            if i >= 16 - K: 
                # Relleno ROL (K=4): Mapea Input_A[0, 1, 2, 3] a Output[12, 13, 14, 15]
                self.__4bit__stage[i].set_Input_B(self.__Input_A.get_Line_bit(i - (16 - K)))
            else: 
                self.__4bit__stage[i].set_Input_B(input.get_Line_bit(i + K))
        for i in range(16): self.__4bit__stage[i].Calculate()
        Output = Bus(16)
        for i in range(16): Output.set_Line_bit(i, self.__4bit__stage[i].get_Output())
        return Output

    def __Calculate_Stage_3(self, input: Bus, S_in: Bit) -> Bus:
        K = 8
        for i in range(16):
            self.__8bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__8bit__stage[i].set_S(S_in)
            if i >= 16 - K: 
                # Relleno ROL (K=8): Mapea Input_A[0...7] a Output[8...15]
                self.__8bit__stage[i].set_Input_B(self.__Input_A.get_Line_bit(i - (16 - K))) 
            else: 
                self.__8bit__stage[i].set_Input_B(input.get_Line_bit(i + K))
        for i in range(16): self.__8bit__stage[i].Calculate()
        Output = Bus(16)
        for i in range(16): Output.set_Line_bit(i, self.__8bit__stage[i].get_Output())
        return Output
    
    def Calculate(self) -> Bus:
        S0, S1, S2, S3 = (self.__Input_B.get_Line_bit(i) for i in range(15, 11, -1))
        self.__Stage_0 = self.__Calculate_Stage_0(self.__Input_A, S0)
        self.__Stage_1 = self.__Calculate_Stage_1(self.__Stage_0, S1)
        self.__Stage_2 = self.__Calculate_Stage_2(self.__Stage_1, S2)
        self.__Stage_3 = self.__Calculate_Stage_3(self.__Stage_2, S3)
        return self.__Stage_3