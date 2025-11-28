import unittest
import sys
import os

# Configurar path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit

class TestBit(unittest.TestCase):
    
    def test_creacion_valida(self):
        """Test: Creación de Bits con valores válidos"""
        bit0 = Bit(0)
        bit1 = Bit(1)
        
        self.assertEqual(bit0.get_value(), 0)
        self.assertEqual(bit1.get_value(), 1)
    
    def test_creacion_invalida(self):
        """Test: Creación de Bits con valores inválidos debe lanzar error"""
        with self.assertRaises(ValueError):
            Bit(2)
        with self.assertRaises(ValueError):
            Bit(-1)
        with self.assertRaises(ValueError):
            Bit(10)
    
    def test_set_value_valido(self):
        """Test: set_value con valores válidos"""
        bit = Bit(0)
        bit.set_value(1)
        self.assertEqual(bit.get_value(), 1)
        
        bit.set_value(0)
        self.assertEqual(bit.get_value(), 0)
    
    def test_set_value_invalido(self):
        """Test: set_value con valores inválidos debe lanzar error"""
        bit = Bit(0)
        
        with self.assertRaises(ValueError):
            bit.set_value(2)
        with self.assertRaises(ValueError):
            bit.set_value(-5)
        with self.assertRaises(ValueError):
            bit.set_value(100)
    
    def test_toggle(self):
        """Test: toggle cambia correctamente el valor"""
        bit0 = Bit(0)
        bit1 = Bit(1)
        
        bit0.toggle()
        self.assertEqual(bit0.get_value(), 1)
        
        bit1.toggle()
        self.assertEqual(bit1.get_value(), 0)
        
        # Toggle múltiple
        bit0.toggle()
        bit0.toggle()
        self.assertEqual(bit0.get_value(), 1)
    
    def test_representaciones(self):
        """Test: __str__ y __repr__ funcionan correctamente"""
        bit = Bit(1)
        
        self.assertEqual(str(bit), "Bit: 1")
        self.assertEqual(repr(bit), "Bit(1)")
    
    def test_igualdad(self):
        """Test: comparación entre Bits"""
        bit1a = Bit(1)
        bit1b = Bit(1)
        bit0 = Bit(0)
        
        self.assertEqual(bit1a, bit1b)
        self.assertNotEqual(bit1a, bit0)
        self.assertNotEqual(bit1a, "no es un bit")  # Comparación con tipo diferente
    
    def test_encapsulamiento(self):
        """Test: los atributos internos están protegidos"""
        bit = Bit(1)
        
        # Verificar que no se puede acceder directamente al atributo privado
        with self.assertRaises(AttributeError):
            _ = bit.__value

if __name__ == '__main__':
    unittest.main()