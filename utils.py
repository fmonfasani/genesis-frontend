"""
Utilidades para Genesis Frontend

Este módulo contiene funciones de utilidad específicas para la generación
de frontend en el ecosistema Genesis.

Siguiendo la doctrina del ecosistema genesis-frontend:
- Se especializa solo en frontend
- Colabora con genesis-templates  
- No coordina workflows generales
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
import hashlib
import subprocess
import shutil
from dataclasses import asdict

from .config import config, SUPPORTED_FRAMEWORKS, DEV_SERVER_DEFAULTS
from .exceptions import FrontendValidationError, FrontendGenerationError


def validate_project_name(name: str) -> List[str]:
    """
    Validar nombre de proyecto frontend
    
    Args:
        name: Nombre del proyecto
        
    Returns:
        Lista de errores de validación
    """
    errors = []
    
    if not name:
        errors.append("El nombre del proyecto es requerido")
        return errors
    
    if not re.match(r'^[a-z][a-z0-9-]*$', name):
        errors.append("El nombre debe empezar con letra minúscula y contener solo letras, números y guiones")
    
    if len(name) > 50:
        errors.append("El nombre no puede exceder 50 caracteres")
    
    if len(name) < 3:
        errors.append("El nombre debe tener al menos 3 caracteres")
    
    # Palabras reservadas
    reserved_words = ['node_modules', 'public', 'src', 'build', 'dist', 'test', 'tests']
    if name.lower() in reserved_words:
        errors.append(f"'{name}' es una palabra reservada")
    
    return errors


def validate_framework_config(framework: str, params: Dict[str, Any]) -> List[str]:
    """
    Validar configuración de framework
    
    Args:
        framework: Nombre del framework
        params: Parámetros de configuración
        
    Returns:
        Lista de errores de validación
    """
    errors = []
    
    # Validar framework soportado
    if framework not in SUPPORTED_FRAMEWORKS:
        errors.append(f"Framework '{framework}' no soportado. Soportados: {SUPPORTED_FRAMEWORKS}")
        return errors
    
    # Validar output_path
    output_path = params.get("output_path")
    if output_path:
        try:
            path = Path(output_path)
            if path.exists() and not path.is_dir():
                errors.append("output_path debe ser un directorio")
        except Exception:
            errors.append("output_path no es una ruta válida")
    
    # Validaciones específicas del framework
    framework_errors = config.validate_framework_compatibility(framework, params)
    errors.extend(framework_errors)
    
    return errors


def generate_file_hash(content: str) -> str:
    """
    Generar hash MD5 para contenido de archivo
    
    Args:
        content: Contenido del archivo
        
    Returns:
        Hash MD5 hexadecimal
    """
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def ensure_directory_exists(path: Union[str, Path]) -> Path:
    """
    Asegurar que un directorio existe
    
    Args:
        path: Ruta del directorio
        
    Returns:
        Path object del directorio
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def safe_file_write(file_path: Union[str, Path], content: str, encoding: str = 'utf-8') -> bool:
    """
    Escribir archivo de forma segura
    
    Args:
        file_path: Ruta del archivo
        content: Contenido a escribir
        encoding: Codificación del archivo
        
    Returns:
        True si se escribió correctamente
        
    Raises:
        FrontendGenerationError: Si hay error escribiendo
    """
    try:
        path = Path(file_path)
        ensure_directory_exists(path.parent)
        
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        
        return True
    except Exception as e:
        raise FrontendGenerationError(f"Error escribiendo archivo {file_path}: {e}")


def read_json_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Leer archivo JSON de forma segura
    
    Args:
        file_path: Ruta del archivo JSON
        
    Returns:
        Contenido del archivo como diccionario
        
    Raises:
        FrontendGenerationError: Si hay error leyendo
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FrontendGenerationError(f"Archivo no encontrado: {file_path}")
    except json.JSONDecodeError as e:
        raise FrontendGenerationError(f"Error decodificando JSON en {file_path}: {e}")
    except Exception as e:
        raise FrontendGenerationError(f"Error leyendo archivo {file_path}: {e}")


