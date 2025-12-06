# Business/CPU_Core/CPU.py
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from .Control_Unit.Record_Bank import Record_Bank
from .Arithmetic_Logical_Unit.ALU import ALU
from .Control_Unit.ControlStore import ControlStore
from .Control_Unit.SignalGenerator import SignalGenerator
from .Control_Unit.MicroCounter import MicroCounter
from .Control_Unit.FSM import FSM
from .Control_Unit.Decoder import Decoder

class CPU:
    """
    Unidad Central de Procesamiento completa
    """
    
    def __init__(self, bus=None):
        # Componentes principales
        self.registers = Record_Bank()
        self.alu = ALU()
        self.control_store = ControlStore()
        self.signal_generator = SignalGenerator()
        self.micro_counter = MicroCounter()
        self.fsm = FSM()
        self.decoder = Decoder()
        
        # Estado
        self.running = Bit(0)
        self.halted = Bit(0)
        self.clock_cycle = 0
        self.instructions_executed = 0
        
        # Bus del sistema
        self.bus = bus
        
        # Buffers de E/S
        self.input_buffer = 0
        self.output_buffer = 0
        
        # Registro de operación actual
        self.current_opcode = 0
        self.current_operand = 0
        
        # Conexiones de bus (para comunicación externa)
        self.address_out = Bus(12, 0)
        self.data_out = Bus(16, 0)
        self.data_in = Bus(16, 0)
        
        # Señales de control externas
        self.mem_read = Bit(0)
        self.mem_write = Bit(0)
        self.io_read = Bit(0)
        self.io_write = Bit(0)
    
    def connect_bus(self, bus):
        """Conecta la CPU al bus del sistema"""
        self.bus = bus
    
    def reset(self):
        """Resetea la CPU a estado inicial"""
        print("Reseteando CPU...")
        
        self.running.set_value(0)
        self.halted.set_value(0)
        self.clock_cycle = 0
        self.instructions_executed = 0
        
        # Resetear componentes
        self.micro_counter.reset()
        self.fsm.set_reset(Bit(1))
        self.signal_generator.clear()
        
        # Resetear registros
        self.registers.set_PC(Bus(16, 0))
        self.registers.set_IR(Bus(16, 0))
        self.registers.set_AC(Bus(16, 0))
        self.registers.set_MAR(Bus(16, 0))
        self.registers.set_MDR(Bus(16, 0))
        self.registers.set_TEMP(Bus(16, 0))
        
        # Resetear flags
        self.registers.set_FLAG_Z(Bit(0))
        self.registers.set_FLAG_C(Bit(0))
        self.registers.set_FLAG_N(Bit(0))
        
        print("CPU reseteada")
    
    def fetch(self):
        """Ciclo de fetch: obtiene instrucción de memoria"""
        # 1. MAR ← PC
        pc_value = self.registers.get_PC().get_Dec_Value()
        self.registers.set_MAR(Bus(16, pc_value))
        
        # 2. Leer memoria en dirección MAR
        if self.bus:
            mar_value = self.registers.get_MAR().get_Dec_Value()
            data = self.bus.read(mar_value, "CPU")
            self.registers.set_MDR(data)
        else:
            # Modo simulación sin bus
            self.registers.set_MDR(Bus(16, 0))
        
        # 3. IR ← MDR
        self.registers.set_IR(self.registers.get_MDR().get_Value())
        
        # 4. PC ← PC + 1
        self.registers.get_PC().set_Value_int(pc_value + 1)
        
        print(f"[Fetch] PC={pc_value:04X}, IR={self.registers.get_IR().get_Hex_Value()}")
    
    def decode(self):
        """Decodifica la instrucción actual"""
        ir = self.registers.get_IR().get_Value()
        ir_value = ir.get_Decimal_value()
        
        # Extraer opcode (4 bits MSB) y operando (12 bits LSB)
        self.current_opcode = (ir_value >> 12) & 0xF
        self.current_operand = ir_value & 0xFFF
        
        # Mapeo de opcodes a nombres
        opcode_names = {
            0x0: "NOP", 0x1: "LOAD", 0x2: "STORE", 0x3: "ADD",
            0x4: "SUB", 0x5: "JUMP", 0x6: "JZ", 0x7: "IN",
            0x8: "OUT", 0x9: "LOADI", 0xA: "AND", 0xB: "OR",
            0xC: "XOR", 0xD: "SLL", 0xE: "SRA", 0xF: "HALT"
        }
        
        instr_name = opcode_names.get(self.current_opcode, f"UNK({self.current_opcode:X})")
        print(f"[Decode] {instr_name} opcode={self.current_opcode:X}, operand={self.current_operand:03X}")
        
        return self.current_opcode, self.current_operand
    
    def execute_microinstruction(self):
        """Ejecuta una microinstrucción usando microcódigo"""
        step = self.micro_counter.get_value_int()
        
        # Obtener palabra de control
        control_word = self.control_store.read_by_opcode_step(self.current_opcode, step)
        
        # Generar señales
        self.signal_generator.generate(control_word)
        
        # Procesar señales
        self._process_control_signals()
        
        # Verificar fin de instrucción
        if self.signal_generator.get_signal_value('END_INSTR') == 1:
            self.micro_counter.reset()
            self.instructions_executed += 1
            return True  # Instrucción completada
        else:
            self.micro_counter.increment()
            return False
    
    def _process_control_signals(self):
        """Procesa todas las señales de control generadas"""
        sig = self.signal_generator
        
        # Señales de ALU
        if sig.get_signal_value('ALUop0') == 1 or sig.get_signal_value('ALUop1') == 1:
            self._process_alu_operation()
        
        # Señales de memoria
        if sig.get_signal_value('MAR_LOAD') == 1:
            self.registers.set_MAR(Bus(16, self.current_operand))
        
        if sig.get_signal_value('MEM_READ') == 1:
            self._memory_read()
        
        if sig.get_signal_value('MEM_WRITE') == 1:
            self._memory_write()
        
        # Señales de registro
        if sig.get_signal_value('MDR_LOAD') == 1:
            self.registers.set_MDR(self.data_in)
        
        if sig.get_signal_value('IR_LOAD') == 1:
            self.registers.set_IR(self.data_in)
        
        if sig.get_signal_value('PC_LOAD') == 1:
            self.registers.get_PC().set_Value_int(self.current_operand)
        
        if sig.get_signal_value('PC_INC') == 1:
            pc = self.registers.get_PC().get_Dec_Value()
            self.registers.get_PC().set_Value_int(pc + 1)
        
        # Señales de sistema
        if sig.get_signal_value('HALT') == 1:
            self.halted.set_value(1)
            self.running.set_value(0)
    
    def _process_alu_operation(self):
        """Procesa operación de ALU"""
        sig = self.signal_generator
        
        # Obtener señales ALU
        aluop = sig.get_aluop()
        alufunc = sig.get_alufunc()
        
        # Configurar ALU
        self.alu.set_aluop(aluop)
        self.alu.set_modo_funcion(alufunc)
        
        # Preparar operandos
        input_a = self.registers.get_AC().get_Value()
        
        # Determinar segundo operando
        if self.current_opcode == 0x9:  # LOADI
            input_b = Bus(16, self.current_operand)
        elif sig.get_signal_value('MDR_LOAD') == 1:
            input_b = self.registers.get_MDR().get_Value()
        else:
            input_b = Bus(16, 0)
        
        self.alu.set_input_a(input_a)
        self.alu.set_input_b(input_b)
        
        # Ejecutar ALU
        result = self.alu.execute()
        
        # Cargar resultado si AC_LOAD está activo
        if sig.get_signal_value('AC_LOAD') == 1:
            self.registers.set_AC(result)
        
        # Actualizar flags
        self.registers.set_FLAG_Z(Bit(self.alu.get_zero_flag().get_value()))
        self.registers.set_FLAG_C(Bit(self.alu.get_carry_out().get_value()))
        self.registers.set_FLAG_N(Bit(self.alu.get_negative_flag().get_value()))
        
        print(f"[ALU] {input_a.get_Decimal_value()} op {input_b.get_Decimal_value()} = {result.get_Decimal_value()}")
    
    def _memory_read(self):
        """Operación de lectura de memoria"""
        if self.bus:
            mar = self.registers.get_MAR().get_Dec_Value()
            data = self.bus.read(mar, "CPU")
            self.registers.set_MDR(data)
            print(f"[MemRead] {mar:04X} -> {data.get_Hexadecimal_value()}")
    
    def _memory_write(self):
        """Operación de escritura en memoria"""
        if self.bus:
            mar = self.registers.get_MAR().get_Dec_Value()
            mdr = self.registers.get_MDR().get_Value()
            self.bus.write(mar, mdr, "CPU")
            print(f"[MemWrite] {mar:04X} <- {mdr.get_Hexadecimal_value()}")
    
    def clock_cycle(self):
        """Ejecuta un ciclo de reloj de CPU"""
        if self.halted.get_value() == 1:
            return
        
        self.clock_cycle += 1
        step = self.micro_counter.get_value_int()
        
        print(f"\n[Ciclo {self.clock_cycle}, Micro-paso {step}]")
        
        # Secuencia de microinstrucciones
        if step == 0:
            self.fetch()
        elif step == 1:
            # Continuación de fetch
            pass
        elif step == 2:
            # Decodificación
            self.decode()
        elif step >= 3:
            # Ejecución
            instruction_completed = self.execute_microinstruction()
            if instruction_completed:
                print(f"Instrucción completada. Total: {self.instructions_executed}")
        
        # Mostrar estado
        self._show_status()
    
    def run(self, cycles: int = 100):
        """Ejecuta la CPU por un número específico de ciclos"""
        self.running.set_value(1)
        
        print(f"\n{'='*60}")
        print("EJECUTANDO CPU")
        print(f"{'='*60}")
        
        for i in range(cycles):
            if self.halted.get_value() == 1:
                print("CPU detenida (instrucción HALT)")
                break
            
            self.clock_cycle()
        
        print(f"\n{'='*60}")
        print("EJECUCIÓN COMPLETADA")
        print(f"Ciclos: {self.clock_cycle}, Instrucciones: {self.instructions_executed}")
        print(f"{'='*60}")
    
    def _show_status(self):
        """Muestra estado actual de la CPU"""
        print(f"  PC: {self.registers.get_PC_HEX()}  IR: {self.registers.get_IR_HEX()}")
        print(f"  AC: {self.registers.get_AC_HEX()}  MAR: {self.registers.get_MAR_HEX()}")
        
        flags = self.registers
        print(f"  Flags: Z={flags.get_FLAG_Z().get_value()}, "
              f"C={flags.get_FLAG_C().get_value()}, "
              f"N={flags.get_FLAG_N().get_value()}")
    
    def load_immediate(self, address: int, value: int):
        """Carga un valor inmediato en memoria (para pruebas)"""
        if self.bus:
            self.bus.write(address, Bus(16, value), "CPU")
    
    def get_status(self):
        """Retorna estado completo de la CPU"""
        return {
            'running': self.running.get_value(),
            'halted': self.halted.get_value(),
            'clock_cycle': self.clock_cycle,
            'instructions': self.instructions_executed,
            'pc': self.registers.get_PC_HEX(),
            'ir': self.registers.get_IR_HEX(),
            'ac': self.registers.get_AC_HEX(),
            'flags': {
                'Z': self.registers.get_FLAG_Z().get_value(),
                'C': self.registers.get_FLAG_C().get_value(),
                'N': self.registers.get_FLAG_N().get_value()
            }
        }
    
    def __str__(self):
        status = self.get_status()
        return (f"CPU(PC={status['pc']}, IR={status['ir']}, "
                f"AC={status['ac']}, Instrucciones={status['instructions']})")