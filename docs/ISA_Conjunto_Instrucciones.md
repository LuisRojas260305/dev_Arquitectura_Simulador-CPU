# Conjunto de Instrucciones (ISA) Estandarizado

Formato de instrucción: 16 bits = 4 bits opcode + 12 bits operando/dirección.

| Opcode (hex) | Mnemónico | ALUop (2 bits) | ModoFunción (3 bits) | Descripción | Bytes |
|--------------|-----------|----------------|----------------------|-------------|-------|
| **0x0** | NOP | -- | --- | No operación | 1 |
| **0x1** | LOAD | -- | --- | AC ← Memoria[operando] | 1 |
| **0x2** | STORE | -- | --- | Memoria[operando] ← AC | 1 |
| **0x3** | ADD | 00 | 000 | AC ← AC + Memoria[operando] | 1 |
| **0x4** | SUB | 00 | 001 | AC ← AC - Memoria[operando] | 1 |
| **0x5** | MULT | 00 | 010 | HI:LO ← AC × Memoria[operando] | 1 |
| **0x6** | DIV | 00 | 011 | LO←AC÷Memoria[operando], HI←resto | 1 |
| **0x7** | JUMP | -- | --- | PC ← operando | 1 |
| **0x8** | JZ | -- | --- | PC ← operando si Z=1 | 1 |
| **0x9** | LOADI | -- | --- | AC ← operando (inmediato) | 1 |
| **0xA** | AND | 01 | 000 | AC ← AC AND Memoria[operando] | 1 |
| **0xB** | OR | 01 | 001 | AC ← AC OR Memoria[operando] | 1 |
| **0xC** | XOR | 01 | 010 | AC ← AC XOR Memoria[operando] | 1 |
| **0xD** | SHL | 10 | 000 | AC ← AC << (operando & 0xF) | 1 |
| **0xE** | SHR | 10 | 001 | AC ← AC >> (operando & 0xF) | 1 |
| **0xF** | HALT | -- | --- | Detener CPU | 1 |

## Campos de Control ALU

### ALUop (2 bits):
- **00:** Operación Aritmética
- **01:** Operación Lógica
- **10:** Operación de Desplazamiento
- **11:** Reservado

### ModoFunción (3 bits) por categoría:

#### Aritmética (ALUop=00):
- **000:** ADD (Suma)
- **001:** SUB (Resta)
- **010:** MULT (Multiplicación - especial)
- **011:** DIV (División - especial)
- **100:** Reservado
- **101:** Reservado
- **110:** Reservado
- **111:** Reservado

#### Lógica (ALUop=01):
- **000:** AND
- **001:** OR
- **010:** XOR
- **011:** NOT (unaria, usa solo AC)
- **100-111:** Reservado

#### Desplazamiento (ALUop=10):
- **000:** SHL (Shift Left Logical)
- **001:** SHR (Shift Right Logical)
- **010:** ROL (Rotate Left)
- **011:** ROR (Rotate Right)
- **100:** ASR (Arithmetic Shift Right)
- **101-111:** Reservado