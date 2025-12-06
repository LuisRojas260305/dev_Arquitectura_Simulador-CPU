import json
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class RAM:
    """
    Memoria RAM con carga desde JSON
    Implementa 4K palabras de 16 bits (4096 direcciones)
    """
    
    def __init__(self, size_kb: int = 4):
        self.size = size_kb * 1024  # 4096 palabras
        self.memory = [Bus(16, 0) for _ in range(self.size)]
        
        # Control
        self.read_enable = Bit(0)
        self.write_enable = Bit(0)
        
        # Estadísticas
        self.read_count = 0
        self.write_count = 0
    
    def load_from_json(self, json_file: str):
        """Carga programa desde archivo JSON usando la plantilla"""
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
            
            print(f"Cargando programa desde {json_file}...")
            
            # Cargar programa (sección 'program')
            if 'program' in data:
                program_loaded = 0
                for instruction in data['program']:
                    addr = instruction['address']
                    
                    # Convertir instrucción a valor
                    if isinstance(instruction['instruction'], str):
                        # Formato "0xXXXX"
                        value = int(instruction['instruction'], 16)
                    else:
                        value = instruction['instruction']
                    
                    if 0 <= addr < self.size:
                        self.memory[addr] = Bus(16, value)
                        program_loaded += 1
                        
                        # Mostrar información de la instrucción
                        mnemonic = instruction.get('mnemonic', 'UNKNOWN')
                        comment = instruction.get('comment', '')
                        print(f"  [{addr:04X}] {value:04X}  ; {mnemonic} - {comment}")
            
            # Cargar datos (sección 'data_section')
            data_loaded = 0
            if 'data_section' in data:
                # Variables
                if 'variables' in data['data_section']:
                    for var_name, var_data in data['data_section']['variables'].items():
                        addr = var_data['address']
                        value = var_data['value']
                        
                        if 0 <= addr < self.size:
                            self.memory[addr] = Bus(16, value)
                            data_loaded += 1
                            print(f"  [{addr:04X}] {value:04X}  ; Variable: {var_name}")
                
                # Strings
                if 'strings' in data['data_section']:
                    for str_name, str_data in data['data_section']['strings'].items():
                        addr = str_data['address']
                        string = str_data['value']
                        
                        for i, char in enumerate(string):
                            if addr + i < self.size:
                                self.memory[addr + i] = Bus(16, ord(char))
                                data_loaded += 1
            
            print(f"Programa cargado: {program_loaded} instrucciones, {data_loaded} datos")
            
            # Establecer punto de entrada si está especificado
            if 'execution_info' in data and 'entry_point' in data['execution_info']:
                entry = data['execution_info']['entry_point']
                print(f"Punto de entrada: 0x{entry:04X}")
            
        except FileNotFoundError:
            print(f"Error: Archivo {json_file} no encontrado")
        except json.JSONDecodeError:
            print(f"Error: {json_file} no es un JSON válido")
        except Exception as e:
            print(f"Error cargando programa: {e}")
    
    def read(self, address: int) -> Bus:
        """Lee una palabra de memoria"""
        if 0 <= address < self.size:
            self.read_count += 1
            return self.memory[address]
        return Bus(16, 0xFFFF)  # Error
    
    def write(self, address: int, data: Bus):
        """Escribe una palabra en memoria"""
        if 0 <= address < self.size:
            self.write_count += 1
            self.memory[address] = data
    
    def read_direct(self, address: int) -> int:
        """Lee directamente un valor entero"""
        if 0 <= address < self.size:
            return self.memory[address].get_Decimal_value()
        return 0
    
    def write_direct(self, address: int, value: int):
        """Escribe directamente un valor entero"""
        if 0 <= address < self.size:
            self.memory[address] = Bus(16, value)
    
    def dump(self, start_addr: int = 0, count: int = 32):
        """Muestra contenido de memoria"""
        print(f"\nDUMP MEMORIA (0x{start_addr:04X} - 0x{start_addr+count-1:04X})")
        print("=" * 50)
        print(f"{'Dirección':<10} {'Hex':<6} {'Decimal':<8} {'Binario':<20}")
        print("-" * 50)
        
        for i in range(count):
            addr = start_addr + i
            if addr < self.size:
                word = self.memory[addr]
                dec_val = word.get_Decimal_value()
                if dec_val != 0:  # Mostrar solo valores no cero
                    print(f"0x{addr:04X}      {word.get_Hexadecimal_value():<6} "
                          f"{dec_val:<8} {word.get_Binary_value():<20}")
    
    def get_stats(self):
        """Retorna estadísticas de uso"""
        return {
            'size': self.size,
            'reads': self.read_count,
            'writes': self.write_count
        }
    
    def __str__(self):
        stats = self.get_stats()
        return f"Memory({self.size} words, {stats['reads']} reads, {stats['writes']} writes)"