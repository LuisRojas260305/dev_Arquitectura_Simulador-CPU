"""
Prueba detallada del motor LSL con mensajes de control
"""

import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit
from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.LSL import LSL

def test_lsl_basic():
    """Prueba básica de LSL con mensajes detallados"""
    print("=== PRUEBA DETALLADA DE LSL ===")
    print("Configuración: bit 0 = MSB, bit 15 = LSB\n")
    
    # Crear LSL
    lsl = LSL()
    
    # --- Caso 1: Desplazar 0x0001 a la izquierda 1 bit ---
    print("1. LSL: 0x0001 << 1 = 0x0002")
    
    # Configurar entrada A
    input_a = Bus(16)
    input_a.set_Binary_value(0x0001)
    print(f"   Input A: {input_a.get_Hexadecimal_value()} = {input_a.get_Binary_value()}")
    print(f"   Bits A: {list(input_a.get_Ordered_lines_values(msb_first=True).values())}")
    
    # Configurar entrada B (control de desplazamiento)
    input_b = Bus(16)
    # Para desplazar 1 bit: activar bit 15 (S0)
    # 0x0001 = 0000 0000 0000 0001 (bit 15=1)
    input_b.set_Binary_value(0x0001)
    print(f"\n   Input B (control): {input_b.get_Hexadecimal_value()} = {input_b.get_Binary_value()}")
    
    # Mostrar bits de control específicos
    print(f"   Bit 15 (S0): {input_b.get_Line_bit(15).get_value()} (1-bit shift)")
    print(f"   Bit 14 (S1): {input_b.get_Line_bit(14).get_value()} (2-bit shift)")
    print(f"   Bit 13 (S2): {input_b.get_Line_bit(13).get_value()} (4-bit shift)")
    print(f"   Bit 12 (S3): {input_b.get_Line_bit(12).get_value()} (8-bit shift)")
    
    # Configurar LSL
    lsl.set_Input_A(input_a)
    lsl.set_Input_B(input_b)
    
    # Calcular
    print("\n   Calculando LSL...")
    resultado = lsl.Calculate()
    
    print(f"\n   Resultado: {resultado.get_Hexadecimal_value()} = {resultado.get_Binary_value()}")
    print(f"   Bits resultado: {list(resultado.get_Ordered_lines_values(msb_first=True).values())}")
    
    expected = 0x0002
    actual = resultado.get_Decimal_value()
    
    if actual == expected:
        print(f"   ✓ CORRECTO: 0x{expected:04X}")
    else:
        print(f"   ✗ ERROR: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")
    
    # --- Caso 2: Desplazar 0x0001 a la izquierda 4 bits ---
    print("\n\n2. LSL: 0x0001 << 4 = 0x0010")
    
    input_a.set_Binary_value(0x0001)
    # Para desplazar 4 bits: activar bit 13 (S2)
    # 0x0004 = 0000 0000 0000 0100 (bit 13=1)
    input_b.set_Binary_value(0x0004)
    
    print(f"   Input A: {input_a.get_Hexadecimal_value()}")
    print(f"   Input B (control): {input_b.get_Hexadecimal_value()}")
    print(f"   Bit 15 (S0): {input_b.get_Line_bit(15).get_value()}")
    print(f"   Bit 14 (S1): {input_b.get_Line_bit(14).get_value()}")
    print(f"   Bit 13 (S2): {input_b.get_Line_bit(13).get_value()} ← ACTIVADO (4-bit shift)")
    print(f"   Bit 12 (S3): {input_b.get_Line_bit(12).get_value()}")
    
    lsl.set_Input_A(input_a)
    lsl.set_Input_B(input_b)
    
    resultado = lsl.Calculate()
    print(f"\n   Resultado: {resultado.get_Hexadecimal_value()}")
    
    expected = 0x0010
    actual = resultado.get_Decimal_value()
    
    if actual == expected:
        print(f"   ✓ CORRECTO: 0x{expected:04X}")
    else:
        print(f"   ✗ ERROR: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")
    
    # --- Caso 3: Desplazar 0x1234 a la izquierda 1 bit ---
    print("\n\n3. LSL: 0x1234 << 1 = 0x2468")
    
    input_a.set_Binary_value(0x1234)
    input_b.set_Binary_value(0x0001)  # 1-bit shift
    
    print(f"   Input A: {input_a.get_Hexadecimal_value()}")
    print(f"   Input B (control): {input_b.get_Hexadecimal_value()}")
    
    lsl.set_Input_A(input_a)
    lsl.set_Input_B(input_b)
    
    resultado = lsl.Calculate()
    print(f"\n   Resultado: {resultado.get_Hexadecimal_value()}")
    
    expected = 0x2468
    actual = resultado.get_Decimal_value()
    
    if actual == expected:
        print(f"   ✓ CORRECTO: 0x{expected:04X}")
    else:
        print(f"   ✗ ERROR: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")
    
    return actual == expected

