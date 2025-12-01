import unittest
import sys
import os

# Ajuste de path para importar Business (asumiendo tu estructura de carpetas)
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.LSL import LSL 
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.LSR import LSR
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.ASR import ASR 
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.ROL import ROL 
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.ROR import ROR 

class TestFullBarrelShifter(unittest.TestCase):
    
    def setUp(self):
        print("\n" + "="*70)
        print("Configurando Test Suite Completo de Barrel Shifter...")
        self.lsl = LSL()
        self.lsr = LSR()
        self.asr = ASR()
        self.rol = ROL()
        self.ror = ROR()
        
        self.data_bus = Bus(width=16)
        self.shift_bus = Bus(width=16)

    # --- Funciones Auxiliares para ejecutar y reportar ---
    def _execute_test(self, shifter_instance, data_hex, shift_amount, expected_hex, operation_name):
        self.data_bus.set_Binary_value(int(data_hex, 16)) 
        
        self.shift_bus.set_Binary_value(shift_amount)
        
        shifter_instance.set_Input_A(self.data_bus)
        
        shifter_instance.set_Input_A(self.data_bus)
        shifter_instance.set_Input_B(self.shift_bus)
        result_bus = shifter_instance.Calculate()
        result_hex = result_bus.get_Hexadecimal_value()
        
        expected_hex = expected_hex.upper().replace('0X', '')
        result_hex_cleaned = result_hex.upper().replace('0X', '')
        
        print(f"[{operation_name}] {data_hex} {operation_name.replace('L', '<<').replace('R', '>>')} {shift_amount} -> Obtenido: {result_hex} | Esperado: 0x{expected_hex}")
        self.assertEqual(result_hex_cleaned, expected_hex)


    # =================================================================
    # PRUEBAS LSL y LSR (ya existentes, pero consolidadas)
    # =================================================================

    def test_01_LSL_basic(self):
        self._execute_test(self.lsl, "0x0001", 1, "0x0002", "LSL")

    def test_02_LSR_padding_and_loss(self):
        # 0xFFFF >> 8 = 0x00FF (0s por la izquierda, 1s por la derecha se pierden)
        self._execute_test(self.lsr, "0xFFFF", 8, "0x00FF", "LSR")

    # =================================================================
    # PRUEBAS ASR (ARITHMETIC SHIFT RIGHT)
    # =================================================================

    def test_03_ASR_positive(self):
        """ASR en positivo debe ser igual a LSR."""
        # 0x0100 (256) >> 1 = 0x0080 (128)
        self._execute_test(self.asr, "0x0100", 1, "0x0080", "ASR_Pos")

    def test_04_ASR_negative_shift_1(self):
        """ASR en negativo: -32768 (0x8000) >> 1 = -16384 (0xC000). Relleno con '1'."""
        # 1000 0000 0000 0000 >> 1 -> 1100 0000 0000 0000
        self._execute_test(self.asr, "0x8000", 1, "0xC000", "ASR_Neg_1")

    def test_05_ASR_negative_shift_4(self):
        """ASR en negativo con más relleno."""
        # 1111 0000 0000 0000 (0xF000, -4096) >> 4 -> 1111 1111 0000 0000 (0xFF00, -256)
        self._execute_test(self.asr, "0xF000", 4, "0xFF00", "ASR_Neg_4")

    # =================================================================
    # PRUEBAS ROL (ROTATE LEFT)
    # =================================================================

    def test_06_ROL_shift_1(self):
        """ROL 1: El MSB (0x8000) se mueve al LSB (0x0001)."""
        # 1000 0000 0000 0000 (0x8000) ROL 1 -> 0000 0000 0000 0001 (0x0001)
        self._execute_test(self.rol, "0x8000", 1, "0x0001", "ROL")

    def test_07_ROL_shift_4(self):
        """ROL 4: 4 bits se mueven y regresan."""
        # 0x1234 (0001 0010 0011 0100) ROL 4 -> 0010 0011 0100 0001 (0x2341)
        self._execute_test(self.rol, "0x1234", 4, "0x2341", "ROL")

    # =================================================================
    # PRUEBAS ROR (ROTATE RIGHT)
    # =================================================================

    def test_08_ROR_shift_1(self):
        """ROR 1: El LSB (0x0001) se mueve al MSB (0x8000)."""
        # 0000 0000 0000 0001 (0x0001) ROR 1 -> 1000 0000 0000 0000 (0x8000)
        self._execute_test(self.ror, "0x0001", 1, "0x8000", "ROR")

    def test_09_ROR_shift_4(self):
        """ROR 4: 4 bits se mueven y regresan."""
        # 0x1234 (0001 0010 0011 0100) ROR 4 -> 0100 0001 0010 0011 (0x4123)
        self._execute_test(self.ror, "0x1234", 4, "0x4123", "ROR")

    def test_10_ROL_full_rotation(self):
        """Verificar que ROL 16 devuelve el mismo número."""
        self._execute_test(self.rol, "0xABCD", 16, "0xABCD", "ROL")

    def test_11_ROR_full_rotation(self):
        """Verificar que ROR 16 devuelve el mismo número."""
        self._execute_test(self.ror, "0xABCD", 16, "0xABCD", "ROR")


def run_full_shifter_tests():
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFullBarrelShifter)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    # Para ejecutar: asegúrate de que tus clases están en el path correcto (ej. Business.CPU_Core)
    run_full_shifter_tests()