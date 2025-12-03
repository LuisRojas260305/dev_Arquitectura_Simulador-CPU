# test_Alu_fixed.py
import sys
import os

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Business.CPU_Core.Arithmetic_Logical_Unit.ALU import ALU
from Business.Basic_Components.Bus import Bus
from Business.Basic_Components.Bit import Bit

def test_alu_basic():
    """Pruebas básicas de la ALU"""
    print("=== Iniciando pruebas de la ALU ===")
    alu = ALU()
    
    # --- Pruebas Aritméticas (ALUop=00) ---
    print("\n1. Pruebas Aritméticas (ALUop=00):")
    
    # ADD (ModoFunción=000, C_in=0)
    print("  ADD: 10 + 5 = 15")
    a = Bus(16)
    b = Bus(16)
    a.set_Binary_value(10)  # 0x000A
    b.set_Binary_value(5)   # 0x0005
    
    aluop = Bus(2)
    modo = Bus(3)
    aluop.set_Binary_value(0b00)  # Aritmética
    modo.set_Binary_value(0b000)  # ADD (C_in=0)
    
    alu.set_input_a(a)
    alu.set_input_b(b)
    alu.set_aluop(aluop)
    alu.set_modo_funcion(modo)
    
    resultado = alu.execute()
    decimal = resultado.get_Decimal_value()
    print(f"  Resultado: {decimal} (0x{resultado.get_Hexadecimal_value()[2:]})")
    assert decimal == 15, f"Error en ADD: esperado 15, obtenido {decimal}"
    
    # SUB (ModoFunción=001, C_in=1)
    print("\n  SUB: 10 - 5 = 5")
    modo.set_Binary_value(0b001)  # SUB (C_in=1)
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    decimal = resultado.get_Decimal_value()
    print(f"  Resultado: {decimal} (0x{resultado.get_Hexadecimal_value()[2:]})")
    assert decimal == 5, f"Error en SUB: esperado 5, obtenido {decimal}"
    
    # SUB con negativo (en complemento a 2)
    print("\n  SUB: 5 - 10 = -5 (0xFFFB en complemento a 2)")
    a.set_Binary_value(5)
    b.set_Binary_value(10)
    alu.set_input_a(a)
    alu.set_input_b(b)
    resultado = alu.execute()
    decimal = resultado.get_Decimal_value()
    print(f"  Resultado: {decimal} (0x{resultado.get_Hexadecimal_value()[2:]})")
    # En complemento a 2 de 16 bits: -5 = 0xFFFB = 65531
    assert decimal == 65531, f"Error en SUB negativo: esperado 65531, obtenido {decimal}"
    
    # --- Pruebas Lógicas (ALUop=01) ---
    print("\n2. Pruebas Lógicas (ALUop=01):")
    
    aluop.set_Binary_value(0b01)  # Lógica
    
    # AND (ModoFunción=000)
    print("  AND: 0xFF00 & 0x0F0F = 0x0F00")
    a.set_Binary_value(0xFF00)
    b.set_Binary_value(0x0F0F)
    modo.set_Binary_value(0b000)  # AND
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x0F00", f"Error en AND: esperado 0x0F00, obtenido {hex_result}"
    
    # OR (ModoFunción=001)
    print("\n  OR: 0x00FF | 0xFF00 = 0xFFFF")
    a.set_Binary_value(0x00FF)
    b.set_Binary_value(0xFF00)
    modo.set_Binary_value(0b001)  # OR
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0xFFFF", f"Error en OR: esperado 0xFFFF, obtenido {hex_result}"
    
    # XOR (ModoFunción=010)
    print("\n  XOR: 0xFFFF ^ 0x0F0F = 0xF0F0")
    a.set_Binary_value(0xFFFF)
    b.set_Binary_value(0x0F0F)
    modo.set_Binary_value(0b010)  # XOR
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0xF0F0", f"Error en XOR: esperado 0xF0F0, obtenido {hex_result}"
    
    # NOT (ModoFunción=011) - operación unaria
    print("\n  NOT: ~0xAAAA = 0x5555")
    a.set_Binary_value(0xAAAA)
    b.set_Binary_value(0)  # No se usa en NOT
    modo.set_Binary_value(0b011)  # NOT
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x5555", f"Error en NOT: esperado 0x5555, obtenido {hex_result}"
    
    # --- Pruebas de Desplazamiento (ALUop=10) ---
    print("\n3. Pruebas de Desplazamiento (ALUop=10):")
    
    aluop.set_Binary_value(0b10)  # Desplazamiento
    
    # SLL (Shift Left Logical) - ModoFunción=000
    print("  SLL: 0x0001 << 1 = 0x0002")
    a.set_Binary_value(0x0001)
    # Para desplazamiento: Input_B contiene la cantidad en los bits 12-15
    # 1 bit de desplazamiento = activar bit 15 (0x0001)
    # Índice 0 = MSB, índice 15 = LSB
    b.set_Binary_value(0x0001)  # Activar bit 15
    modo.set_Binary_value(0b000)  # SLL
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x0002", f"Error en SLL: esperado 0x0002, obtenido {hex_result}"
    
    # SLL con 4 bits de desplazamiento
    print("\n  SLL: 0x0001 << 4 = 0x0010")
    a.set_Binary_value(0x0001)
    # 4 bits de desplazamiento = activar bit 13 (0x0004)
    b.set_Binary_value(0x0004)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x0010", f"Error en SLL 4 bits: esperado 0x0010, obtenido {hex_result}"
    
    # SRA (Shift Right Arithmetic) - ModoFunción=001
    print("\n  SRA: 0x8000 >> 1 = 0xC000 (extensión de signo)")
    a.set_Binary_value(0x8000)  # -32768 en complemento a 2
    b.set_Binary_value(0x0001)  # 1 bit de desplazamiento (bit 15)
    modo.set_Binary_value(0b001)  # SRA
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0xC000", f"Error en SRA: esperado 0xC000, obtenido {hex_result}"
    
    # ROL (Rotate Left) - ModoFunción=010
    print("\n  ROL: 0x8000 ROL 1 = 0x0001")
    a.set_Binary_value(0x8000)
    b.set_Binary_value(0x0001)  # 1 bit de desplazamiento
    modo.set_Binary_value(0b010)  # ROL
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x0001", f"Error en ROL: esperado 0x0001, obtenido {hex_result}"
    
    # ROR (Rotate Right) - ModoFunción=011
    print("\n  ROR: 0x0001 ROR 1 = 0x8000")
    a.set_Binary_value(0x0001)
    b.set_Binary_value(0x0001)  # 1 bit de desplazamiento
    modo.set_Binary_value(0b011)  # ROR
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x8000", f"Error en ROR: esperado 0x8000, obtenido {hex_result}"
    
    # LSR (Shift Right Logical) - ModoFunción=100
    print("\n  LSR: 0x8000 >> 1 = 0x4000 (relleno con 0)")
    a.set_Binary_value(0x8000)
    b.set_Binary_value(0x0001)  # 1 bit de desplazamiento
    modo.set_Binary_value(0b100)  # LSR
    alu.set_modo_funcion(modo)
    resultado = alu.execute()
    hex_result = resultado.get_Hexadecimal_value()
    print(f"  Resultado: {hex_result}")
    assert hex_result == "0x4000", f"Error en LSR: esperado 0x4000, obtenido {hex_result}"
    
    # --- Verificación de Flags ---
    print("\n4. Verificación de Flags:")
    
    # Zero Flag
    print("  Zero Flag: 5 - 5 = 0 (Z=1)")
    a.set_Binary_value(5)
    b.set_Binary_value(5)
    aluop.set_Binary_value(0b00)  # Aritmética
    modo.set_Binary_value(0b001)  # SUB
    alu.set_input_a(a)
    alu.set_input_b(b)
    alu.set_aluop(aluop)
    alu.set_modo_funcion(modo)
    alu.execute()
    zero_flag = alu.get_zero_flag().get_value()
    print(f"  Zero Flag: {zero_flag}")
    assert zero_flag == 1, f"Error Zero Flag: esperado 1, obtenido {zero_flag}"
    
    # Negative Flag
    print("\n  Negative Flag: 0 - 1 = -1 (N=1, MSB=1)")
    a.set_Binary_value(0)
    b.set_Binary_value(1)
    alu.execute()
    negative_flag = alu.get_negative_flag().get_value()
    print(f"  Negative Flag: {negative_flag}")
    assert negative_flag == 1, f"Error Negative Flag: esperado 1, obtenido {negative_flag}"
    
    # Carry Flag (para suma con acarreo)
    print("\n  Carry Flag: 0xFFFF + 1 = 0x0000 con acarreo (C=1)")
    a.set_Binary_value(0xFFFF)
    b.set_Binary_value(1)
    modo.set_Binary_value(0b000)  # ADD
    alu.set_modo_funcion(modo)
    alu.execute()
    carry_flag = alu.get_carry_out().get_value()
    print(f"  Carry Flag: {carry_flag}")
    assert carry_flag == 1, f"Error Carry Flag: esperado 1, obtenido {carry_flag}"
    
    print("\n=== ¡Todas las pruebas pasaron exitosamente! ===")

