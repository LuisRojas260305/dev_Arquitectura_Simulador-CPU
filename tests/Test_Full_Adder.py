import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Full_Adder import Full_Adder

class TestFullAdder(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test de Full Adder...")
        self.fa = Full_Adder()
        self.bit0 = Bit(0)
        self.bit1 = Bit(1)
        print(f"✓ Full Adder creado: {self.fa}")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test de Full Adder completado")
        print("="*50)
    
    def test_full_adder_truth_table(self):
        """Test: Full Adder - Tabla de verdad completa"""
        print("Ejecutando test_full_adder_truth_table")
        
        test_cases = [
            ((0, 0, 0), (0, 0), "0 + 0 + 0 = 0, carry 0"),
            ((0, 0, 1), (1, 0), "0 + 0 + 1 = 1, carry 0"),
            ((0, 1, 0), (1, 0), "0 + 1 + 0 = 1, carry 0"),
            ((0, 1, 1), (0, 1), "0 + 1 + 1 = 0, carry 1"),
            ((1, 0, 0), (1, 0), "1 + 0 + 0 = 1, carry 0"),
            ((1, 0, 1), (0, 1), "1 + 0 + 1 = 0, carry 1"),
            ((1, 1, 0), (0, 1), "1 + 1 + 0 = 0, carry 1"),
            ((1, 1, 1), (1, 1), "1 + 1 + 1 = 1, carry 1")
        ]
        
        for inputs, expected, description in test_cases:
            input_a, input_b, carry_in = inputs
            expected_sum, expected_carry = expected
            
            # Configurar entradas
            self.fa.set_Input_A(Bit(input_a))
            self.fa.set_Input_B(Bit(input_b))
            self.fa.set_C_in(Bit(carry_in))
            
            # Calcular
            self.fa.Calculate()
            
            # Verificar resultados
            actual_sum = self.fa.get_Output().get_value()
            actual_carry = self.fa.get_C_out().get_value()
            
            print(f"✓ {description}: Suma={actual_sum}, Carry={actual_carry}")
            
            self.assertEqual(actual_sum, expected_sum)
            self.assertEqual(actual_carry, expected_carry)
    
    def test_full_adder_multiple_calculations(self):
        """Test: Múltiples cálculos consecutivos"""
        print("Ejecutando test_full_adder_multiple_calculations")
        
        # Primer cálculo: 1 + 0 + 0 = 1, carry 0
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        
        sum1 = self.fa.get_Output().get_value()
        carry1 = self.fa.get_C_out().get_value()
        print(f"✓ Primer cálculo (1+0+0): Suma={sum1}, Carry={carry1}")
        self.assertEqual(sum1, 1)
        self.assertEqual(carry1, 0)
        
        # Cambiar entradas y recalcular: 1 + 1 + 0 = 0, carry 1
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        
        sum2 = self.fa.get_Output().get_value()
        carry2 = self.fa.get_C_out().get_value()
        print(f"✓ Segundo cálculo (1+1+0): Suma={sum2}, Carry={carry2}")
        self.assertEqual(sum2, 0)
        self.assertEqual(carry2, 1)
    
    def test_full_adder_encapsulamiento(self):
        """Test: Los atributos internos están protegidos"""
        print("Ejecutando test_full_adder_encapsulamiento")
        
        # Verificar que no se puede acceder directamente a atributos privados
        with self.assertRaises(AttributeError):
            _ = self.fa.__Input_A
        print("✓ Atributo __Input_A correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.fa.__Input_B
        print("✓ Atributo __Input_B correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.fa.__C_in
        print("✓ Atributo __C_in correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.fa.__Output
        print("✓ Atributo __Output correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.fa.__C_out
        print("✓ Atributo __C_out correctamente protegido")
    
    def test_full_adder_str_representation(self):
        """Test: Representación string del Full Adder"""
        print("Ejecutando test_full_adder_str_representation")
        
        # Configurar valores específicos
        self.fa.set_Input_A(Bit(1))
        self.fa.set_Input_B(Bit(0))
        self.fa.set_C_in(Bit(1))
        
        try:
            str_representation = str(self.fa)
            print(f"✓ Representación string: {str_representation}")
            self.assertIsInstance(str_representation, str)
            # Verificar que contiene información básica
            self.assertIn("FullAdder", str_representation)
        except Exception as e:
            self.fail(f"❌ __str__ method failed: {e}")
    
    def test_full_adder_edge_cases(self):
        """Test: Casos extremos del Full Adder"""
        print("Ejecutando test_full_adder_edge_cases")
        
        # Caso: máximo carry propagation
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        
        sum_result = self.fa.get_Output().get_value()
        carry_result = self.fa.get_C_out().get_value()
        print(f"✓ Caso extremo (1+1+1): Suma={sum_result}, Carry={carry_result}")
        self.assertEqual(sum_result, 1)
        self.assertEqual(carry_result, 1)
        
        # Caso: sin carry
        self.fa.set_Input_A(self.bit0)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        
        sum_result = self.fa.get_Output().get_value()
        carry_result = self.fa.get_C_out().get_value()
        print(f"✓ Caso sin carry (0+0+0): Suma={sum_result}, Carry={carry_result}")
        self.assertEqual(sum_result, 0)
        self.assertEqual(carry_result, 0)
    
    def test_full_adder_method_consistency(self):
        """Test: Consistencia entre métodos getter"""
        print("Ejecutando test_full_adder_method_consistency")
        
        # Configurar valores
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        
        # Verificar que los getters devuelven objetos Bit válidos
        output_bit = self.fa.get_Output()
        carry_bit = self.fa.get_C_out()
        
        self.assertIsInstance(output_bit, Bit)
        self.assertIsInstance(carry_bit, Bit)
        
        output_value = output_bit.get_value()
        carry_value = carry_bit.get_value()
        
        print(f"✓ Output: {output_value} (tipo: {type(output_bit)})")
        print(f"✓ Carry: {carry_value} (tipo: {type(carry_bit)})")
        
        # Verificar valores esperados para 1 + 0 + 1 = 0, carry 1
        self.assertEqual(output_value, 0)
        self.assertEqual(carry_value, 1)

def run_full_adder_tests():
    """Función para ejecutar tests de Full Adder con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE FULL ADDER")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFullAdder)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS FULL ADDER:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS DE FULL ADDER PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas de Full Adder fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_full_adder_tests()