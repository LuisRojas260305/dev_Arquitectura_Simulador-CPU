# test_microcounter.py

import sys
sys.path.append('.')

from Business.CPU_Core.Control_Unit.MicroCounter import MicroCounter
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus

class TestMicroCounter:
    """Pruebas para el contador de microinstrucciones"""
    
    def __init__(self):
        self.counter = MicroCounter()
        self.test_count = 0
        self.passed_count = 0
    
    def run_all_tests(self):
        """Ejecuta todas las pruebas"""
        print("=" * 60)
        print("TESTING MICRO COUNTER")
        print("=" * 60)
        
        self.test_initial_state()
        self.test_increment()
        self.test_reset()
        self.test_load()
        self.test_priority()
        self.test_wrap_around()
        self.test_query_methods()
        
        self.print_summary()
        return self.passed_count == self.test_count
    
    def test_initial_state(self):
        """Prueba estado inicial"""
        print("\n🔰 1. Prueba Estado Inicial")
        print("-" * 40)
        
        # Valor inicial debe ser 0
        initial_value = self.counter.get_value_int()
        self.assert_test(
            "Valor inicial es 0",
            initial_value == 0,
            "0",
            str(initial_value)
        )
        
        # Debe estar en mínimo
        is_min = self.counter.is_min().get_value()
        self.assert_test(
            "is_min() retorna 1",
            is_min == 1,
            "1",
            str(is_min)
        )
    
    def test_increment(self):
        """Prueba incremento"""
        print("\n➕ 2. Prueba Incremento")
        print("-" * 40)
        
        # Incrementar una vez
        self.counter.set_increment(Bit(1))
        self.counter.clock_tick()
        self.counter.set_increment(Bit(0))
        
        value_after = self.counter.get_value_int()
        self.assert_test(
            "Incrementar de 0 a 1",
            value_after == 1,
            "1",
            str(value_after)
        )
        
        # Incrementar 4 veces más
        for _ in range(4):
            self.counter.set_increment(Bit(1))
            self.counter.clock_tick()
            self.counter.set_increment(Bit(0))
        
        value_after_5 = self.counter.get_value_int()
        self.assert_test(
            "Incrementar 5 veces total",
            value_after_5 == 5,
            "5",
            str(value_after_5)
        )
    
    def test_reset(self):
        """Prueba reset"""
        print("\n🔄 3. Prueba Reset")
        print("-" * 40)
        
        # Llevar a 7
        self.counter.load(7)
        value_before = self.counter.get_value_int()
        
        # Resetear
        self.counter.set_reset(Bit(1))
        self.counter.clock_tick()
        self.counter.set_reset(Bit(0))
        
        value_after = self.counter.get_value_int()
        
        self.assert_test(
            f"Reset desde {value_before}",
            value_after == 0,
            "0",
            str(value_after)
        )
    
    def test_load(self):
        """Prueba carga de valores"""
        print("\n📥 4. Prueba Carga de Valores")
        print("-" * 40)
        
        test_values = [3, 8, 12, 15]
        
        for test_val in test_values:
            # Cargar valor
            load_bus = Bus(4, test_val)
            self.counter.set_load_data(load_bus)
            self.counter.set_load(Bit(1))
            self.counter.clock_tick()
            self.counter.set_load(Bit(0))
            
            loaded_value = self.counter.get_value_int()
            self.assert_test(
                f"Cargar valor {test_val}",
                loaded_value == test_val,
                str(test_val),
                str(loaded_value)
            )
    
    def test_priority(self):
        """Prueba prioridad de señales"""
        print("\n🎯 5. Prueba Prioridad de Señales")
        print("-" * 40)
        
        # Situación: contador en 5, todas las señales activas
        # Prioridad: RESET > LOAD > INCREMENT
        
        self.counter.load(5)  # Cargar 5
        
        # Activar todas las señales
        self.counter.set_reset(Bit(1))
        self.counter.set_increment(Bit(1))
        self.counter.set_load(Bit(1))
        self.counter.set_load_data_int(10)
        
        self.counter.clock_tick()
        
        # Desactivar señales
        self.counter.set_reset(Bit(0))
        self.counter.set_increment(Bit(0))
        self.counter.set_load(Bit(0))
        
        # Debería resetear a 0 (RESET tiene prioridad)
        value = self.counter.get_value_int()
        self.assert_test(
            "RESET tiene prioridad sobre LOAD e INCREMENT",
            value == 0,
            "0 (reset)",
            str(value)
        )
        
        # Test 2: LOAD vs INCREMENT (sin RESET)
        self.counter.load(5)  # Volver a 5
        
        self.counter.set_increment(Bit(1))
        self.counter.set_load(Bit(1))
        self.counter.set_load_data_int(10)
        
        self.counter.clock_tick()
        
        self.counter.set_increment(Bit(0))
        self.counter.set_load(Bit(0))
        
        # Debería cargar 10 (LOAD tiene prioridad sobre INCREMENT)
        value = self.counter.get_value_int()
        self.assert_test(
            "LOAD tiene prioridad sobre INCREMENT",
            value == 10,
            "10 (load)",
            str(value)
        )
    
    def test_wrap_around(self):
        """Prueba wrap-around (15 → 0)"""
        print("\n🔄 6. Prueba Wrap-Around")
        print("-" * 40)
        
        # Cargar 15
        self.counter.load(15)
        
        # is_max() debe ser 1
        is_max_before = self.counter.is_max().get_value()
        self.assert_test(
            "is_max() en 15",
            is_max_before == 1,
            "1",
            str(is_max_before)
        )
        
        # Incrementar (debería ir a 0 por wrap-around)
        self.counter.set_increment(Bit(1))
        self.counter.clock_tick()
        self.counter.set_increment(Bit(0))
        
        value_after = self.counter.get_value_int()
        self.assert_test(
            "Wrap-around 15 → 0",
            value_after == 0,
            "0",
            str(value_after)
        )
        
        # Ahora is_min() debe ser 1
        is_min_after = self.counter.is_min().get_value()
        self.assert_test(
            "is_min() en 0",
            is_min_after == 1,
            "1",
            str(is_min_after)
        )
    
    def test_query_methods(self):
        """Prueba métodos de consulta"""
        print("\n📊 7. Prueba Métodos de Consulta")
        print("-" * 40)
        
        # Test is_equal_to
        self.counter.load(7)
        
        for test_val in [0, 7, 15]:
            is_equal = self.counter.is_equal_to(test_val).get_value()
            expected = 1 if test_val == 7 else 0
            
            self.assert_test(
                f"is_equal_to({test_val}) cuando valor=7",
                is_equal == expected,
                str(expected),
                str(is_equal)
            )
        
        # Test get_value_bus
        bus = self.counter.get_value_bus()
        self.assert_test(
            "get_value_bus() retorna Bus(4)",
            bus.width == 4 and isinstance(bus, Bus),
            "Bus(4)",
            f"Bus({bus.width})"
        )
        
        # Test get_value (Record)
        record = self.counter.get_value()
        self.assert_test(
            "get_value() retorna Record",
            hasattr(record, 'get_Dec_Value'),
            "Record",
            type(record).__name__
        )
    
    def assert_test(self, test_name, condition, expected, actual):
        """Método helper para assertions"""
        self.test_count += 1
        if condition:
            self.passed_count += 1
            print(f"  ✓ {test_name}: {expected} [OK]")
        else:
            print(f"  ✗ {test_name}")
            print(f"     Esperado: {expected}")
            print(f"     Obtenido: {actual}")
    
    def print_summary(self):
        """Imprime resumen de pruebas"""
        print("\n" + "=" * 60)
        print("RESUMEN DE PRUEBAS - MICRO COUNTER")
        print("=" * 60)
        
        failed = self.test_count - self.passed_count
        percentage = (self.passed_count / self.test_count * 100) if self.test_count > 0 else 0
        
        print(f"Pruebas ejecutadas: {self.test_count}")
        print(f"Pruebas pasadas:    {self.passed_count}")
        print(f"Pruebas falladas:   {failed}")
        print(f"Porcentaje éxito:   {percentage:.1f}%")
        
        if failed == 0:
            print("\n🎉 ¡MICRO COUNTER FUNCIONA CORRECTAMENTE!")
        else:
            print(f"\n⚠️  {failed} prueba(s) fallaron")
        
        return failed == 0