def test_alu_comprehensive():
    """Pruebas exhaustivas de todas las operaciones"""
    print("\n=== Pruebas Exhaustivas de la ALU ===")
    alu = ALU()
    
    # Mapeo de operaciones según ISA
    operations = [
        # (nombre, aluop_bin, modo_bin, a, b, expected)
        ("ADD 15+25", 0b00, 0b000, 15, 25, 40),
        ("SUB 100-30", 0b00, 0b001, 100, 30, 70),
        ("AND 0xFF00&0x0F0F", 0b01, 0b000, 0xFF00, 0x0F0F, 0x0F00),
        ("OR 0x00FF|0xFF00", 0b01, 0b001, 0x00FF, 0xFF00, 0xFFFF),
        ("XOR 0xFFFF^0x0F0F", 0b01, 0b010, 0xFFFF, 0x0F0F, 0xF0F0),
        ("NOT ~0xAAAA", 0b01, 0b011, 0xAAAA, 0, 0x5555),
    ]
    
    for name, aluop, modo, a_val, b_val, expected in operations:
        a = Bus(16)
        b = Bus(16)
        a.set_Binary_value(a_val)
        b.set_Binary_value(b_val)
        
        aluop_bus = Bus(2)
        modo_bus = Bus(3)
        aluop_bus.set_Binary_value(aluop)
        modo_bus.set_Binary_value(modo)
        
        alu.set_input_a(a)
        alu.set_input_b(b)
        alu.set_aluop(aluop_bus)
        alu.set_modo_funcion(modo_bus)
        
        resultado = alu.execute()
        resultado_val = resultado.get_Decimal_value()
        
        if resultado_val == expected:
            print(f"✓ {name}: OK")
        else:
            print(f"✗ {name}: ERROR - Esperado {expected} (0x{expected:04X}), "
                  f"Obtenido {resultado_val} (0x{resultado_val:04X})")
            return False
    
    # Pruebas de desplazamiento con diferentes cantidades
    print("\nPruebas de desplazamiento:")
    shift_tests = [
        # (nombre, aluop, modo, a_val, b_val (bits de control), expected)
        ("SLL 1<<0", 0b10, 0b000, 0x0001, 0x0000, 0x0001),  # Sin desplazamiento
        ("SLL 1<<1", 0b10, 0b000, 0x0001, 0x0001, 0x0002),  # 1 bit (bit 15)
        ("SLL 1<<4", 0b10, 0b000, 0x0001, 0x0004, 0x0010),  # 4 bits (bit 13)
        ("SLL 1<<8", 0b10, 0b000, 0x0001, 0x0008, 0x0100),  # 8 bits (bit 12)
        ("LSR 0x8000>>1", 0b10, 0b100, 0x8000, 0x0001, 0x4000),
        ("ROL 0xC000>>1", 0b10, 0b010, 0xC000, 0x0001, 0x8001), # ROL de 0xC000 por 1
    ]
    
    for name, aluop, modo, a_val, b_val, expected in shift_tests:
        a = Bus(16)
        b = Bus(16)
        a.set_Binary_value(a_val)
        b.set_Binary_value(b_val)
        
        aluop_bus = Bus(2)
        modo_bus = Bus(3)
        aluop_bus.set_Binary_value(aluop)
        modo_bus.set_Binary_value(modo)
        
        alu.set_input_a(a)
        alu.set_input_b(b)
        alu.set_aluop(aluop_bus)
        alu.set_modo_funcion(modo_bus)
        
        resultado = alu.execute()
        resultado_val = resultado.get_Decimal_value()
        
        if resultado_val == expected:
            print(f"✓ {name}: OK")
        else:
            print(f"✗ {name}: ERROR - Esperado {expected} (0x{expected:04X}), "
                  f"Obtenido {resultado_val} (0x{resultado_val:04X})")
            return False
    
    print("\n=== ¡Pruebas exhaustivas completadas! ===")
    return True

