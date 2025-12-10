# Mapeo de Control para la Unidad Aritmético-Lógica (ALU)

Esta tabla define las señales de control de 5 bits que la **Unidad de Control (UC)** genera para configurar la ALU.

* **ALUop (2 bits):** Selecciona la categoría de operación
* **ModoFunción (3 bits):** Selecciona la operación específica dentro de la categoría

## Tabla Completa de Control

| Mnemónico | Opcode | ALUop | ModoFunción | Operación |
|-----------|--------|-------|-------------|-----------|
| **ADD** | 0x3 | `00` (Aritmética) | `000` | AC + Memoria → AC |
| **SUB** | 0x4 | `00` (Aritmética) | `001` | AC - Memoria → AC |
| **MULT** | 0x5 | `00` (Aritmética) | `010` | AC × Memoria → HI:LO |
| **DIV** | 0x6 | `00` (Aritmética) | `011` | AC ÷ Memoria → LO, Resto→HI |
| **AND** | 0xA | `01` (Lógica) | `000` | AC AND Memoria → AC |
| **OR** | 0xB | `01` (Lógica) | `001` | AC OR Memoria → AC |
| **XOR** | 0xC | `01` (Lógica) | `010` | AC XOR Memoria → AC |
| **NOT** | (Instrucción especial) | `01` (Lógica) | `011` | NOT AC → AC |
| **SHL** | 0xD | `10` (Desplazamiento) | `000` | AC << n → AC |
| **SHR** | 0xE | `10` (Desplazamiento) | `001` | AC >> n → AC |
| **ROL** | (Instrucción especial) | `10` (Desplazamiento) | `010` | Rotate Left AC |
| **ROR** | (Instrucción especial) | `10` (Desplazamiento) | `011` | Rotate Right AC |

## Implementación en Hardware
