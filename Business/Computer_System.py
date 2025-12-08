# Business/SystemAssembler.py
from Business.Memory.RAM import RAM
from Business.Memory.SystemBus import SystemBus
from Business.CPU_Core.CPU import CPU
from Business.CPU_Core.Control_Unit.Control_Unit import Control_Unit
from typing import Dict, Any, Optional, Tuple
import json
from pathlib import Path
from datetime import datetime

class System:
    """
    Ensamblador del sistema completo - Orquesta la creación y conexión
    de todos los componentes (CPU, RAM, Bus, etc.)
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa el ensamblador con configuración
        
        Args:
            config: Configuración del sistema (opcional)
        """
        # Configuración por defecto
        self.default_config = {
            'data_width': 16,
            'address_width': 12,
            'ram_size_kb': 4,
            'cpu_frequency': 1_000_000,
            'enable_debug': True,
            'bus_arbitration': True
        }
        
        # Combinar configuración
        self.config = {**self.default_config, **(config or {})}
        
        # Componentes del sistema (se inicializan en assemble())
        self.system_bus: Optional[SystemBus] = None
        self.ram: Optional[RAM] = None
        self.cpu: Optional[CPU] = None
        self.control_unit: Optional[Control_Unit] = None
        
        # Estado del ensamblaje
        self.assembled = False
        self.assembly_time: Optional[datetime] = None
        self.assembly_log: list = []
        
        # Programa actual
        self.current_program: Optional[Dict] = None
        self.program_loaded = False
    
    def assemble(self, verbose: bool = True) -> bool:
        """
        Ensambla todos los componentes del sistema
        
        Args:
            verbose: Mostrar información detallada del ensamblaje
            
        Returns:
            True si el ensamblaje fue exitoso, False en caso contrario
        """
        try:
            if verbose:
                print("\n" + "="*60)
                print("ENSAMBLANDO SISTEMA...")
                print("="*60)
            
            self.assembly_time = datetime.now()
            self.assembly_log = []
            
            # 1. Crear SystemBus
            if verbose:
                print("1. Creando SystemBus...")
            
            self.system_bus = SystemBus(
                data_width=self.config['data_width'],
                addr_width=self.config['address_width']
            )
            
            self._log_step("SystemBus creado", True)
            if verbose:
                print(f"   ✓ SystemBus: {self.config['data_width']} bits datos, "
                      f"{self.config['address_width']} bits dirección")
            
            # 2. Crear RAM
            if verbose:
                print("2. Creando RAM...")
            
            self.ram = RAM(self.config['ram_size_kb'])
            
            self._log_step("RAM creada", True)
            if verbose:
                print(f"   ✓ RAM: {self.ram.size} palabras "
                      f"(0x0000 - 0x{self.ram.size-1:04X})")
            
            # 3. Crear CPU
            if verbose:
                print("3. Creando CPU...")
            
            self.cpu = CPU(self.system_bus)
            
            self._log_step("CPU creada", True)
            if verbose:
                print(f"   ✓ CPU: Procesador de {self.config['data_width']} bits")
            
            # 4. Crear Unidad de Control
            if verbose:
                print("4. Creando Unidad de Control...")
            
            self.control_unit = Control_Unit()
            
            self._log_step("Control Unit creada", True)
            if verbose:
                print("   ✓ Control Unit: Lista para decodificar instrucciones")
            
            # 5. Conectar componentes
            if verbose:
                print("5. Conectando componentes...")
            
            # Conectar RAM al SystemBus
            self.system_bus.connect_device(
                self.ram,
                "RAM",
                (0, self.ram.size - 1),
                "slave"
            )
            
            # Conectar memoria a la CPU
            self.cpu.connect_memory(self.ram)
            
            self._log_step("Componentes conectados", True)
            
            # 6. Resetear todo el sistema
            if verbose:
                print("6. Resetendo sistema...")
            
            self.reset_all_components()
            
            self._log_step("Sistema reseteado", True)
            
            # Marcar como ensamblado
            self.assembled = True
            self.program_loaded = False
            self.current_program = None
            
            if verbose:
                duration = (datetime.now() - self.assembly_time).total_seconds()
                print("\n" + "="*60)
                print(f"✓ SISTEMA ENSAMBLADO CORRECTAMENTE")
                print(f"  Tiempo de ensamblaje: {duration:.3f} segundos")
                print(f"  Componentes: {len(self.assembly_log)}")
                print("="*60)
            
            return True
            
        except Exception as e:
            self._log_step(f"Error en ensamblaje: {str(e)}", False)
            
            if verbose:
                print(f"\n✗ ERROR EN ENSAMBLADO: {e}")
            
            # Limpiar componentes en caso de error
            self.system_bus = None
            self.ram = None
            self.cpu = None
            self.control_unit = None
            self.assembled = False
            
            return False
    
    def _log_step(self, message: str, success: bool):
        """Registra un paso del ensamblaje"""
        self.assembly_log.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'success': success
        })
    
    def reset_all_components(self):
        """Resetea todos los componentes del sistema"""
        if self.cpu:
            self.cpu.reset()
        
        if self.system_bus:
            self.system_bus.reset()
        
        if self.control_unit:
            self.control_unit.reset()
        
        if self.ram:
            self.ram.read_count = 0
            self.ram.write_count = 0
    
    def load_program_from_json(self, json_path: str, verbose: bool = True) -> bool:
        """
        Carga un programa desde un archivo JSON
        
        Args:
            json_path: Ruta al archivo JSON
            verbose: Mostrar información detallada
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        if not self.assembled:
            if verbose:
                print("✗ Sistema no ensamblado. Ejecute assemble() primero.")
            return False
        
        try:
            path = Path(json_path)
            if not path.exists():
                if verbose:
                    print(f"✗ Archivo no encontrado: {json_path}")
                return False
            
            # Resetear sistema antes de cargar nuevo programa
            self.reset_all_components()
            
            # Cargar programa
            self.ram.load_from_json(str(path))
            
            # Leer metadatos del programa
            with open(path, 'r') as f:
                program_data = json.load(f)
                
                self.current_program = {
                    'filename': path.name,
                    'path': str(path),
                    'name': program_data.get('metadata', {}).get('name', path.stem),
                    'author': program_data.get('metadata', {}).get('author', 'Desconocido'),
                    'description': program_data.get('metadata', {}).get('description', ''),
                    'entry_point': program_data.get('execution_info', {}).get('entry_point', 0),
                    'loaded_at': datetime.now().isoformat(),
                    'instructions_count': len(program_data.get('program', [])),
                    'data_count': len(program_data.get('data_section', {}).get('variables', {}))
                }
            
            self.program_loaded = True
            
            if verbose:
                print(f"\n✓ PROGRAMA CARGADO: {self.current_program['name']}")
                print(f"  • Archivo: {self.current_program['filename']}")
                print(f"  • Instrucciones: {self.current_program['instructions_count']}")
                print(f"  • Variables de datos: {self.current_program['data_count']}")
                print(f"  • Punto de entrada: 0x{self.current_program['entry_point']:04X}")
                print(f"  • Autor: {self.current_program['author']}")
            
            return True
            
        except Exception as e:
            if verbose:
                print(f"✗ Error cargando programa: {e}")
            return False
    
    def run_program(self, mode: str = 'full', steps: int = 10, max_cycles: int = 1000) -> bool:
        """
        Ejecuta el programa cargado
        
        Args:
            mode: 'full' (completo) o 'step' (paso a paso)
            steps: Número de pasos (si mode='step')
            max_cycles: Ciclos máximos (si mode='full')
            
        Returns:
            True si la ejecución fue exitosa, False en caso contrario
        """
        if not self.assembled:
            print("✗ Sistema no ensamblado")
            return False
        
        if not self.program_loaded:
            print("✗ No hay programa cargado")
            return False
        
        try:
            entry_point = self.current_program['entry_point']
            self.cpu.registers.get_PC().set_Value_int(entry_point)
            self.cpu.running.set_value(1)
            
            if mode == 'full':
                print(f"\nEjecutando programa completo...")
                print(f"Punto de entrada: 0x{entry_point:04X}")
                print("="*60)
                
                self.cpu.run_program(start_address=entry_point, max_cycles=max_cycles)
                
                print("\n" + "="*60)
                print("EJECUCIÓN COMPLETADA")
                print("="*60)
                
            elif mode == 'step':
                print(f"\nEjecutando {steps} pasos...")
                print("="*60)
                
                for step in range(steps):
                    print(f"\n--- Paso {step + 1} ---")
                    
                    # Obtener estado antes
                    pc_before = self.cpu.registers.get_PC().get_Dec_Value()
                    
                    # Ejecutar ciclo
                    self.cpu.run_cycle()
                    
                    # Obtener estado después
                    pc_after = self.cpu.registers.get_PC().get_Dec_Value()
                    instruction = self.cpu.registers.get_IR().get_Hex_Value()
                    
                    print(f"PC: 0x{pc_before:04X} → 0x{pc_after:04X}")
                    print(f"Instrucción: {instruction}")
                    print(f"AC: {self.cpu.registers.get_AC().get_Hex_Value()}")
                    
                    # Verificar si se detuvo
                    if not self.cpu.running.get_value():
                        print("✓ Programa finalizado (HALT)")
                        break
                
                print("\n" + "="*60)
                print("EJECUCIÓN PASO A PASO COMPLETADA")
                print("="*60)
            
            return True
            
        except Exception as e:
            print(f"✗ Error ejecutando programa: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Obtiene el estado completo del sistema"""
        if not self.assembled:
            return {
                'status': 'not_assembled',
                'message': 'Sistema no ensamblado',
                'timestamp': datetime.now().isoformat()
            }
        
        status = {
            'status': 'assembled',
            'assembled': self.assembled,
            'program_loaded': self.program_loaded,
            'timestamp': datetime.now().isoformat(),
            'assembly_time': self.assembly_time.isoformat() if self.assembly_time else None,
            'components': {}
        }
        
        # Información de componentes
        if self.cpu:
            status['components']['cpu'] = self.cpu.get_status()
        
        if self.ram:
            status['components']['ram'] = self.ram.get_stats()
        
        if self.system_bus:
            status['components']['system_bus'] = self.system_bus.get_status()
        
        if self.control_unit:
            status['components']['control_unit'] = self.control_unit.get_current_status()
        
        # Información del programa
        if self.current_program:
            status['current_program'] = self.current_program
        
        return status
    
    def print_system_status(self):
        """Muestra el estado del sistema de forma legible"""
        status = self.get_system_status()
        
        print("\n" + "="*60)
        print("ESTADO DEL SISTEMA")
        print("="*60)
        
        if status['status'] == 'not_assembled':
            print("Sistema no ensamblado")
            return
        
        print(f"Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Ensamblado: {status['assembly_time']}")
        
        if status.get('current_program'):
            prog = status['current_program']
            print(f"\nPrograma: {prog.get('name', 'N/A')}")
            print(f"  • Archivo: {prog.get('filename', 'N/A')}")
            print(f"  • Instrucciones: {prog.get('instructions_count', 0)}")
            print(f"  • Punto de entrada: 0x{prog.get('entry_point', 0):04X}")
        
        # Estado de CPU
        cpu = status['components'].get('cpu')
        if cpu:
            print(f"\nCPU:")
            print(f"  • Estado: {'Ejecutando' if cpu.get('running') else 'Detenido'}")
            print(f"  • PC: {cpu.get('pc', 'N/A')}")
            print(f"  • AC: {cpu.get('ac', 'N/A')}")
            print(f"  • IR: {cpu.get('ir', 'N/A')}")
            print(f"  • Ciclos: {cpu.get('clock_cycle', 0)}")
            print(f"  • Instrucciones: {cpu.get('instructions', 0)}")
        
        # Estado de RAM
        ram = status['components'].get('ram')
        if ram:
            print(f"\nRAM:")
            print(f"  • Tamaño: {ram.get('size', 0)} palabras")
            print(f"  • Lecturas: {ram.get('reads', 0)}")
            print(f"  • Escrituras: {ram.get('writes', 0)}")
        
        print("="*60)
    
    def quick_test(self) -> Dict[str, Any]:
        """
        Ejecuta una prueba rápida del sistema
        
        Returns:
            Diccionario con resultados de la prueba
        """
        print("\n" + "="*60)
        print("PRUEBA RÁPIDA DEL SISTEMA")
        print("="*60)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'tests': {},
            'passed': 0,
            'failed': 0
        }
        
        # Test 1: Verificar ensamblaje
        print("\n1. Verificando ensamblaje del sistema...")
        if self.assembled:
            print("   ✓ Sistema ensamblado correctamente")
            results['tests']['assembly'] = {'passed': True, 'message': 'Sistema ensamblado'}
            results['passed'] += 1
        else:
            print("   ✗ Sistema no ensamblado")
            results['tests']['assembly'] = {'passed': False, 'message': 'Sistema no ensamblado'}
            results['failed'] += 1
            return results
        
        # Test 2: Verificar componentes
        print("\n2. Verificando componentes...")
        components = [
            ('CPU', self.cpu),
            ('RAM', self.ram),
            ('SystemBus', self.system_bus),
            ('Control Unit', self.control_unit)
        ]
        
        for name, component in components:
            if component is not None:
                print(f"   ✓ {name}: OK")
                results['tests'][f'component_{name.lower()}'] = {'passed': True, 'message': f'{name} presente'}
                results['passed'] += 1
            else:
                print(f"   ✗ {name}: Ausente")
                results['tests'][f'component_{name.lower()}'] = {'passed': False, 'message': f'{name} ausente'}
                results['failed'] += 1
        
        # Test 3: Prueba de memoria
        print("\n3. Probando RAM...")
        try:
            test_addr = 0x0100
            test_value = 0x1234
            self.ram.write_direct(test_addr, test_value)
            read_value = self.ram.read_direct(test_addr).get_Decimal_value()
            
            if read_value == test_value:
                print(f"   ✓ RAM: Lectura/escritura correcta")
                print(f"   ✓ Escrito: 0x{test_value:04X}, Leído: 0x{read_value:04X}")
                results['tests']['ram_rw'] = {'passed': True, 'message': 'Lectura/escritura correcta'}
                results['passed'] += 1
            else:
                print(f"   ✗ RAM: Datos no coinciden")
                results['tests']['ram_rw'] = {'passed': False, 'message': f'Datos no coinciden: 0x{read_value:04X}'}
                results['failed'] += 1
        except Exception as e:
            print(f"   ✗ RAM: Error - {e}")
            results['tests']['ram_rw'] = {'passed': False, 'message': str(e)}
            results['failed'] += 1
        
        # Resumen
        print("\n" + "="*60)
        print("RESUMEN DE PRUEBA")
        print("="*60)
        print(f"Pruebas pasadas: {results['passed']}")
        print(f"Pruebas falladas: {results['failed']}")
        
        if results['failed'] == 0:
            print("✓ TODAS LAS PRUEBAS PASARON")
            results['overall'] = 'PASS'
        else:
            print(f"✗ {results['failed']} prueba(s) fallaron")
            results['overall'] = 'FAIL'
        
        return results
    
    def get_assembly_log(self) -> list:
        """Obtiene el log completo del ensamblaje"""
        return self.assembly_log.copy()