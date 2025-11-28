import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.CPU_Core.Shift_Unit import Shift_Unit
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class TestShiftUnit(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test de Shift Unit...")
        self.shift_unit = Shift_Unit(width=8)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test de Shift Unit completado")
        print("="*50)
    
    def test_sll_basic(self):
        """Test: Desplazamiento lógico a la izquierda básico"""
        print("Ejecutando test_sll_basic")
        
        # Bus inicial: 00000001 (1)
        input_bus = Bus(width=8, initial_value=1)
        
        # Desplazar 1 bit a la izquierda
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=1,
            Input=input_bus,
            Mode=Shift_Unit.SLL
        )
        
        # Resultado esperado: 00000010 (2)
        self.assertEqual(result.get_Decimal_value(), 2)
        self.assertEqual(carry_out.get_value(), 0)  # El bit 0 (MSB) era 0
        print("✓ SLL básico correcto: 1 << 1 = 2, carry=0")
    
    def test_sll_with_carry(self):
        """Test: SLL que genera carry out"""
        print("Ejecutando test_sll_with_carry")
        
        # Bus inicial: 10000000 (128)
        input_bus = Bus(width=8, initial_value=128)
        
        # Desplazar 1 bit a la izquierda
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=1,
            Input=input_bus,
            Mode=Shift_Unit.SLL
        )
        
        # Resultado esperado: 00000000 (0) con carry = 1
        self.assertEqual(result.get_Decimal_value(), 0)
        self.assertEqual(carry_out.get_value(), 1)  # El bit 0 (MSB) era 1
        print("✓ SLL con carry correcto: 128 << 1 = 0, carry=1")
    
    def test_sll_multiple_bits(self):
        """Test: Desplazamiento múltiple a la izquierda"""
        print("Ejecutando test_sll_multiple_bits")
        
        # Bus inicial: 00000101 (5)
        input_bus = Bus(width=8, initial_value=5)
        
        # Desplazar 3 bits a la izquierda
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=3,
            Input=input_bus,
            Mode=Shift_Unit.SLL
        )
        
        # Resultado esperado: 00101000 (40)
        self.assertEqual(result.get_Decimal_value(), 40)
        self.assertEqual(carry_out.get_value(), 0)  # El bit 2 era 0
        print("✓ SLL múltiple correcto: 5 << 3 = 40, carry=0")
    
    def test_sra_basic(self):
        """Test: Desplazamiento aritmético a la derecha básico"""
        print("Ejecutando test_sra_basic")
        
        # Bus inicial: 00000010 (2)
        input_bus = Bus(width=8, initial_value=2)
        
        # Desplazar 1 bit a la derecha
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=1,
            Input=input_bus,
            Mode=Shift_Unit.SRA
        )
        
        # Resultado esperado: 00000001 (1)
        self.assertEqual(result.get_Decimal_value(), 1)
        self.assertEqual(carry_out.get_value(), 0)  # El bit 7 (LSB) era 0
        print("✓ SRA básico correcto: 2 >> 1 = 1, carry=0")
    
    def test_sra_negative_number(self):
        """Test: SRA con número negativo (extensión de signo)"""
        print("Ejecutando test_sra_negative_number")
        
        # Bus inicial: 10000000 (128) - MSB = 1 (negativo en complemento a 2)
        input_bus = Bus(width=8, initial_value=128)
        
        # Desplazar 2 bits a la derecha
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=2,
            Input=input_bus,
            Mode=Shift_Unit.SRA
        )
        
        # Verificar que se extendió el signo correctamente
        # Resultado esperado: 11100000 (224 en decimal sin signo)
        self.assertEqual(result.get_Decimal_value(), 224)
        self.assertEqual(result.get_Binary_value(), "11100000")
        self.assertEqual(carry_out.get_value(), 0)  # El bit 6 era 0
        print("✓ SRA con extensión de signo correcto: 10000000 >> 2 = 11100000, carry=0")
    
    def test_sra_with_carry(self):
        """Test: SRA que genera carry out"""
        print("Ejecutando test_sra_with_carry")
        
        # Bus inicial: 00000001 (1)
        input_bus = Bus(width=8, initial_value=1)
        
        # Desplazar 1 bit a la derecha
        result, carry_out = self.shift_unit.Calculate(
            Shift_Amount=1,
            Input=input_bus,
            Mode=Shift_Unit.SRA
        )
        
        # Resultado esperado: 00000000 (0) con carry = 1
        self.assertEqual(result.get_Decimal_value(), 0)
        self.assertEqual(carry_out.get_value(), 1)  # El bit 7 (LSB) era 1
        print("✓ SRA con carry correcto: 1 >> 1 = 0, carry=1")
    
    def test_zero_shift(self):
        """Test: Desplazamiento de 0 bits en ambos modos"""
        print("Ejecutando test_zero_shift")
        
        input_bus = Bus(width=8, initial_value=42)
        
        # SLL con 0 bits
        result_sll, carry_sll = self.shift_unit.Calculate(
            Shift_Amount=0,
            Input=input_bus,
            Mode=Shift_Unit.SLL
        )
        
        # SRA con 0 bits
        result_sra, carry_sra = self.shift_unit.Calculate(
            Shift_Amount=0,
            Input=input_bus,
            Mode=Shift_Unit.SRA
        )
        
        # Ambos deben devolver el mismo bus sin cambios
        self.assertEqual(result_sll.get_Decimal_value(), 42)
        self.assertEqual(result_sra.get_Decimal_value(), 42)
        self.assertEqual(carry_sll.get_value(), 0)
        self.assertEqual(carry_sra.get_value(), 0)
        print("✓ Desplazamiento cero correcto en ambos modos")
    
    def test_invalid_shift_amount(self):
        """Test: Validación de Shift_Amount fuera de rango"""
        print("Ejecutando test_invalid_shift_amount")
        
        input_bus = Bus(width=8, initial_value=10)
        
        # Shift_Amount negativo
        with self.assertRaises(ValueError):
            self.shift_unit.Calculate(-1, input_bus, Shift_Unit.SLL)
        print("✓ Shift_Amount negativo correctamente rechazado")
        
        # Shift_Amount mayor o igual al ancho del bus
        with self.assertRaises(ValueError):
            self.shift_unit.Calculate(8, input_bus, Shift_Unit.SLL)
        print("✓ Shift_Amount >= ancho del bus correctamente rechazado")
    
    def test_invalid_input_type(self):
        """Test: Validación de tipo de entrada incorrecto"""
        print("Ejecutando test_invalid_input_type")
        
        # Input que no es Bus
        with self.assertRaises(TypeError):
            self.shift_unit.Calculate(1, "not_a_bus", Shift_Unit.SLL)
        print("✓ Tipo de entrada incorrecto correctamente rechazado")
    
    def test_invalid_mode(self):
        """Test: Validación de modo de operación inválido"""
        print("Ejecutando test_invalid_mode")
        
        input_bus = Bus(width=8, initial_value=10)
        
        # Modo inválido
        with self.assertRaises(ValueError):
            self.shift_unit.Calculate(1, input_bus, 999)
        print("✓ Modo de operación inválido correctamente rechazado")
    
    def test_comprehensive_shift_operations(self):
        """Test: Operaciones comprehensivas de desplazamiento"""
        print("Ejecutando test_comprehensive_shift_operations")
        
        # Probar varios valores y desplazamientos
        test_cases = [
            # (valor_inicial, shift_amount, mode, valor_esperado, carry_esperado)
            (1, 1, Shift_Unit.SLL, 2, 0),    # 00000001 -> 00000010 (bit 0=0)
            (3, 2, Shift_Unit.SLL, 12, 0),   # 00000011 -> 00001100 (bit 1=0)
            (64, 1, Shift_Unit.SLL, 128, 0), # 01000000 -> 10000000 (bit 0=0)
            (128, 1, Shift_Unit.SLL, 0, 1),  # 10000000 -> 00000000 (bit 0=1)
            (4, 1, Shift_Unit.SRA, 2, 0),    # 00000100 -> 00000010 (bit 7=0)
            (1, 1, Shift_Unit.SRA, 0, 1),    # 00000001 -> 00000000 (bit 7=1)
            (255, 2, Shift_Unit.SRA, 255, 1), # 11111111 -> 11111111 (bit 6=1)
        ]
        
        for initial_val, shift_amt, mode, expected_val, expected_carry in test_cases:
            with self.subTest(initial_val=initial_val, shift_amt=shift_amt, mode=mode):
                input_bus = Bus(width=8, initial_value=initial_val)
                result, carry = self.shift_unit.Calculate(shift_amt, input_bus, mode)
                
                self.assertEqual(result.get_Decimal_value(), expected_val)
                self.assertEqual(carry.get_value(), expected_carry)
        
        print("✓ Todas las operaciones comprehensivas verificadas correctamente")

def run_shift_unit_tests():
    """Función para ejecutar tests con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE SHIFT UNIT")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestShiftUnit)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS SHIFT UNIT:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS DE SHIFT UNIT PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas de Shift Unit fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_shift_unit_tests()