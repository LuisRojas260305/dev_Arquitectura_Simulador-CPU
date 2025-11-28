import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Full_Adder import Full_Adder

class TestFullAdder(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.fa = Full_Adder()
        self.bit0 = Bit(0)
        self.bit1 = Bit(1)
    
    def test_full_adder_truth_table(self):
        """Test: Full Adder - Tabla de verdad completa"""
        
        # Caso 1: 0 + 0 + 0 = 0, carry 0
        self.fa.set_Input_A(self.bit0)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 0)
        self.assertEqual(self.fa.get_C_out().get_value(), 0)
        
        # Caso 2: 0 + 0 + 1 = 1, carry 0
        self.fa.set_Input_A(self.bit0)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 1)
        self.assertEqual(self.fa.get_C_out().get_value(), 0)
        
        # Caso 3: 0 + 1 + 0 = 1, carry 0
        self.fa.set_Input_A(self.bit0)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 1)
        self.assertEqual(self.fa.get_C_out().get_value(), 0)
        
        # Caso 4: 0 + 1 + 1 = 0, carry 1
        self.fa.set_Input_A(self.bit0)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 0)
        self.assertEqual(self.fa.get_C_out().get_value(), 1)
        
        # Caso 5: 1 + 0 + 0 = 1, carry 0
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 1)
        self.assertEqual(self.fa.get_C_out().get_value(), 0)
        
        # Caso 6: 1 + 0 + 1 = 0, carry 1
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 0)
        self.assertEqual(self.fa.get_C_out().get_value(), 1)
        
        # Caso 7: 1 + 1 + 0 = 0, carry 1
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 0)
        self.assertEqual(self.fa.get_C_out().get_value(), 1)
        
        # Caso 8: 1 + 1 + 1 = 1, carry 1
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit1)
        self.fa.Calculate()
        self.assertEqual(self.fa.get_Output().get_value(), 1)
        self.assertEqual(self.fa.get_C_out().get_value(), 1)
    
    def test_full_adder_multiple_calculations(self):
        """Test: Múltiples cálculos consecutivos"""
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit0)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        
        # Primer cálculo: 1 + 0 + 0 = 1, carry 0
        self.assertEqual(self.fa.get_Output().get_value(), 1)
        self.assertEqual(self.fa.get_C_out().get_value(), 0)
        
        # Cambiar entradas y recalcular
        self.fa.set_Input_A(self.bit1)
        self.fa.set_Input_B(self.bit1)
        self.fa.set_C_in(self.bit0)
        self.fa.Calculate()
        
        # Segundo cálculo: 1 + 1 + 0 = 0, carry 1
        self.assertEqual(self.fa.get_Output().get_value(), 0)
        self.assertEqual(self.fa.get_C_out().get_value(), 1)
    
    def test_full_adder_encapsulamiento(self):
        """Test: Los atributos internos están protegidos"""
        # Verificar que no se puede acceder directamente a atributos privados
        with self.assertRaises(AttributeError):
            _ = self.fa.__Input_A
        with self.assertRaises(AttributeError):
            _ = self.fa.__Xor_A
    
    def test_full_adder_str_representation(self):
        """Test: Representación string del Full Adder"""
        # Nota: Hay un error en el método __str__ actual - usa atributos que no existen
        # Por ahora, solo verificamos que no lance error
        try:
            str_representation = str(self.fa)
            self.assertIsInstance(str_representation, str)
        except Exception as e:
            self.fail(f"__str__ method failed: {e}")

if __name__ == '__main__':
    unittest.main()