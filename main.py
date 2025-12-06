# main.py
import sys
import os
from Business.Computer_System import ComputerSystem

def print_banner():
    print("\n" + "="*60)
    print("        SIMULADOR DE CPU - ARQUITECTURA 16 BITS")
    print("="*60)

def main():
    # Crear sistema
    computer = ComputerSystem()
    
    print_banner()
    
    # Menú principal
    while True:
        print("\nMENÚ PRINCIPAL:")
        print("1. Encender sistema")
        print("2. Cargar programa desde JSON")
        print("3. Ejecutar programa")
        print("4. Ejecutar paso a paso")
        print("5. Inspeccionar memoria")
        print("6. Inspeccionar registros")
        print("7. Inspeccionar bus")
        print("8. Guardar estado")
        print("9. Cargar estado")
        print("10. Apagar sistema")
        print("0. Salir")
        
        try:
            opcion = input("\nSeleccione opción: ").strip()
            
            if opcion == "0":
                print("Saliendo del simulador...")
                break
            
            elif opcion == "1":
                computer.power_on()
            
            elif opcion == "2":
                archivo = input("Archivo JSON: ").strip()
                if os.path.exists(archivo):
                    computer.load_program(archivo)
                else:
                    print(f"Error: {archivo} no encontrado")
            
            elif opcion == "3":
                try:
                    inicio = input("Dirección inicio (hex, default=0): ").strip()
                    if inicio:
                        addr = int(inicio, 16)
                    else:
                        addr = 0
                    
                    ciclos = input("Ciclos máximos (default=100): ").strip()
                    if ciclos:
                        max_ciclos = int(ciclos)
                    else:
                        max_ciclos = 100
                    
                    computer.run(addr, max_ciclos)
                except ValueError:
                    print("Error: Entrada inválida")
            
            elif opcion == "4":
                computer.single_step()
            
            elif opcion == "5":
                try:
                    inicio = input("Dirección inicio (hex, default=0): ").strip()
                    if inicio:
                        addr = int(inicio, 16)
                    else:
                        addr = 0
                    
                    cantidad = input("Cantidad (default=16): ").strip()
                    if cantidad:
                        count = int(cantidad)
                    else:
                        count = 16
                    
                    computer.inspect_memory(addr, count)
                except ValueError:
                    print("Error: Entrada inválida")
            
            elif opcion == "6":
                computer.inspect_registers()
            
            elif opcion == "7":
                computer.inspect_bus()
            
            elif opcion == "8":
                archivo = input("Archivo para guardar: ").strip()
                computer.save_state(archivo)
            
            elif opcion == "9":
                archivo = input("Archivo a cargar: ").strip()
                computer.load_state(archivo)
            
            elif opcion == "10":
                computer.power_off()
            
            else:
                print("Opción inválida")
        
        except KeyboardInterrupt:
            print("\n\nInterrumpido por usuario")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()