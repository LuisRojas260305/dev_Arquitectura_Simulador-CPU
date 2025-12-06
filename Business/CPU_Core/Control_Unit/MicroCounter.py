from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Record import Record

class MicroCounter:
    """
    Contador de 4 bits para microinstrucciones.
    Implementa incremento, reset, carga paralela y detección de límites.
    """
    
    def __init__(self):
        self.__value = Record(4, 0)  # Valor actual (0-15)
        
        # Señales de control
        self.__reset_signal = Bit(0)
        self.__increment_signal = Bit(0)
        self.__load_signal = Bit(0)
        self.__load_data = Bus(4, 0)
        
        # Estado interno del "reloj"
        self.__clock_state = Bit(0)
    
    def clock_tick(self):
        """
        Simula un flanco de reloj ascendente.
        En hardware real, esto sería disparado por el reloj del sistema.
        """
        if self.__clock_state.get_value() == 0:
            # Flanco ascendente: actualizar valor
            self.__update_value()
            self.__clock_state.set_value(1)
        else:
            # Flanco descendente
            self.__clock_state.set_value(0)
    
    def __update_value(self):
        """Calcula y actualiza el próximo valor del contador"""
        current = self.__value.get_Dec_Value()
        next_val = current
        
        # Prioridad: RESET > LOAD > INCREMENT
        if self.__reset_signal.get_value() == 1:
            next_val = 0
        elif self.__load_signal.get_value() == 1:
            next_val = self.__load_data.get_Decimal_value()
        elif self.__increment_signal.get_value() == 1:
            next_val = (current + 1) % 16  # Wrap-around en 15→0
        
        # Actualizar solo si hubo cambio
        if next_val != current:
            self.__value.set_Value_int(next_val)
    
    # === Métodos de consulta ===
    
    def get_value(self) -> Record:
        """Retorna el valor actual como Record"""
        return self.__value
    
    def get_value_bus(self) -> Bus:
        """Retorna el valor actual como Bus de 4 bits"""
        return self.__value.get_Value()
    
    def get_value_int(self) -> int:
        """Retorna el valor actual como entero"""
        return self.__value.get_Dec_Value()
    
    def is_max(self) -> Bit:
        """Retorna 1 si el contador está en 15 (máximo)"""
        return Bit(1) if self.__value.get_Dec_Value() == 15 else Bit(0)
    
    def is_min(self) -> Bit:
        """Retorna 1 si el contador está en 0 (mínimo)"""
        return Bit(1) if self.__value.get_Dec_Value() == 0 else Bit(0)
    
    def is_equal_to(self, value: int) -> Bit:
        """Retorna 1 si el contador es igual al valor dado"""
        if value < 0 or value > 15:
            raise ValueError("El valor debe estar entre 0 y 15")
        return Bit(1) if self.__value.get_Dec_Value() == value else Bit(0)
    
    # === Setters para señales de control ===
    
    def set_reset(self, signal: Bit):
        """Activa/desactiva la señal de reset"""
        self.__reset_signal = signal
    
    def set_increment(self, signal: Bit):
        """Activa/desactiva la señal de incremento"""
        self.__increment_signal = signal
    
    def set_load(self, signal: Bit):
        """Activa/desactiva la señal de carga"""
        self.__load_signal = signal
    
    def set_load_data(self, data: Bus):
        """Establece los datos a cargar"""
        if data.width != 4:
            raise ValueError("Los datos de carga deben ser de 4 bits")
        self.__load_data = data
    
    def set_load_data_int(self, value: int):
        """Establece los datos a cargar desde un entero"""
        if value < 0 or value > 15:
            raise ValueError("El valor debe estar entre 0 y 15")
        self.__load_data = Bus(4, value)
    
    # === Métodos de utilidad ===
    
    def reset(self):
        """Resetea el contador a 0"""
        self.__reset_signal = Bit(1)
        self.clock_tick()
        self.__reset_signal = Bit(0)
    
    def increment(self):
        """Incrementa el contador una vez"""
        self.__increment_signal = Bit(1)
        self.clock_tick()
        self.__increment_signal = Bit(0)
    
    def load(self, value: int):
        """Carga un valor específico"""
        self.set_load_data_int(value)
        self.__load_signal = Bit(1)
        self.clock_tick()
        self.__load_signal = Bit(0)
    
    def __str__(self):
        value = self.__value.get_Dec_Value()
        reset = self.__reset_signal.get_value()
        inc = self.__increment_signal.get_value()
        load = self.__load_signal.get_value()
        
        return (f"MicroCounter(value={value:02d}, "
                f"reset={reset}, inc={inc}, load={load})")