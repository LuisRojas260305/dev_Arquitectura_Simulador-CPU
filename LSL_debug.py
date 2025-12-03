from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.MUX2to1 import MUX2to1

class LSL_debug:
    
    # Constructor
    def __init__(self, Input_A: Bus = None, Input_B: Bus = None):
        # MUX Stages
        self.__1bit__stage = [MUX2to1() for _ in range(16)]
        self.__2bit__stage = [MUX2to1() for _ in range(16)]
        self.__4bit__stage = [MUX2to1() for _ in range(16)]
        self.__8bit__stage = [MUX2to1() for _ in range(16)]

        # Inputs 
        self.__Input_A = Input_A if Input_A else Bus(16)
        self.__Input_B = Input_B if Input_B else Bus(16)

        # Stages Storage
        self.__Stage_0 = None
        self.__Stage_1 = None
        self.__Stage_2 = None
        self.__Stage_3 = None
        
        # Debug mode
        self.debug = True

    # --- Setters y Getters ---
    def set_Input_A(self, input_bus: Bus):
        self.__Input_A = input_bus
    def set_Input_B(self, shift_amount_bus: Bus):
        self.__Input_B = shift_amount_bus
    def get_Input_A(self) -> Bus:
        return self.__Input_A
    def get_Input_B(self) -> Bus:
        return self.__Input_B
    def get_Output(self) -> Bus:
        return self.__Stage_3
    
    # --- Metodos Internos ---
    def __Calculate_Stage_0(self, input: Bus, S_in: Bit) -> Bus:
        if self.debug:
            print(f"\n[LSL DEBUG] Etapa 0 (1-bit shift)")
            print(f"  S_in = {S_in.get_value()}")
            print(f"  Input: {input.get_Hexadecimal_value()} = {input.get_Binary_value()}")
        
        Output = Bus(16)
        for i in range(16):
            input_a_bit = input.get_Line_bit(i)
            self.__1bit__stage[i].set_Input_A(input_a_bit)
            self.__1bit__stage[i].set_S(S_in)
            
            if i >= 15: # LSL: Relleno en LSB (Indice alto)
                input_b_bit = Bit(0)
                self.__1bit__stage[i].set_Input_B(input_b_bit)
                if self.debug and S_in.get_value() == 1:
                    print(f"  Bit {i:2d} (LSB): A={input_a_bit.get_value()}, B=0 (relleno), S=1 → ", end="")
            else:
                input_b_bit = input.get_Line_bit(i + 1)
                self.__1bit__stage[i].set_Input_B(input_b_bit)
                if self.debug and S_in.get_value() == 1:
                    print(f"  Bit {i:2d}: A={input_a_bit.get_value()}, B={input_b_bit.get_value()} (bit {i+1}), S=1 → ", end="")
            
            self.__1bit__stage[i].Calculate()
            output_bit = self.__1bit__stage[i].get_Output()
            Output.set_Line_bit(i, output_bit)
            
            if self.debug and S_in.get_value() == 1:
                print(f"Out={output_bit.get_value()}")
        
        if self.debug:
            print(f"  Output: {Output.get_Hexadecimal_value()} = {Output.get_Binary_value()}")
        
        return Output

    def __Calculate_Stage_1(self, input: Bus, S_in: Bit) -> Bus:
        if self.debug:
            print(f"\n[LSL DEBUG] Etapa 1 (2-bit shift)")
            print(f"  S_in = {S_in.get_value()}")
            print(f"  Input: {input.get_Hexadecimal_value()}")
        
        Output = Bus(16)
        for i in range(16):
            self.__2bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__2bit__stage[i].set_S(S_in)

            if i >= 14:
                self.__2bit__stage[i].set_Input_B(Bit(0))
            else:
                self.__2bit__stage[i].set_Input_B(input.get_Line_bit(i + 2))
            
            self.__2bit__stage[i].Calculate()
            Output.set_Line_bit(i, self.__2bit__stage[i].get_Output())
        
        if self.debug and S_in.get_value() == 1:
            print(f"  Output: {Output.get_Hexadecimal_value()}")
        
        return Output
    
    def __Calculate_Stage_2(self, input: Bus, S_in: Bit) -> Bus:
        if self.debug:
            print(f"\n[LSL DEBUG] Etapa 2 (4-bit shift)")
            print(f"  S_in = {S_in.get_value()}")
            print(f"  Input: {input.get_Hexadecimal_value()}")
        
        Output = Bus(16)
        for i in range(16):
            self.__4bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__4bit__stage[i].set_S(S_in)

            if i >= 12:
                self.__4bit__stage[i].set_Input_B(Bit(0))
            else:
                self.__4bit__stage[i].set_Input_B(input.get_Line_bit(i + 4))
            
            self.__4bit__stage[i].Calculate()
            Output.set_Line_bit(i, self.__4bit__stage[i].get_Output())
        
        if self.debug and S_in.get_value() == 1:
            print(f"  Output: {Output.get_Hexadecimal_value()}")
        
        return Output

    def __Calculate_Stage_3(self, input: Bus, S_in: Bit) -> Bus:
        if self.debug:
            print(f"\n[LSL DEBUG] Etapa 3 (8-bit shift)")
            print(f"  S_in = {S_in.get_value()}")
            print(f"  Input: {input.get_Hexadecimal_value()}")
        
        Output = Bus(16)
        for i in range(16):
            self.__8bit__stage[i].set_Input_A(input.get_Line_bit(i))
            self.__8bit__stage[i].set_S(S_in)

            if i >= 8:
                self.__8bit__stage[i].set_Input_B(Bit(0))
            else:
                self.__8bit__stage[i].set_Input_B(input.get_Line_bit(i + 8))
            
            self.__8bit__stage[i].Calculate()
            Output.set_Line_bit(i, self.__8bit__stage[i].get_Output())
        
        if self.debug and S_in.get_value() == 1:
            print(f"  Output: {Output.get_Hexadecimal_value()}")
        
        return Output
    
    def Calculate(self) -> Bus:
        # Señales de control (Bits 12-15 del bus de control)
        S0 = self.__Input_B.get_Line_bit(15)
        S1 = self.__Input_B.get_Line_bit(14)
        S2 = self.__Input_B.get_Line_bit(13)
        S3 = self.__Input_B.get_Line_bit(12)
        
        if self.debug:
            print("\n" + "="*60)
            print(f"[LSL DEBUG] Iniciando cálculo")
            print(f"  Input A: {self.__Input_A.get_Hexadecimal_value()}")
            print(f"  Input B: {self.__Input_B.get_Hexadecimal_value()}")
            print(f"  Bits de control: S0(bit15)={S0.get_value()}, S1(bit14)={S1.get_value()}, "
                  f"S2(bit13)={S2.get_value()}, S3(bit12)={S3.get_value()}")
            print("="*60)

        # Calcular Etapas en cascada
        self.__Stage_0 = self.__Calculate_Stage_0(self.__Input_A, S0)
        self.__Stage_1 = self.__Calculate_Stage_1(self.__Stage_0, S1)
        self.__Stage_2 = self.__Calculate_Stage_2(self.__Stage_1, S2)
        self.__Stage_3 = self.__Calculate_Stage_3(self.__Stage_2, S3)
        
        if self.debug:
            print("\n" + "="*60)
            print(f"[LSL DEBUG] Resultado final: {self.__Stage_3.get_Hexadecimal_value()}")
            print("="*60)
        
        return self.__Stage_3