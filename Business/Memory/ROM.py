# Business/Memory/ROM.py
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, TYPE_CHECKING

# Importación condicional para evitar ciclos
if TYPE_CHECKING:
    from Business.Computer_System import System

class ROM:
    """
    Memoria de Solo Lectura - Sistema de Configuración y Programas
    Maneja la carga de programas y configuración del sistema
    """
    
    def __init__(self, base_path: str = None):
        # Configuración del sistema
        self.config = {
            'programs_dir': 'Data/Programs',
            'configs_dir': 'Data/Configs',
            'logs_dir': 'logs',
            'max_test_history': 50,
            'default_config': 'default.json'
        }
        
        # Establecer rutas base
        if base_path:
            self.base_path = Path(base_path)
        else:
            self.base_path = Path(__file__).parent.parent.parent
        
        # Ensamblador del sistema - inicialmente None
        self.assembler = None
        
        # Historial de pruebas
        self.test_history: List[Dict] = []
        self.loaded_configs: List[Dict] = []
        
        # Crear directorios necesarios
        self._create_directories()
    
    def _create_directories(self):
        """Crea los directorios necesarios para el sistema"""
        dirs = [
            self.base_path / self.config['programs_dir'],
            self.base_path / self.config['configs_dir'],
            self.base_path / self.config['logs_dir']
        ]
        
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def _get_system_class(self):
        """Importa y retorna la clase System para evitar ciclos"""
        from Business.Computer_System import System
        return System
    
    def create_system_assembler(self, system_config: Dict = None):
        """
        Crea un nuevo ensamblador del sistema
        
        Args:
            system_config: Configuración específica del sistema
            
        Returns:
            Instancia de System
        """
        SystemClass = self._get_system_class()
        self.assembler = SystemClass(system_config)
        return self.assembler
    
    def get_system_assembler(self):
        """
        Obtiene el ensamblador actual del sistema
        
        Returns:
            Instancia de System actual
        """
        if not self.assembler:
            SystemClass = self._get_system_class()
            self.assembler = SystemClass()
        return self.assembler
    
    def list_programs(self) -> List[Dict[str, Any]]:
        """
        Lista todos los programas disponibles
        
        Returns:
            Lista de diccionarios con información de programas
        """
        programs_dir = self.base_path / self.config['programs_dir']
        programs = []
        
        for json_file in programs_dir.glob("*.json"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                program_info = {
                    'filename': json_file.name,
                    'path': str(json_file),
                    'name': data.get('metadata', {}).get('name', json_file.stem),
                    'author': data.get('metadata', {}).get('author', 'Desconocido'),
                    'description': data.get('metadata', {}).get('description', ''),
                    'created': data.get('metadata', {}).get('created', ''),
                    'format_version': data.get('metadata', {}).get('format_version', '1.0'),
                    'instructions_count': len(data.get('program', [])),
                    'entry_point': data.get('execution_info', {}).get('entry_point', 0)
                }
                programs.append(program_info)
                
            except Exception as e:
                programs.append({
                    'filename': json_file.name,
                    'path': str(json_file),
                    'name': json_file.stem,
                    'error': str(e)
                })
        
        return programs
    
    def load_program(self, program_filename: str, verbose: bool = True) -> bool:
        """
        Carga un programa usando el ensamblador
        
        Args:
            program_filename: Nombre del archivo del programa
            verbose: Mostrar información detallada
            
        Returns:
            True si la carga fue exitosa, False en caso contrario
        """
        if not self.assembler:
            if verbose:
                print("✗ Ensamblador no creado. Use create_system_assembler() primero.")
            return False
        
        program_path = self.base_path / self.config['programs_dir'] / program_filename
        
        if not program_path.exists():
            if verbose:
                print(f"✗ Archivo no encontrado: {program_path}")
            return False
        
        # Usamos la interfaz pública del ensamblador
        try:
            success = self.assembler.load_program_from_json(str(program_path), verbose)
            return success
        except AttributeError:
            if verbose:
                print("✗ El ensamblador no tiene el método load_program_from_json")
            return False
    
    def run_system_test(self) -> Dict[str, Any]:
        """
        Ejecuta una prueba completa del sistema
        
        Returns:
            Resultados de la prueba
        """
        if not self.assembler:
            print("✗ Ensamblador no creado. Use create_system_assembler() primero.")
            return {'error': 'Ensamblador no creado'}
        
        # Usamos la interfaz pública del ensamblador
        try:
            results = self.assembler.quick_test()
            
            # Guardar en historial
            self.test_history.append(results)
            
            # Mantener solo el historial más reciente
            if len(self.test_history) > self.config['max_test_history']:
                self.test_history = self.test_history[-self.config['max_test_history']:]
            
            # Guardar log
            self._save_test_log(results)
            
            return results
        except AttributeError:
            print("✗ El ensamblador no tiene el método quick_test")
            return {'error': 'Método quick_test no disponible'}
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Obtiene el estado del sistema
        
        Returns:
            Estado del sistema
        """
        if not self.assembler:
            return {'status': 'assembler_not_created'}
        
        # Usamos la interfaz pública del ensamblador
        try:
            return self.assembler.get_system_status()
        except AttributeError:
            return {'status': 'error', 'message': 'Método get_system_status no disponible'}
    
    def print_system_status(self):
        """Muestra el estado del sistema"""
        if not self.assembler:
            print("Ensamblador no creado")
            return
        
        # Usamos la interfaz pública del ensamblador
        try:
            self.assembler.print_system_status()
        except AttributeError:
            print("✗ No se puede mostrar el estado del sistema")
    
    def load_configuration(self, config_filename: str = None) -> Dict:
        """
        Carga una configuración del sistema
        
        Args:
            config_filename: Nombre del archivo de configuración (opcional)
            
        Returns:
            Configuración cargada
        """
        if not config_filename:
            config_filename = self.config['default_config']
        
        config_path = self.base_path / self.config['configs_dir'] / config_filename
        
        if not config_path.exists():
            # Crear configuración por defecto
            default_config = {
                'system': {
                    'data_width': 16,
                    'address_width': 12,
                    'ram_size_kb': 4,
                    'cpu_frequency': 1000000,
                    'enable_debug': True
                },
                'bus': {
                    'arbitration': True,
                    'priority': ['CPU', 'DMA', 'IO']
                },
                'cpu': {
                    'registers': {
                        'pc': 0,
                        'ac': 0,
                        'ir': 0
                    },
                    'flags': {
                        'zero': 0,
                        'carry': 0,
                        'negative': 0
                    }
                }
            }
            
            # Guardar configuración por defecto
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=2)
            
            config = default_config
        else:
            # Cargar configuración existente
            with open(config_path, 'r') as f:
                config = json.load(f)
        
        # Guardar en historial de configuraciones cargadas
        self.loaded_configs.append({
            'filename': config_filename,
            'path': str(config_path),
            'loaded_at': datetime.now().isoformat(),
            'config': config
        })
        
        return config
    
    def save_configuration(self, config: Dict, config_filename: str):
        """
        Guarda una configuración del sistema
        
        Args:
            config: Configuración a guardar
            config_filename: Nombre del archivo
        """
        config_path = self.base_path / self.config['configs_dir'] / config_filename
        
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_test_history(self, limit: int = 10) -> List[Dict]:
        """
        Obtiene el historial de pruebas
        
        Args:
            limit: Número máximo de pruebas a retornar
            
        Returns:
            Historial de pruebas
        """
        return self.test_history[-limit:] if self.test_history else []
    
    def _save_test_log(self, test_result: Dict):
        """Guarda los resultados de una prueba en un archivo de log"""
        log_dir = self.base_path / self.config['logs_dir']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"test_{timestamp}.json"
        
        try:
            with open(log_file, 'w') as f:
                json.dump(test_result, f, indent=2, default=str)
        except Exception as e:
            print(f"✗ Error guardando log: {e}")
    
    def run_program(self, mode: str = 'full', steps: int = 10, max_cycles: int = 1000) -> bool:
        """
        Ejecuta el programa cargado
        
        Args:
            mode: 'full' (completo) o 'step' (paso a paso)
            steps: Número de pasos (solo para modo 'step')
            max_cycles: Ciclos máximos (solo para modo 'full')
            
        Returns:
            True si la ejecución fue exitosa, False en caso contrario
        """
        if not self.assembler:
            print("✗ Ensamblador no creado")
            return False
        
        # Usamos la interfaz pública del ensamblador
        try:
            return self.assembler.run_program(mode, steps, max_cycles)
        except AttributeError:
            print("✗ El ensamblador no tiene el método run_program")
            return False
    
    def assemble_system(self, config: Dict = None, verbose: bool = True) -> bool:
        """
        Ensambla el sistema usando el ensamblador
        
        Args:
            config: Configuración del sistema
            verbose: Mostrar información detallada
            
        Returns:
            True si el ensamblaje fue exitoso, False en caso contrario
        """
        if not self.assembler:
            SystemClass = self._get_system_class()
            self.assembler = SystemClass(config)
        
        # Usamos la interfaz pública del ensamblador
        try:
            return self.assembler.assemble(verbose)
        except AttributeError:
            print("✗ El ensamblador no tiene el método assemble")
            return False