import unittest
import sys
import os

# Ajuste de path para importar Business
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bus import Bus
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.LSL import LSL  # Asegúrate de la ruta correcta
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.LSR import LSR  # Asegúrate de la ruta correcta

class TestBarrelShifter(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial: Instanciar motores y buses auxiliares"""
        print("\n" + "="*60)
        print("Configurando test de Barrel Shifter...")
        
        self.lsl = LSL()
        self.lsr = LSR()
        
        # Buses reusables
        self.data_bus = Bus(width=16)
        self.shift_bus = Bus(width=16)
        
    def tearDown(self):
        print("Test de Shifter completado")
        print("="*60)

    # =================================================================
    # PRUEBAS LSL (Desplazamiento Lógico a la Izquierda)
    # =================================================================

    def test_LSL_shift_1(self):
        """Test LSL: Desplazar 1 bit a la izquierda"""
        print("Ejecutando test_LSL_shift_1")
        
        # Entrada: 0000 0000 0000 0001 (0x0001)
        self.data_bus.set_Binary_value(1) 
        # Shift: 1
        self.shift_bus.set_Binary_value(1)
        
        self.lsl.set_Input_A(self.data_bus)
        self.lsl.set_Input_B(self.shift_bus)
        
        result_bus = self.lsl.Calculate()
        result_val = result_bus.get_Decimal_value()
        
        print(f"✓ LSL Entrada: {self.data_bus.get_Hexadecimal_value()} << 1")
        print(f"✓ Resultado:   {result_bus.get_Hexadecimal_value()}")
        
        # 1 << 1 = 2 (0x0002)
        self.assertEqual(result_val, 2)

    def test_LSL_padding(self):
        """Test LSL: Verificar relleno de ceros por la derecha"""
        print("Ejecutando test_LSL_padding")
        
        # Entrada: 1111 1111 1111 1111 (0xFFFF) - Todos unos para ver el relleno
        self.data_bus.set_Binary_value(0xFFFF)
        # Shift: 4
        self.shift_bus.set_Binary_value(4)
        
        self.lsl.set_Input_A(self.data_bus)
        self.lsl.set_Input_B(self.shift_bus)
        
        result_bus = self.lsl.Calculate()
        
        # Esperado: 1111 1111 1111 0000 (0xFFF0)
        expected = 0xFFF0
        
        print(f"✓ LSL Entrada: {self.data_bus.get_Hexadecimal_value()} << 4")
        print(f"✓ Obtenido:    {result_bus.get_Hexadecimal_value()}")
        print(f"✓ Esperado:    0xFFF0")
        
        self.assertEqual(result_bus.get_Decimal_value(), expected)

    def test_LSL_overflow(self):
        """Test LSL: Bits que salen por la izquierda se pierden"""
        print("Ejecutando test_LSL_overflow")
        
        # Entrada: 1000 ... 0000 (0x8000) - El bit más significativo activo
        self.data_bus.set_Binary_value(0x8000)
        # Shift: 1
        self.shift_bus.set_Binary_value(1)
        
        self.lsl.set_Input_A(self.data_bus)
        self.lsl.set_Input_B(self.shift_bus)
        
        result_bus = self.lsl.Calculate()
        
        # Esperado: 0x0000 (El 1 se cayó del bus)
        print(f"✓ LSL Entrada: {self.data_bus.get_Hexadecimal_value()} << 1")
        print(f"✓ Resultado:   {result_bus.get_Hexadecimal_value()}")
        
        self.assertEqual(result_bus.get_Decimal_value(), 0)

    # =================================================================
    # PRUEBAS LSR (Desplazamiento Lógico a la Derecha)
    # =================================================================

    def test_LSR_shift_1(self):
        """Test LSR: Desplazar 1 bit a la derecha"""
        print("Ejecutando test_LSR_shift_1")
        
        # Entrada: 0000 ... 0010 (2)
        self.data_bus.set_Binary_value(2)
        # Shift: 1
        self.shift_bus.set_Binary_value(1)
        
        self.lsr.set_Input_A(self.data_bus)
        self.lsr.set_Input_B(self.shift_bus)
        
        result_bus = self.lsr.Calculate()
        
        # 2 >> 1 = 1
        print(f"✓ LSR Entrada: {self.data_bus.get_Hexadecimal_value()} >> 1")
        print(f"✓ Resultado:   {result_bus.get_Hexadecimal_value()}")
        
        self.assertEqual(result_bus.get_Decimal_value(), 1)

    def test_LSR_padding(self):
        """Test LSR: Verificar relleno de ceros por la izquierda (MSB)"""
        print("Ejecutando test_LSR_padding")
        
        # Entrada: 1111 1111 1111 1111 (0xFFFF)
        self.data_bus.set_Binary_value(0xFFFF)
        # Shift: 8
        self.shift_bus.set_Binary_value(8)
        
        self.lsr.set_Input_A(self.data_bus)
        self.lsr.set_Input_B(self.shift_bus)
        
        result_bus = self.lsr.Calculate()
        
        # Esperado: 0000 0000 1111 1111 (0x00FF)
        expected = 0x00FF
        
        print(f"✓ LSR Entrada: {self.data_bus.get_Hexadecimal_value()} >> 8")
        print(f"✓ Obtenido:    {result_bus.get_Hexadecimal_value()}")
        print(f"✓ Esperado:    0x00FF")
        
        self.assertEqual(result_bus.get_Decimal_value(), expected)

    def test_max_shift(self):
        """Test: Desplazamiento máximo (15)"""
        print("Ejecutando test_max_shift")
        
        # 0xFFFF
        self.data_bus.set_Binary_value(0xFFFF)
        # Shift: 15 (0x000F) - 1111 en binario para shift bus
        self.shift_bus.set_Binary_value(15)
        
        # Test LSR 15
        self.lsr.set_Input_A(self.data_bus)
        self.lsr.set_Input_B(self.shift_bus)
        res_lsr = self.lsr.Calculate()
        
        # Esperado LSR: 0000...0001 (0x0001)
        self.assertEqual(res_lsr.get_Decimal_value(), 1)
        print("✓ LSR 15 OK")

        # Test LSL 15
        self.lsl.set_Input_A(self.data_bus)
        self.lsl.set_Input_B(self.shift_bus)
        res_lsl = self.lsl.Calculate()
        
        # Esperado LSL: 1000...0000 (0x8000)
        self.assertEqual(res_lsl.get_Decimal_value(), 0x8000)
        print("✓ LSL 15 OK")

def run_shifter_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestBarrelShifter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    run_shifter_tests()