def test_lsl_cascada():
    """Prueba el funcionamiento en cascada de las etapas"""
    print("\n=== PRUEBA DE CASCADA LSL ===")
    
    lsl = LSL()
    
    # Crear un bus con patrón específico para ver el desplazamiento
    input_a = Bus(16)
    # Patrón: 1010 1010 1010 1010 = 0xAAAA
    input_a.set_Binary_value(0xAAAA)
    
    print(f"Input A: {input_a.get_Hexadecimal_value()} = {input_a.get_Binary_value()}")
    print("Bit pattern: ", end="")
    for i in range(16):
        print(f"{input_a.get_Line_bit(i).get_value()}", end="")
        if (i+1) % 4 == 0 and i < 15:
            print(" ", end="")
    print()
    
    # Probar diferentes cantidades de desplazamiento
    test_cases = [
        (0x0000, 0, "Sin desplazamiento"),
        (0x0001, 1, "1-bit shift"),
        (0x0002, 2, "2-bit shift (S1)"),
        (0x0003, 3, "1+2 bit shift"),
        (0x0004, 4, "4-bit shift (S2)"),
        (0x0008, 8, "8-bit shift (S3)"),
        (0x000F, 15, "Máximo desplazamiento (1+2+4+8)"),
    ]
    
    print("\n" + "="*60)
    for b_val, shift_amount, desc in test_cases:
        input_b = Bus(16)
        input_b.set_Binary_value(b_val)
        
        lsl.set_Input_A(input_a)
        lsl.set_Input_B(input_b)
        
        resultado = lsl.Calculate()
        
        print(f"\n{desc}:")
        print(f"  Control: 0x{b_val:04X} (S0={input_b.get_Line_bit(15).get_value()}, "
              f"S1={input_b.get_Line_bit(14).get_value()}, "
              f"S2={input_b.get_Line_bit(13).get_value()}, "
              f"S3={input_b.get_Line_bit(12).get_value()})")
        print(f"  Resultado: {resultado.get_Hexadecimal_value()}")
        print(f"  Binario: {resultado.get_Binary_value()}")
        
        # Verificar manualmente para algunos casos
        if shift_amount == 0:
            expected = 0xAAAA
        elif shift_amount == 1:
            expected = 0x5554  # 0xAAAA << 1 = 0x5554
        elif shift_amount == 2:
            expected = 0xAAA8  # 0xAAAA << 2 = 0xAAA8
        
        if shift_amount <= 2:
            actual = resultado.get_Decimal_value()
            if actual == expected:
                print(f"  ✓ Verificado: 0x{expected:04X}")
            else:
                print(f"  ✗ ERROR: Esperado 0x{expected:04X}, Obtenido 0x{actual:04X}")

