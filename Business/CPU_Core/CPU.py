# Business/CPU_Core/CPU.py - VERSIÓN OPTIMIZADA
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from Business.CPU_Core.Control_Unit.Record_Bank import Record_Bank
from Business.CPU_Core.Control_Unit.Control_Unit import Control_Unit
from Business.CPU_Core.Arithmetic_Logical_Unit.ALU import ALU
from Business.Memory.SystemBus import SystemBus
from Business.Memory.RAM import RAM

class CPU:
    """Unidad Central de Procesamiento optimizada"""
    
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
        
        print(f"CPU: Fetch en PC={pc_value:04X}, Instrucción={self.registers.get_IR().get_Hex_Value()}")
        return True
    
    def execute(self):
        """Ejecuta la instrucción actual"""
        if not self.running.get_value():
            return False
        
        # Obtener información de la instrucción
        ir_value = self.registers.get_IR().get_Dec_Value()
        opcode = (ir_value >> 12) & 0xF
        operand = ir_value & 0xFFF
        
        print(f"CPU: Ejecutando {opcode:01X} con operando {operand:03X}")
        
        # Configurar OP_TYPE
        self.registers.set_OP_TYPE(Bus(4, opcode))
        
        # Ejecutar según opcode (versión simplificada)
        if opcode == 0x0:  # NOP
            print("CPU: NOP")
            
        elif opcode == 0x1:  # LOAD
            self._load_instruction(operand)
            
        elif opcode == 0x2:  # STORE
            self._store_instruction(operand)
            
        elif opcode == 0x3:  # ADD
            self._add_instruction(operand)
            
        elif opcode == 0x9:  # LOADI
            # Cargar inmediato en AC
            self.registers.set_AC(Bus(16, operand))
            print(f"CPU: LOADI {operand:03X} -> AC={operand:04X}")
            
        elif opcode == 0xB:  # MULT
            self._execute_multiplication(operand)
            
        elif opcode == 0xC:  # DIV
            self._execute_division(operand)
            
        elif opcode == 0xF:  # HALT
            print("CPU: HALT")
            self.running.set_value(0)
            
        else:
            print(f"CPU: Instrucción {opcode:01X} no implementada")
        
        self.instructions_executed += 1
        return True
    
    def _load_instruction(self, address):
        """Ejecuta instrucción LOAD"""
        # MAR <- address
        self.registers.set_MAR(Bus(16, address))
        
        # Leer memoria
        if self.memory:
            data_bus = self.memory.read_direct(address)
            self.registers.set_MDR(data_bus)
        
        # AC <- MDR
        self.registers.set_AC(self.registers.get_MDR().get_Value())
        
        print(f"CPU: LOAD [{address:04X}]={self.registers.get_AC().get_Hex_Value()}")
    
    def _store_instruction(self, address):
        """Ejecuta instrucción STORE"""
        # MAR <- address
        self.registers.set_MAR(Bus(16, address))
        
        # MDR <- AC
        self.registers.set_MDR(self.registers.get_AC().get_Value())
        
        # Escribir memoria
        if self.memory:
            mdr_value = self.registers.get_MDR().get_Dec_Value()
            self.memory.write_direct(address, mdr_value)
        
        print(f"CPU: STORE AC={self.registers.get_AC().get_Hex_Value()} -> [{address:04X}]")
    
    def _add_instruction(self, address):
        """Ejecuta instrucción ADD"""
        # MAR <- address
        self.registers.set_MAR(Bus(16, address))
        
        # Leer memoria
        if self.memory:
            data_bus = self.memory.read_direct(address)
            self.registers.set_MDR(data_bus)
        
        # Configurar ALU
        self.alu.set_input_a(self.registers.get_AC().get_Value())
        self.alu.set_input_b(self.registers.get_MDR().get_Value())
        
        aluop = Bus(2)
        aluop.set_Binary_value(0b00)  # Aritmética
        modo = Bus(3)
        modo.set_Binary_value(0b000)  # ADD
        
        self.alu.set_aluop(aluop)
        self.alu.set_modo_funcion(modo)
        
        # Ejecutar ALU
        result = self.alu.execute()
        self.registers.set_AC(result)
        
        # Actualizar flags
        self.registers.set_FLAG_Z(self.alu.get_zero_flag())
        self.registers.set_FLAG_C(self.alu.get_carry_out())
        self.registers.set_FLAG_N(self.alu.get_negative_flag())
        
        print(f"CPU: ADD [{address:04X}]={self.registers.get_MDR().get_Hex_Value()}, AC={self.registers.get_AC().get_Hex_Value()}")
    
    def _execute_multiplication(self, operand):
        """Ejecuta multiplicación simplificada"""
        multiplicand = self.registers.get_AC().get_Dec_Value()
        multiplier = operand
        
        result = multiplicand * multiplier
        hi = (result >> 16) & 0xFFFF
        lo = result & 0xFFFF
        
        self.registers.set_HI(Bus(16, hi))
        self.registers.set_LO(Bus(16, lo))
        
        # Actualizar flags
        self.registers.set_FLAG_Z(Bit(1 if result == 0 else 0))
        self.registers.set_FLAG_N(Bit(1 if result & 0x80000000 else 0))
        
        print(f"CPU: MULT {multiplicand} * {multiplier} = {result} (HI={hi:04X}, LO={lo:04X})")
    
    def _execute_division(self, divisor):
        """Ejecuta división simplificada"""
        dividendo = self.registers.get_AC().get_Dec_Value()
        
        if divisor == 0:
            # Error: división por cero
            self.registers.set_STATUS(Bus(8, 0x01))
            self.registers.set_MD_STATE(Bus(3, 5))
            print("CPU: Error - División por cero")
            return
        
        cociente = dividendo // divisor
        residuo = dividendo % divisor
        
        self.registers.set_HI(Bus(16, residuo))
        self.registers.set_LO(Bus(16, cociente))
        
        # Actualizar flags
        self.registers.set_FLAG_Z(Bit(1 if cociente == 0 else 0))
        self.registers.set_FLAG_N(Bit(1 if cociente & 0x8000 else 0))
        
        print(f"CPU: DIV {dividendo} / {divisor} = {cociente} (residuo {residuo})")
    
    def run_cycle(self):
        """Ejecuta un ciclo completo de la CPU"""
        if not self.running.get_value():
            return
            
        # Incrementar contador de ciclos
        self.clock_cycle += 1
        
        # Fetch
        if not self.fetch():
            return
        
        # Execute
        self.execute()
        
        print(f"CPU: Ciclo {self.clock_cycle} completado. PC={self.registers.get_PC().get_Hex_Value()}")
    
    def run_program(self, start_address: int = 0, max_cycles: int = 100):
        """Ejecuta un programa desde una dirección de memoria"""
        print("=== INICIANDO EJECUCIÓN ===")
        print(f"PC inicial: {start_address:04X}")
        
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
        """Retorna el estado actual de la CPU"""
        return {
            'running': self.running.get_value(),
            'clock_cycle': self.clock_cycle,
            'instructions': self.instructions_executed,
            'pc': self.registers.get_PC().get_Hex_Value(),
            'ir': self.registers.get_IR().get_Hex_Value(),
            'ac': self.registers.get_AC().get_Hex_Value(),
            'mar': self.registers.get_MAR().get_Hex_Value(),
            'mdr': self.registers.get_MDR().get_Hex_Value(),
            'hi': self.registers.get_HI().get_Hex_Value(),
            'lo': self.registers.get_LO().get_Hex_Value(),
            'flags': {
                'Z': self.registers.get_FLAG_Z().get_value(),
                'C': self.registers.get_FLAG_C().get_value(),
                'N': self.registers.get_FLAG_N().get_value()
            },
            'sequential_regs': {  # AÑADIDO: Registros secuenciales
                'md_cnt': self.registers.get_MD_CNT().get_Hex_Value(),
                'md_state': self.registers.get_MD_STATE().get_Hex_Value(),
                'step_cnt': self.registers.get_STEP_CNT().get_Hex_Value(),
                'op_type': self.registers.get_OP_TYPE().get_Hex_Value(),
                'status': self.registers.get_STATUS().get_Hex_Value()
            }
        }
    
    def load_program(self, program: list, start_address: int = 0):
        """Carga un programa en memoria"""
        if not self.memory:
            print("CPU: Error - Memoria no conectada")
            return False
        
        for i, instruction in enumerate(program):
            self.memory.write_direct(start_address + i, instruction)
        
        print(f"CPU: Programa cargado en memoria [{start_address:04X}-{start_address + len(program) - 1:04X}]")
        return True