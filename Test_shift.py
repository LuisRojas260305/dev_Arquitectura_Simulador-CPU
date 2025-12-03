import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.Shift_Unit import Shift_Unit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.Multiplex import Multiplex
from Business.CPU_Core.Arithmetic_Logical_Unit.ALU import ALU

def test_correct_mapping():
    """Verifica que el mapeo del multiplexor sea correcto"""
    print("=== VERIFICACIÓN DE MAPEO CORRECTO ===")
    
    mux = Multiplex()
    
    # Valores únicos para cada operación
    test_values = {
        "LSL": 0x1111,
        "ASR": 0x2222,
        "ROL": 0x3333,
        "ROR": 0x4444,
        "LSR": 0x5555
    }
    
    # Configurar multiplexor
    bus_lsl = Bus(16); bus_lsl.set_Binary_value(test_values["LSL"])
    bus_asr = Bus(16); bus_asr.set_Binary_value(test_values["ASR"])
    bus_rol = Bus(16); bus_rol.set_Binary_value(test_values["ROL"])
    bus_ror = Bus(16); bus_ror.set_Binary_value(test_values["ROR"])
    bus_lsr = Bus(16); bus_lsr.set_Binary_value(test_values["LSR"])
    
    mux.set_input_LSL(bus_lsl)
    mux.set_input_ASR(bus_asr)
    mux.set_input_ROL(bus_rol)
    mux.set_input_ROR(bus_ror)
    mux.set_input_LSR(bus_lsr)
    
    print("Valores de entrada:")
    for name, val in test_values.items():
        print(f"  {name}: 0x{val:04X}")
    
    print("\nProbando cada código de operación:")
    
    # Mapeo esperado según la especificación
    expected_mapping = {
        0b000: ("LSL", 0x1111),
        0b001: ("ASR", 0x2222),
        0b010: ("ROL", 0x3333),
        0b011: ("ROR", 0x4444),
        0b100: ("LSR", 0x5555),
    }
    
    all_correct = True
    for code in range(8):
        select_bus = Bus(3)
        select_bus.set_Binary_value(code)
        
        mux.set_select(select_bus)
        mux.calculate()
        result = mux.get_output()
        actual = result.get_Decimal_value()
        
        if code in expected_mapping:
            expected_name, expected_val = expected_mapping[code]
            if actual == expected_val:
                print(f"  ✓ {code:03b} ({code}) -> {expected_name}: 0x{actual:04X}")
            else:
                print(f"  ✗ {code:03b} ({code}) -> Esperado {expected_name}: 0x{expected_val:04X}, "
                      f"Obtenido: 0x{actual:04X}")
                all_correct = False
        else:
            # Códigos no definidos deberían dar 0
            if actual == 0:
                print(f"  ✓ {code:03b} ({code}) -> No definido: 0x0000")
            else:
                print(f"  ✗ {code:03b} ({code}) -> Esperado 0x0000, Obtenido: 0x{actual:04X}")
                all_correct = False
    
    return all_correct

def test_shift_unit_corrected():
    """Prueba Shift_Unit con el mapeo corregido"""
    print("\n=== PRUEBA DE SHIFT_UNIT (MApeo Corregido) ===")
    
    su = Shift_Unit()
    
    test_cases = [
        # (operación, valor_a, valor_b_control, valor_esperado, descripción)
        # LSL (000)
        (0b000, 0x0001, 0x0001, 0x0002, "LSL: 0x0001 << 1 = 0x0002"),
        (0b000, 0x0001, 0x0004, 0x0010, "LSL: 0x0001 << 4 = 0x0010"),
        (0b000, 0x1234, 0x0001, 0x2468, "LSL: 0x1234 << 1 = 0x2468"),
        (0b000, 0xAAAA, 0x0001, 0x5554, "LSL: 0xAAAA << 1 = 0x5554"),
        
        # ASR (001) 
        (0b001, 0x8000, 0x0001, 0xC000, "ASR: 0x8000 >> 1 = 0xC000"),
        (0b001, 0x4000, 0x0001, 0x2000, "ASR: 0x4000 >> 1 = 0x2000"),
        (0b001, 0x0001, 0x0001, 0x0000, "ASR: 0x0001 >> 1 = 0x0000"),
        
        # ROL (010)
        (0b010, 0x8000, 0x0001, 0x0001, "ROL: 0x8000 << 1 = 0x0001"),
        (0b010, 0x0001, 0x0001, 0x0002, "ROL: 0x0001 << 1 = 0x0002"),
        
        # ROR (011)
        (0b011, 0x0001, 0x0001, 0x8000, "ROR: 0x0001 >> 1 = 0x8000"),
        (0b011, 0x8000, 0x0001, 0x4000, "ROR: 0x8000 >> 1 = 0x4000"),
        
        # LSR (100)
        (0b100, 0x8000, 0x0001, 0x4000, "LSR: 0x8000 >> 1 = 0x4000"),
        (0b100, 0x0001, 0x0001, 0x0000, "LSR: 0x0001 >> 1 = 0x0000"),
    ]
    
    all_pass = True
    for op, a_val, b_val, expected, desc in test_cases:
        input_a = Bus(16)
        input_b = Bus(16)
        operation = Bus(3)
        
        input_a.set_Binary_value(a_val)
        input_b.set_Binary_value(b_val)
        operation.set_Binary_value(op)
        
        su.set_input_A(input_a)
        su.set_input_B(input_b)
        su.set_operation_bus(operation)
        
        result = su.calculate()
        actual = result.get_Decimal_value()
        
        if actual == expected:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc}: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")
            all_pass = False
    
    return all_pass

