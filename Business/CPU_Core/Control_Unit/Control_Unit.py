from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from .ControlStore import ControlStore
from .SignalGenerator import SignalGenerator
from .MicroCounter import MicroCounter
from .FSM import FSM
from .Decoder import Decoder

class Control_Unit:
    """
    Unidad de Control principal que coordina todos los componentes
    """
    
    def __init__(self):
        # Componentes de la UC
        self.control_store = ControlStore()
        self.signal_generator = SignalGenerator()
        self.micro_counter = MicroCounter()
        self.fsm = FSM()
        self.decoder = Decoder()
        
        # Estado actual
        self.current_instruction = Bus(16, 0)
        self.current_opcode = 0
        self.current_step = 0
        self.halted = Bit(0)
        
        # Señales de control actuales
        self.control_signals = {}
        
        # Estadísticas
        self.cycles_executed = 0
    
    def reset(self):
        """Resetea la Unidad de Control a estado inicial"""
        self.micro_counter.reset()
        self.fsm.reset()
        self.signal_generator.clear()
        self.decoder.reset()
        
        self.current_instruction = Bus(16, 0)
        self.current_opcode = 0
        self.current_step = 0
        self.halted.set_value(0)
        self.cycles_executed = 0
        
        print("UC: Unidad de Control reseteada")
    
    def load_instruction(self, instruction_bus: Bus):
        """
        Carga una nueva instrucción para decodificar
        """
        if not isinstance(instruction_bus, Bus):
            raise TypeError("La instrucción debe ser un Bus")
        
        self.current_instruction = instruction_bus
        self.decoder.set_instruction(instruction_bus)
        self.current_opcode = self.decoder.get_opcode()
        
        # Reiniciar microcontador para nueva instrucción
        self.micro_counter.reset()
        self.current_step = 0
        
        print(f"UC: Instrucción cargada: {instruction_bus.get_Hexadecimal_value()}")
        print(f"UC: Opcode decodificado: 0x{self.current_opcode:X}")
    
    def execute_cycle(self):
        """
        Ejecuta un ciclo de microinstrucción
        Retorna True si la instrucción ha terminado
        """
        if self.halted.get_value() == 1:
            print("UC: Sistema detenido")
            return True
        
        # Obtener la palabra de control actual
        control_word = self.control_store.read_by_opcode_step(
            self.current_opcode,
            self.micro_counter.get_value_int()
        )
        
        # Generar señales de control
        self.signal_generator.generate(control_word)
        # CORRECCIÓN: Cambiar get_signals() por get_all_signals()
        self.control_signals = self.signal_generator.get_all_signals()
        
        # Verificar si es el fin de la instrucción
        end_instruction = False
        if self.signal_generator.get_signal_value('END_INSTR') == 1:
            end_instruction = True
            print("UC: Fin de instrucción alcanzado")
        
        # Incrementar contador si no es el final
        if not end_instruction:
            self.micro_counter.increment()
            self.current_step += 1
        else:
            self.micro_counter.reset()
            self.current_step = 0
        
        self.cycles_executed += 1
        
        # Verificar señal de HALT
        if self.signal_generator.get_signal_value('HALT') == 1:
            self.halted.set_value(1)
            print("UC: Señal HALT recibida")
        
        return end_instruction
    
    def get_alu_control(self):
        """
        Retorna las señales de control para la ALU
        """
        alu_ctrl = {
            'aluop': self.signal_generator.get_aluop(),
            'modo_funcion': self.signal_generator.get_alufunc()
        }
        
        # Convertir los buses a enteros para mayor facilidad
        alu_ctrl['aluop_value'] = alu_ctrl['aluop'].get_Decimal_value() if alu_ctrl['aluop'] else None
        alu_ctrl['modo_funcion_value'] = alu_ctrl['modo_funcion'].get_Decimal_value() if alu_ctrl['modo_funcion'] else None
        
        return alu_ctrl
    
    def get_memory_control(self):
        """
        Retorna las señales de control para memoria
        """
        return {
            'mem_read': self.signal_generator.get_signal_value('MEM_READ'),
            'mem_write': self.signal_generator.get_signal_value('MEM_WRITE'),
            'mar_load': self.signal_generator.get_signal_value('MAR_LOAD'),
            'mdr_load': self.signal_generator.get_signal_value('MDR_LOAD')
        }
    
    def get_register_control(self):
        """
        Retorna las señales de control para registros
        """
        return {
            'pc_load': self.signal_generator.get_signal_value('PC_LOAD'),
            'pc_inc': self.signal_generator.get_signal_value('PC_INC'),
            'ir_load': self.signal_generator.get_signal_value('IR_LOAD'),
            'ac_load': self.signal_generator.get_signal_value('AC_LOAD')
        }
    
    def get_current_status(self):
        """
        Retorna el estado actual de la UC
        """
        return {
            'instruction': self.current_instruction.get_Hexadecimal_value(),
            'opcode': self.current_opcode,
            'micro_step': self.current_step,
            'halted': self.halted.get_value(),
            'cycles': self.cycles_executed,
            'signals': self.control_signals
        }
    
    def get_operand(self):
        """
        Retorna el operando de la instrucción actual
        """
        return self.decoder.get_operand()
    
    def get_instruction_type(self):
        """
        Retorna el tipo de instrucción actual
        """
        return self.decoder.get_instruction_type()
    
    def is_halted(self):
        """Retorna True si la UC está en estado HALT"""
        return self.halted.get_value() == 1
    
    def __str__(self):
        status = self.get_current_status()
        return (f"Control_Unit(Inst={status['instruction']}, "
                f"Opcode=0x{status['opcode']:X}, "
                f"Step={status['micro_step']}, "
                f"Halted={status['halted']})")