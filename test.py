# test_modules_fixed.py
import sys
import os
from pathlib import Path
import json

# Añadir el directorio raíz al path para importaciones
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_bit():
    """Prueba la clase Bit"""
    print("=== Prueba de Bit ===")
    try:
        from Business.Basic_Components.Bit import Bit
        
        # Crear bits
        b0 = Bit(0)
        b1 = Bit(1)
        
        print(f"b0 = {b0}, valor: {b0.get_value()}")
        print(f"b1 = {b1}, valor: {b1.get_value()}")
        
        # Probar toggle
        b0.toggle()
        b1.toggle()
        print(f"Después de toggle - b0: {b0.get_value()}, b1: {b1.get_value()}")
        
        # Probar igualdad
        print(f"b0 == Bit(1): {b0 == Bit(1)}")
        print(f"b1 == Bit(0): {b1 == Bit(0)}")
        
        # Probar valor inválido
        try:
            b_inv = Bit(2)
            print("ERROR: Debería haber lanzado ValueError")
        except ValueError as e:
            print(f"✓ Correcto - Valor inválido detectado: {e}")
        
        print("✓ Bit: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ Bit: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_bus():
    """Prueba la clase Bus - CORREGIDO"""
    print("=== Prueba de Bus ===")
    try:
        from Business.Basic_Components.Bus import Bus
        from Business.Basic_Components.Bit import Bit  # Importar Bit explícitamente
        
        # Bus de 8 bits
        bus8 = Bus(8, 42)  # 42 decimal = 00101010 binario
        print(f"Bus8: {bus8}")
        print(f"  Decimal: {bus8.get_Decimal_value()}")
        print(f"  Binario: {bus8.get_Binary_value()}")
        print(f"  Hex: {bus8.get_Hexadecimal_value()}")
        
        # Verificar MSB en índice 0 (bit más significativo primero)
        lines = bus8.get_Ordered_lines_values(msb_first=True)
        print(f"  Líneas (MSB primero): {lines}")
        print(f"  MSB (índice 0): {lines[0]}, LSB (índice 7): {lines[7]}")
        
        # Convertir binario a decimal para verificar
        binary_str = bus8.get_Binary_value()
        decimal_from_binary = int(binary_str, 2)
        print(f"  Verificación: binario '{binary_str}' = decimal {decimal_from_binary}")
        
        # Pruebas de límites
        try:
            Bus(0, 0)  # Ancho inválido
            print("ERROR: Debería haber lanzado ValueError")
        except ValueError as e:
            print(f"✓ Correcto - Ancho inválido detectado: {e}")
            
        try:
            Bus(8, 256)  # Valor fuera de rango
            print("ERROR: Debería haber lanzado ValueError")
        except ValueError as e:
            print(f"✓ Correcto - Valor fuera de rango detectado: {e}")
        
        # Probar set/get de línea individual - CORREGIDO
        print("\nProbando set_Line_bit y get_Line_bit...")
        # Usar el Bit importado explícitamente
        bus8.set_Line_bit(0, Bit(0))  # Cambiar MSB a 0
        bus8.set_Line_bit(7, Bit(1))  # Cambiar LSB a 1
        print(f"Bus8 modificado: {bus8.get_Binary_value()}")
        
        # Verificar bits individuales
        print(f"  Línea 0 (MSB): {bus8.get_Line_bit(0).get_value()}")
        print(f"  Línea 7 (LSB): {bus8.get_Line_bit(7).get_value()}")
        
        print("✓ Bus: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ Bus: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_ram():
    """Prueba la memoria RAM - CORREGIDO"""
    print("=== Prueba de RAM ===")
    try:
        from Business.Memory.RAM import RAM
        
        # Crear RAM de 4K
        ram = RAM(4)
        
        # Verificar tamaño
        print(f"RAM tamaño: {ram.size} palabras (0x0000 - 0x{ram.size-1:04X})")
        
        # Probar lectura/escritura directa
        ram.write_direct(0x100, 0x1234)
        value = ram.read_direct(0x100).get_Decimal_value()
        print(f"Escritura directa [0x100] = 0x1234, Lectura = 0x{value:04X}")
        
        if value != 0x1234:
            print(f"✗ ERROR: Valor incorrecto. Esperado: 0x1234, Obtenido: 0x{value:04X}")
            return False
        
        # Cargar programa desde JSON
        json_path = project_root / "Data" / "Programs" / "Test.json"
        if not json_path.exists():
            print(f"✗ ERROR: Archivo {json_path} no encontrado")
            return False
        
        # Leer el JSON para ver el valor real
        with open(json_path, 'r') as f:
            test_data = json.load(f)
        
        # Obtener el valor real de la variable (es 0, no 42)
        expected_value = test_data['data_section']['variables']['valor1']['value']
        print(f"Valor esperado en JSON para 'valor1': {expected_value}")
        
        # Cargar el JSON
        ram.load_from_json(str(json_path))
        
        # Verificar que se cargó la primera instrucción
        inst0 = ram.read_direct(0).get_Decimal_value()
        print(f"Instrucción en [0x0000]: 0x{inst0:04X} (esperado: 0x9005)")
        
        if inst0 != 0x9005:
            print(f"✗ ERROR: Instrucción incorrecta")
            return False
        
        # Verificar dato cargado (debe ser 0 según el JSON)
        data16 = ram.read_direct(16).get_Decimal_value()
        print(f"Dato en [0x0010]: {data16} (esperado: {expected_value})")
        
        if data16 != expected_value:
            print(f"✗ ERROR: Dato incorrecto. Esperado: {expected_value}, Obtenido: {data16}")
            return False
        
        # Mostrar dump de memoria
        print("\nDump de memoria (primeras 8 posiciones):")
        for i in range(8):
            val = ram.read_direct(i).get_Decimal_value()
            bin_val = ram.read_direct(i).get_Binary_value()
            print(f"  [{i:04X}]: 0x{val:04X} = {bin_val}")
        
        print("✓ RAM: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ RAM: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_system_bus():
    """Prueba el bus del sistema - CORREGIDO"""
    print("=== Prueba de SystemBus ===")
    try:
        from Business.Memory.SystemBus import SystemBus
        from Business.Memory.RAM import RAM
        from Business.Basic_Components.Bus import Bus
        
        # Crear bus del sistema (12 bits de dirección = 0-4095)
        sysbus = SystemBus(data_width=16, addr_width=12)
        print(f"Bus del sistema creado: {sysbus.address_bus.width} bits de dirección")
        print(f"Rango de direcciones: 0 - 0x{(1 << sysbus.address_bus.width) - 1:04X}")
        
        # Crear RAM
        ram = RAM(4)
        
        # Conectar RAM al bus
        sysbus.connect_device(ram, "RAM", (0, 4095), "slave")
        
        # Escribir a través del bus
        test_data = Bus(16, 0xABCD)
        sysbus.write(0x200, test_data, master_name="CPU_TEST")
        
        # Leer a través del bus
        read_data = sysbus.read(0x200, master_name="CPU_TEST")
        read_value = read_data.get_Decimal_value()
        
        print(f"Escrito: 0xABCD, Leído: 0x{read_value:04X}")
        
        if read_value != 0xABCD:
            print(f"✗ ERROR: Datos no coinciden. Esperado: 0xABCD, Obtenido: 0x{read_value:04X}")
            return False
        
        # Probar dirección dentro del rango pero no mapeada (fuera de RAM)
        # Usar 0x1000 que está en el rango del bus (12 bits) pero fuera de la RAM (4K)
        error_data = sysbus.read(0x1000, master_name="CPU_TEST")
        error_value = error_data.get_Decimal_value()
        print(f"Lectura dirección no mapeada [0x1000]: 0x{error_value:04X} (esperado: 0xFFFF)")
        
        if error_value != 0xFFFF:
            print(f"✗ ERROR: Valor de error incorrecto")
            return False
        
        # Mostrar estado del bus
        status = sysbus.get_status()
        print(f"Estado del bus: {status}")
        
        print("✓ SystemBus: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ SystemBus: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_alu():
    """Prueba la ALU"""
    print("=== Prueba de ALU ===")
    try:
        from Business.CPU_Core.Arithmetic_Logical_Unit.ALU import ALU
        from Business.Basic_Components.Bus import Bus
        
        alu = ALU()
        
        # Prueba 1: Suma (5 + 3 = 8)
        resultado = alu.execute_with_signals(5, 3, 0b00, 0b000)
        print(f"5 + 3 = {resultado} (esperado: 8)")
        if resultado != 8:
            print(f"✗ ERROR: Suma incorrecta")
            return False
        
        # Prueba 2: AND (5 & 3 = 1)
        resultado = alu.execute_with_signals(5, 3, 0b01, 0b000)
        print(f"5 AND 3 = {resultado} (esperado: 1)")
        if resultado != 1:
            print(f"✗ ERROR: AND incorrecto")
            return False
        
        # Prueba 3: OR (5 | 3 = 7)
        resultado = alu.execute_with_signals(5, 3, 0b01, 0b001)
        print(f"5 OR 3 = {resultado} (esperado: 7)")
        if resultado != 7:
            print(f"✗ ERROR: OR incorrecto")
            return False
        
        # Prueba 4: XOR (5 ^ 3 = 6)
        resultado = alu.execute_with_signals(5, 3, 0b01, 0b010)
        print(f"5 XOR 3 = {resultado} (esperado: 6)")
        if resultado != 6:
            print(f"✗ ERROR: XOR incorrecto")
            return False
        
        # Prueba 5: Desplazamiento izquierda (5 << 1 = 10)
        resultado = alu.execute_with_signals(5, 1, 0b10, 0b000)
        print(f"5 << 1 = {resultado} (esperado: 10)")
        if resultado != 10:
            print(f"✗ ERROR: Desplazamiento incorrecto")
            return False
        
        # Prueba 6: Resta (5 - 3 = 2)
        resultado = alu.execute_with_signals(5, 3, 0b00, 0b001)  # bit 0 en 1 para resta
        print(f"5 - 3 = {resultado} (esperado: 2)")
        if resultado != 2:
            print(f"✗ ERROR: Resta incorrecta")
            return False
        
        # Verificar flags después de la última operación
        print(f"Flags: Z={alu.get_zero_flag().get_value()}, "
              f"C={alu.get_carry_out().get_value()}, "
              f"N={alu.get_negative_flag().get_value()}")
        
        print("✓ ALU: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ ALU: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_control_unit():
    """Prueba la Unidad de Control"""
    print("=== Prueba de Control Unit ===")
    try:
        from Business.CPU_Core.Control_Unit.Control_Unit import Control_Unit
        from Business.Basic_Components.Bus import Bus
        
        cu = Control_Unit()
        
        # Cargar una instrucción de prueba (LOADI 5 = 0x9005)
        inst_bus = Bus(16, 0x9005)
        cu.load_instruction(inst_bus)
        
        # Obtener estado
        status = cu.get_current_status()
        print(f"Instrucción cargada: {status['instruction']}")
        print(f"Opcode: 0x{status['opcode']:X} (esperado: 0x9)")
        print(f"Micro step: {status['micro_step']}")
        
        if status['opcode'] != 0x9:
            print(f"✗ ERROR: Opcode incorrecto")
            return False
        
        # Obtener operando
        operand = cu.get_operand()
        print(f"Operando: 0x{operand:03X} (esperado: 0x005)")
        
        if operand != 0x005:
            print(f"✗ ERROR: Operando incorrecto")
            return False
        
        # Ejecutar un ciclo
        print("\nEjecutando ciclo de control...")
        end_instruction = cu.execute_cycle()
        
        # Obtener señales de control
        alu_ctrl = cu.get_alu_control()
        mem_ctrl = cu.get_memory_control()
        reg_ctrl = cu.get_register_control()
        
        print(f"Señales ALU: {alu_ctrl}")
        print(f"Señales Memoria: {mem_ctrl}")
        print(f"Señales Registros: {reg_ctrl}")
        print(f"Fin de instrucción: {end_instruction}")
        
        print("✓ Control Unit: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ Control Unit: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_cpu_integration():
    """Prueba integración básica de CPU - CORREGIDO"""
    print("=== Prueba de Integración CPU ===")
    try:
        from Business.CPU_Core.CPU import CPU
        from Business.Memory.SystemBus import SystemBus
        from Business.Memory.RAM import RAM
        
        # Configurar sistema
        sysbus = SystemBus(data_width=16, addr_width=12)
        ram = RAM(4)
        
        # Conectar RAM al bus
        sysbus.connect_device(ram, "RAM", (0, 4095), "slave")
        
        # Crear CPU
        cpu = CPU(sysbus)
        cpu.connect_memory(ram)
        
        # Resetear CPU
        cpu.reset()
        
        # Cargar programa simple manualmente - solo LOADI 5 y HALT
        program = [
            0x9005,  # LOADI 5
            0xF000   # HALT
        ]
        
        cpu.load_program(program, 0x0000)
        
        # Verificar estado inicial
        status = cpu.get_status()
        print(f"Estado inicial - PC: {status['pc']}, AC: {status['ac']}")
        
        # Ejecutar un ciclo (fetch primera instrucción)
        cpu.running.set_value(1)
        cpu.run_cycle()
        
        # Verificar estado después de fetch y ejecución de LOADI 5
        status = cpu.get_status()
        print(f"Después de ejecutar LOADI 5 - PC: {status['pc']}, AC: {status['ac']}")
        
        if status['ac'] != "0x0005":
            print(f"✗ ERROR: AC incorrecto después de LOADI. Esperado: 0x0005, Obtenido: {status['ac']}")
            return False
        
        # Ejecutar otro ciclo (fetch y ejecutar HALT)
        cpu.run_cycle()
        
        # Verificar que se detuvo
        if cpu.running.get_value() != 0:
            print(f"✗ ERROR: CPU no se detuvo después de HALT")
            return False
        
        print(f"CPU detenida correctamente después de HALT")
        
        print("✓ Integración CPU: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ Integración CPU: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def test_full_program_execution():
    """Prueba ejecución completa del programa de prueba"""
    print("=== Prueba de Ejecución Completa ===")
    try:
        from Business.CPU_Core.CPU import CPU
        from Business.Memory.SystemBus import SystemBus
        from Business.Memory.RAM import RAM
        
        # Configurar sistema
        sysbus = SystemBus(data_width=16, addr_width=12)
        ram = RAM(4)
        
        # Conectar RAM al bus
        sysbus.connect_device(ram, "RAM", (0, 4095), "slave")
        
        # Crear CPU
        cpu = CPU(sysbus)
        cpu.connect_memory(ram)
        
        # Cargar programa desde JSON
        json_path = project_root / "Data" / "Programs" / "Test.json"
        if not json_path.exists():
            print(f"✗ ERROR: Archivo {json_path} no encontrado")
            return False
        
        ram.load_from_json(str(json_path))
        
        # Ejecutar programa completo
        print("Ejecutando programa completo...")
        cpu.run_program(start_address=0, max_cycles=50)
        
        # Verificar resultados esperados
        status = cpu.get_status()
        
        # Después del programa, AC debería tener algún valor
        # El programa hace: 5 + 3 = 8, luego AND, luego shift
        print(f"\nResultados finales:")
        print(f"  AC: {status['ac']}")
        print(f"  Instrucciones ejecutadas: {status['instructions']}")
        print(f"  Ciclos: {status['clock_cycle']}")
        
        # Leer memoria para verificar resultados
        print(f"\nVerificando memoria:")
        
        # Dirección 16 debería tener 5
        mem16 = ram.read_direct(16).get_Decimal_value()
        print(f"  [0x0010]: {mem16} (esperado: 5)")
        
        # Dirección 17 debería tener 8 (5+3)
        mem17 = ram.read_direct(17).get_Decimal_value()
        print(f"  [0x0011]: {mem17} (esperado: 8)")
        
        if mem16 != 5 or mem17 != 8:
            print(f"✗ ERROR: Valores en memoria incorrectos")
            return False
        
        print("✓ Ejecución completa: PRUEBA EXITOSA\n")
        return True
    except Exception as e:
        print(f"✗ Ejecución completa: ERROR - {e}\n")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("INICIANDO PRUEBAS CORREGIDAS DE CPU_SIMULATOR")
    print("=" * 60)
    print(f"Directorio actual: {project_root}\n")
    
    results = []
    
    # Ejecutar pruebas
    results.append(("Bit", test_bit()))
    results.append(("Bus", test_bus()))
    results.append(("RAM", test_ram()))
    results.append(("SystemBus", test_system_bus()))
    results.append(("ALU", test_alu()))
    results.append(("Control Unit", test_control_unit()))
    results.append(("CPU Integration", test_cpu_integration()))
    results.append(("Full Program", test_full_program_execution()))
    
    # Resumen
    print("=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, success in results:
        if success:
            print(f"✓ {name}: PASÓ")
            passed += 1
        else:
            print(f"✗ {name}: FALLÓ")
            failed += 1
    
    print(f"\nTotal: {passed} pasadas, {failed} falladas")
    
    if failed == 0:
        print("\n¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
    else:
        print(f"\nADVERTENCIA: {failed} prueba(s) fallaron")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)