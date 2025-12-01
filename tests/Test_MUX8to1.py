# TEST_MUX8to1.py

from Business.Basic_Components.Logic_Gates.AND_Gate import AND_Gate
from Business.Basic_Components.Logic_Gates.NOT_Gate import NOT_Gate
from Business.Basic_Components.Logic_Gates.OR_Gate import OR_Gate
from Business.Basic_Components.Bit import Bit
from Business.Basic_Components.Bus import Bus
from typing import List

# Asumo que la clase MUX8to1_1Bit corregida está disponible en el entorno
# Aquí se incluye su definición mínima para que el script sea ejecutable:
# =========================================================================
class MUX8to1_1Bit:
    # ... (código completo del MUX corregido de la respuesta anterior)
    # Por simplicidad en el test, usaremos métodos de configuración.
    
    def __init__(self):
        # Inicialización de compuertas (similar a la anterior)
        self.__Not_S0 = NOT_Gate(); self.__Not_S1 = NOT_Gate(); self.__Not_S2 = NOT_Gate()
        self.__And_Gates = [AND_Gate() for _ in range(8)]
        self.__Or_Gate = OR_Gate()
        self.__S: List[Bit] = [Bit() for _ in range(3)] 
        self.__Output = Bit()
        self.__Input = Bus(8)

    def set_Data_Inputs(self, input_bus: Bus):
        self.__Input = input_bus

    def set_Control_Inputs(self, S_bus: Bus):
        self.__S[0] = S_bus.get_Line_bit(2) 
        self.__S[1] = S_bus.get_Line_bit(1) 
        self.__S[2] = S_bus.get_Line_bit(0) 

    def get_output(self) -> Bit:
        return self.__Output

    def Calculate(self) -> Bit:
        # Lógica de cálculo (omito la reescritura de la lógica corregida)
        # Asumimos que esta función ejecuta la lógica SOP correcta.
        
        S0, S1, S2 = self.__S[0], self.__S[1], self.__S[2]

        self.__Not_S0.connect_input(S0, 0); self.__Not_S1.connect_input(S1, 0); self.__Not_S2.connect_input(S2, 0)
        self.__Not_S0.calculate(); self.__Not_S1.calculate(); self.__Not_S2.calculate()

        S0_Not = self.__Not_S0.get_output()
        S1_Not = self.__Not_S1.get_output()
        S2_Not = self.__Not_S2.get_output()

        minterm_inputs = [
            (self.__Input.get_Line_bit(0), S2_Not, S1_Not, S0_Not), (self.__Input.get_Line_bit(1), S2_Not, S1_Not, S0), 
            (self.__Input.get_Line_bit(2), S2_Not, S1, S0_Not),     (self.__Input.get_Line_bit(3), S2_Not, S1, S0),         
            (self.__Input.get_Line_bit(4), S2, S1_Not, S0_Not),     (self.__Input.get_Line_bit(5), S2, S1_Not, S0),         
            (self.__Input.get_Line_bit(6), S2, S1, S0_Not),         (self.__Input.get_Line_bit(7), S2, S1, S0)              
        ]
        
        minterm_outputs = []
        for i in range(8):
            D_i, S_C, S_B, S_A = minterm_inputs[i]
            self.__And_Gates[i].connect_input(D_i, 0); self.__And_Gates[i].connect_input(S_C, 1)
            self.__And_Gates[i].connect_input(S_B, 2); self.__And_Gates[i].connect_input(S_A, 3)
            minterm_outputs.append(self.__And_Gates[i].calculate())

        for i in range(8):
            self.__Or_Gate.connect_input(minterm_outputs[i], i)
            
        self.__Output = self.__Or_Gate.calculate()
        return self.__Output
# =========================================================================

def test_mux8to1():
    print("--- 🔬 Test de MUX 8x1 (Construido con Compuertas) ---")
    
    # 1. SETUP: Inicializar el MUX
    mux = MUX8to1_1Bit()
    
    # 2. DEFINIR ENTRADAS DE DATOS FIJAS (D0 a D7)
    # Patrón de datos: 10101010 (D0=1, D1=0, D2=1, ..., D7=0)
    # Esto asegura que podemos distinguir fácilmente si se selecciona el dato par o impar.
    data_values = [1, 0, 1, 0, 1, 0, 1, 0]
    data_bus = Bus(width=8, initial_value=0)
    for i, val in enumerate(data_values):
        data_bus.set_Line_bit(i, Bit(val))
        
    mux.set_Data_Inputs(data_bus)
    print(f"Patrón de Datos (D0-D7): {data_bus.to_Binary()} ({data_bus.get_Decimal_value()})")
    
    
    # 3. EJECUTAR TODOS LOS CASOS DE PRUEBA (S = 0 a 7)
    test_results = []
    
    for selector_decimal in range(8):
        # Convertir selector a Bus de 3 bits (S2 S1 S0)
        # S2 S1 S0 es el valor binario del selector_decimal
        control_bus = Bus(width=3, initial_value=selector_decimal)
        mux.set_Control_Inputs(control_bus)
        
        # Calcular el resultado
        output_bit = mux.Calculate()
        output_value = output_bit.get_value()
        
        # Valor esperado: es el valor de la línea Di donde i = selector_decimal
        expected_value = data_values[selector_decimal]
        
        # Verificar
        is_correct = output_value == expected_value
        status = "✅ PASÓ" if is_correct else f"❌ FALLÓ (Esperado: {expected_value}, Obtenido: {output_value})"
        
        test_results.append({
            "S": selector_decimal,
            "S_bin": control_bus.to_Binary(),
            "D_selected": f"D{selector_decimal}",
            "Expected": expected_value,
            "Actual": output_value,
            "Status": status
        })

    # 4. IMPRIMIR RESULTADOS
    all_passed = all(r["Status"].startswith("✅") for r in test_results)
    
    print("\n| Selector (S2 S1 S0) | Dato Seleccionado | Valor Esperado | Valor Obtenido | Resultado |")
    print("|:---:|:---:|:---:|:---:|:---:|")
    for result in test_results:
        print(f"| {result['S_bin']} | {result['D_selected']} | {result['Expected']} | {result['Actual']} | {result['Status']} |")

    print("\n---------------------------------------------------------")
    if all_passed:
        print("🎉 ¡TODOS LOS 8 TESTS PASARON! El MUX está funcionando correctamente según la lógica de compuertas.")
    else:
        print("🛑 ¡FALLA EN EL TEST! Revisa la lógica de conexión de las compuertas AND.")
    print("---------------------------------------------------------")

if __name__ == '__main__':
    # Nota: Ejecuta este script después de asegurarte de que tus clases Bit, Bus y Logic Gates 
    # (incluyendo la lógica N-input) estén correctamente configuradas.
    try:
        test_mux8to1()
    except Exception as e:
        print(f"\nError durante la ejecución del test: {e}")
        print("Asegúrate de que la clase MUX8to1_1Bit esté disponible y las compuertas soporten N-entradas.")