def test_alu_final():
    """Prueba final de la ALU completa"""
    print("\n=== PRUEBA FINAL DE LA ALU ===")
    
    alu = ALU()
    
    test_cases = [
        # (a_val, b_val, aluop, modo, expected, desc)
        # Aritmética
        (10, 5, 0b00, 0b000, 15, "ADD: 10 + 5 = 15"),
        (10, 5, 0b00, 0b001, 5, "SUB: 10 - 5 = 5"),
        
        # Lógica
        (0xFF00, 0x0F0F, 0b01, 0b000, 0x0F00, "AND: 0xFF00 & 0x0F0F = 0x0F00"),
        (0x00FF, 0xFF00, 0b01, 0b001, 0xFFFF, "OR: 0x00FF | 0xFF00 = 0xFFFF"),
        (0xAAAA, 0, 0b01, 0b011, 0x5555, "NOT: ~0xAAAA = 0x5555"),
        
        # Desplazamiento - ¡ESTOS SON LOS QUE FALLABAN!
        (0x0001, 0x0001, 0b10, 0b000, 0x0002, "SLL: 0x0001 << 1 = 0x0002"),
        (0x0001, 0x0004, 0b10, 0b000, 0x0010, "SLL: 0x0001 << 4 = 0x0010"),
        (0x8000, 0x0001, 0b10, 0b001, 0xC000, "SRA: 0x8000 >> 1 = 0xC000"),
        (0x8000, 0x0001, 0b10, 0b100, 0x4000, "LSR: 0x8000 >> 1 = 0x4000"),
        (0x8000, 0x0001, 0b10, 0b010, 0x0001, "ROL: 0x8000 rotar izq 1 = 0x0001"),
        (0x0001, 0x0001, 0b10, 0b011, 0x8000, "ROR: 0x0001 rotar der 1 = 0x8000"),
    ]
    
    all_pass = True
    for a_val, b_val, aluop, modo, expected, desc in test_cases:
        # Configurar buses
        a = Bus(16)
        b = Bus(16)
        aluop_bus = Bus(2)
        modo_bus = Bus(3)
        
        a.set_Binary_value(a_val)
        b.set_Binary_value(b_val)
        aluop_bus.set_Binary_value(aluop)
        modo_bus.set_Binary_value(modo)
        
        # Configurar ALU
        alu.set_input_a(a)
        alu.set_input_b(b)
        alu.set_aluop(aluop_bus)
        alu.set_modo_funcion(modo_bus)
        
        # Ejecutar
        resultado = alu.execute()
        actual = resultado.get_Decimal_value()
        
        if actual == expected:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc}: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")
            
            # Debug adicional para desplazamientos
            if aluop == 0b10:
                print(f"     Input B (control): 0x{b_val:04X}")
                print(f"     Bits de control: S0={b.get_Line_bit(15).get_value()}, "
                      f"S1={b.get_Line_bit(14).get_value()}, "
                      f"S2={b.get_Line_bit(13).get_value()}, "
                      f"S3={b.get_Line_bit(12).get_value()}")
            
            all_pass = False
    
    return all_pass

def main():
    """Función principal"""
    print("TEST FINAL DEL SISTEMA DE DESPLAZAMIENTO\n")
    
    results = []
    
    try:
        # Test 1: Mapeo del multiplexor
        print("\n" + "="*60)
        results.append(("Mapeo Multiplexor", test_correct_mapping()))
        
        # Test 2: Shift_Unit con mapeo corregido
        print("\n" + "="*60)
        results.append(("Shift_Unit corregido", test_shift_unit_corrected()))
        
        # Test 3: ALU completa
        print("\n" + "="*60)
        results.append(("ALU completa", test_alu_final()))
        
        # Resumen
        print("\n" + "="*60)
        print("RESUMEN FINAL:")
        print("="*60)
        
        all_pass = True
        for test_name, passed in results:
            status = "✓ PASÓ" if passed else "✗ FALLÓ"
            print(f"  {test_name:25} {status}")
            if not passed:
                all_pass = False
        
        print("\n" + "="*60)
        if all_pass:
            print("¡¡¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!!!")
            print("El sistema de desplazamiento funciona correctamente.")
        else:
            print("ALGUNAS PRUEBAS FALLARON - Revisar los logs anteriores")
        print("="*60)
        
        return 0 if all_pass else 1
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())