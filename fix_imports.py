# fix_imports.py
import os

def fix_current_issues():
    """Corrige los problemas de importación actuales"""
    
    # 1. Corregir Business/__init__.py
    business_init = os.path.join('Business', '__init__.py')
    business_content = '''"""
Paquete principal del Simulador de CPU
"""

__version__ = "0.1.0"
__author__ = "Luis"

# Importaciones principales - mantenerlas mínimas para evitar problemas
from Business.Basic_Components import Bit, Bus

__all__ = ['Bit', 'Bus']
'''
    
    with open(business_init, 'w', encoding='utf-8') as f:
        f.write(business_content)
    print("✅ Business/__init__.py corregido")
    
    # 2. Verificar que todos los __init__.py existan
    required_inits = [
        'Business/Basic_Components/__init__.py',
        'Business/Basic_Components/Logic_Gates/__init__.py',
        'Business/CPU_Core/__init__.py',
        'Business/CPU_Core/Arithmetic_Logical_Unit/__init__.py',
        'Business/CPU_Core/Arithmetic_Logical_Unit/Arithmetic_Unit/__init__.py',
        'Business/CPU_Core/Arithmetic_Logical_Unit/Logical_Unit/__init__.py',
        'Business/CPU_Core/Arithmetic_Logical_Unit/Shift_Unit/__init__.py'
    ]
    
    for init_file in required_inits:
        if not os.path.exists(init_file):
            # Crear archivo vacío si no existe
            os.makedirs(os.path.dirname(init_file), exist_ok=True)
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write("# Auto-generated init file\n\n__all__ = []")
            print(f"✅ Creado: {init_file}")

if __name__ == '__main__':
    fix_current_issues()
    print("\n🎉 Problemas de importación corregidos!")
