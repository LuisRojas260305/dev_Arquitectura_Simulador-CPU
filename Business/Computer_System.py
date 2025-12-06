# Business/ComputerSystem.py
import json
from Business.Memory.RAM import RAM
from Business.CPU_Core.CPU import CPU
from Business.Memory.SystemBus import SystemBus

class ComputerSystem:
    """
    Sistema computador completo
    Integra CPU, memoria y bus
    """
    
    def __init__(self, memory_size_kb: int = 4):
        # Componentes
        self.system_bus = SystemBus()
        self.memory = RAM(memory_size_kb)
        self.cpu = CPU(self.system_bus)
        
        # Estado
        self.powered_on = False
        self.clock_speed = 1  # 1 Hz
        
        # Conectar componentes
        self._connect_components()
    
    def _connect_components(self):
        """Conecta todos los componentes al bus"""
        # Conectar memoria (0x0000 - 0x0FFF)
        self.system_bus.connect_device(
            device=self.memory,
            name="RAM",
            address_range=(0x0000, 0x0FFF),
            device_type="slave"
        )
        
        # Conectar CPU como maestro
        self.system_bus.connect_device(
            device=self.cpu,
            name="CPU",
            address_range=(0x0000, 0xFFFF),  # Acceso completo
            device_type="master"
        )
        
        print("Sistema conectado:")
        print(f"  - Memoria: 0x0000 - 0x{self.memory.size-1:04X}")
        print(f"  - CPU conectada como maestro del bus")
    
    def power_on(self):
        """Enciende el sistema computador"""
        self.powered_on = True
        self.cpu.reset()
        self.system_bus.reset()
        
        print(f"\n{'='*60}")
        print("SISTEMA COMPUTADOR ENCENDIDO")
        print(f"{'='*60}")
        print(f"Memoria: {self.memory.size} palabras (16 bits)")
        print(f"CPU: Arquitectura de 16 bits")
        print(f"Bus: 12 bits dirección, 16 bits datos")
        print(f"{'='*60}")
    
    def power_off(self):
        """Apaga el sistema"""
        self.powered_on = False
        print("Sistema apagado")
    
    def load_program(self, json_file: str):
        """Carga un programa desde archivo JSON"""
        if not self.powered_on:
            print("Error: Sistema apagado. Use power_on() primero.")
            return
        
        self.memory.load_from_json(json_file)
    
    def run(self, start_address: int = 0, max_cycles: int = 100):
        """Ejecuta el programa desde una dirección"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        # Establecer PC inicial
        self.cpu.registers.get_PC().set_Value_int(start_address)
        
        print(f"\nIniciando ejecución desde 0x{start_address:04X}")
        print(f"Máximo de ciclos: {max_cycles}")
        
        self.cpu.run(max_cycles)
        
        # Mostrar resumen
        self._show_summary()
    
    def single_step(self):
        """Ejecuta un solo ciclo de CPU"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        self.cpu.clock_cycle()
    
    def inspect_memory(self, start: int = 0, count: int = 16):
        """Inspecciona contenido de memoria"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        self.memory.dump(start, count)
    
    def inspect_registers(self):
        """Muestra estado de registros"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        print("\n=== REGISTROS DE CPU ===")
        print(f"PC (Program Counter):  {self.cpu.registers.get_PC_HEX()}")
        print(f"IR (Instruction Reg):  {self.cpu.registers.get_IR_HEX()}")
        print(f"AC (Accumulator):      {self.cpu.registers.get_AC_HEX()}")
        print(f"MAR (Mem Addr Reg):    {self.cpu.registers.get_MAR_HEX()}")
        print(f"MDR (Mem Data Reg):    {self.cpu.registers.get_MDR_HEX()}")
        print(f"TEMP (Temporal):       {self.cpu.registers.get_TEMP_HEX()}")
        
        flags = self.cpu.registers
        print(f"\nFlags:")
        print(f"  Z (Zero):     {flags.get_FLAG_Z().get_value()}")
        print(f"  C (Carry):    {flags.get_FLAG_C().get_value()}")
        print(f"  N (Negative): {flags.get_FLAG_N().get_value()}")
    
    def inspect_bus(self):
        """Muestra estado del bus"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        print("\n=== ESTADO DEL BUS ===")
        print(self.system_bus)
        
        stats = self.system_bus.get_status()
        print(f"Dirección: {stats['address']}")
        print(f"Datos:     {stats['data']}")
        print(f"Control:   {stats['control']}")
        print(f"Maestro:   {stats['current_master']}")
        print(f"Ciclos:    {stats['cycles']}")
    
    def _show_summary(self):
        """Muestra resumen de ejecución"""
        print(f"\n{'='*60}")
        print("RESUMEN DE EJECUCIÓN")
        print(f"{'='*60}")
        
        # Estado CPU
        cpu_status = self.cpu.get_status()
        print(f"CPU:")
        print(f"  Ciclos totales: {cpu_status['clock_cycle']}")
        print(f"  Instrucciones:  {cpu_status['instructions']}")
        print(f"  PC final:       {cpu_status['pc']}")
        print(f"  AC final:       {cpu_status['ac']}")
        
        # Estadísticas memoria
        mem_stats = self.memory.get_stats()
        print(f"\nMemoria:")
        print(f"  Lecturas: {mem_stats['reads']}")
        print(f"  Escrituras: {mem_stats['writes']}")
        
        # Estado bus
        bus_stats = self.system_bus.get_status()
        print(f"\nBus:")
        print(f"  Ciclos bus: {bus_stats['cycles']}")
        
        print(f"{'='*60}")
    
    def save_state(self, filename: str):
        """Guarda estado del sistema en archivo"""
        if not self.powered_on:
            print("Error: Sistema apagado.")
            return
        
        state = {
            'cpu': self.cpu.get_status(),
            'memory': {
                'non_zero': []
            },
            'bus': self.system_bus.get_status()
        }
        
        # Guardar memoria no cero
        for addr in range(self.memory.size):
            value = self.memory.read_direct(addr)
            if value != 0:
                state['memory']['non_zero'].append({
                    'address': addr,
                    'value': value
                })
        
        with open(filename, 'w') as f:
            json.dump(state, f, indent=2)
        
        print(f"Estado guardado en {filename}")
    
    def load_state(self, filename: str):
        """Carga estado del sistema desde archivo"""
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            # Cargar CPU
            cpu_state = state['cpu']
            self.cpu.clock_cycle = cpu_state['clock_cycle']
            self.cpu.instructions_executed = cpu_state['instructions']
            
            # Cargar memoria
            for item in state['memory']['non_zero']:
                self.memory.write_direct(item['address'], item['value'])
            
            print(f"Estado cargado desde {filename}")
            
        except Exception as e:
            print(f"Error cargando estado: {e}")
    
    def __str__(self):
        status = "ENCENDIDO" if self.powered_on else "APAGADO"
        return (f"ComputerSystem[{status}] - "
                f"CPU: {self.cpu.registers.get_PC_HEX()}, "
                f"Memoria: {self.memory.size} palabras")