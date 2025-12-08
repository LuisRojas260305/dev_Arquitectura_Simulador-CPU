# Business/Memory/__init__.py
# Importaciones directas para evitar ciclos
import sys

# Importamos solo lo necesario para evitar ciclos
from .SystemBus import SystemBus
from .RAM import RAM

# Importación diferida de ROM para evitar ciclos
__all__ = ['SystemBus', 'RAM', 'ROM']

# Función para obtener ROM cuando sea necesario
def get_ROM():
    """Importa y retorna la clase ROM para evitar ciclos de importación"""
    from .ROM import ROM
    return ROM