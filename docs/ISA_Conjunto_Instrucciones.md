# Conjunto de Instrucciones (ISA) Estandarizado - VERSIÓN EXTENDIDA

Formato de instrucción: 16 bits = 4 bits opcode + 12 bits operando/dirección.

## Tabla Principal de Instrucciones

| Opcode (hex) | Mnemónico | Descripción | Bytes |
|--------------|-----------|-------------|-------|
| **0x0** | NOP | No operación | 1 |
| **0x1** | LOAD | AC ← Memoria[operando] | 1 |
| **0x2** | STORE | Memoria[operando] ← AC | 1 |
| **0x3** | ADD | AC ← AC + Memoria[operando] | 1 |
| **0x4** | SUB | AC ← AC - Memoria[operando] | 1 |
| **0x5** | MULT | HI:LO ← AC × Memoria[operando], AC ← LO | 1 |
| **0x6** | DIV | LO←AC÷Memoria[operando], HI←resto, AC ← LO | 1 |
| **0x7** | JUMP | PC ← operando | 1 |
| **0x8** | JZ | PC ← operando si Z=1 | 1 |
| **0x9** | LOADI | AC ← operando (inmediato) | 1 |
| **0xA** | AND | AC ← AC AND Memoria[operando] | 1 |
| **0xB** | OR | AC ← AC OR Memoria[operando] | 1 |
| **0xC** | XOR | AC ← AC XOR Memoria[operando] | 1 |
| **0xD** | SHL | AC ← AC << (operando & 0xF) | 1 |
| **0xE** | SHR | AC ← AC >> (operando & 0xF) | 1 |
| **0x10** | MOVLO | AC ← LO | 1 |
| **0x11** | MOVHI | AC ← HI | 1 |
| **0xF** | HALT | Detener CPU | 1 |

## Campos de Control ALU

### ALUop (2 bits):
- **00:** Operación Aritmética
- **01:** Operación Lógica
- **10:** Operación de Desplazamiento
- **11:** Reservado

### ModoFunción (3 bits):

#### Aritmética (ALUop=00):
- **000:** ADD (Suma)
- **001:** SUB (Resta)
- **010:** MULT (Multiplicación)
- **011:** DIV (División)
- **100-111:** Reservado

#### Lógica (ALUop=01):
- **000:** AND
- **001:** OR
- **010:** XOR
- **011:** NOT (unaria)
- **100-111:** Reservado

#### Desplazamiento (ALUop=10):
- **000:** SHL (Shift Left Logical)
- **001:** SHR (Shift Right Logical)
- **010-111:** Reservado