# Mapeo de Control para la Unidad Aritmético-Lógica (ALU)

Esta tabla define las señales de control de 2 bits que la **Unidad de Control (UC)** genera para configurar la ALU (Unidad Aritmética, Lógica o Desplazamiento) y su operación interna.

* **ALUop (2 bits):** Selecciona cuál de las tres unidades funcionales pasa su resultado al bus de salida.
* **ModoFunción (2 bits):** Selecciona la operación específica dentro de la unidad elegida.

| Mnemónico | Opcode (Hex) | **ALUop (2 bits)** (Unidad Seleccionada) | **ModoFunción (2 bits)** (Operación Interna) |
| :--- | :---: | :---: | :---: |
| **ADD** | 0x3 | `00` (Aritmética) | `00` (Suma / $\text{C}_{in}=0$) |
| **SUB** | 0x4 | `00` (Aritmética) | `01` (Resta / $\text{C}_{in}=1$) |
| **AND** | 0xA | `01` (Lógica) | `00` (AND) |
| **OR** | 0xB | `01` (Lógica) | `01` (OR) |
| **XOR** | 0xC | `01` (Lógica) | `10` (XOR) |
| **SLL** | 0xD | `10` (Desplazamiento) | `00` (SLL) |
| **SRA** | 0xE | `10` (Desplazamiento) | `01` (SRA) |