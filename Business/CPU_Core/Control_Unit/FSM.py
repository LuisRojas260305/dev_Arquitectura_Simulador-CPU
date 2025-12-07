from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Logic_Gates import AND_Gate, OR_Gate, NOT_Gate

class FSM:
    """
    Máquina de Estados Finitos para algoritmos secuenciales
    de multiplicación y división.
    Estados: 0=IDLE, 1=MULT_INIT, 2=MULT_CYCLE, 3=DIV_INIT, 4=DIV_CYCLE, 5=ERROR
    """
    
    def __init__(self):
        # Estado actual (3 bits para 8 estados posibles)
        self.__state_bits = [Bit(0), Bit(0), Bit(0)]  # S2, S1, S0
        
        # Señales de entrada
        self.__start_mult = Bit(0)
        self.__start_div = Bit(0)
        self.__md_done = Bit(0)
        self.__div_zero = Bit(0)
        self.__reset = Bit(0)
        
        # Señales de salida
        self.__md_start = Bit(0)
        self.__md_shift = Bit(0)
        self.__md_add = Bit(0)
        self.__md_sub = Bit(0)
        self.__md_error = Bit(0)
        self.__busy = Bit(0)  # 1 si está en MULT_CYCLE o DIV_CYCLE
        
        # Inicializar puertas lógicas
        self.__and_gates = []
        self.__or_gates = []
        self.__not_gates = []
    
    def reset(self):
        """Resetea la FSM al estado IDLE"""
        self.__set_state_value(0)  # Estado IDLE
        self.__update_outputs()
        
        # Resetear señales de entrada
        self.__start_mult.set_value(0)
        self.__start_div.set_value(0)
        self.__md_done.set_value(0)
        self.__div_zero.set_value(0)
        self.__reset.set_value(0)

    def update_state(self):
        """Calcula y actualiza el próximo estado"""
        if self.__reset.get_value() == 1:
            self.__set_state_value(0)  # Reset a IDLE
            self.__update_outputs()
            return
        
        current = self.__get_state_value()
        next_state = current
        
        # Lógica de transición de estados
        if current == 0:  # IDLE
            if self.__start_mult.get_value() == 1:
                next_state = 1  # MULT_INIT
            elif self.__start_div.get_value() == 1:
                if self.__div_zero.get_value() == 1:
                    next_state = 5  # ERROR por división por cero
                else:
                    next_state = 3  # DIV_INIT
        
        elif current == 1:  # MULT_INIT
            next_state = 2  # MULT_CYCLE
        
        elif current == 2:  # MULT_CYCLE
            if self.__md_done.get_value() == 1:
                next_state = 0  # IDLE
            else:
                next_state = 2  # Continúa en MULT_CYCLE
        
        elif current == 3:  # DIV_INIT
            next_state = 4  # DIV_CYCLE
        
        elif current == 4:  # DIV_CYCLE
            if self.__md_done.get_value() == 1:
                next_state = 0  # IDLE
            else:
                next_state = 4  # Continúa en DIV_CYCLE
        
        elif current == 5:  # ERROR
            # Se queda en ERROR hasta reset
            next_state = 5
        
        self.__set_state_value(next_state)
        self.__update_outputs()
    
    def __get_state_value(self) -> int:
        """Convierte bits de estado a entero"""
        value = 0
        for i in range(3):
            value = (value << 1) | self.__state_bits[i].get_value()
        return value
    
    def __set_state_value(self, value: int):
        """Establece el valor del estado desde entero"""
        if value < 0 or value > 7:
            raise ValueError("Valor de estado debe estar entre 0 y 7")
        
        for i in range(2, -1, -1):  # MSB first
            bit_val = (value >> i) & 1
            self.__state_bits[2-i].set_value(bit_val)
    
    def __update_outputs(self):
        """Actualiza señales de salida según estado actual"""
        state = self.__get_state_value()
        
        # Reiniciar todas las salidas
        self.__md_start = Bit(0)
        self.__md_shift = Bit(0)
        self.__md_add = Bit(0)
        self.__md_sub = Bit(0)
        self.__md_error = Bit(0)
        self.__busy = Bit(0)
        
        if state == 1:  # MULT_INIT
            self.__md_start = Bit(1)
        elif state == 2:  # MULT_CYCLE
            self.__md_shift = Bit(1)
            self.__busy = Bit(1)
        elif state == 3:  # DIV_INIT
            self.__md_start = Bit(1)
        elif state == 4:  # DIV_CYCLE
            self.__md_shift = Bit(1)
            self.__busy = Bit(1)
        elif state == 5:  # ERROR
            self.__md_error = Bit(1)
    
    # Setters para señales de entrada
    def set_start_mult(self, signal: Bit):
        if not isinstance(signal, Bit):
            raise TypeError("La señal debe ser un objeto Bit")
        self.__start_mult = signal
    
    def set_start_div(self, signal: Bit):
        if not isinstance(signal, Bit):
            raise TypeError("La señal debe ser un objeto Bit")
        self.__start_div = signal
    
    def set_md_done(self, signal: Bit):
        if not isinstance(signal, Bit):
            raise TypeError("La señal debe ser un objeto Bit")
        self.__md_done = signal
    
    def set_div_zero(self, signal: Bit):
        if not isinstance(signal, Bit):
            raise TypeError("La señal debe ser un objeto Bit")
        self.__div_zero = signal
    
    def set_reset(self, signal: Bit):
        if not isinstance(signal, Bit):
            raise TypeError("La señal debe ser un objeto Bit")
        self.__reset = signal
    
    # Getters para señales de salida
    def get_md_start(self) -> Bit:
        return self.__md_start
    
    def get_md_shift(self) -> Bit:
        return self.__md_shift
    
    def get_md_add(self) -> Bit:
        return self.__md_add
    
    def get_md_sub(self) -> Bit:
        return self.__md_sub
    
    def get_md_error(self) -> Bit:
        return self.__md_error
    
    def get_busy(self) -> Bit:
        return self.__busy
    
    def get_state(self) -> int:
        return self.__get_state_value()
    
    def get_state_bus(self) -> Bus:
        """Retorna el estado actual como bus de 3 bits"""
        bus = Bus(3, 0)
        for i in range(3):
            bus.set_Line_bit(i, self.__state_bits[i])
        return bus
    
    def is_idle(self) -> bool:
        return self.get_state() == 0
    
    def is_busy(self) -> bool:
        return self.get_busy().get_value() == 1
    
    def is_error(self) -> bool:
        return self.get_state() == 5