# Business/CPU_Core/Control_Unit/SignalGenerator.py

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class SignalGenerator:
    """
    Extrae 32 señales individuales de una palabra de control de 32 bits.
    """
    
    def __init__(self):
        # Definición de todas las señales
        self.__signals = {
            # Bits 0-1: ALUop
            'ALUop0': Bit(0),    # LSB
            'ALUop1': Bit(0),    # MSB
            
            # Bits 2-4: ALU función (3 bits)
            'ALUfunc0': Bit(0),
            'ALUfunc1': Bit(0),
            'ALUfunc2': Bit(0),
            
            # Bits 5-15: Control de registros
            'MAR_LOAD': Bit(0),
            'MDR_LOAD': Bit(0),
            'IR_LOAD': Bit(0),
            'AC_LOAD': Bit(0),
            'PC_LOAD': Bit(0),
            'PC_INC': Bit(0),
            'HI_LOAD': Bit(0),
            'LO_LOAD': Bit(0),
            'TEMP_LOAD': Bit(0),
            'MD_CNT_LOAD': Bit(0),
            'STEP_CNT_LOAD': Bit(0),
            
            # Bits 16-19: Control memoria/E/S
            'MEM_READ': Bit(0),
            'MEM_WRITE': Bit(0),
            'IO_READ': Bit(0),
            'IO_WRITE': Bit(0),
            
            # Bits 20-23: Control MULT/DIV
            'MD_START': Bit(0),
            'MD_SHIFT': Bit(0),
            'MD_ADD': Bit(0),
            'MD_SUB': Bit(0),
            
            # Bits 24-27: Control Display
            'DISP_LOAD': Bit(0),
            'DISP_SHIFT_L': Bit(0),
            'DISP_SHIFT_R': Bit(0),
            'DISP_CLEAR': Bit(0),
            
            # Bits 28-31: Control sistema
            'HALT': Bit(0),
            'RESET': Bit(0),
            'WAIT': Bit(0),
            'END_INSTR': Bit(0)
        }

        self.__signals.update({
            # Señales para multiplexores de bus (bits 32-39)
            'BUS_SEL_PC': Bit(0),
            'BUS_SEL_AC': Bit(0),
            'BUS_SEL_MDR': Bit(0),
            'BUS_SEL_ALU': Bit(0),
            'BUS_SEL_IR_OPERAND': Bit(0),
            'BUS_SEL_MEM_IN': Bit(0),
            'BUS_SEL_IO_IN': Bit(0),
            'BUS_SEL_CONST': Bit(0),
        })
        
        # Mapeo bit → nombre de señal (corregido para ser consistente)
        self.__bit_to_signal = {
            0: 'ALUop0',
            1: 'ALUop1',
            2: 'ALUfunc0',
            3: 'ALUfunc1',
            4: 'ALUfunc2',
            5: 'MAR_LOAD',
            6: 'MDR_LOAD',
            7: 'IR_LOAD',
            8: 'AC_LOAD',
            9: 'PC_LOAD',
            10: 'PC_INC',
            11: 'HI_LOAD',
            12: 'LO_LOAD',
            13: 'TEMP_LOAD',
            14: 'MD_CNT_LOAD',
            15: 'STEP_CNT_LOAD',
            16: 'MEM_READ',
            17: 'MEM_WRITE',
            18: 'IO_READ',
            19: 'IO_WRITE',
            20: 'MD_START',
            21: 'MD_SHIFT',
            22: 'MD_ADD',
            23: 'MD_SUB',
            24: 'DISP_LOAD',
            25: 'DISP_SHIFT_L',
            26: 'DISP_SHIFT_R',
            27: 'DISP_CLEAR',
            28: 'HALT',
            29: 'RESET',
            30: 'WAIT',
            31: 'END_INSTR'
        }
        
        # Inversa: señal → bit
        self.__signal_to_bit = {v: k for k, v in self.__bit_to_signal.items()}
    
    def generate(self, control_word: Bus):
        """Extrae señales de la palabra de control"""
        if control_word.width != 32:
            raise ValueError("La palabra de control debe ser de 32 bits")
        
        # Extraer cada bit y asignar a su señal correspondiente
        for bit_pos in range(32):
            bit_value = control_word.get_Line_bit(bit_pos).get_value()
            if bit_pos in self.__bit_to_signal:
                signal_name = self.__bit_to_signal[bit_pos]
                self.__signals[signal_name].set_value(bit_value)
    
    def get_signal(self, signal_name: str) -> Bit:
        """Obtiene el estado de una señal específica"""
        if signal_name not in self.__signals:
            raise ValueError(f"Señal '{signal_name}' no existe")
        return self.__signals[signal_name]
    
    def get_signal_value(self, signal_name: str) -> int:
        """Obtiene el valor de una señal específica"""
        return self.get_signal(signal_name).get_value()
    
    def get_aluop(self) -> Bus:
        """Retorna ALUop como bus de 2 bits (MSB en índice 0, LSB en índice 1)"""
        bus = Bus(2, 0)
        # En el convenio del programa: índice 0 = MSB, índice 1 = LSB
        # ALUop1 es el MSB (bit 1 en la palabra de control), ALUop0 es el LSB (bit 0)
        bus.set_Line_bit(0, self.__signals['ALUop1'])  # MSB
        bus.set_Line_bit(1, self.__signals['ALUop0'])  # LSB
        return bus

    def get_alufunc(self) -> Bus:
        """Retorna ALU función como bus de 3 bits (MSB en índice 0, LSB en índice 2)"""
        bus = Bus(3, 0)
        # ALUfunc2 es MSB, ALUfunc1 es medio, ALUfunc0 es LSB
        bus.set_Line_bit(0, self.__signals['ALUfunc2'])  # MSB
        bus.set_Line_bit(1, self.__signals['ALUfunc1'])  # Medio
        bus.set_Line_bit(2, self.__signals['ALUfunc0'])  # LSB
        return bus
        
    def get_all_signals(self) -> dict:
        """Retorna todas las señales como diccionario"""
        return {k: v.get_value() for k, v in self.__signals.items()}
    
    def get_active_signals(self) -> list:
        """Retorna lista de señales activas"""
        return [name for name, bit in self.__signals.items() if bit.get_value() == 1]
    
    def clear(self):
        """Desactiva todas las señales"""
        for signal in self.__signals.values():
            signal.set_value(0)