def test_mux2to1():
    """Prueba el componente MUX2to1 básico"""
    print("\n=== PRUEBA DE MUX2to1 ===")
    
    from Business.CPU_Core.Arithmetic_Logical_Unit.Shift_Unit.MUX2to1 import MUX2to1
    
    mux = MUX2to1()
    
    test_cases = [
        (0, 0, 0, 0, "S=0, A=0, B=0 -> 0"),
        (0, 0, 1, 0, "S=0, A=0, B=1 -> 0 (pasa A)"),
        (0, 1, 0, 1, "S=0, A=1, B=0 -> 1 (pasa A)"),
        (0, 1, 1, 1, "S=0, A=1, B=1 -> 1 (pasa A)"),
        (1, 0, 0, 0, "S=1, A=0, B=0 -> 0 (pasa B)"),
        (1, 0, 1, 1, "S=1, A=0, B=1 -> 1 (pasa B)"),
        (1, 1, 0, 0, "S=1, A=1, B=0 -> 0 (pasa B)"),
        (1, 1, 1, 1, "S=1, A=1, B=1 -> 1 (pasa B)"),
    ]
    
    all_pass = True
    for s, a, b, expected, desc in test_cases:
        mux.set_S(Bit(s))
        mux.set_Input_A(Bit(a))
        mux.set_Input_B(Bit(b))
        mux.Calculate()
        actual = mux.get_Output().get_value()
        
        if actual == expected:
            print(f"  ✓ {desc}")
        else:
            print(f"  ✗ {desc}: Esperado {expected}, Obtenido {actual}")
            all_pass = False
    
    return all_pass

def debug_lsl_internals():
    """Función para debuggear los internals de LSL"""
    print("\n=== DEBUG INTERNO DE LSL ===")
    
    # Modificar temporalmente la clase LSL para agregar prints
    # O crear una versión de depuración
    class LSL_Debug(LSL):
        def __Calculate_Stage_0(self, input: Bus, S_in: Bit) -> Bus:
            print(f"\n[DEBUG Stage_0] S_in = {S_in.get_value()}")
            print(f"  Input (hex): {input.get_Hexadecimal_value()}")
            
            Output = Bus(16)
            for i in range(16):
                self.__1bit__stage[i].set_Input_A(input.get_Line_bit(i))
                self.__1bit__stage[i].set_S(S_in)
                
                if i >= 15:
                    self.__1bit__stage[i].set_Input_B(Bit(0))
                else:
                    self.__1bit__stage[i].set_Input_B(input.get_Line_bit(i + 1))
                
                self.__1bit__stage[i].Calculate()
                Output.set_Line_bit(i, self.__1bit__stage[i].get_Output())
                
                # Debug info
                input_a_val = input.get_Line_bit(i).get_value()
                input_b_val = self.__1bit__stage[i].get_Input_B().get_value()
                output_val = self.__1bit__stage[i].get_Output().get_value()
                
                if S_in.get_value() == 1:
                    print(f"  Bit {i:2d}: A={input_a_val}, B={input_b_val}, S={S_in.get_value()} -> Out={output_val}")
            
            print(f"  Output (hex): {Output.get_Hexadecimal_value()}")
            return Output
    
    # Probar con caso simple
    lsl_debug = LSL_Debug()
    
    input_a = Bus(16)
    input_a.set_Binary_value(0x0001)
    
    input_b = Bus(16)
    input_b.set_Binary_value(0x0001)  # S0=1
    
    lsl_debug.set_Input_A(input_a)
    lsl_debug.set_Input_B(input_b)
    
    print("\nDebug caso: 0x0001 << 1")
    resultado = lsl_debug.Calculate()
    print(f"Resultado final: {resultado.get_Hexadecimal_value()}")

def main():
    """Función principal"""
    print("TESTEO COMPLETO DE COMPONENTES DE DESPLAZAMIENTO\n")
    
    try:
        # Test MUX2to1
        mux_ok = test_mux2to1()
        
        # Test LSL básico
        lsl_ok = test_lsl_basic()
        
        # Test cascada
        test_lsl_cascada()
        
        # Debug
        debug_lsl_internals()
        
        if mux_ok and lsl_ok:
            print("\n" + "="*60)
            print("¡TODOS LOS TESTS PASARON!")
            print("="*60)
            return 0
        else:
            print("\n" + "="*60)
            print("ALGUNOS TESTS FALLARON")
            print("="*60)
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())