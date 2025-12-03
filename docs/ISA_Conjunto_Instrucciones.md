# Conjunto de Instrucciones (ISA) Simplificado

Este ISA utiliza un formato fijo de **16 bits**: 4 bits para el **Opcode** y 12 bits para el Operando/Dirección/Valor.

|Mnemónico	|Opcode (Hex)	|ALUop (2 bits) (Unidad)	|ModoFunción (3 bits) (Operación Interna)|
|-----------|---------------|---------------------------|----------------------------------------|
|ADD	    |0x3	        |00                         |000 (Suma / Cin​=0)                      |
|SUB	    |0x4	        |00                         |001 (Resta / Cin​=1)                     |
|---	    |N/A	        |00                         |010-111 (Reservado para Aritmética)     |
|---	    |---	        |---                        |---                                     |
|AND	    |0xA	        |01                         |000 (AND)                               |
|OR	        |0xB	        |01                         |001 (OR)                                |
|XOR	    |0xC	        |01                         |010 (XOR)                               |
|NOT	    |N/A	        |01                         |011 (NOT) - Unaria                      |
|---	    |N/A	        |01                         |100-111 (Reservado para Lógica)         |
|---	    |---	        |---	                    |---                                     |
|SLL	    |0xD	        |10                         |000 (SLL - Shift Left Logical)          |
|SRA	    |0xE	        |10                         |001 (SRA - Shift Right Arithmetic)      |
|ROL	    |0xF	        |10                         |010 (ROL - Rotate Left)                 |
|ROR	    |N/A	        |10                         |011 (ROR - Rotate Right)                |
|LSR	    |N/A	        |10                         |100 (LSR - Shift Right Logical)         |
|---	    |N/A	        |10                         |101-111 (Reservado para Desplazamiento) |