def test_visual_sequence():
    """Prueba visual de secuencia del contador"""
    print("\n👁️  PRUEBA VISUAL DE SECUENCIA")
    print("=" * 60)
    
    counter = MicroCounter()
    
    print("Secuencia: START → INC×3 → LOAD 10 → INC×2 → RESET → INC×1")
    print("-" * 60)
    
    print(f"Estado inicial: {counter.get_value_int()}")
    
    # Incrementar 3 veces
    for i in range(3):
        counter.increment()
        print(f"Incremento {i+1}: {counter.get_value_int()}")
    
    # Cargar 10
    counter.load(10)
    print(f"Load 10: {counter.get_value_int()}")
    
    # Incrementar 2 veces
    for i in range(2):
        counter.increment()
        print(f"Incremento {i+1}: {counter.get_value_int()}")
    
    # Reset
    counter.reset()
    print(f"Reset: {counter.get_value_int()}")
    
    # Incrementar 1 vez
    counter.increment()
    print(f"Incremento final: {counter.get_value_int()}")
    
    print("-" * 60)
    print("Secuencia completada correctamente! ✅")

if __name__ == "__main__":
    # Ejecutar pruebas automáticas
    tester = TestMicroCounter()
    success = tester.run_all_tests()
    
    # Mostrar prueba visual
    test_visual_sequence()
    
    # Código de salida para CI/CD
    sys.exit(0 if success else 1)