# Conjunto de Instrucciones (ISA) Simplificado

Este ISA utiliza un formato fijo de **16 bits**: 4 bits para el **Opcode** y 12 bits para el Operando/Dirección/Valor.

| Opcode (Hex) | Mnemónico | Descripción | Unidad Funcional | Tipo de Operando |
| :---: | :---: | :--- | :--- | :--- |
| **0x1** | **LOAD addr** | Carga el dato de la dirección `addr` de la RAM en el AC. | Memoria/Transferencia | Dirección (12 bits) |
| **0x2** | **STORE addr** | Almacena el valor del AC en la dirección `addr` de la RAM. | Memoria/Transferencia | Dirección (12 bits) |
| **0x3** | **ADD addr** | Suma el dato en `addr` al AC. El resultado queda en el AC. | **ALU (Aritmética)** | Dirección (12 bits) |
| **0x4** | **SUB addr** | Resta el dato en `addr` al AC. El resultado queda en el AC. | **ALU (Aritmética)** | Dirección (12 bits) |
| **0x5** | **JUMP addr** | Cambia el PC a la dirección `addr`. | Control/Secuencia | Dirección (12 bits) |
| **0x6** | **JZ addr** | Cambia el PC a `addr` solo si el **FLAG\_Z** está activado (es 1). | Control/Secuencia | Dirección (12 bits) |
| **0x7** | **IN** | Lee un carácter desde la entrada y lo almacena en el AC. | E/S | Implícito (N/A) |
| **0x8** | **OUT** | Envía el valor del AC (ASCII) a la salida. | E/S | Implícito (N/A) |
| **0x9** | **LOADI val** | Carga un valor inmediato (`val`) directamente en el AC. | Transferencia | Valor Inmediato (12 bits) |
| **0xA** | **AND addr** | Operación lógica **AND** bit a bit: AC & RAM[addr] → AC. | **ALU (Lógica)** | Dirección (12 bits) |
| **0xB** | **OR addr** | Operación lógica **OR** bit a bit: AC $\mid$ RAM[addr] → AC. | **ALU (Lógica)** | Dirección (12 bits) |
| **0xC** | **XOR addr** | Operación lógica **XOR** bit a bit: AC $\oplus$ RAM[addr] → AC. | **ALU (Lógica)** | Dirección (12 bits) |
| **0xD** | **SLL val** | **Desplazamiento Lógico a la Izquierda** (`val` posiciones) → AC. | **ALU (Desplazamiento)** | Valor de Desplazamiento (12 bits) |
| **0xE** | **SRA val** | **Desplazamiento Aritmético a la Derecha** (`val` posiciones) → AC. | **ALU (Desplazamiento)** | Valor de Desplazamiento (12 bits) |
| **0xF** | **HALT** | Detiene la ejecución del programa. | Control/Secuencia | Implícito (N/A) |