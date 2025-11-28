import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit
from Business.Logic_Gates.AND_Gate import AND_Gate
from Business.Logic_Gates.OR_Gate import OR_Gate
from Business.Logic_Gates.XOR_Gate import XOR_Gate
from Business.Logic_Gates.NOT_Gate import NOT_Gate

class TestLogicGates(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test de Puertas Lógicas...")
        self.bit0 = Bit(0)
        self.bit1 = Bit(1)
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test de Puertas Lógicas completado")
        print("="*50)
    
    def test_and_gate_truth_table(self):
        """Test: AND Gate - Tabla de verdad completa"""
        print("Ejecutando test_and_gate_truth_table")
        
        and_gate = AND_Gate()
        print(f"✓ Puerta AND creada: {and_gate}")
        
        test_cases = [
            ((0, 0), 0, "0 AND 0 = 0"),
            ((0, 1), 0, "0 AND 1 = 0"),
            ((1, 0), 0, "1 AND 0 = 0"),
            ((1, 1), 1, "1 AND 1 = 1")
        ]
        
        for inputs, expected, description in test_cases:
            bit_a = Bit(inputs[0])
            bit_b = Bit(inputs[1])
            
            and_gate.connect_input(bit_a, 0)
            and_gate.connect_input(bit_b, 1)
            result = and_gate.calculate()
            
            actual_value = result.get_value()
            print(f"✓ {description}: {actual_value}")
            self.assertEqual(actual_value, expected)
    
    def test_or_gate_truth_table(self):
        """Test: OR Gate - Tabla de verdad completa"""
        print("Ejecutando test_or_gate_truth_table")
        
        or_gate = OR_Gate()
        print(f"✓ Puerta OR creada: {or_gate}")
        
        test_cases = [
            ((0, 0), 0, "0 OR 0 = 0"),
            ((0, 1), 1, "0 OR 1 = 1"),
            ((1, 0), 1, "1 OR 0 = 1"),
            ((1, 1), 1, "1 OR 1 = 1")
        ]
        
        for inputs, expected, description in test_cases:
            bit_a = Bit(inputs[0])
            bit_b = Bit(inputs[1])
            
            or_gate.connect_input(bit_a, 0)
            or_gate.connect_input(bit_b, 1)
            result = or_gate.calculate()
            
            actual_value = result.get_value()
            print(f"✓ {description}: {actual_value}")
            self.assertEqual(actual_value, expected)
    
    def test_xor_gate_truth_table(self):
        """Test: XOR Gate - Tabla de verdad completa"""
        print("Ejecutando test_xor_gate_truth_table")
        
        xor_gate = XOR_Gate()
        print(f"✓ Puerta XOR creada: {xor_gate}")
        
        test_cases = [
            ((0, 0), 0, "0 XOR 0 = 0"),
            ((0, 1), 1, "0 XOR 1 = 1"),
            ((1, 0), 1, "1 XOR 0 = 1"),
            ((1, 1), 0, "1 XOR 1 = 0")
        ]
        
        for inputs, expected, description in test_cases:
            bit_a = Bit(inputs[0])
            bit_b = Bit(inputs[1])
            
            xor_gate.connect_input(bit_a, 0)
            xor_gate.connect_input(bit_b, 1)
            result = xor_gate.calculate()
            
            actual_value = result.get_value()
            print(f"✓ {description}: {actual_value}")
            self.assertEqual(actual_value, expected)
    
    def test_not_gate_truth_table(self):
        """Test: NOT Gate - Tabla de verdad completa"""
        print("Ejecutando test_not_gate_truth_table")
        
        not_gate = NOT_Gate()
        print(f"✓ Puerta NOT creada: {not_gate}")
        
        test_cases = [
            (0, 1, "NOT 0 = 1"),
            (1, 0, "NOT 1 = 0")
        ]
        
        for input_val, expected, description in test_cases:
            bit_input = Bit(input_val)
            
            not_gate.connect_input(bit_input, 0)
            result = not_gate.calculate()
            
            actual_value = result.get_value()
            print(f"✓ {description}: {actual_value}")
            self.assertEqual(actual_value, expected)
    
    def test_conexiones_invalidas(self):
        """Test: Manejo de conexiones inválidas"""
        print("Ejecutando test_conexiones_invalidas")
        
        and_gate = AND_Gate()
        print(f"✓ Puerta AND para test de conexiones: {and_gate}")
        
        # Índice fuera de rango
        with self.assertRaises(ValueError) as cm:
            and_gate.connect_input(self.bit0, 5)
        print(f"✓ Índice 5 en AND (2 entradas): {cm.exception}")
        
        with self.assertRaises(ValueError) as cm:
            and_gate.connect_input(self.bit0, -1)
        print(f"✓ Índice -1 en AND: {cm.exception}")
    
    def test_entradas_no_conectadas(self):
        """Test: Comportamiento con entradas no conectadas"""
        print("Ejecutando test_entradas_no_conectadas")
        
        and_gate = AND_Gate()
        print(f"✓ Puerta AND sin conexiones: {and_gate}")
        
        # Sin conectar entradas - debería manejarse gracefuly
        result = and_gate.calculate()
        actual_value = result.get_value()
        print(f"✓ AND sin entradas: {actual_value}")
        self.assertEqual(actual_value, 0)  # Valor por defecto
    
    def test_encapsulamiento_estricto(self):
        """Test: Verificar que los atributos privados no son accesibles"""
        print("Ejecutando test_encapsulamiento_estricto")
        
        and_gate = AND_Gate()
        print(f"✓ Puerta AND para test encapsulamiento: {and_gate}")
        
        # Verificar que NO se puede acceder directamente a atributos privados
        with self.assertRaises(AttributeError):
            _ = and_gate.__inputs
        print("✓ Atributo __inputs correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = and_gate.__output
        print("✓ Atributo __output correctamente protegido")
        
        with self.assertRaises(AttributeError):
            _ = and_gate.__n_inputs
        print("✓ Atributo __n_inputs correctamente protegido")
        
        # Verificar que los métodos públicos funcionan correctamente
        and_gate.connect_input(self.bit1, 0)
        and_gate.connect_input(self.bit1, 1)
        result = and_gate.calculate()
        
        actual_value = result.get_value()
        print(f"✓ AND(1, 1) = {actual_value}")
        self.assertEqual(actual_value, 1)
        self.assertIsNotNone(and_gate.get_output())
    
    def test_comparacion_puertas(self):
        """Test: Comparación entre diferentes tipos de puertas"""
        print("Ejecutando test_comparacion_puertas")
        
        and_gate = AND_Gate()
        or_gate = OR_Gate()
        xor_gate = XOR_Gate()
        not_gate = NOT_Gate()
        
        print(f"✓ AND: {and_gate}")
        print(f"✓ OR: {or_gate}")
        print(f"✓ XOR: {xor_gate}")
        print(f"✓ NOT: {not_gate}")
        
        # Todas deberían tener salidas diferentes para las mismas entradas
        and_gate.connect_input(self.bit1, 0)
        and_gate.connect_input(self.bit1, 1)
        and_result = and_gate.calculate().get_value()
        
        or_gate.connect_input(self.bit1, 0)
        or_gate.connect_input(self.bit1, 1)
        or_result = or_gate.calculate().get_value()
        
        xor_gate.connect_input(self.bit1, 0)
        xor_gate.connect_input(self.bit1, 1)
        xor_result = xor_gate.calculate().get_value()
        
        not_gate.connect_input(self.bit1, 0)
        not_result = not_gate.calculate().get_value()
        
        print(f"✓ AND(1,1) = {and_result}")
        print(f"✓ OR(1,1) = {or_result}")
        print(f"✓ XOR(1,1) = {xor_result}")
        print(f"✓ NOT(1) = {not_result}")
        
        self.assertNotEqual(and_result, xor_result)
        self.assertNotEqual(or_result, xor_result)
        self.assertNotEqual(not_result, and_result)

def run_logic_gates_tests():
    """Función para ejecutar tests de Puertas Lógicas con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE PUERTAS LÓGICAS")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestLogicGates)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS PUERTAS LÓGICAS:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS DE PUERTAS LÓGICAS PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas de Puertas Lógicas fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_logic_gates_tests()