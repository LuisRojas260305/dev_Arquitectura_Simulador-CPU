import unittest
import sys
import os

# Configurar path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bus import Bus

class TestBus(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        print("\n" + "="*50)
        print("Configurando test...")
    
    def tearDown(self):
        """Limpieza después de cada test"""
        print("Test completado")
        print("="*50)
    
    def test_creacion_valida(self):
        """Test: Creación de Buses con valores válidos"""
        print("Ejecutando test_creacion_valida")
        
        # Test con valores por defecto
        bus_default = Bus()
        print(f"✓ Bus por defecto: {bus_default}")
        self.assertEqual(bus_default.get_Decimal_value(), 0)
        self.assertEqual(bus_default.width, 16)
        
        # Test con valores específicos
        bus_8bit = Bus(width=8, initial_value=42)
        print(f"✓ Bus 8-bit: {bus_8bit}")
        self.assertEqual(bus_8bit.get_Decimal_value(), 42)
        self.assertEqual(bus_8bit.width, 8)
        
        # Test con valor máximo
        bus_max = Bus(width=4, initial_value=15)
        print(f"✓ Bus máximo 4-bit: {bus_max}")
        self.assertEqual(bus_max.get_Decimal_value(), 15)
    
    def test_creacion_invalida(self):
        """Test: Creación de Buses con valores inválidos debe lanzar error"""
        print("Ejecutando test_creacion_invalida")
        
        # Ancho inválido
        with self.assertRaises(ValueError) as cm:
            Bus(width=0, initial_value=0)
        print(f"✓ Ancho 0: {cm.exception}")
        
        with self.assertRaises(ValueError) as cm:
            Bus(width=17, initial_value=0)
        print(f"✓ Ancho 17: {cm.exception}")
        
        # Valor inicial inválido
        with self.assertRaises(ValueError) as cm:
            Bus(width=4, initial_value=16)
        print(f"✓ Valor 16 en bus 4-bit: {cm.exception}")
        
        with self.assertRaises(ValueError) as cm:
            Bus(width=4, initial_value=-1)
        print(f"✓ Valor negativo: {cm.exception}")
    
    def test_set_binary_value_valido(self):
        """Test: set_Binary_value con valores válidos"""
        print("Ejecutando test_set_binary_value_valido")
        
        bus = Bus(width=8, initial_value=0)
        
        # Test con diferentes valores
        test_values = [0, 1, 42, 127, 255]
        for value in test_values:
            bus.set_Binary_value(value)
            actual_value = bus.get_Decimal_value()
            print(f"✓ Set {value} -> Get {actual_value}")
            self.assertEqual(actual_value, value)
    
    def test_set_binary_value_invalido(self):
        """Test: set_Binary_value con valores inválidos debe lanzar error"""
        print("Ejecutando test_set_binary_value_invalido")
        
        bus = Bus(width=4, initial_value=0)
        
        # Valores fuera de rango
        invalid_values = [-1, 16, 100, 255]
        for value in invalid_values:
            with self.assertRaises(ValueError) as cm:
                bus.set_Binary_value(value)
            print(f"✓ Valor {value} en bus 4-bit: {cm.exception}")
    
    def test_representaciones(self):
        """Test: Representaciones de string funcionan correctamente"""
        print("Ejecutando test_representaciones")
        
        bus = Bus(width=8, initial_value=170)  # 170 = 10101010
        
        binary = bus.get_Binary_value()
        decimal = bus.get_Decimal_value()
        hex_val = bus.get_Hexadecimal_value()
        str_repr = str(bus)
        
        print(f"✓ Binario: {binary}")
        print(f"✓ Decimal: {decimal}")
        print(f"✓ Hexadecimal: {hex_val}")
        print(f"✓ String: {str_repr}")
        
        self.assertEqual(binary, "10101010")
        self.assertEqual(decimal, 170)
        self.assertEqual(hex_val, "0xAA")
        self.assertEqual(str_repr, "Bus8(0xAA)")
    
    def test_get_lines_values(self):
        """Test: get_Lines_values devuelve mapa correcto"""
        print("Ejecutando test_get_lines_values")
        
        # Test con bus de 4 bits
        bus = Bus(width=4, initial_value=10)  # 10 = 1010
        
        lines_map = bus.get_Lines_values()
        print(f"✓ Mapa de líneas: {lines_map}")
        
        expected_map = {0: 1, 1: 0, 2: 1, 3: 0}
        self.assertEqual(lines_map, expected_map)
        
        # Verificar que los valores son correctos
        for i, bit in lines_map.items():
            self.assertIn(bit, [0, 1])
    
    def test_get_ordered_lines_values(self):
        """Test: get_Ordered_lines_values con diferentes órdenes"""
        print("Ejecutando test_get_ordered_lines_values")
        
        bus = Bus(width=4, initial_value=10)  # 10 = 1010
        
        # MSB first (por defecto)
        ordered_msb = bus.get_Ordered_lines_values(msb_first=True)
        print(f"✓ Orden MSB first: {ordered_msb}")
        self.assertEqual(ordered_msb, {0: 1, 1: 0, 2: 1, 3: 0})
        
        # LSB first
        ordered_lsb = bus.get_Ordered_lines_values(msb_first=False)
        print(f"✓ Orden LSB first: {ordered_lsb}")
        self.assertEqual(ordered_lsb, {3: 0, 2: 1, 1: 0, 0: 1})
    
    def test_len(self):
        """Test: __len__ funciona correctamente"""
        print("Ejecutando test_len")
        
        bus_4 = Bus(width=4, initial_value=5)
        bus_8 = Bus(width=8, initial_value=100)
        bus_16 = Bus(width=16, initial_value=255)
        
        print(f"✓ Bus 4-bit length: {len(bus_4)}")
        print(f"✓ Bus 8-bit length: {len(bus_8)}")
        print(f"✓ Bus 16-bit length: {len(bus_16)}")
        
        self.assertEqual(len(bus_4), 4)
        self.assertEqual(len(bus_8), 8)
        self.assertEqual(len(bus_16), 16)
    
    def test_encapsulamiento(self):
        """Test: los atributos internos están protegidos"""
        print("Ejecutando test_encapsulamiento")
        
        bus = Bus(width=4, initial_value=7)
        
        # Verificar que no se puede acceder directamente al atributo privado
        with self.assertRaises(AttributeError):
            _ = bus.__lines
        print("✓ Atributo __lines correctamente protegido")
    
    def test_comprehensive_bus_operations(self):
        """Test: Operaciones comprehensivas del bus"""
        print("Ejecutando test_comprehensive_bus_operations")
        
        # Crear bus y realizar múltiples operaciones
        bus = Bus(width=8, initial_value=0)
        
        # Secuencia de operaciones
        operations = [
            ("Inicial", 0),
            ("Set 85", 85),
            ("Set 170", 170),
            ("Set 255", 255),
            ("Reset a 0", 0)
        ]
        
        for desc, value in operations:
            if desc != "Inicial":
                bus.set_Binary_value(value)
            
            decimal = bus.get_Decimal_value()
            binary = bus.get_Binary_value()
            hex_val = bus.get_Hexadecimal_value()
            lines = bus.get_Lines_values()
            
            print(f"✓ {desc}: Decimal={decimal}, Binario={binary}, Hex={hex_val}")
            print(f"  Líneas: {lines}")
            
            self.assertEqual(decimal, value)

def run_tests():
    """Función para ejecutar tests con output detallado"""
    print("INICIANDO PRUEBAS COMPLETAS DE BUS")
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
    run_tests()