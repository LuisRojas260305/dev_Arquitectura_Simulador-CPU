#!/usr/bin/env python3
"""
Tests corregidos para SignalGenerator y FSM (con convenio índice 0 = MSB)
"""

import sys
sys.path.append('.')

from Business.CPU_Core.Control_Unit.SignalGenerator import SignalGenerator
from Business.CPU_Core.Control_Unit.FSM import FSM
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

class TestSignalGenerator:
    """Pruebas para SignalGenerator"""
    
    def __init__(self):
        self.signal_gen = SignalGenerator()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_all_tests(self):
        print("=" * 60)
        print("TESTING SIGNAL GENERATOR")
        print("=" * 60)
        
        self.test_initial_state()
        self.test_generate_signals()
        self.test_alu_signals()
        self.test_invalid_control_word()
        
        self.print_summary()
        return self.tests_failed == 0
    
    def test_initial_state(self):
        print("\n📍 1. Estado Inicial")
        print("-" * 40)
        
        all_signals = self.signal_gen.get_all_signals()
        all_zero = all(value == 0 for value in all_signals.values())
        
        self.assert_test(
            "Todas las señales inicializadas a 0",
            all_zero,
            "Todas en 0",
            "Alguna señal no está en 0"
        )
        
        active = self.signal_gen.get_active_signals()
        self.assert_test(
            "Ninguna señal activa inicialmente",
            len(active) == 0,
            "0 señales activas",
            f"{len(active)} señales activas"
        )
    
    def test_generate_signals(self):
        print("\n🔧 2. Generación de Señales")
        print("-" * 40)
        
        control_word = Bus(32, 0)
        
        # Activar HALT (bit 28), MEM_READ (bit 16), AC_LOAD (bit 8)
        control_word.set_Line_bit(28, Bit(1))
        control_word.set_Line_bit(16, Bit(1))
        control_word.set_Line_bit(8, Bit(1))
        
        self.signal_gen.generate(control_word)
        
        self.assert_test(
            "HALT activado",
            self.signal_gen.get_signal_value('HALT') == 1,
            "1",
            str(self.signal_gen.get_signal_value('HALT'))
        )
        
        self.assert_test(
            "MEM_READ activado",
            self.signal_gen.get_signal_value('MEM_READ') == 1,
            "1",
            str(self.signal_gen.get_signal_value('MEM_READ'))
        )
        
        self.assert_test(
            "AC_LOAD activado",
            self.signal_gen.get_signal_value('AC_LOAD') == 1,
            "1",
            str(self.signal_gen.get_signal_value('AC_LOAD'))
        )
        
        # Verificar lista de señales activas
        active = self.signal_gen.get_active_signals()
        expected_active = {'HALT', 'MEM_READ', 'AC_LOAD'}
        actual_active = set(active)
        
        self.assert_test(
            "Señales activas correctas",
            actual_active == expected_active,
            str(expected_active),
            str(actual_active)
        )
    
    def test_alu_signals(self):
        print("\n🧮 3. Señales ALU")
        print("-" * 40)
        
        # IMPORTANTE: Recordar convenio índice 0 = MSB
        # Para ALUop = 2 (10 binario): ALUop1=1 (MSB), ALUop0=0 (LSB)
        # Para ALUfunc = 5 (101 binario): ALUfunc2=1 (MSB), ALUfunc1=0, ALUfunc0=1 (LSB)
        
        control_word = Bus(32, 0)
        
        # Configurar bits según mapeo de SignalGenerator
        # bit 0: ALUop0 (LSB) -> 0
        # bit 1: ALUop1 (MSB) -> 1
        # bit 2: ALUfunc0 (LSB) -> 1
        # bit 3: ALUfunc1 -> 0
        # bit 4: ALUfunc2 (MSB) -> 1
        
        control_word.set_Line_bit(1, Bit(1))  # ALUop1 (MSB) = 1
        control_word.set_Line_bit(0, Bit(0))  # ALUop0 (LSB) = 0
        
        control_word.set_Line_bit(4, Bit(1))  # ALUfunc2 (MSB) = 1
        control_word.set_Line_bit(3, Bit(0))  # ALUfunc1 = 0
        control_word.set_Line_bit(2, Bit(1))  # ALUfunc0 (LSB) = 1
        
        self.signal_gen.generate(control_word)
        
        # Verificar buses ALU
        aluop_bus = self.signal_gen.get_aluop()
        alufunc_bus = self.signal_gen.get_alufunc()
        
        print(f"  Debug: ALUop bus binario = {aluop_bus.get_Binary_value()}")
        print(f"  Debug: ALUfunc bus binario = {alufunc_bus.get_Binary_value()}")
        
        # ALUop debe ser 2 (10 binario con MSB en índice 0)
        self.assert_test(
            "ALUop = 2 (10 binario)",
            aluop_bus.get_Decimal_value() == 2,
            "2",
            str(aluop_bus.get_Decimal_value())
        )
        
        # ALUfunc debe ser 5 (101 binario con MSB en índice 0)
        self.assert_test(
            "ALUfunc = 5 (101 binario)",
            alufunc_bus.get_Decimal_value() == 5,
            "5",
            str(alufunc_bus.get_Decimal_value())
        )
    
    def test_invalid_control_word(self):
        print("\n⚠️ 4. Palabra de Control Inválida")
        print("-" * 40)
        
        invalid_bus = Bus(16, 0)
        try:
            self.signal_gen.generate(invalid_bus)
            self.assert_test("Control word de 16 bits", False, "ValueError", "No error")
        except ValueError as e:
            self.assert_test(
                "ValueError para tamaño incorrecto",
                "32 bits" in str(e),
                "Mensaje apropiado",
                str(e)
            )
    
    def assert_test(self, description, condition, expected, actual):
        if condition:
            self.tests_passed += 1
            print(f"  ✓ {description}")
        else:
            self.tests_failed += 1
            print(f"  ✗ {description}")
            print(f"     Esperado: {expected}")
            print(f"     Obtenido: {actual}")
    
    def print_summary(self):
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("RESUMEN SIGNAL GENERATOR")
        print("=" * 60)
        print(f"Pruebas pasadas: {self.tests_passed}/{total}")
        print(f"Pruebas falladas: {self.tests_failed}/{total}")
        print(f"Porcentaje éxito: {percentage:.1f}%")
        
        if self.tests_failed == 0:
            print("✅ ¡SIGNAL GENERATOR FUNCIONA CORRECTAMENTE!")
        else:
            print(f"❌ {self.tests_failed} prueba(s) fallaron")


