# Business/CPU_Core/CPU.py - ISA ESTANDARIZADO
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.CPU_Core.Control_Unit.Record_Bank import Record_Bank
from Business.CPU_Core.Control_Unit.Control_Unit import Control_Unit
from Business.CPU_Core.Arithmetic_Logical_Unit.ALU import ALU
from Business.Memory.SystemBus import SystemBus
from Business.Memory.RAM import RAM

class CPU:
    """Unidad Central de Procesamiento con ISA Estandarizado"""
    
    def __init__(self, bus: SystemBus):
        # Componentes principales
        self.bus = bus
        self.registers = Record_Bank()
        self.alu = ALU()
        self.control_unit = Control_Unit()
        
        # Estado de la CPU
        self.running = Bit(0)
        self.clock_cycle = 0
        self.instructions_executed = 0
        
        # Conexión con memoria
        self.memory = None
        
    def connect_memory(self, memory: RAM):
        """Conecta la memoria a la CPU"""
        self.memory = memory
        
    def reset(self):
        """Resetea la CPU a estado inicial"""
        # Resetear registros usando setters
        self.registers.set_PC(Bus(16, 0))
        self.registers.set_IR(Bus(16, 0))
        self.registers.set_AC(Bus(16, 0))
        self.registers.set_MAR(Bus(16, 0))
        self.registers.set_MDR(Bus(16, 0))
        self.registers.set_TEMP(Bus(16, 0))
        
        # Resetear registros secuenciales
        self.registers.set_HI(Bus(16, 0))
        self.registers.set_LO(Bus(16, 0))
        self.registers.set_MD_CNT(Bus(4, 0))
        self.registers.set_MD_STATE(Bus(3, 0))
        
        # Resetear registros de control
        self.registers.set_STEP_CNT(Bus(4, 0))
        self.registers.set_OP_TYPE(Bus(4, 0))
        self.registers.set_STATUS(Bus(8, 0))
        
        # Resetear flags
        self.registers.set_FLAG_Z(Bit(0))
        self.registers.set_FLAG_C(Bit(0))
        self.registers.set_FLAG_N(Bit(0))
        
        # Resetear estado interno
        self.running.set_value(0)
        self.clock_cycle = 0
        self.instructions_executed = 0
        
        # Resetear componentes
        self.control_unit.reset()
        
        print("CPU: Reset completo")
        
    def fetch(self):
        """Ciclo de fetch simplificado"""
        if not self.running.get_value():
            return False
            
        # Obtener dirección del PC
        pc_value = self.registers.get_PC().get_Dec_Value()
        
        # MAR <- PC
        self.registers.set_MAR(Bus(16, pc_value))
        
        # Leer memoria
        if self.memory:
            data_bus = self.memory.read_direct(pc_value)
            self.registers.set_MDR(data_bus)
        
        # IR <- MDR
        self.registers.set_IR(self.registers.get_MDR().get_Value())
        
        # PC <- PC + 1
        self.registers.get_PC().set_Value_int(pc_value + 1)
        
        # Cargar instrucción en Unidad de Control
        self.control_unit.load_instruction(self.registers.get_IR().get_Value())
        
        print(f"CPU: Fetch en PC={pc_value:04X}, Inst={self.registers.get_IR().get_Hex_Value()}")
        return True
    
    def execute(self):
        """Ejecuta la instrucción actual según ISA estandarizado"""
        if not self.running.get_value():
            return False
        
        # Obtener información de la instrucción
        ir_value = self.registers.get_IR().get_Dec_Value()
        opcode = (ir_value >> 12) & 0xF
        operand = ir_value & 0xFFF
        
        print(f"CPU: Ejecutando {self._get_mnemonic(opcode)} (0x{opcode:X}) con operando 0x{operand:03X}")
        
        # Configurar OP_TYPE
        self.registers.set_OP_TYPE(Bus(4, opcode))
        
        # Dispatch según ISA estandarizado
        if opcode == 0x0:  # NOP
            print("CPU: NOP - No operation")
            
        elif opcode == 0x1:  # LOAD
            self._execute_load(operand)
            
        elif opcode == 0x2:  # STORE
            self._execute_store(operand)
            
        elif opcode == 0x3:  # ADD
            self._execute_alu_operation(operand, aluop=0b00, mode=0b000)
            
        elif opcode == 0x4:  # SUB
            self._execute_alu_operation(operand, aluop=0b00, mode=0b001)
            
        elif opcode == 0x5:  # MULT
            self._execute_multiplication(operand)
            
        elif opcode == 0x6:  # DIV
            self._execute_division(operand)
            
        elif opcode == 0x7:  # JUMP
            self.registers.get_PC().set_Value_int(operand)
            print(f"CPU: JUMP a 0x{operand:03X}")
            
        elif opcode == 0x8:  # JZ (Jump if Zero)
            if self.registers.get_FLAG_Z().get_value() == 1:
                self.registers.get_PC().set_Value_int(operand)
                print(f"CPU: JZ tomado a 0x{operand:03X} (Z=1)")
            else:
                print("CPU: JZ no tomado (Z=0)")
            
        elif opcode == 0x9:  # LOADI
            self.registers.set_AC(Bus(16, operand))
            print(f"CPU: LOADI 0x{operand:03X} -> AC=0x{operand:04X}")
            
        elif opcode == 0xA:  # AND
            self._execute_alu_operation(operand, aluop=0b01, mode=0b000)
            
        elif opcode == 0xB:  # OR
            self._execute_alu_operation(operand, aluop=0b01, mode=0b001)
            
        elif opcode == 0xC:  # XOR
            self._execute_alu_operation(operand, aluop=0b01, mode=0b010)
            
        elif opcode == 0xD:  # SHL
            self._execute_shift(operand, aluop=0b10, mode=0b000)
            
        elif opcode == 0xE:  # SHR
            self._execute_shift(operand, aluop=0b10, mode=0b001)
            
        elif opcode == 0xF:  # HALT
            print("CPU: HALT - Deteniendo ejecución")
            self.running.set_value(0)
            
        else:
            print(f"CPU: ERROR - Opcode 0x{opcode:X} no implementado")
        
        self.instructions_executed += 1
        return True
    
    # ===== MÉTODOS DE EJECUCIÓN DE INSTRUCCIONES =====
    
    def _execute_load(self, address):
        """LOAD: AC ← Memoria[address]"""
        # MAR ← address
        self.registers.set_MAR(Bus(16, address))
        
        # Leer memoria
        if self.memory:
            data_bus = self.memory.read_direct(address)
            self.registers.set_MDR(data_bus)
            self.registers.set_AC(self.registers.get_MDR().get_Value())
            print(f"CPU: LOAD [0x{address:03X}] = {self.registers.get_AC().get_Hex_Value()} -> AC")
    
    def _execute_store(self, address):
        """STORE: Memoria[address] ← AC"""
        # MAR ← address
        self.registers.set_MAR(Bus(16, address))
        
        # MDR ← AC
        self.registers.set_MDR(self.registers.get_AC().get_Value())
        
        # Escribir memoria
        if self.memory:
            mdr_value = self.registers.get_MDR().get_Dec_Value()
            self.memory.write_direct(address, mdr_value)
            print(f"CPU: STORE AC={self.registers.get_AC().get_Hex_Value()} -> [0x{address:03X}]")
    
    def _execute_alu_operation(self, address, aluop, mode):
        """Operaciones ALU básicas: ADD, SUB, AND, OR, XOR"""
        # MAR ← address
        self.registers.set_MAR(Bus(16, address))
        
        # Leer operando de memoria
        if self.memory:
            data_bus = self.memory.read_direct(address)
            self.registers.set_MDR(data_bus)
        
        # Configurar ALU
        self.alu.set_input_a(self.registers.get_AC().get_Value())
        self.alu.set_input_b(self.registers.get_MDR().get_Value())
        
        aluop_bus = Bus(2)
        aluop_bus.set_Binary_value(aluop)
        
        mode_bus = Bus(3)
        mode_bus.set_Binary_value(mode)
        
        self.alu.set_aluop(aluop_bus)
        self.alu.set_modo_funcion(mode_bus)
        
        # Ejecutar ALU
        result = self.alu.execute()
        self.registers.set_AC(result)
        
        # Actualizar flags
        try:
            self.registers.set_FLAG_Z(self.alu.get_zero_flag())
            self.registers.set_FLAG_C(self.alu.get_carry_out())
            self.registers.set_FLAG_N(self.alu.get_negative_flag())
        except:
            pass
        
        mnemonic = self._get_alu_mnemonic(aluop, mode)
        print(f"CPU: {mnemonic} [0x{address:03X}]={self.registers.get_MDR().get_Hex_Value()}, AC={self.registers.get_AC().get_Hex_Value()}")
    
    def _execute_shift(self, shift_amount, aluop, mode):
        """Operaciones de desplazamiento: SHL, SHR"""
        # Solo usar los 4 bits bajos para desplazamiento
        shift = shift_amount & 0xF
        
        # Configurar ALU
        self.alu.set_input_a(self.registers.get_AC().get_Value())
        
        # Para desplazamientos, usar shift amount como segundo operando
        shift_bus = Bus(16, shift)
        self.alu.set_input_b(shift_bus)
        
        aluop_bus = Bus(2)
        aluop_bus.set_Binary_value(aluop)
        
        mode_bus = Bus(3)
        mode_bus.set_Binary_value(mode)
        
        self.alu.set_aluop(aluop_bus)
        self.alu.set_modo_funcion(mode_bus)
        
        # Ejecutar ALU
        result = self.alu.execute()
        self.registers.set_AC(result)
        
        # Actualizar flags
        try:
            self.registers.set_FLAG_Z(self.alu.get_zero_flag())
            self.registers.set_FLAG_C(self.alu.get_carry_out())
            self.registers.set_FLAG_N(self.alu.get_negative_flag())
        except:
            pass
        
        mnemonic = "SHL" if mode == 0b000 else "SHR"
        print(f"CPU: {mnemonic} AC por {shift} bits = {self.registers.get_AC().get_Hex_Value()}")
    
    def _execute_multiplication(self, address):
        """MULT: HI:LO ← AC × Memoria[address]"""
        multiplicand = self.registers.get_AC().get_Dec_Value()
        
        # Obtener multiplicador de memoria
        if self.memory:
            bus = self.memory.read_direct(address)
            multiplier = bus.get_Decimal_value()
        else:
            multiplier = address  # Fallback
        
        result = multiplicand * multiplier
        hi = (result >> 16) & 0xFFFF
        lo = result & 0xFFFF
        
        # Guardar en HI/LO
        self.registers.set_HI(Bus(16, hi))
        self.registers.set_LO(Bus(16, lo))
        
        # Actualizar flags
        self.registers.set_FLAG_Z(Bit(1 if result == 0 else 0))
        self.registers.set_FLAG_N(Bit(1 if (lo & 0x8000) else 0))
        self.registers.set_FLAG_C(Bit(1 if hi != 0 else 0))
        
        print(f"CPU: MULT {multiplicand} × {multiplier} = {result} (HI=0x{hi:04X}, LO=0x{lo:04X})")
    
    def _execute_division(self, address):
        """DIV: LO ← AC ÷ Memoria[address], HI ← resto"""
        dividendo = self.registers.get_AC().get_Dec_Value()
        
        # Obtener divisor de memoria
        if self.memory:
            bus = self.memory.read_direct(address)
            divisor = bus.get_Decimal_value()
        else:
            divisor = address
        
        if divisor == 0:
            # Error: división por cero
            self.registers.set_STATUS(Bus(8, 0x01))
            self.registers.set_FLAG_C(Bit(1))
            print("CPU: ERROR - División por cero")
            return
        
        cociente = dividendo // divisor
        resto = dividendo % divisor
        
        self.registers.set_HI(Bus(16, resto))
        self.registers.set_LO(Bus(16, cociente))
        
        # Actualizar flags
        self.registers.set_FLAG_Z(Bit(1 if cociente == 0 else 0))
        self.registers.set_FLAG_N(Bit(1 if (cociente & 0x8000) else 0))
        
        print(f"CPU: DIV {dividendo} ÷ {divisor} = {cociente} (resto {resto})")
    
    # ===== MÉTODOS AUXILIARES =====
    
    def _get_mnemonic(self, opcode):
        """Devuelve el mnemónico para un opcode"""
        mnemonics = {
            0x0: "NOP", 0x1: "LOAD", 0x2: "STORE", 0x3: "ADD",
            0x4: "SUB", 0x5: "MULT", 0x6: "DIV", 0x7: "JUMP",
            0x8: "JZ", 0x9: "LOADI", 0xA: "AND", 0xB: "OR",
            0xC: "XOR", 0xD: "SHL", 0xE: "SHR", 0xF: "HALT"
        }
        return mnemonics.get(opcode, f"UNKNOWN(0x{opcode:X})")
    
    def _get_alu_mnemonic(self, aluop, mode):
        """Devuelve el mnemónico para operación ALU"""
        if aluop == 0b00:  # Aritmética
            return ["ADD", "SUB", "MULT", "DIV", "???", "???", "???", "???"][mode]
        elif aluop == 0b01:  # Lógica
            return ["AND", "OR", "XOR", "NOT", "???", "???", "???", "???"][mode]
        elif aluop == 0b10:  # Desplazamiento
            return ["SHL", "SHR", "ROL", "ROR", "ASR", "???", "???", "???"][mode]
        return "UNKNOWN"
    
    def run_cycle(self):
        """Ejecuta un ciclo completo de la CPU"""
        if not self.running.get_value():
            return
            
        self.clock_cycle += 1
        
        # Fetch y Execute
        if self.fetch():
            self.execute()
        
        print(f"CPU: Ciclo {self.clock_cycle} completado. PC={self.registers.get_PC().get_Hex_Value()}")
    
    def run_program(self, start_address: int = 0, max_cycles: int = 100):
        """Ejecuta un programa desde una dirección de memoria"""
        print("=== INICIANDO EJECUCIÓN ===")
        print(f"PC inicial: 0x{start_address:04X}")
        
        # Resetear
        self.reset()
        self.registers.get_PC().set_Value_int(start_address)
        self.running.set_value(1)
        
        # Ciclo principal
        while self.running.get_value() and self.clock_cycle < max_cycles:
            self.run_cycle()
        
        if self.clock_cycle >= max_cycles:
            print(f"CPU: Advertencia - Límite de {max_cycles} ciclos alcanzado")
        
        print("=== EJECUCIÓN FINALIZADA ===")
        print(f"Ciclos: {self.clock_cycle}, Instrucciones: {self.instructions_executed}")
        
    def get_status(self):
        """Retorna el estado actual de la CPU con TODOS los registros"""
        return {
            'running': self.running.get_value(),
            'clock_cycle': self.clock_cycle,
            'instructions': self.instructions_executed,
            
            # Registros principales
            'pc': self.registers.get_PC().get_Hex_Value(),
            'ir': self.registers.get_IR().get_Hex_Value(),
            'ac': self.registers.get_AC().get_Hex_Value(),
            'mar': self.registers.get_MAR().get_Hex_Value(),
            'mdr': self.registers.get_MDR().get_Hex_Value(),
            'temp': self.registers.get_TEMP().get_Hex_Value(),
            
            # Registros secuenciales
            'hi': self.registers.get_HI().get_Hex_Value(),
            'lo': self.registers.get_LO().get_Hex_Value(),
            'md_cnt': self.registers.get_MD_CNT().get_Hex_Value(),
            'md_state': self.registers.get_MD_STATE().get_Hex_Value(),
            
            # Registros de control
            'step_cnt': self.registers.get_STEP_CNT().get_Hex_Value(),
            'op_type': self.registers.get_OP_TYPE().get_Hex_Value(),
            'status': self.registers.get_STATUS().get_Hex_Value(),
            
            # Banderas
            'flags': {
                'Z': self.registers.get_FLAG_Z().get_value(),
                'C': self.registers.get_FLAG_C().get_value(),
                'N': self.registers.get_FLAG_N().get_value()
            }
        }
    
    def load_program(self, program: list, start_address: int = 0):
        """Carga un programa en memoria"""
        if not self.memory:
            print("CPU: Error - Memoria no conectada")
            return False
        
        for i, instruction in enumerate(program):
            self.memory.write_direct(start_address + i, instruction)
        
        print(f"CPU: Programa cargado en memoria [0x{start_address:04X}-0x{start_address + len(program) - 1:04X}]")
        return True