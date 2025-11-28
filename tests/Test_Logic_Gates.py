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
        self.bit0 = Bit(0)
        self.bit1 = Bit(1)
    
    def test_and_gate_truth_table(self):
        """Test: AND Gate - Tabla de verdad completa"""
        and_gate = AND_Gate()
        
        # 0 AND 0 = 0
        and_gate.connect_input(self.bit0, 0)
        and_gate.connect_input(self.bit0, 1)
        result = and_gate.calculate()
        self.assertEqual(result.get_value(), 0)
        
        # 0 AND 1 = 0
        and_gate.connect_input(self.bit0, 0)
        and_gate.connect_input(self.bit1, 1)
        result = and_gate.calculate()
        self.assertEqual(result.get_value(), 0)
        
        # 1 AND 0 = 0
        and_gate.connect_input(self.bit1, 0)
        and_gate.connect_input(self.bit0, 1)
        result = and_gate.calculate()
        self.assertEqual(result.get_value(), 0)
        
        # 1 AND 1 = 1
        and_gate.connect_input(self.bit1, 0)
        and_gate.connect_input(self.bit1, 1)
        result = and_gate.calculate()
        self.assertEqual(result.get_value(), 1)
    
    def test_or_gate_truth_table(self):
        """Test: OR Gate - Tabla de verdad completa"""
        or_gate = OR_Gate()
        
        # 0 OR 0 = 0
        or_gate.connect_input(self.bit0, 0)
        or_gate.connect_input(self.bit0, 1)
        result = or_gate.calculate()
        self.assertEqual(result.get_value(), 0)
        
        # 0 OR 1 = 1
        or_gate.connect_input(self.bit0, 0)
        or_gate.connect_input(self.bit1, 1)
        result = or_gate.calculate()
        self.assertEqual(result.get_value(), 1)
        
        # 1 OR 0 = 1
        or_gate.connect_input(self.bit1, 0)
        or_gate.connect_input(self.bit0, 1)
        result = or_gate.calculate()
        self.assertEqual(result.get_value(), 1)
        
        # 1 OR 1 = 1
        or_gate.connect_input(self.bit1, 0)
        or_gate.connect_input(self.bit1, 1)
        result = or_gate.calculate()
        self.assertEqual(result.get_value(), 1)
    
    def test_xor_gate_truth_table(self):
        """Test: XOR Gate - Tabla de verdad completa"""
        xor_gate = XOR_Gate()
        
        # 0 XOR 0 = 0
        xor_gate.connect_input(self.bit0, 0)
        xor_gate.connect_input(self.bit0, 1)
        result = xor_gate.calculate()
        self.assertEqual(result.get_value(), 0)
        
        # 0 XOR 1 = 1
        xor_gate.connect_input(self.bit0, 0)
        xor_gate.connect_input(self.bit1, 1)
        result = xor_gate.calculate()
        self.assertEqual(result.get_value(), 1)
        
        # 1 XOR 0 = 1
        xor_gate.connect_input(self.bit1, 0)
        xor_gate.connect_input(self.bit0, 1)
        result = xor_gate.calculate()
        self.assertEqual(result.get_value(), 1)
        
        # 1 XOR 1 = 0
        xor_gate.connect_input(self.bit1, 0)
        xor_gate.connect_input(self.bit1, 1)
        result = xor_gate.calculate()
        self.assertEqual(result.get_value(), 0)
    
    def test_not_gate_truth_table(self):
        """Test: NOT Gate - Tabla de verdad completa"""
        not_gate = NOT_Gate()
        
        # NOT 0 = 1
        not_gate.connect_input(self.bit0, 0)
        result = not_gate.calculate()
        self.assertEqual(result.get_value(), 1)
        
        # NOT 1 = 0
        not_gate.connect_input(self.bit1, 0)
        result = not_gate.calculate()
        self.assertEqual(result.get_value(), 0)
    
    def test_conexiones_invalidas(self):
        """Test: Manejo de conexiones inválidas"""
        and_gate = AND_Gate()  # 2 entradas por defecto
        
        # Índice fuera de rango
        with self.assertRaises(ValueError):
            and_gate.connect_input(self.bit0, 5)
        
        with self.assertRaises(ValueError):
            and_gate.connect_input(self.bit0, -1)
    
    def test_entradas_no_conectadas(self):
        """Test: Comportamiento con entradas no conectadas"""
        and_gate = AND_Gate()
        
        # Sin conectar entradas - debería manejarse gracefuly
        result = and_gate.calculate()
        self.assertEqual(result.get_value(), 0)  # Valor por defecto
    
    def test_encapsulamiento_estricto(self):
        """Test: Verificar que los atributos privados no son accesibles"""
        and_gate = AND_Gate()
        
        # Verificar que NO se puede acceder directamente a atributos privados
        with self.assertRaises(AttributeError):
            _ = and_gate.__inputs
        with self.assertRaises(AttributeError):
            _ = and_gate.__output
        with self.assertRaises(AttributeError):
            _ = and_gate.__n_inputs
        
        # Verificar que los métodos públicos funcionan correctamente
        and_gate.connect_input(self.bit1, 0)
        and_gate.connect_input(self.bit1, 1)
        result = and_gate.calculate()
        
        self.assertEqual(result.get_value(), 1)
        self.assertIsNotNone(and_gate.get_output())

if __name__ == '__main__':
    unittest.main()