class TestFSM:
    """Pruebas para FSM"""
    
    def __init__(self):
        self.fsm = FSM()
        self.tests_passed = 0
        self.tests_failed = 0
    
    def run_all_tests(self):
        print("\n" + "=" * 60)
        print("TESTING FSM (FINITE STATE MACHINE)")
        print("=" * 60)
        
        self.test_initial_state()
        self.test_multiplication_flow()
        self.test_division_flow()
        self.test_error_handling()
        self.test_reset_functionality()
        
        self.print_summary()
        return self.tests_failed == 0
    
    def test_initial_state(self):
        print("\n📍 1. Estado Inicial")
        print("-" * 40)
        
        self.assert_test(
            "Estado inicial es IDLE (0)",
            self.fsm.get_state() == 0,
            "0",
            str(self.fsm.get_state())
        )
        
        self.assert_test(
            "is_idle() retorna True",
            self.fsm.is_idle(),
            "True",
            str(self.fsm.is_idle())
        )
    
    def test_multiplication_flow(self):
        print("\n➗ 2. Flujo de Multiplicación")
        print("-" * 40)
        
        self.fsm.set_start_mult(Bit(1))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición IDLE → MULT_INIT (1)",
            self.fsm.get_state() == 1,
            "1",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_start_mult(Bit(0))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición MULT_INIT → MULT_CYCLE (2)",
            self.fsm.get_state() == 2,
            "2",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_md_done(Bit(1))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición MULT_CYCLE → IDLE al completar",
            self.fsm.get_state() == 0,
            "0",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_md_done(Bit(0))
    
    def test_division_flow(self):
        print("\n✖️ 3. Flujo de División (sin error)")
        print("-" * 40)
        
        self.fsm.set_reset(Bit(1))
        self.fsm.update_state()
        self.fsm.set_reset(Bit(0))
        
        self.fsm.set_start_div(Bit(1))
        self.fsm.set_div_zero(Bit(0))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición IDLE → DIV_INIT (3)",
            self.fsm.get_state() == 3,
            "3",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_start_div(Bit(0))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición DIV_INIT → DIV_CYCLE (4)",
            self.fsm.get_state() == 4,
            "4",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_md_done(Bit(1))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición DIV_CYCLE → IDLE al completar",
            self.fsm.get_state() == 0,
            "0",
            str(self.fsm.get_state())
        )
        
        self.fsm.set_md_done(Bit(0))
    
    def test_error_handling(self):
        print("\n⚠️ 4. Manejo de Errores (división por cero)")
        print("-" * 40)
        
        self.fsm.set_reset(Bit(1))
        self.fsm.update_state()
        self.fsm.set_reset(Bit(0))
        
        # Activar start_div y div_zero simultáneamente
        self.fsm.set_start_div(Bit(1))
        self.fsm.set_div_zero(Bit(1))
        self.fsm.update_state()
        
        self.assert_test(
            "Transición directa a ERROR (5) por división por cero",
            self.fsm.get_state() == 5,
            "5",
            str(self.fsm.get_state())
        )
        
        self.assert_test(
            "md_error activado en estado ERROR",
            self.fsm.get_md_error().get_value() == 1,
            "1",
            str(self.fsm.get_md_error().get_value())
        )
        
        # Desactivar señales y verificar que se mantiene en ERROR
        self.fsm.set_start_div(Bit(0))
        self.fsm.set_div_zero(Bit(0))
        self.fsm.update_state()
        
        self.assert_test(
            "Se mantiene en estado ERROR",
            self.fsm.get_state() == 5,
            "5",
            str(self.fsm.get_state())
        )
    
    def test_reset_functionality(self):
        print("\n🔄 5. Funcionalidad de Reset")
        print("-" * 40)
        
        # Poner en estado ERROR
        self.fsm.set_start_div(Bit(1))
        self.fsm.set_div_zero(Bit(1))
        self.fsm.update_state()
        
        # Aplicar reset
        self.fsm.set_reset(Bit(1))
        self.fsm.update_state()
        
        self.assert_test(
            "Reset desde ERROR a IDLE",
            self.fsm.get_state() == 0,
            "0",
            str(self.fsm.get_state())
        )
        
        self.assert_test(
            "md_error desactivado después de reset",
            self.fsm.get_md_error().get_value() == 0,
            "0",
            str(self.fsm.get_md_error().get_value())
        )
    
    def assert_test(self, description, condition, expected, actual):
        if condition:
            self.tests_passed += 1
            print(f"  ✓ {description}")
        else:
            self.tests_failed += 1
            print(f"  ✗ {description}")
            print(f"     Esperado: {expected}")
            print(f"     Obtenido: {actual}")
    
    def print_summary(self):
        total = self.tests_passed + self.tests_failed
        percentage = (self.tests_passed / total * 100) if total > 0 else 0
        
        print("\n" + "=" * 60)
        print("RESUMEN FSM")
        print("=" * 60)
        print(f"Pruebas pasadas: {self.tests_passed}/{total}")
        print(f"Pruebas falladas: {self.tests_failed}/{total}")
        print(f"Porcentaje éxito: {percentage:.1f}%")
        
        if self.tests_failed == 0:
            print("✅ ¡FSM FUNCIONA CORRECTAMENTE!")
        else:
            print(f"❌ {self.tests_failed} prueba(s) fallaron")


def main():
    print("=" * 80)
    print("SISTEMA DE PRUEBAS - COMPONENTES DE CONTROL (CONVENIO ÍNDICE 0 = MSB)")
    print("=" * 80)
    
    signal_tester = TestSignalGenerator()
    fsm_tester = TestFSM()
    
    signal_success = signal_tester.run_all_tests()
    fsm_success = fsm_tester.run_all_tests()
    
    print("\n" + "=" * 80)
    print("RESUMEN FINAL")
    print("=" * 80)
    
    if signal_success and fsm_success:
        print("🎉 ¡TODOS LOS COMPONENTES FUNCIONAN CORRECTAMENTE!")
        return 0
    else:
        print("⚠️  ALGUNOS COMPONENTES TIENEN PROBLEMAS")
        return 1


if __name__ == "__main__":
    sys.exit(main())