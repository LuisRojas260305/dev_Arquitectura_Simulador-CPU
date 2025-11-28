import unittest
import sys
import os

# Configurar path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit

class TestBit(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test de Bit...")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test de Bit completado")
        print("="*50)
    
    def test_creacion_valida(self):
        """Test: Creación de Bits con valores válidos"""
        print("Ejecutando test_creacion_valida")
        
        bit0 = Bit(0)
        bit1 = Bit(1)
        
        print(f"✓ Bit(0): {bit0}")
        print(f"✓ Bit(1): {bit1}")
        
        self.assertEqual(bit0.get_value(), 0)
        self.assertEqual(bit1.get_value(), 1)
    
    def test_creacion_invalida(self):
        """Test: Creación de Bits con valores inválidos debe lanzar error"""
        print("Ejecutando test_creacion_invalida")
        
        invalid_values = [2, -1, 10, -5, 100]
        for value in invalid_values:
            with self.assertRaises(ValueError) as cm:
                Bit(value)
            print(f"✓ Bit({value}): {cm.exception}")
    
    def test_set_value_valido(self):
        """Test: set_value con valores válidos"""
        print("Ejecutando test_set_value_valido")
        
        bit = Bit(0)
        print(f"✓ Bit inicial: {bit}")
        
        bit.set_value(1)
        print(f"✓ Después set_value(1): {bit}")
        self.assertEqual(bit.get_value(), 1)
        
        bit.set_value(0)
        print(f"✓ Después set_value(0): {bit}")
        self.assertEqual(bit.get_value(), 0)
    
    def test_set_value_invalido(self):
        """Test: set_value con valores inválidos debe lanzar error"""
        print("Ejecutando test_set_value_invalido")
        
        bit = Bit(0)
        invalid_values = [2, -5, 100, -1]
        
        for value in invalid_values:
            with self.assertRaises(ValueError) as cm:
                bit.set_value(value)
            print(f"✓ set_value({value}): {cm.exception}")
    
    def test_toggle(self):
        """Test: toggle cambia correctamente el valor"""
        print("Ejecutando test_toggle")
        
        bit0 = Bit(0)
        bit1 = Bit(1)
        
        print(f"✓ Bit inicial 0: {bit0}")
        print(f"✓ Bit inicial 1: {bit1}")
        
        bit0.toggle()
        print(f"✓ Bit0 después toggle: {bit0}")
        self.assertEqual(bit0.get_value(), 1)
        
        bit1.toggle()
        print(f"✓ Bit1 después toggle: {bit1}")
        self.assertEqual(bit1.get_value(), 0)
        
        # Toggle múltiple
        bit0.toggle()
        bit0.toggle()
        print(f"✓ Bit0 después dos toggles: {bit0}")
        self.assertEqual(bit0.get_value(), 1)
    
    def test_representaciones(self):
        """Test: __str__ y __repr__ funcionan correctamente"""
        print("Ejecutando test_representaciones")
        
        bit = Bit(1)
        
        str_repr = str(bit)
        repr_repr = repr(bit)
        
        print(f"✓ str(bit): {str_repr}")
        print(f"✓ repr(bit): {repr_repr}")
        
        self.assertEqual(str_repr, "Bit: 1")
        self.assertEqual(repr_repr, "Bit(1)")
    
    def test_igualdad(self):
        """Test: comparación entre Bits"""
        print("Ejecutando test_igualdad")
        
        bit1a = Bit(1)
        bit1b = Bit(1)
        bit0 = Bit(0)
        
        print(f"✓ Bit1a: {bit1a}")
        print(f"✓ Bit1b: {bit1b}")
        print(f"✓ Bit0: {bit0}")
        
        self.assertEqual(bit1a, bit1b)
        self.assertNotEqual(bit1a, bit0)
        self.assertNotEqual(bit1a, "no es un bit")
        
        print("✓ Comparaciones de igualdad funcionan correctamente")
    
    def test_encapsulamiento(self):
        """Test: los atributos internos están protegidos"""
        print("Ejecutando test_encapsulamiento")
        
        bit = Bit(1)
        
        # Verificar que no se puede acceder directamente al atributo privado
        with self.assertRaises(AttributeError):
            _ = bit.__value
        print("✓ Atributo __value correctamente protegido")

def run_bit_tests():
    """Función para ejecutar tests de Bit con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE BIT")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBit)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS BIT:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS DE BIT PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas de Bit fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_bit_tests()