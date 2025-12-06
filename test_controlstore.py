# test_controlstore.py

import sys
sys.path.append('.')

from Business.CPU_Core.Control_Unit.ControlStore import ControlStore

class TestControlStore:
    """Pruebas para la memoria de control"""
    
    def __init__(self):
        self.control_store = ControlStore()
        self.test_count = 0
        self.passed_count = 0
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("=" * 60)
        print("TESTING CONTROL STORE")
        print("=" * 60)
        
        self.test_address_calculation()
        self.test_memory_access()
        self.test_instruction_halt()
        self.test_instruction_add()
        self.test_file_operations()
        
        self.print_summary()
        return self.passed_count == self.test_count
    
    def test_address_calculation(self):
        """Prueba el cálculo de direcciones"""
        print("\n📍 1. Prueba Cálculo de Direcciones")
        print("-" * 40)
        
        test_cases = [
            (0x0, 0, 0x00),   # Opcode 0, step 0
            (0x1, 0, 0x10),   # Opcode 1, step 0
            (0x3, 5, 0x35),   # Opcode 3, step 5 (ADD paso 5)
            (0xF, 15, 0xFF),  # Opcode 15, step 15
            (0xA, 7, 0xA7),   # Opcode 10, step 7
        ]
        
        for opcode, step, expected in test_cases:
            # Usamos método interno para calcular
            address = (opcode << 4) | step
            self.assert_test(
                f"Opcode 0x{opcode:X}, Step {step}",
                address == expected,
                f"0x{expected:02X}",
                f"0x{address:02X}"
            )
    
    def test_memory_access(self):
        """Prueba acceso a memoria"""
        print("\n📚 2. Prueba Acceso a Memoria")
        print("-" * 40)
        
        # Test 1: Todas las direcciones son válidas
        for addr in [0, 127, 255]:
            try:
                word = self.control_store.read(addr)
                self.assert_test(
                    f"Lectura dirección {addr}",
                    word.width == 32,
                    "Bus(32)",
                    f"Bus({word.width})"
                )
            except ValueError:
                self.assert_test(
                    f"Lectura dirección {addr}",
                    False,
                    "Éxito",
                    "ValueError"
                )
        
        # Test 2: Direcciones fuera de rango
        for addr in [-1, 256, 300]:
            try:
                word = self.control_store.read(addr)
                self.assert_test(
                    f"Dirección {addr} (fuera de rango)",
                    False,
                    "ValueError",
                    "Éxito"
                )
            except ValueError:
                self.assert_test(
                    f"Dirección {addr} (fuera de rango)",
                    True,
                    "ValueError",
                    "ValueError"
                )
    
    def test_instruction_halt(self):
        """Prueba microcódigo para instrucción HALT"""
        print("\n🛑 3. Prueba Instrucción HALT (0xF)")
        print("-" * 40)
        
        # HALT debería activar la señal HALT en step 3
        word = self.control_store.read_by_opcode_step(0xF, 3)
        binary = word.get_Binary_value()
        
        # Bit 28 es HALT (contando desde 0)
        halt_bit = binary[28]
        end_instr_bit = binary[31]
        
        self.assert_test(
            "HALT activa bit 28",
            halt_bit == '1',
            "Bit 28 = '1'",
            f"Bit 28 = '{halt_bit}'"
        )
        
        self.assert_test(
            "END_INSTR activa bit 31",
            end_instr_bit == '1',
            "Bit 31 = '1'",
            f"Bit 31 = '{end_instr_bit}'"
        )
        
        # Verificar que otros pasos no tengan HALT activo
        for step in [0, 1, 2, 4, 5]:
            word = self.control_store.read_by_opcode_step(0xF, step)
            binary = word.get_Binary_value()
            halt_bit = binary[28]
            
            if step != 3:
                self.assert_test(
                    f"HALT inactivo en step {step}",
                    halt_bit == '0',
                    "Bit 28 = '0'",
                    f"Bit 28 = '{halt_bit}'"
                )
    
    def test_instruction_add(self):
        """Prueba microcódigo para instrucción ADD"""
        print("\n➕ 4. Prueba Instrucción ADD (0x3)")
        print("-" * 40)
        
        # ADD paso 5: Configurar ALU para suma
        word = self.control_store.read_by_opcode_step(0x3, 5)
        binary = word.get_Binary_value()
        
        # ALUop bits 0-1: deberían ser 00 (Aritmética)
        aluop_bits = binary[0:2]
        self.assert_test(
            "ALUop = 00 (Aritmética)",
            aluop_bits == "00",
            "'00'",
            f"'{aluop_bits}'"
        )
        
        # ALUfunc bits 2-4: deberían ser 000 (Suma)
        alufunc_bits = binary[2:5]
        self.assert_test(
            "ALUfunc = 000 (Suma)",
            alufunc_bits == "000",
            "'000'",
            f"'{alufunc_bits}'"
        )
        
        # ADD paso 6: AC_LOAD y END_INSTR activos
        word = self.control_store.read_by_opcode_step(0x3, 6)
        binary = word.get_Binary_value()
        
        ac_load_bit = binary[8]  # Bit 8 es AC_LOAD
        end_instr_bit = binary[31]  # Bit 31 es END_INSTR
        
        self.assert_test(
            "AC_LOAD activo en step 6",
            ac_load_bit == '1',
            "Bit 8 = '1'",
            f"Bit 8 = '{ac_load_bit}'"
        )
        
        self.assert_test(
            "END_INSTR activo en step 6",
            end_instr_bit == '1',
            "Bit 31 = '1'",
            f"Bit 31 = '{end_instr_bit}'"
        )
    
    def test_file_operations(self):
        """Prueba guardar y cargar desde archivo"""
        print("\n💾 5. Prueba Operaciones con Archivos")
        print("-" * 40)
        
        import os
        import tempfile
        
        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
            tmp_file = tmp.name
        
        try:
            # Guardar microcódigo
            self.control_store.save_to_file(tmp_file)
            self.assert_test(
                "Guardar microcódigo",
                os.path.exists(tmp_file),
                "Archivo creado",
                f"Archivo {'existe' if os.path.exists(tmp_file) else 'no existe'}"
            )
            
            # Leer y verificar que no está vacío
            file_size = os.path.getsize(tmp_file)
            self.assert_test(
                "Archivo no vacío",
                file_size > 100,  # Debería tener al menos 100 bytes
                f"Tamaño > 100 bytes",
                f"Tamaño = {file_size} bytes"
            )
            
            # Crear nueva instancia y cargar
            new_store = ControlStore()
            new_store.load_from_file(tmp_file)
            
            # Verificar que algunas direcciones sean iguales
            test_addresses = [0x00, 0x35, 0xFF]
            all_match = True
            
            for addr in test_addresses:
                original = self.control_store.read(addr).get_Decimal_value()
                loaded = new_store.read(addr).get_Decimal_value()
                
                if original != loaded:
                    all_match = False
                    print(f"  ✗ Dirección 0x{addr:02X}: original={original}, loaded={loaded}")
            
            self.assert_test(
                "Carga desde archivo",
                all_match,
                "Todas las direcciones coinciden",
                "Algunas direcciones no coinciden" if not all_match else "Todas coinciden"
            )
            
        finally:
            # Limpiar archivo temporal
            if os.path.exists(tmp_file):
                os.unlink(tmp_file)
    
    def assert_test(self, test_name, condition, expected, actual):
        """Método helper para assertions"""
        self.test_count += 1
        if condition:
            self.passed_count += 1
            print(f"  ✓ {test_name}: {expected} [OK]")
        else:
            print(f"  ✗ {test_name}")
            print(f"     Esperado: {expected}")
            print(f"     Obtenido: {actual}")
    
    def print_summary(self):
        """Imprime resumen de pruebas"""
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS - CONTROL STORE")
        print("=" * 60)
        
        failed = self.test_count - self.passed_count
        percentage = (self.passed_count / self.test_count * 100) if self.test_count > 0 else 0
        
        print(f"Pruebas ejecutadas: {self.test_count}")
        print(f"Pruebas pasadas:    {self.passed_count}")
        print(f"Pruebas falladas:   {failed}")
        print(f"Porcentaje éxito:   {percentage:.1f}%")
        
        if failed == 0:
            print("\n🎉 ¡CONTROL STORE FUNCIONA CORRECTAMENTE!")
        else:
            print(f"\n⚠️  {failed} prueba(s) fallaron")
        
        return failed == 0

def test_visual_dump():
    """Prueba visual del volcado de memoria"""
    print("\n👁️  VOLCADO VISUAL DE MEMORIA DE CONTROL")
    print("=" * 80)
    
    store = ControlStore()
    
    # Mostrar solo algunas direcciones clave
    print("\n📋 Direcciones clave para HALT (0xF):")
    store.dump_memory(0xF0, 0xFF)  # Opcode F, todos los steps
    
    print("\n📋 Direcciones clave para ADD (0x3):")
    store.dump_memory(0x30, 0x3F)  # Opcode 3, todos los steps
    
    print("\n📋 Direcciones clave para LOAD (0x1):")
    store.dump_memory(0x10, 0x1F)  # Opcode 1, todos los steps

if __name__ == "__main__":
    # Ejecutar pruebas automáticas
    tester = TestControlStore()
    success = tester.run_all_tests()
    
    # Mostrar volcado visual
    test_visual_dump()
    
    # Código de salida para CI/CD
    sys.exit(0 if success else 1)