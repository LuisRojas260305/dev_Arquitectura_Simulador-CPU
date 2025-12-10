# main.py
import sys
import os
from pathlib import Path

# Añadir el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importar ROM directamente desde su módulo para evitar ciclos
from Business.Memory.ROM import ROM

def clear_screen():
    """Limpia la pantalla de la terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title: str):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)

def show_banner():
    """Muestra el banner del simulador"""
    clear_screen()
    print_header("SIMULADOR DE CPU - ARQUITECTURA MODULAR")
    print("Sistema: 16-bit CPU con ALU, RAM 4K, Bus de sistema")
    print("Versión: 2.0 - Sistema modular con ensamblador")
    print("="*60)

def main_menu():
    """Menú principal del simulador"""
    # Crear instancia de ROM
    rom = ROM()
    system_assembled = False
    
    while True:
        show_banner()
        
        # Estado del sistema
        status_msg = "✓ Sistema ensamblado" if system_assembled else "✗ Sistema no ensamblado"
        print(f"\nEstado: {status_msg}")
        
        print("\nMENÚ PRINCIPAL")
        print("-"*60)
        print("1. Crear y ensamblar sistema")
        print("2. Cargar configuración del sistema")
        print("3. Listar programas disponibles")
        print("4. Cargar programa")
        print("5. Ejecutar prueba del sistema")
        print("6. Mostrar estado del sistema")
        print("7. Ejecutar programa (paso a paso)")
        print("8. Ejecutar programa (completo)")
        print("9. Ver historial de pruebas")
        print("0. Salir")
        print("-"*60)
        
        try:
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == "1":
                # Opción 1: Crear y ensamblar sistema
                print_header("CREAR Y ENSAMBLAR SISTEMA")
                
                # Preguntar por configuración personalizada
                use_custom = input("¿Usar configuración personalizada? (s/n): ").lower() == 's'
                
                config = None
                if use_custom:
                    try:
                        data_width = int(input("Ancho de datos (bits) [16]: ") or "16")
                        address_width = int(input("Ancho de dirección (bits) [12]: ") or "12")
                        ram_size = int(input("Tamaño de RAM (KB) [4]: ") or "4")
                        
                        config = {
                            'data_width': data_width,
                            'address_width': address_width,
                            'ram_size_kb': ram_size
                        }
                    except ValueError:
                        print("✗ Valores inválidos. Usando configuración por defecto.")
                
                # Crear ensamblador y ensamblar sistema
                rom.create_system_assembler(config)
                system_assembled = rom.assemble_system(verbose=True)
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "2":
                # Opción 2: Cargar configuración
                print_header("CARGAR CONFIGURACIÓN")
                
                config_name = input("Nombre del archivo de configuración [default.json]: ") or "default.json"
                config = rom.load_configuration(config_name)
                
                print(f"\n✓ Configuración cargada: {config_name}")
                print(f"  • Ancho de datos: {config.get('system', {}).get('data_width', 16)} bits")
                print(f"  • Ancho de dirección: {config.get('system', {}).get('address_width', 12)} bits")
                print(f"  • Tamaño de RAM: {config.get('system', {}).get('ram_size_kb', 4)} KB")
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "3":
                # Opción 3: Listar programas
                print_header("PROGRAMAS DISPONIBLES")
                
                programs = rom.list_programs()
                
                if not programs:
                    print("No hay programas disponibles en Data/Programs/")
                else:
                    for i, prog in enumerate(programs, 1):
                        print(f"\n{i}. {prog['name']}")
                        print(f"   Archivo: {prog['filename']}")
                        print(f"   Instrucciones: {prog.get('instructions_count', 0)}")
                        print(f"   Punto de entrada: 0x{prog.get('entry_point', 0):04X}")
                        
                        if prog.get('description'):
                            print(f"   Descripción: {prog['description']}")
                
                print("\n" + "="*60)
                input("\nPresione Enter para continuar...")
            
            elif choice == "4":
                # Opción 4: Cargar programa
                if not system_assembled:
                    print("✗ Sistema no ensamblado. Ejecute la opción 1 primero.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                print_header("CARGAR PROGRAMA")
                
                programs = rom.list_programs()
                if not programs:
                    print("No hay programas disponibles")
                    input("\nPresione Enter para continuar...")
                    continue
                
                print("\nProgramas disponibles:")
                for i, prog in enumerate(programs, 1):
                    print(f"{i}. {prog['filename']} - {prog['name']}")
                
                try:
                    selection = int(input(f"\nSeleccione programa (1-{len(programs)}): "))
                    if 1 <= selection <= len(programs):
                        selected_program = programs[selection - 1]
                        success = rom.load_program(selected_program['filename'])
                        if not success:
                            print("✗ Error cargando el programa")
                    else:
                        print("✗ Selección inválida")
                except ValueError:
                    print("✗ Entrada inválida")
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "5":
                # Opción 5: Ejecutar prueba del sistema
                if not system_assembled:
                    print("✗ Sistema no ensamblado. Ejecute la opción 1 primero.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                rom.run_system_test()
                input("\nPresione Enter para continuar...")
            
            elif choice == "6":
                # Opción 6: Mostrar estado del sistema
                if not system_assembled:
                    print("✗ Sistema no ensamblado. Ejecute la opción 1 primero.")
                else:
                    rom.print_system_status()
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "7":
                # Opción 7: Ejecutar programa paso a paso
                if not system_assembled:
                    print("✗ Sistema no ensamblado. Ejecute la opción 1 primero.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                print_header("EJECUTAR PROGRAMA (PASO A PASO)")
                
                try:
                    steps = input("Número de pasos a ejecutar [100]: ").strip()
                    steps = int(steps) if steps else 100
                    
                    rom.run_program(mode='step', steps=steps)
                except ValueError:
                    print("✗ Número inválido")
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "8":
                # Opción 8: Ejecutar programa completo
                if not system_assembled:
                    print("✗ Sistema no ensamblado. Ejecute la opción 1 primero.")
                    input("\nPresione Enter para continuar...")
                    continue
                
                print_header("EJECUTAR PROGRAMA (COMPLETO)")
                
                try:
                    max_cycles = input("Ciclos máximos [1000]: ").strip()
                    max_cycles = int(max_cycles) if max_cycles else 1000
                    
                    rom.run_program(mode='full', max_cycles=max_cycles)
                except ValueError:
                    print("✗ Número inválido")
                
                input("\nPresione Enter para continuar...")
            
            elif choice == "9":
                # Opción 9: Ver historial de pruebas
                print_header("HISTORIAL DE PRUEBAS")
                
                history = rom.get_test_history(10)
                if not history:
                    print("No hay pruebas en el historial")
                else:
                    for i, test in enumerate(history, 1):
                        timestamp = test.get('timestamp', 'Desconocido')
                        passed = test.get('passed', 0)
                        failed = test.get('failed', 0)
                        overall = test.get('overall', 'UNKNOWN')
                        
                        print(f"\nPrueba {i}: {timestamp}")
                        print(f"  Resultado: {overall}")
                        print(f"  Pasadas: {passed}, Falladas: {failed}")
                
                print("\n" + "="*60)
                input("\nPresione Enter para continuar...")
            
            elif choice == "0":
                # Opción 0: Salir
                print("\nSaliendo del simulador...")
                break
            
            else:
                print("\n✗ Opción inválida")
                input("Presione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\nOperación cancelada por el usuario")
            input("Presione Enter para continuar...")
        
        except Exception as e:
            print(f"\n✗ Error: {e}")
            input("Presione Enter para continuar...")

def main():
    """Función principal del programa"""
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nSimulador interrumpido por el usuario")
    except Exception as e:
        print(f"\nError inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()