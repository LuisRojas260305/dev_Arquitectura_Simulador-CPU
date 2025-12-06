# Business/CPU_Core/Control_Unit/ControlStore.py

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
import json

class ControlStore:
    """
    Memoria de Control (ROM) de 256 palabras × 32 bits.
    Dirección = (opcode << 4) | micro_counter (step)
    Implementa microcódigo para el conjunto de instrucciones.
    """
    
    # Definición de las señales de control (bit positions)
    SIGNAL_BITS = {
        # Bits 0-1: ALUop
        'ALUop0': 0,    # LSB
        'ALUop1': 1,    # MSB
        
        # Bits 2-4: ALU función (3 bits)
        'ALUfunc0': 2,
        'ALUfunc1': 3,
        'ALUfunc2': 4,
        
        # Bits 5-15: Control de registros
        'MAR_LOAD': 5,
        'MDR_LOAD': 6,
        'IR_LOAD': 7,
        'AC_LOAD': 8,
        'PC_LOAD': 9,
        'PC_INC': 10,
        'HI_LOAD': 11,
        'LO_LOAD': 12,
        'TEMP_LOAD': 13,
        'MD_CNT_LOAD': 14,
        'STEP_CNT_LOAD': 15,
        
        # Bits 16-19: Control memoria/E/S
        'MEM_READ': 16,
        'MEM_WRITE': 17,
        'IO_READ': 18,
        'IO_WRITE': 19,
        
        # Bits 20-23: Control MULT/DIV
        'MD_START': 20,
        'MD_SHIFT': 21,
        'MD_ADD': 22,
        'MD_SUB': 23,
        
        # Bits 24-27: Control Display
        'DISP_LOAD': 24,
        'DISP_SHIFT_L': 25,
        'DISP_SHIFT_R': 26,
        'DISP_CLEAR': 27,
        
        # Bits 28-31: Control sistema
        'HALT': 28,
        'RESET': 29,
        'WAIT': 30,
        'END_INSTR': 31
    }
    
    def __init__(self):
        # Inicializar memoria con ceros
        self.__memory = [Bus(32, 0) for _ in range(256)]
        self.__initialize_microcode()
    
    def __initialize_microcode(self):
        """Inicializa toda la memoria de control con microcódigo"""
        
        # Para cada opcode (0-15) y cada step (0-15)
        for opcode in range(16):
            for step in range(16):
                address = self._calculate_address(opcode, step)
                control_word = self._generate_microinstruction(opcode, step)
                self.__memory[address] = control_word
    
    def _calculate_address(self, opcode: int, step: int) -> int:
        """Calcula dirección: (opcode << 4) | step"""
        return (opcode << 4) | step
    
    def _generate_microinstruction(self, opcode: int, step: int) -> Bus:
        """Genera una microinstrucción para opcode y step dados"""
        control_word = Bus(32, 0)
        
        # Microcódigo común para FETCH (primeros 3 pasos)
        if step == 0:
            # Paso 0: MAR <- PC
            self._set_signal(control_word, 'MAR_LOAD', 1)
            self._set_signal(control_word, 'PC_TO_BUS', 1)  # Nota: necesitaríamos esta señal
            
        elif step == 1:
            # Paso 1: MDR <- Mem[MAR], PC <- PC + 1
            self._set_signal(control_word, 'MEM_READ', 1)
            self._set_signal(control_word, 'MDR_LOAD', 1)
            self._set_signal(control_word, 'PC_INC', 1)
            
        elif step == 2:
            # Paso 2: IR <- MDR
            self._set_signal(control_word, 'IR_LOAD', 1)
            
        else:
            # Pasos específicos de cada instrucción (3-15)
            self._generate_execution_microcode(control_word, opcode, step)
        
        return control_word
    
    def _generate_execution_microcode(self, control_word: Bus, opcode: int, step: int):
        """Genera microcódigo de ejecución para cada instrucción"""
        
        # INSTRUCCIÓN HALT (0xF)
        if opcode == 0xF:
            if step == 3:
                self._set_signal(control_word, 'HALT', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN ADD (0x3)
        elif opcode == 0x3:
            if step == 3:
                # MAR <- IR[11:0] (dirección del operando)
                self._set_signal(control_word, 'MAR_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
            elif step == 4:
                # MDR <- Mem[MAR]
                self._set_signal(control_word, 'MEM_READ', 1)
                self._set_signal(control_word, 'MDR_LOAD', 1)
            elif step == 5:
                # Configurar ALU para suma
                self._set_signal(control_word, 'ALUop0', 0)
                self._set_signal(control_word, 'ALUop1', 0)  # 00: Aritmética
                self._set_signal(control_word, 'ALUfunc0', 0)
                self._set_signal(control_word, 'ALUfunc1', 0)
                self._set_signal(control_word, 'ALUfunc2', 0)  # 000: Suma
            elif step == 6:
                # AC <- AC + MDR
                self._set_signal(control_word, 'AC_LOAD', 1)
                self._set_signal(control_word, 'UPDATE_FLAGS', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN SUB (0x4)
        elif opcode == 0x4:
            if step == 3:
                # MAR <- IR[11:0]
                self._set_signal(control_word, 'MAR_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
            elif step == 4:
                # MDR <- Mem[MAR]
                self._set_signal(control_word, 'MEM_READ', 1)
                self._set_signal(control_word, 'MDR_LOAD', 1)
            elif step == 5:
                # Configurar ALU para resta
                self._set_signal(control_word, 'ALUop0', 0)
                self._set_signal(control_word, 'ALUop1', 0)  # 00: Aritmética
                self._set_signal(control_word, 'ALUfunc0', 1)
                self._set_signal(control_word, 'ALUfunc1', 0)
                self._set_signal(control_word, 'ALUfunc2', 0)  # 001: Resta
            elif step == 6:
                # AC <- AC - MDR
                self._set_signal(control_word, 'AC_LOAD', 1)
                self._set_signal(control_word, 'UPDATE_FLAGS', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN LOAD (0x1)
        elif opcode == 0x1:
            if step == 3:
                # MAR <- IR[11:0]
                self._set_signal(control_word, 'MAR_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
            elif step == 4:
                # MDR <- Mem[MAR]
                self._set_signal(control_word, 'MEM_READ', 1)
                self._set_signal(control_word, 'MDR_LOAD', 1)
            elif step == 5:
                # AC <- MDR
                self._set_signal(control_word, 'AC_LOAD', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN STORE (0x2)
        elif opcode == 0x2:
            if step == 3:
                # MAR <- IR[11:0]
                self._set_signal(control_word, 'MAR_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
            elif step == 4:
                # MDR <- AC
                self._set_signal(control_word, 'MDR_LOAD', 1)
                self._set_signal(control_word, 'AC_TO_BUS', 1)
            elif step == 5:
                # Mem[MAR] <- MDR
                self._set_signal(control_word, 'MEM_WRITE', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN JUMP (0x5)
        elif opcode == 0x5:
            if step == 3:
                # PC <- IR[11:0]
                self._set_signal(control_word, 'PC_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN JZ (0x6) - Jump if Zero
        elif opcode == 0x6:
            if step == 3:
                # Si FLAG_Z = 1, PC <- IR[11:0]
                # Esto requiere lógica condicional en hardware
                self._set_signal(control_word, 'COND_JUMP', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN IN (0x7)
        elif opcode == 0x7:
            if step == 3:
                # AC <- Input Device
                self._set_signal(control_word, 'AC_LOAD', 1)
                self._set_signal(control_word, 'IO_READ', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN OUT (0x8)
        elif opcode == 0x8:
            if step == 3:
                # Output Device <- AC
                self._set_signal(control_word, 'IO_WRITE', 1)
                self._set_signal(control_word, 'AC_TO_BUS', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # INSTRUCCIÓN LOADI (0x9) - Load Immediate
        elif opcode == 0x9:
            if step == 3:
                # AC <- IR[11:0] (valor inmediato)
                self._set_signal(control_word, 'AC_LOAD', 1)
                self._set_signal(control_word, 'IR_OPERAND_TO_BUS', 1)
                self._set_signal(control_word, 'END_INSTR', 1)
        
        # Instrucciones AND, OR, XOR, etc. seguirían aquí...
    
    def _set_signal(self, control_word: Bus, signal_name: str, value: int):
        """Establece una señal en la palabra de control"""
        if signal_name in self.SIGNAL_BITS:
            bit_pos = self.SIGNAL_BITS[signal_name]
            control_word.set_Line_bit(bit_pos, Bit(value))
    
    def read(self, address: int) -> Bus:
        """Lee una palabra de control de la dirección especificada"""
        if 0 <= address < 256:
            return self.__memory[address]
        raise ValueError(f"Dirección {address} fuera de rango [0, 255]")
    
    def read_by_opcode_step(self, opcode: int, step: int) -> Bus:
        """Lee usando opcode y step directamente"""
        address = self._calculate_address(opcode, step)
        return self.read(address)
    
    def save_to_file(self, filename: str):
        """Guarda el microcódigo a un archivo JSON"""
        microcode_dict = {}
        for addr in range(256):
            value = self.__memory[addr].get_Decimal_value()
            microcode_dict[str(addr)] = {
                'hex': f"0x{value:08X}",
                'bin': bin(value)[2:].zfill(32),
                'dec': value
            }
        
        with open(filename, 'w') as f:
            json.dump(microcode_dict, f, indent=2)
    
    def load_from_file(self, filename: str):
        """Carga microcódigo desde un archivo JSON"""
        try:
            with open(filename, 'r') as f:
                microcode_dict = json.load(f)
            
            for addr_str, data in microcode_dict.items():
                addr = int(addr_str)
                if 0 <= addr < 256:
                    value = int(data['hex'], 16) if 'hex' in data else data['dec']
                    self.__memory[addr] = Bus(32, value)
        except FileNotFoundError:
            print(f"Archivo {filename} no encontrado. Usando microcódigo por defecto.")
    
    def get_word_hex(self, address: int) -> str:
        """Obtiene la palabra de control en hexadecimal"""
        return self.read(address).get_Hexadecimal_value()
    
    def get_word_bin(self, address: int) -> str:
        """Obtiene la palabra de control en binario"""
        return self.read(address).get_Binary_value()
    
    def dump_memory(self, start_addr: int = 0, end_addr: int = 255):
        """Muestra un volcado de la memoria de control"""
        print("=" * 80)
        print("DUMP MEMORIA DE CONTROL")
        print("=" * 80)
        print(f"{'Addr':^6} {'Hex':^10} {'Binary':^35} {'Opcode':^7} {'Step':^5}")
        print("-" * 80)
        
        for addr in range(start_addr, min(end_addr + 1, 256)):
            word = self.__memory[addr]
            opcode = (addr >> 4) & 0xF
            step = addr & 0xF
            
            print(f"{addr:^6} {word.get_Hexadecimal_value():^10} "
                  f"{word.get_Binary_value():^35} "
                  f"{opcode:^7} {step:^5}")