ESTADO_PROYECTO.md - Simulador de CPU 16-bit
ESTADO ACTUAL DEL PROYECTO

Fecha: 8 de diciembre de 2025
Última Actualización: 11:37 AM
Estado: Sistema funcional en consola - Interfaz gráfica en desarrollo
✅ COMPLETADO (Funcionalidad Core)

    Arquitectura Modular Business completamente implementada:

        Componentes básicos (Bit, Bus, Record, Logic Gates)

        CPU Core con ALU, Unidad de Control, Registros

        Sistema de memoria (RAM 4K, ROM, SystemBus)

        Ensamblador del sistema (Computer_System.py)

    Sistema de Ejecución Funcional:

        Carga de programas desde archivos JSON

        Ejecución paso a paso y completa

        Pruebas automáticas del sistema

        Manejo de configuración

    Interfaz de Consola:

        Menú principal con 10 opciones

        Visualización de estado del sistema

        Historial de pruebas y logs

🚧 EN PROGRESO (Interfaz Gráfica PyGame)

    Estructura de UI creada (carpeta Interface/)

    Módulos planificados pero no implementados:

        ui_main.py - Ventana principal

        ui_constants.py - Constantes y colores

        ui_ram_panel.py - Visualización de RAM

        ui_cpu_panel.py - Visualización de CPU

        ui_bus_panel.py - Visualización de buses

        ui_control_panel.py - Panel de control

        ui_io_panel.py - Panel E/S (teletipo y teclado)

        ui_alu_panel.py - Panel detallado de ALU

❌ PENDIENTE DE IMPLEMENTAR

    Integración PyGame con sistema Business

    Implementación real de módulos UI

    Dispositivos de E/S mapeados en memoria

    Animaciones de transferencia de datos

    Teclado virtual y teletipo funcional

ARQUITECTURA DEL SISTEMA
Componentes Business (COMPLETOS)
text

Business/
├── Basic_Components/     # Componentes fundamentales (Bit, Bus, Record)
├── CPU_Core/            # CPU, ALU, Unidad de Control
├── Memory/              # RAM, ROM, SystemBus
└── Computer_System.py   # Ensamblador principal

Interfaz Planificada (POR IMPLEMENTAR)
text

Interface/
├── ui_main.py          # Ventana principal y bucle PyGame
├── ui_constants.py     # Colores, dimensiones, configuraciones
├── ui_ram_panel.py     # Panel de visualización de RAM (4096 slots)
├── ui_cpu_panel.py     # Panel de CPU (registros, ALU, UC)
├── ui_bus_panel.py     # Panel de buses (address, data, control)
├── ui_control_panel.py # Panel de control (botones, programas)
├── ui_io_panel.py      # Panel E/S (teletipo + teclado)
├── ui_alu_panel.py     # Panel detallado de ALU
├── ui_components.py    # Componentes UI base
├── ui_memory_view.py   # Vista detallada de memoria
└── ui_system_monitor.py # Monitor del sistema

PLAN DE IMPLEMENTACIÓN (FASES)
FASE 1: Estructura Base (2-3 días)

    ✅ Crear estructura de carpetas Interface/

    🚧 Implementar ui_constants.py con paleta de colores verde/negro

    ❌ Crear ui_main.py con bucle principal PyGame

    ❌ Panel de RAM básico con scroll

    ❌ Integración mínima con sistema Business

FASE 2: Paneles Básicos (3-4 días)

    ❌ Panel de CPU mostrando registros

    ❌ Panel de control con botones funcionales

    ❌ Panel de buses con visualización básica

    ❌ Conexión completa entre UI y sistema

FASE 3: Visualización Avanzada (3-4 días)

    ❌ Animaciones de transferencia en buses

    ❌ Panel de ALU detallado

    ❌ Panel de E/S con teletipo funcional

    ❌ Sistema de teclado virtual

FASE 4: Integración Completa (2-3 días)

    ❌ Dispositivos E/S mapeados en memoria

    ❌ Teclado físico integrado

    ❌ Persistencia de configuración

    ❌ Exportación de estados

PALETA DE COLORES DEFINIDA
python

# Tema: Terminal verde sobre negro (estilo CRT)
BACKGROUND:  "#000000"  # Negro puro
TONE_1:      "#003300"  # Verde muy oscuro
TONE_2:      "#006600"  # Verde oscuro
TONE_3:      "#009900"  # Verde medio (texto principal)
TONE_4:      "#00CC00"  # Verde brillante intermedio
TONE_5:      "#00FF00"  # Verde fósforo (máximo brillo)

# Colores de resaltado
HIGHLIGHT_PC:    "#FF9900"   # Naranja para Program Counter
HIGHLIGHT_MAR:   "#FF6600"   # Naranja oscuro para MAR
HIGHLIGHT_READ:  "#00FF99"   # Verde cian para lecturas
HIGHLIGHT_WRITE: "#FF0099"   # Rosa para escrituras

LAYOUT DE INTERFAZ
text

