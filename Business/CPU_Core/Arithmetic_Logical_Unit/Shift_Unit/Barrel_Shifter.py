# Business/CPU_Core/Arithmetic_Logical_Unit/Shift_Unit/Barrel_Shifter.py
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.MUX2to1 import MUX2to1

class Barrel_Shifter:
    def __init__(self):
        self.__width = 16
        
        # Reset all MUX states
        self.__1bit_state = [MUX2to1() for _ in range(16)]
        self.__2bit_state = [MUX2to1() for _ in range(16)]
        self.__4bit_state = [MUX2to1() for _ in range(16)]
        self.__8bit_state = [MUX2to1() for _ in range(16)]

    def __reset_muxes(self):
        """Reinicia todos los MUX a su estado inicial"""
        for mux in self.__1bit_state + self.__2bit_state + self.__4bit_state + self.__8bit_state:
            mux.set_Input_A(Bit(0))
            mux.set_Input_B(Bit(0))
            mux.set_S(Bit(0))
            mux.Calculate()

    def shift_left_logical(self, input_bus: Bus, shift_amount: Bus) -> Bus:
        # Reiniciar MUXes
        self.__reset_muxes()
        
        # Obtener los bits de control de las posiciones 12-15
        s0 = shift_amount.get_Line_bit(12)  # Bit 12 - control etapa 1-bit
        s1 = shift_amount.get_Line_bit(13)  # Bit 13 - control etapa 2-bit  
        s2 = shift_amount.get_Line_bit(14)  # Bit 14 - control etapa 4-bit
        s3 = shift_amount.get_Line_bit(15)  # Bit 15 - control etapa 8-bit

        # Start with original input
        current_stage = [input_bus.get_Line_bit(i) for i in range(16)]

        # === Stage 1: 1-bit shift ===
        stage1_output = []
        for i in range(16):
            mux = self.__1bit_state[i]
            
            # For LEFT shift: bit i viene de la posición i-1 (rellenar con 0 en LSB)
            if i == 0:  # MSB gets 0 when shifting left
                shifted_bit = Bit(0)
            else:
                shifted_bit = current_stage[i - 1]  # Tomar de la izquierda
            
            mux.set_Input_A(current_stage[i])  # No shift
            mux.set_Input_B(shifted_bit)       # Shift by 1
            mux.set_S(s0)
            mux.Calculate()
            stage1_output.append(mux.get_Output())
        
        current_stage = stage1_output

        # === Stage 2: 2-bit shift ===
        stage2_output = []
        for i in range(16):
            mux = self.__2bit_state[i]
            
            # For LEFT shift by 2: bit i viene de la posición i-2 (rellenar con 0)
            if i < 2:  # Primeros 2 bits obtienen 0
                shifted_bit = Bit(0)
            else:
                shifted_bit = current_stage[i - 2]  # Tomar de la izquierda
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 2-bit shift
            mux.set_S(s1)
            mux.Calculate()
            stage2_output.append(mux.get_Output())
        
        current_stage = stage2_output

        # === Stage 3: 4-bit shift ===
        stage3_output = []
        for i in range(16):
            mux = self.__4bit_state[i]
            
            # For LEFT shift by 4: bit i viene de la posición i-4 (rellenar con 0)
            if i < 4:  # Primeros 4 bits obtienen 0
                shifted_bit = Bit(0)
            else:
                shifted_bit = current_stage[i - 4]  # Tomar de la izquierda
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 4-bit shift
            mux.set_S(s2)
            mux.Calculate()
            stage3_output.append(mux.get_Output())
        
        current_stage = stage3_output

        # === Stage 4: 8-bit shift ===
        stage4_output = []
        for i in range(16):
            mux = self.__8bit_state[i]
            
            # For LEFT shift by 8: bit i viene de la posición i-8 (rellenar con 0)
            if i < 8:  # Primeros 8 bits obtienen 0
                shifted_bit = Bit(0)
            else:
                shifted_bit = current_stage[i - 8]  # Tomar de la izquierda
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 8-bit shift
            mux.set_S(s3)
            mux.Calculate()
            stage4_output.append(mux.get_Output())
        
        current_stage = stage4_output

        # Build final result
        result_bus = Bus(16)
        for i in range(16):
            result_bus.set_Line_bit(i, current_stage[i])
        
        return result_bus

    def shift_right_arithmetic(self, input_bus: Bus, shift_amount: Bus) -> Bus:
        # Reiniciar MUXes
        self.__reset_muxes()
        
        # Obtener los bits de control de las posiciones 12-15
        s0 = shift_amount.get_Line_bit(12)  # Bit 12 - control etapa 1-bit
        s1 = shift_amount.get_Line_bit(13)  # Bit 13 - control etapa 2-bit  
        s2 = shift_amount.get_Line_bit(14)  # Bit 14 - control etapa 4-bit
        s3 = shift_amount.get_Line_bit(15)  # Bit 15 - control etapa 8-bit

        sign_bit = input_bus.get_Line_bit(0)  # MSB para extensión de signo

        # Start with original input
        current_stage = [input_bus.get_Line_bit(i) for i in range(16)]

        # === Stage 1: 1-bit shift ===
        stage1_output = []
        for i in range(16):
            mux = self.__1bit_state[i]
            
            # For RIGHT shift: bit i viene de la posición i+1 (rellenar con signo en MSB)
            if i == 15:  # LSB obtiene extensión de signo para shift aritmético
                shifted_bit = sign_bit
            else:
                shifted_bit = current_stage[i + 1]  # Tomar de la derecha
            
            mux.set_Input_A(current_stage[i])  # No shift
            mux.set_Input_B(shifted_bit)       # Shift by 1
            mux.set_S(s0)
            mux.Calculate()
            stage1_output.append(mux.get_Output())
        
        current_stage = stage1_output

        # === Stage 2: 2-bit shift ===
        stage2_output = []
        for i in range(16):
            mux = self.__2bit_state[i]
            
            # For RIGHT shift by 2: bit i viene de la posición i+2 (rellenar con signo)
            if i >= 14:  # Últimos 2 bits obtienen extensión de signo
                shifted_bit = sign_bit
            else:
                shifted_bit = current_stage[i + 2]  # Tomar de la derecha
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 2-bit shift
            mux.set_S(s1)
            mux.Calculate()
            stage2_output.append(mux.get_Output())
        
        current_stage = stage2_output

        # === Stage 3: 4-bit shift ===
        stage3_output = []
        for i in range(16):
            mux = self.__4bit_state[i]
            
            # For RIGHT shift by 4: bit i viene de la posición i+4 (rellenar con signo)
            if i >= 12:  # Últimos 4 bits obtienen extensión de signo
                shifted_bit = sign_bit
            else:
                shifted_bit = current_stage[i + 4]  # Tomar de la derecha
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 4-bit shift
            mux.set_S(s2)
            mux.Calculate()
            stage3_output.append(mux.get_Output())
        
        current_stage = stage3_output

        # === Stage 4: 8-bit shift ===
        stage4_output = []
        for i in range(16):
            mux = self.__8bit_state[i]
            
            # For RIGHT shift by 8: bit i viene de la posición i+8 (rellenar con signo)
            if i >= 8:  # Últimos 8 bits obtienen extensión de signo
                shifted_bit = sign_bit
            else:
                shifted_bit = current_stage[i + 8]  # Tomar de la derecha
            
            mux.set_Input_A(current_stage[i])  # Previous stage
            mux.set_Input_B(shifted_bit)       # Additional 8-bit shift
            mux.set_S(s3)
            mux.Calculate()
            stage4_output.append(mux.get_Output())
        
        current_stage = stage4_output

        # Build final result
        result_bus = Bus(16)
        for i in range(16):
            result_bus.set_Line_bit(i, current_stage[i])
        
        return result_bus

    # Los métodos de debugging y representación se mantienen igual
    def get_etapa1_result(self):
        return [mux.get_Output() for mux in self.__1bit_state]
    
    def get_etapa2_result(self):
        return [mux.get_Output() for mux in self.__2bit_state]
    
    def get_etapa3_result(self):
        return [mux.get_Output() for mux in self.__4bit_state]
    
    def get_etapa4_result(self):
        return [mux.get_Output() for mux in self.__8bit_state]
    
    def get_mux_states(self):
        return {
            'etapa_1bit': self.__get_mux_stage_state(self.__1bit_state),
            'etapa_2bits': self.__get_mux_stage_state(self.__2bit_state),
            'etapa_4bits': self.__get_mux_stage_state(self.__4bit_state),
            'etapa_8bits': self.__get_mux_stage_state(self.__8bit_state)
        }
    
    def __get_mux_stage_state(self, stage_muxes):
        return [(mux.get_Input_A(), mux.get_Input_B(), mux.get_S(), mux.get_Output()) 
                for mux in stage_muxes]
    
    def __str__(self):
        return "BarrelShifter_16bit(corregido_con_bits_12_15)"