def write_json_file(file_path: Union[str, Path], data: Dict[str, Any], indent: int = 2) -> bool:
    """
    Escribir archivo JSON de forma segura
    
    Args:
        file_path: Ruta del archivo
        data: Datos a escribir
        indent: Indentación del JSON
        
    Returns:
        True si se escribió correctamente
    """
    content = json.dumps(data, indent=indent, ensure_ascii=False)
    return safe_file_write(file_path, content)


def merge_package_json(base_package: Dict[str, Any], additional_deps: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fusionar dependencias en package.json
    
    Args:
        base_package: package.json base
        additional_deps: Dependencias adicionales
        
    Returns:
        package.json fusionado
    """
    merged = base_package.copy()
    
    # Fusionar dependencies
    if "dependencies" in additional_deps:
        if "dependencies" not in merged:
            merged["dependencies"] = {}
        merged["dependencies"].update(additional_deps["dependencies"])
    
    # Fusionar devDependencies
    if "devDependencies" in additional_deps:
        if "devDependencies" not in merged:
            merged["devDependencies"] = {}
        merged["devDependencies"].update(additional_deps["devDependencies"])
    
    # Fusionar scripts
    if "scripts" in additional_deps:
        if "scripts" not in merged:
            merged["scripts"] = {}
        merged["scripts"].update(additional_deps["scripts"])
    
    return merged


def check_node_version() -> Tuple[bool, str]:
    """
    Verificar versión de Node.js instalada
    
    Returns:
        (is_valid, version_string)
    """
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            # Verificar que sea una versión soportada (>= 16)
            version_num = int(version.replace('v', '').split('.')[0])
            return version_num >= 16, version
        return False, "No instalado"
    except Exception:
        return False, "Error verificando"


def check_package_manager(preferred: str = "npm") -> Tuple[bool, str]:
    """
    Verificar gestor de paquetes disponible
    
    Args:
        preferred: Gestor preferido (npm, yarn, pnpm, bun)
        
    Returns:
        (is_available, manager_name)
    """
    managers = [preferred, "npm", "yarn", "pnpm", "bun"]
    
    for manager in managers:
        try:
            result = subprocess.run([manager, '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True, manager
        except Exception:
            continue
    
    return False, "ninguno"


def format_dependency_version(package: str, version: str) -> str:
    """
    Formatear versión de dependencia
    
    Args:
        package: Nombre del paquete
        version: Versión
        
    Returns:
        Versión formateada (ej: "^1.0.0")
    """
    if version.startswith('^') or version.startswith('~') or version.startswith('>='):
        return version
    
    # Para versiones estables, usar ^
    if re.match(r'^\d+\.\d+\.\d+$', version):
        return f"^{version}"
    
    return version


def generate_gitignore(framework: str, additional_patterns: List[str] = None) -> str:
    """
    Generar .gitignore para proyecto frontend
    
    Args:
        framework: Nombre del framework
        additional_patterns: Patrones adicionales
        
    Returns:
        Contenido del .gitignore
    """
    base_patterns = [
        "# Dependencies",
        "node_modules/",
        "/.pnp",
        ".pnp.js",
        "",
        "# Testing",
        "/coverage",
        "",
        "# Production",
        "/build",
        "/dist",
        "",
        "# Environment variables",
        ".env",
        ".env.local",
        ".env.development.local",
        ".env.test.local",
        ".env.production.local",
        "",
        "# Logs",
        "npm-debug.log*",
        "yarn-debug.log*",
        "yarn-error.log*",
        "lerna-debug.log*",
        "",
        "# Runtime data",
        "pids",
        "*.pid",
        "*.seed",
        "*.pid.lock",
        "",
        "# IDE",
        ".vscode/",
        ".idea/",
        "*.swp",
        "*.swo",
        "*~",
        "",
        "# OS",
        ".DS_Store",
        ".DS_Store?",
        "._*",
        ".Spotlight-V100",
        ".Trashes",
        "ehthumbs.db",
        "Thumbs.db",
    ]
    
    # Patrones específicos por framework
    if framework == "nextjs":
        base_patterns.extend([
            "",
            "# Next.js",
            ".next/",
            "out/",
            "",
            "# Vercel",
            ".vercel",
        ])
    elif framework == "react":
        base_patterns.extend([
            "",
            "# React",
            "build/",
        ])
    elif framework == "vue":
        base_patterns.extend([
            "",
            "# Vue",
            "dist/",
            ".cache/",
        ])
    
    # Agregar patrones adicionales
    if additional_patterns:
        base_patterns.extend(["", "# Additional patterns"] + additional_patterns)
    
    return "\n".join(base_patterns)


def create_directory_structure(base_path: Path, framework: str) -> List[str]:
    """
    Crear estructura de directorios para un framework
    
    Args:
        base_path: Ruta base del proyecto
        framework: Nombre del framework
        
    Returns:
        Lista de directorios creados
    """
    directories = config.get_directory_structure(framework)
    created = []
    
    for directory in directories:
        dir_path = base_path / directory
        if ensure_directory_exists(dir_path):
            created.append(str(dir_path))
    
    return created


def extract_dependencies_from_content(content: str) -> List[str]:
    """
    Extraer dependencias de imports en código
    
    Args:
        content: Contenido del archivo
        
    Returns:
        Lista de dependencias encontradas
    """
    dependencies = set()
    
    # Buscar imports de ES6
    import_patterns = [
        r"import\s+.*?\s+from\s+['\"]([^'\"]+)['\"]",
        r"import\s+['\"]([^'\"]+)['\"]",
        r"require\(['\"]([^'\"]+)['\"]\)",
    ]
    
    for pattern in import_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            # Filtrar imports relativos
            if not match.startswith('.') and not match.startswith('/'):
                # Extraer nombre del paquete (sin subpaths)
                package_name = match.split('/')[0]
                if package_name.startswith('@'):
                    # Scoped package
                    parts = match.split('/')
                    if len(parts) > 1:
                        package_name = f"{parts[0]}/{parts[1]}"
                dependencies.add(package_name)
    
    return sorted(list(dependencies))


def get_dev_server_config(framework: str, custom_port: Optional[int] = None) -> Dict[str, Any]:
    """
    Obtener configuración del servidor de desarrollo
    
    Args:
        framework: Nombre del framework
        custom_port: Puerto personalizado
        
    Returns:
        Configuración del servidor
    """
    defaults = DEV_SERVER_DEFAULTS.get(framework, {"port": 3000, "host": "localhost"})
    
    config = defaults.copy()
    if custom_port:
        config["port"] = custom_port
    
    return config


def generate_env_template(framework: str, api_url: str = "http://localhost:8000") -> str:
    """
    Generar template de variables de entorno
    
    Args:
        framework: Nombre del framework
        api_url: URL base de la API
        
    Returns:
        Contenido del archivo .env
    """
    if framework == "nextjs":
        return f"""# Next.js Environment Variables
NEXT_PUBLIC_API_URL={api_url}
NEXT_PUBLIC_APP_NAME=Genesis App
NEXT_PUBLIC_APP_VERSION=1.0.0

# Database (if using)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Authentication (if using)
# NEXTAUTH_SECRET=your-secret-here
# NEXTAUTH_URL=http://localhost:3000

# External APIs
# STRIPE_SECRET_KEY=sk_test_...
# STRIPE_PUBLISHABLE_KEY=pk_test_...
"""
    elif framework == "react":
        return f"""# React Environment Variables
REACT_APP_API_URL={api_url}
REACT_APP_NAME=Genesis App
REACT_APP_VERSION=1.0.0

# External APIs
# REACT_APP_GOOGLE_MAPS_API_KEY=your-key-here
# REACT_APP_FIREBASE_API_KEY=your-key-here
"""
    elif framework == "vue":
        return f"""# Vue Environment Variables
VITE_API_URL={api_url}
VITE_APP_NAME=Genesis App
VITE_APP_VERSION=1.0.0

# External APIs
# VITE_GOOGLE_MAPS_API_KEY=your-key-here
# VITE_FIREBASE_API_KEY=your-key-here
"""
    else:
        return f"""# Environment Variables
API_URL={api_url}
APP_NAME=Genesis App
APP_VERSION=1.0.0
"""


def sanitize_component_name(name: str) -> str:
    """
    Sanitizar nombre de componente para que sea válido
    
    Args:
        name: Nombre original
        
    Returns:
        Nombre sanitizado
    """
    # Remover caracteres no válidos
    sanitized = re.sub(r'[^a-zA-Z0-9]', '', name)
    
    # Asegurar que empiece con mayúscula
    if sanitized:
        sanitized = sanitized[0].upper() + sanitized[1:]
    
    # Si queda vacío, usar default
    if not sanitized:
        sanitized = "MyComponent"
    
    return sanitized


def format_file_size(size_bytes: int) -> str:
    """
    Formatear tamaño de archivo en formato legible
    
    Args:
        size_bytes: Tamaño en bytes
        
    Returns:
        Tamaño formateado (ej: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def is_valid_npm_package_name(name: str) -> bool:
    """
    Verificar si un nombre es válido para package npm
    
    Args:
        name: Nombre del paquete
        
    Returns:
        True si es válido
    """
    # Reglas de npm para nombres de paquetes
    if len(name) > 214:
        return False
    
    if not re.match(r'^[a-z0-9]([a-z0-9\-_\.])*$', name):
        return False
    
    # No puede empezar con . o _
    if name.startswith('.') or name.startswith('_'):
        return False
    
    return True


def extract_schema_entities(schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extraer entidades del schema del proyecto
    
    Args:
        schema: Schema del proyecto
        
    Returns:
        Lista de entidades con sus propiedades
    """
    entities = []
    
    # Buscar entidades en diferentes ubicaciones del schema
    if "entities" in schema:
        entities = schema["entities"]
    elif "models" in schema:
        entities = schema["models"]
    elif "database" in schema and "entities" in schema["database"]:
        entities = schema["database"]["entities"]
    
    return entities if isinstance(entities, list) else []


def validate_typescript_syntax(code: str) -> Dict[str, Any]:
    """
    Validar sintaxis básica de TypeScript
    
    Args:
        code: Código TypeScript a validar
        
    Returns:
        Resultado de validación
    """
    validation = {
        "valid": True,
        "errors": [],
        "warnings": []
    }
    
    # Verificar balance de llaves
    open_braces = code.count('{')
    close_braces = code.count('}')
    if open_braces != close_braces:
        validation["valid"] = False
        validation["errors"].append("Llaves no balanceadas")
    
    # Verificar interfaces básicas
    interface_pattern = r'interface\s+(\w+)\s*{'
    interfaces = re.findall(interface_pattern, code)
    for interface_name in interfaces:
        if not interface_name[0].isupper():
            validation["warnings"].append(f"Interface '{interface_name}' debería empezar con mayúscula")
    
    # Verificar imports
    import_pattern = r"import\s+.*?from\s+['\"]([^'\"]+)['\"]"
    imports = re.findall(import_pattern, code)
    for imp in imports:
        if imp.startswith('./') or imp.startswith('../'):
            # Import relativo - verificar extensión
            if not imp.endswith('.tsx') and not imp.endswith('.ts') and '.' in imp:
                validation["warnings"].append(f"Import relativo '{imp}' podría necesitar extensión")
    
    return validation


def optimize_component_imports(code: str) -> str:
    """
    Optimizar imports de componentes
    
    Args:
        code: Código con imports
        
    Returns:
        Código optimizado
    """
    # Agrupar imports por tipo
    react_imports = []
    external_imports = []
    relative_imports = []
    
    import_pattern = r"import\s+(.*?)\s+from\s+['\"]([^'\"]+)['\"]"
    imports = re.findall(import_pattern, code)
    
    for import_content, import_path in imports:
        if import_path == 'react':
            react_imports.append(f"import {import_content} from 'react'")
        elif import_path.startswith('./') or import_path.startswith('../'):
            relative_imports.append(f"import {import_content} from '{import_path}'")
        else:
            external_imports.append(f"import {import_content} from '{import_path}'")
    
    # Remover imports originales
    code_without_imports = re.sub(import_pattern, '', code)
    
    # Reorganizar imports
    optimized_imports = []
    if react_imports:
        optimized_imports.extend(react_imports)
        optimized_imports.append("")
    
    if external_imports:
        optimized_imports.extend(sorted(external_imports))
        optimized_imports.append("")
    
    if relative_imports:
        optimized_imports.extend(sorted(relative_imports))
        optimized_imports.append("")
    
    return '\n'.join(optimized_imports) + code_without_imports.strip()


def generate_component_test(component_name: str, framework: str) -> str:
    """
    Generar test básico para componente
    
    Args:
        component_name: Nombre del componente
        framework: Framework usado
        
    Returns:
        Código del test
    """
    if framework in ["nextjs", "react"]:
        return f"""import {{ render, screen }} from '@testing-library/react'
import {component_name} from './{component_name}'

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />)
    expect(screen.getByRole('main')).toBeInTheDocument()
  }})
  
  it('displays correct content', () => {{
    render(<{component_name} />)
    // Add specific assertions here
  }})
}})
"""
    elif framework == "vue":
        return f"""import {{ describe, it, expect }} from 'vitest'