┌────────────────────────────────────────────────────────────┐
│  SIMULADOR CPU 16-bits                      [X] [-] [□]    │
├─────────────┬─────────────┬────────────────────────────────┤
│             │             │                                │
│   CPU       │   BUSES     │         MEMORIA RAM           │
│ (300x400)   │ (300x400)   │        (680x400)              │
│             │             │    Scroll: 4096 direcciones   │
├─────────────┴─────────────┴────────────────────────────────┤
│                                                              │
│                   CONTROL Y PROGRAMAS                       │
│               Botones, lista programas, estado              │
│                    (1280x150)                               │
├────────────────────────────────────────────────────────────┤
│                                                              │
│                   ENTRADA/SALIDA                            │
│            Teletipo (80x24) + Teclado virtual               │
│                    (1280x250)                               │
└────────────────────────────────────────────────────────────┘

INTEGRACIÓN CON SISTEMA EXISTENTE
Conexión Business ↔ UI

El sistema Business (Computer_System.py) ya está funcional. La UI debe:

    Obtener referencia al objeto System ensamblado

    Suscribirse a eventos de cambio de estado

    Actualizar visualización en tiempo real

    Enviar comandos de control (run/stop/step)

Modificación en main.py
python

# Añadir opción 10 al menú principal
elif choice == "10":
    if not system_assembled:
        print("✗ Sistema no ensamblado")
    else:
        from Interface.ui_main import SimulatorUI
        ui = SimulatorUI(rom.assembler)
        ui.run()

DISPOSITIVOS DE E/S MAPEADOS (PROPUESTA)
Mapa de memoria para E/S:
python

IO_MAP = {
    'KEYBOARD_DATA':   0xFF00,   # Dato del teclado (lectura)
    'KEYBOARD_STATUS': 0xFF01,   # Estado del teclado (1=datos)
    'SCREEN_DATA':     0xFF02,   # Dato para pantalla (escritura)
    'SCREEN_CONTROL':  0xFF03,   # Control de pantalla
    'INTERRUPT_ENABLE':0xFF04,   # Habilitar interrupciones
}

Comportamiento:

    Teclado: Eventos PyGame → buffer → CPU lo lee

    Pantalla: CPU escribe → buffer → UI muestra en teletipo

    Interrupciones: Opcional para I/O asíncrono

PRÓXIMOS PASOS INMEDIATOS
DÍA 1 (Prioridad Máxima):

    Implementar ui_constants.py con toda la paleta de colores

    Crear ui_main.py con bucle PyGame funcional

    Implementar ui_ram_panel.py básico (sin scroll)

    Conectar UI con sistema Business existente

DÍA 2:

    Completar panel de RAM con scroll y resaltado

    Implementar panel de CPU con registros básicos

    Crear panel de control con botones run/stop/step

    Integrar en menú principal (opción 10)

DÍA 3:

    Implementar panel de buses con visualización

    Crear panel de E/S con teletipo básico

    Añadir dispositivos E/S mapeados

    Pruebas de integración completas

DESAFÍOS TÉCNICOS IDENTIFICADOS

    Rendimiento: Renderizar 4096 direcciones de RAM a 60 FPS

    Sincronización: Coordinar UI con ciclos de CPU

    Eventos: Manejar entrada de teclado para CPU y UI

    Arquitectura: Patrón Observer para actualizaciones de estado

    Memoria: Buffer de teletipo para historial de salida

DEPENDENCIAS NECESARIAS
bash

# Ya instaladas:
# - Python 3.8+
# - Sistema Business completo

# Por instalar:
pip install pygame>=2.5.0
pip install numpy>=1.21.0  # (opcional, para animaciones)

ESTADO DE ARCHIVOS UI (Interface/)
✅ Creados (vacíos/estructura):

    __init__.py

    ui_alu_panel.py

    ui_bus_panel.py

    ui_components.py

    ui_constants.py

    ui_control_panel.py

    ui_cpu_panel.py

    ui_io_panel.py

    ui_main.py

    ui_memory_view.py

    ui_ram_panel.py

    ui_system_monitor.py

❌ Por implementar (contenido real):

Todos los archivos necesitan implementación completa.
INSTRUCCIONES PARA EL NUEVO CHAT
Contexto a proporcionar:

    Este archivo ESTADO_PROYECTO.md

    El file tree completo del proyecto

    Archivos clave: main.py, Computer_System.py, Record.py, Test.json

    Especificar: "Continuar implementación de interfaz PyGame para simulador CPU"

Primera tarea solicitada:
text

Implementar ui_constants.py con la paleta de colores verde/negro y 
ui_main.py con el bucle básico de PyGame que muestre una ventana 
con el layout planeado y paneles vacíos.

Requisitos específicos:

    Mantener compatibilidad con sistema Business existente

    Usar patrón Observer para actualizaciones

    Optimizar renderizado para 60 FPS

    Priorizar funcionalidad sobre estética inicial

    Seguir estructura modular planificada

PUNTOS DE INTEGRACIÓN CRÍTICOS

    System → UI: Estado de CPU, RAM, buses, registros

    UI → System: Comandos de control (run/stop/step/reset)

    E/S: Teclado PyGame → buffer → CPU

    E/S: CPU → buffer → teletipo PyGame

ÚLTIMA ACTUALIZACIÓN: 8/12/2025, 11:37 AM
PRÓXIMA REVISIÓN: Al completar Fase 1 (día 3)
CONTACTO: Luis @ Dev Team
PRIORIDAD: ALTA (entrega en 1-2 días)