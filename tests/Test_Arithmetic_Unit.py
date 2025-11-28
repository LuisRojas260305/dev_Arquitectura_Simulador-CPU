import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class TestBus(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test...")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test completado")
        print("="*50)
    
    def test_get_line_bit(self):
        """Test: get_Line_bit funciona correctamente"""
        print("Ejecutando test_get_line_bit")
        
        bus = Bus(width=4, initial_value=10)  # 10 = 1010
        
        # Test valores válidos
        bit_0 = bus.get_Line_bit(0)
        bit_1 = bus.get_Line_bit(1)
        bit_2 = bus.get_Line_bit(2)
        bit_3 = bus.get_Line_bit(3)
        
        self.assertEqual(bit_0.get_value(), 1)  # MSB
        self.assertEqual(bit_1.get_value(), 0)
        self.assertEqual(bit_2.get_value(), 1)
        self.assertEqual(bit_3.get_value(), 0)  # LSB
        
        print("✓ Bits obtenidos correctamente: [1, 0, 1, 0]")
        
        # Test índices inválidos
        with self.assertRaises(ValueError):
            bus.get_Line_bit(-1)
        print("✓ Índice -1 correctamente rechazado")
        
        with self.assertRaises(ValueError):
            bus.get_Line_bit(4)
        print("✓ Índice 4 correctamente rechazado")
    
    def test_set_line_bit(self):
        """Test: set_Line_bit funciona correctamente"""
        print("Ejecutando test_set_line_bit")
        
        bus = Bus(width=4, initial_value=0)  # 0000 inicialmente
        
        # Establecer bits individuales
        bus.set_Line_bit(0, Bit(1))  # MSB
        bus.set_Line_bit(2, Bit(1))
        
        # Verificar el resultado
        self.assertEqual(bus.get_Line_bit(0).get_value(), 1)
        self.assertEqual(bus.get_Line_bit(1).get_value(), 0)
        self.assertEqual(bus.get_Line_bit(2).get_value(), 1)
        self.assertEqual(bus.get_Line_bit(3).get_value(), 0)
        self.assertEqual(bus.get_Decimal_value(), 10)  # 1010 = 10
        
        print("✓ Bits establecidos correctamente: 1010 (10)")
        
        # Test índices inválidos
        with self.assertRaises(ValueError):
            bus.set_Line_bit(-1, Bit(1))
        print("✓ Índice -1 correctamente rechazado")
        
        with self.assertRaises(ValueError):
            bus.set_Line_bit(4, Bit(1))
        print("✓ Índice 4 correctamente rechazado")
        
        # Test tipo inválido
        with self.assertRaises(TypeError):
            bus.set_Line_bit(0, 1)  # No es un Bit
        print("✓ Tipo no Bit correctamente rechazado")
    
    def test_line_operations_comprehensive(self):
        """Test: Operaciones comprehensivas con líneas individuales"""
        print("Ejecutando test_line_operations_comprehensive")
        
        bus = Bus(width=8, initial_value=0)
        
        # Configurar patrón 10101010 usando set_Line_bit
        for i in range(8):
            if i % 2 == 0:
                bus.set_Line_bit(i, Bit(1))
            else:
                bus.set_Line_bit(i, Bit(0))
        
        # Verificar con get_Line_bit
        expected_pattern = [1, 0, 1, 0, 1, 0, 1, 0]
        for i in range(8):
            self.assertEqual(bus.get_Line_bit(i).get_value(), expected_pattern[i])
        
        # Verificar valor total
        self.assertEqual(bus.get_Decimal_value(), 170)  # 10101010 = 170
        self.assertEqual(bus.get_Binary_value(), "10101010")
        
        print("✓ Patrón 10101010 configurado y verificado correctamente")
    
    # ... (el resto de los tests anteriores se mantienen igual)

def run_bus_tests():
    """Función para ejecutar tests con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE BUS (ACTUALIZADO)")
    print("="*60)
    
    # Crear test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBus)
    
    # Ejecutar tests con verbosidad
    runner = unittest.TextTestRunner(verbosity=2, descriptions=True)
    result = runner.run(suite)
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS BUS:")
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Errores: {len(result.errors)}")
    print(f"Fallos: {len(result.failures)}")
    print(f"Éxitos: {result.testsRun - len(result.errors) - len(result.failures)}")
    
    if result.wasSuccessful():
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print("❌ Algunas pruebas fallaron")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    run_bus_tests()