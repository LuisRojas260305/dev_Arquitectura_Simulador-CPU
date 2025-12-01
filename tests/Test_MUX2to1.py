import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.MUX2to1 import MUX2to1

class TestMUX2to1(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test de MUX2to1...")
        self.mux = MUX2to1()
        self.bit0 = Bit(0)
        self.bit1 = Bit(1)
        print(f"✓ MUX2to1 creado: {self.mux}")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test de MUX2to1 completado")
        print("="*50)
    
    def test_mux_truth_table(self):
        """Test: MUX2to1 - Tabla de verdad completa"""
        print("Ejecutando test_mux_truth_table")
        
        test_cases = [
            # (Input_A, Input_B, S, Expected_Output, Description)
            ((0, 0, 0), 0, "S=0: A=0, B=0 → Output=0"),
            ((0, 1, 0), 0, "S=0: A=0, B=1 → Output=0"),
            ((1, 0, 0), 1, "S=0: A=1, B=0 → Output=1"),
            ((1, 1, 0), 1, "S=0: A=1, B=1 → Output=1"),
            ((0, 0, 1), 0, "S=1: A=0, B=0 → Output=0"),
            ((0, 1, 1), 1, "S=1: A=0, B=1 → Output=1"),
            ((1, 0, 1), 0, "S=1: A=1, B=0 → Output=0"),
            ((1, 1, 1), 1, "S=1: A=1, B=1 → Output=1")
        ]
        
        for inputs, expected, description in test_cases:
            input_a, input_b, select = inputs
            
            # Configurar entradas
            self.mux.set_Input_A(Bit(input_a))
            self.mux.set_Input_B(Bit(input_b))
            self.mux.set_S(Bit(select))
            
            # Calcular
            self.mux.Calculate()
            
            # Verificar resultado
            actual_output = self.mux.get_Output().get_value()
            print(f"✓ {description}: {actual_output}")
            
            self.assertEqual(actual_output, expected, f"Failed for {description}")
    
    def test_mux_multiple_calculations(self):
        """Test: Múltiples cálculos consecutivos"""
        print("Ejecutando test_mux_multiple_calculations")
        
        # Primer cálculo: S=0, A=1, B=0 → Output=1
        self.mux.set_Input_A(self.bit1)
        self.mux.set_Input_B(self.bit0)
        self.mux.set_S(self.bit0)
        self.mux.Calculate()
        
        output1 = self.mux.get_Output().get_value()
        print(f"✓ Primer cálculo (S=0, A=1, B=0): Output={output1}")
        self.assertEqual(output1, 1)
        
        # Cambiar a S=1, A=1, B=0 → Output=0
        self.mux.set_S(self.bit1)
        self.mux.Calculate()
        
        output2 = self.mux.get_Output().get_value()
        print(f"✓ Segundo cálculo (S=1, A=1, B=0): Output={output2}")
        self.assertEqual(output2, 0)
        
        # Cambiar B=1, S=1, A=1 → Output=1
        self.mux.set_Input_B(self.bit1)
        self.mux.Calculate()
        
        output3 = self.mux.get_Output().get_value()
        print(f"✓ Tercer cálculo (S=1, A=1, B=1): Output={output3}")
        self.assertEqual(output3, 1)
    
    def test_mux_encapsulamiento(self):
        """Test: Los atributos internos están protegidos"""
        print("Ejecutando test_mux_encapsulamiento")
        
        # Verificar que no se puede acceder directamente a atributos privados
        with self.assertRaises(AttributeError):
            _ = self.mux.__Input_A
        print("✓ Atributo __Input_A correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.mux.__Input_B
        print("✓ Atributo __Input_B correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.mux.__S
        print("✓ Atributo __S correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.mux.__Output
        print("✓ Atributo __Output correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = self.mux.__And_A
        print("✓ Atributo __And_A correctamente protegido")
    
    def test_mux_str_representation(self):
        """Test: Representación string del MUX2to1"""
        print("Ejecutando test_mux_str_representation")
        
        # Configurar valores específicos
        self.mux.set_Input_A(Bit(1))
        self.mux.set_Input_B(Bit(0))
        self.mux.set_S(Bit(1))
        self.mux.Calculate()
        
        try:
            str_representation = str(self.mux)
            print(f"✓ Representación string: {str_representation}")
            self.assertIsInstance(str_representation, str)
            # Verificar que contiene información básica
            self.assertIn("MUX2to1", str_representation)
            self.assertIn("A=Bit: 1", str_representation)
            self.assertIn("B=Bit: 0", str_representation)
            self.assertIn("S=Bit: 1", str_representation)
        except Exception as e:
            self.fail(f"❌ __str__ method failed: {e}")
    
    def test_mux_getters_setters(self):
        """Test: Getters y Setters funcionan correctamente"""
        print("Ejecutando test_mux_getters_setters")
        
        # Test setters
        input_a = Bit(1)
        input_b = Bit(0)
        select = Bit(1)
        
        self.mux.set_Input_A(input_a)
        self.mux.set_Input_B(input_b)
        self.mux.set_S(select)
        
        # Test getters
        retrieved_a = self.mux.get_Input_A()
        retrieved_b = self.mux.get_Input_B()
        retrieved_s = self.mux.get_S()
        
        self.assertEqual(retrieved_a.get_value(), 1)
        self.assertEqual(retrieved_b.get_value(), 0)
        self.assertEqual(retrieved_s.get_value(), 1)
        
        print("✓ Getters y Setters funcionan correctamente")
    
    def test_mux_edge_cases(self):
        """Test: Casos extremos del MUX2to1"""
        print("Ejecutando test_mux_edge_cases")
        
        # Caso: Todas entradas 0
        self.mux.set_Input_A(self.bit0)
        self.mux.set_Input_B(self.bit0)
        self.mux.set_S(self.bit0)
        self.mux.Calculate()
        
        output1 = self.mux.get_Output().get_value()
        print(f"✓ Caso (0,0,0): Output={output1}")
        self.assertEqual(output1, 0)
        
        # Caso: Todas entradas 1
        self.mux.set_Input_A(self.bit1)
        self.mux.set_Input_B(self.bit1)
        self.mux.set_S(self.bit1)
        self.mux.Calculate()
        
        output2 = self.mux.get_Output().get_value()
        print(f"✓ Caso (1,1,1): Output={output2}")
        self.assertEqual(output2, 1)
    
    def test_mux_method_consistency(self):
        """Test: Consistencia entre métodos getter"""
        print("Ejecutando test_mux_method_consistency")
        
        # Configurar valores
        self.mux.set_Input_A(self.bit1)
        self.mux.set_Input_B(self.bit0)
        self.mux.set_S(self.bit1)
        self.mux.Calculate()
        
        # Verificar que los getters devuelven objetos Bit válidos
        output_bit = self.mux.get_Output()
        input_a_bit = self.mux.get_Input_A()
        input_b_bit = self.mux.get_Input_B()
        select_bit = self.mux.get_S()
        
        self.assertIsInstance(output_bit, Bit)
        self.assertIsInstance(input_a_bit, Bit)
        self.assertIsInstance(input_b_bit, Bit)
        self.assertIsInstance(select_bit, Bit)
        
        print(f"✓ Output: {output_bit.get_value()} (tipo: {type(output_bit)})")
        print(f"✓ Input_A: {input_a_bit.get_value()} (tipo: {type(input_a_bit)})")
        print(f"✓ Input_B: {input_b_bit.get_value()} (tipo: {type(input_b_bit)})")
        print(f"✓ Select: {select_bit.get_value()} (tipo: {type(select_bit)})")
        
        # Verificar valores esperados para S=1, A=1, B=0 → Output=0
        self.assertEqual(output_bit.get_value(), 0)

def run_mux2to1_tests():
    """Función para ejecutar tests de MUX2to1 con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE MUX2to1")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestMUX2to1)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS MUX2to1:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS DE MUX2to1 PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas de MUX2to1 fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_mux2to1_tests()