import {{ mount }} from '@vue/test-utils'
import {component_name} from './{component_name}.vue'

describe('{component_name}', () => {{
  it('renders properly', () => {{
    const wrapper = mount({component_name})
    expect(wrapper.exists()).toBe(true)
  }})
  
  it('displays correct content', () => {{
    const wrapper = mount({component_name})
    // Add specific assertions here
  }})
}})
"""
    else:
        return f"// Test for {component_name} - {framework} not supported yet"


def get_framework_specific_config(framework: str) -> Dict[str, Any]:
    """
    Obtener configuración específica del framework
    
    Args:
        framework: Nombre del framework
        
    Returns:
        Configuración específica
    """
    framework_configs = {
        "nextjs": {
            "file_extensions": [".tsx", ".ts", ".jsx", ".js"],
            "config_files": ["next.config.js", "next.config.mjs"],
            "special_dirs": ["app", "pages", "public", ".next"],
            "dev_command": "npm run dev",
            "build_command": "npm run build",
            "type_checking": "npm run type-check"
        },
        "react": {
            "file_extensions": [".tsx", ".ts", ".jsx", ".js"],
            "config_files": ["vite.config.ts", "webpack.config.js"],
            "special_dirs": ["src", "public", "build", "dist"],
            "dev_command": "npm run dev",
            "build_command": "npm run build",
            "type_checking": "npm run type-check"
        },
        "vue": {
            "file_extensions": [".vue", ".ts", ".js"],
            "config_files": ["vite.config.ts", "vue.config.js"],
            "special_dirs": ["src", "public", "dist"],
            "dev_command": "npm run dev",
            "build_command": "npm run build",
            "type_checking": "npm run type-check"
        }
    }
    
    return framework_configs.get(framework, {})


def calculate_bundle_impact(dependencies: List[str]) -> Dict[str, Any]:
    """
    Calcular impacto estimado en el bundle de las dependencias
    
    Args:
        dependencies: Lista de dependencias
        
    Returns:
        Análisis de impacto en el bundle
    """
    # Tamaños aproximados de librerías comunes (en KB)
    library_sizes = {
        "react": 45,
        "react-dom": 130,
        "next": 0,  # Next.js optimiza automáticamente
        "vue": 40,
        "@vue/reactivity": 20,
        "lodash": 70,
        "moment": 230,
        "date-fns": 20,
        "axios": 15,
        "tailwindcss": 0,  # CSS, no JS
        "styled-components": 25,
        "@emotion/react": 30,
        "framer-motion": 120,
        "three": 600,
        "chart.js": 200,
    }
    
    total_size = 0
    heavy_dependencies = []
    recommendations = []
    
    for dep in dependencies:
        size = library_sizes.get(dep, 50)  # Default 50KB
        total_size += size
        
        if size > 100:
            heavy_dependencies.append({"name": dep, "size": size})
        
        # Recomendaciones específicas
        if dep == "moment":
            recommendations.append("Considera usar date-fns en lugar de moment para reducir bundle size")
        elif dep == "lodash":
            recommendations.append("Importa funciones específicas de lodash: import { debounce } from 'lodash'")
        elif dep == "three":
            recommendations.append("Three.js es pesado, considera lazy loading para componentes 3D")
    
    return {
        "total_estimated_size": total_size,
        "heavy_dependencies": heavy_dependencies,
        "recommendations": recommendations,
        "performance_impact": "high" if total_size > 500 else "medium" if total_size > 200 else "low"
    }
