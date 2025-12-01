# auto_init_manager.py
import os
import ast
import importlib.util
from pathlib import Path

class InitFileManager:
    def __init__(self, base_dir="Business"):
        self.base_dir = Path(base_dir)
        self.excluded_files = {'__init__.py', '__pycache__', '.pytest_cache'}
        self.excluded_dirs = {'__pycache__', '.pytest_cache', 'tests'}
    
    def get_python_modules(self, directory):
        """Obtiene todos los módulos Python en un directorio"""
        modules = []
        for item in directory.iterdir():
            if item.is_file() and item.suffix == '.py' and item.name not in self.excluded_files:
                modules.append(item.stem)
        return sorted(modules)
    
    def get_existing_imports(self, init_file):
        """Lee los imports existentes de un __init__.py"""
        if not init_file.exists():
            return set(), []
        
        try:
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            existing_imports = set()
            other_lines = []
            
            # Parsear el AST para encontrar imports
            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.ImportFrom) and node.level == 1:  # Relative imports
                        for alias in node.names:
                            existing_imports.add(alias.name)
            except:
                pass
            
            # Conservar líneas personalizadas (comentarios, docstrings, etc.)
            for line in content.split('\n'):
                line_stripped = line.strip()
                if not line_stripped.startswith('from .') or '__all__' in line_stripped:
                    if line_stripped and not line_stripped.startswith('import'):
                        other_lines.append(line)
            
            return existing_imports, other_lines
        except Exception as e:
            print(f"⚠️  Error leyendo {init_file}: {e}")
            return set(), []
    
    def generate_init_content(self, modules, existing_imports, other_lines):
        """Genera el contenido del archivo __init__.py"""
        lines = []
        
        # Agregar imports que faltan
        for module in modules:
            if module not in existing_imports and not module.startswith('_'):
                lines.append(f"from .{module} import {module}")
        
        # Agregar líneas personalizadas
        if other_lines and lines:
            lines.append('')  # Línea en blanco de separación
        
        lines.extend(other_lines)
        
        # Agregar __all__ si hay módulos
        if modules:
            if not any('__all__' in line for line in lines):
                valid_modules = [m for m in modules if not m.startswith('_')]
                if valid_modules:
                    lines.append(f"\n__all__ = {sorted(valid_modules)}")
        
        return '\n'.join(lines) if lines else "# Auto-generated empty init file\n\n__all__ = []"
    
    def update_directory(self, directory):
        """Actualiza el __init__.py de un directorio específico"""
        init_file = directory / '__init__.py'
        modules = self.get_python_modules(directory)
        
        if not modules:
            # Directorio sin módulos Python, crear init vacío
            if not init_file.exists():
                init_file.write_text("# Empty directory\n\n__all__ = []", encoding='utf-8')
                print(f"📁 Init vacío creado: {init_file}")
            return
        
        existing_imports, other_lines = self.get_existing_imports(init_file)
        new_content = self.generate_init_content(modules, existing_imports, other_lines)
        
        # Escribir solo si hay cambios
        current_content = init_file.read_text(encoding='utf-8') if init_file.exists() else ""
        if current_content.strip() != new_content.strip():
            init_file.write_text(new_content, encoding='utf-8')
            print(f"✅ Actualizado: {init_file}")
            print(f"   Módulos: {modules}")
        else:
            print(f"⏭️  Sin cambios: {init_file}")
    
    def update_all(self):
        """Actualiza todos los __init__.py en el árbol"""
        print("🔄 Actualizando archivos __init__.py...")
        
        for root, dirs, files in os.walk(self.base_dir):
            root_path = Path(root)
            
            # Excluir directorios no deseados
            dirs[:] = [d for d in dirs if d not in self.excluded_dirs]
            
            # Actualizar el __init__.py de este directorio
            self.update_directory(root_path)
        
        print("\n🎉 Todos los archivos __init__.py están actualizados!")

def main():
    manager = InitFileManager()
    manager.update_all()

if __name__ == '__main__':
    main()