def test_alu_with_instruction_set():
    """Prueba la ALU con el conjunto de instrucciones del ISA"""
    print("\n=== Pruebas según ISA ===")
    
    # Crear mapeo de instrucciones según ISA_Conjunto_Instrucciones.md
    isa_tests = [
        # (mnemónico, opcode_hex, aluop, modo_funcion, a, b, expected)
        ("ADD", 0x3, 0b00, 0b000, 0x000A, 0x0005, 0x000F),
        ("SUB", 0x4, 0b00, 0b001, 0x000A, 0x0005, 0x0005),
        ("AND", 0xA, 0b01, 0b000, 0x00FF, 0x0F0F, 0x000F),
        ("OR",  0xB, 0b01, 0b001, 0x00F0, 0x000F, 0x00FF),
        ("XOR", 0xC, 0b01, 0b010, 0x00FF, 0x0F0F, 0x0FF0),
        ("SLL", 0xD, 0b10, 0b000, 0x0001, 0x0001, 0x0002),  # << 1
        ("SRA", 0xE, 0b10, 0b001, 0x8000, 0x0001, 0xC000),  # >> 1 con extensión signo
        ("ROL", 0xF, 0b10, 0b010, 0x8000, 0x0001, 0x0001),  # rotación izquierda 1
    ]
    
    alu = ALU()
    
    for name, opcode, aluop, modo, a_val, b_val, expected in isa_tests:
        print(f"\nProbando {name} (Opcode: 0x{opcode:X}):")
        print(f"  A=0x{a_val:04X}, B=0x{b_val:04X}")
        
        a = Bus(16)
        b = Bus(16)
        a.set_Binary_value(a_val)
        b.set_Binary_value(b_val)
        
        aluop_bus = Bus(2)
        modo_bus = Bus(3)
        aluop_bus.set_Binary_value(aluop)
        modo_bus.set_Binary_value(modo)
        
        alu.set_input_a(a)
        alu.set_input_b(b)
        alu.set_aluop(aluop_bus)
        alu.set_modo_funcion(modo_bus)
        
        resultado = alu.execute()
        resultado_hex = resultado.get_Hexadecimal_value()
        resultado_val = resultado.get_Decimal_value()
        
        print(f"  Resultado: {resultado_hex}")
        
        if resultado_val == expected:
            print(f"  ✓ {name}: CORRECTO")
        else:
            print(f"  ✗ {name}: ERROR - Esperado 0x{expected:04X}, Obtenido {resultado_hex}")
            return False
    
    print("\n=== ¡Todas las instrucciones del ISA funcionan correctamente! ===")
    return True

def main():
    """Función principal para ejecutar todas las pruebas"""
    try:
        test_alu_basic()
        test_alu_comprehensive()
        test_alu_with_instruction_set()
        print("\n" + "="*50)
        print("¡TODAS LAS PRUEBAS DE LA ALU SE COMPLETARON EXITOSAMENTE!")
        print("="*50)
    except AssertionError as e:
        print(f"\n❌ ERROR en prueba: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())