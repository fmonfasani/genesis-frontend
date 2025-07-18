"""
Validadores específicos para Genesis Frontend

Este módulo proporciona validaciones especializadas para frontend
siguiendo la doctrina del ecosistema genesis-frontend.

Siguiendo la doctrina:
- ✅ Se especializa solo en frontend
- ✅ No coordina workflows generales  
- ✅ Colabora con genesis-templates
- ❌ No conoce backend ni DevOps
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from .config import SUPPORTED_FRAMEWORKS, FRAMEWORK_BUILD_TOOL_COMPATIBILITY
from .exceptions import FrontendValidationError


class ValidationSeverity(str, Enum):
    """Niveles de severidad de validación"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Resultado de validación"""
    valid: bool
    errors: List[str]
    warnings: List[str]
    info: List[str]
    
    def add_error(self, message: str):
        """Agregar error"""
        self.errors.append(message)
        self.valid = False
    
    def add_warning(self, message: str):
        """Agregar advertencia"""
        self.warnings.append(message)
    
    def add_info(self, message: str):
        """Agregar información"""
        self.info.append(message)
    
    def has_issues(self) -> bool:
        """Verificar si hay issues"""
        return len(self.errors) > 0 or len(self.warnings) > 0


class FrontendProjectValidator:
    """
    Validador de proyectos frontend
    
    Valida configuraciones, nombres, dependencias y estructura
    específicamente para proyectos frontend.
    """
    
    def __init__(self):
        self.validation_rules = self._load_validation_rules()
    
    def validate_project_config(self, config: Dict[str, Any]) -> ValidationResult:
        """
        Validar configuración completa del proyecto frontend
        
        Args:
            config: Configuración del proyecto
            
        Returns:
            Resultado de validación
        """
        result = ValidationResult(valid=True, errors=[], warnings=[], info=[])
        
        # Validaciones básicas
        self._validate_basic_config(config, result)
        
        # Validar framework específico
        framework = config.get("framework", "").lower()
        if framework:
            self._validate_framework_config(framework, config, result)
        
        # Validar compatibilidades
        self._validate_compatibility(config, result)
        
        # Validar nombres y paths
        self._validate_names_and_paths(config, result)
        
        # Validar dependencias
        self._validate_dependencies(config, result)
        
        return result
    
    def _validate_basic_config(self, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración básica"""
        required_fields = ["framework", "project_name"]
        
        for field in required_fields:
            if field not in config or not config[field]:
                result.add_error(f"Campo requerido faltante: {field}")
        
        # Validar framework soportado
        framework = config.get("framework", "").lower()
        if framework and framework not in SUPPORTED_FRAMEWORKS:
            result.add_error(f"Framework no soportado: {framework}. Soportados: {SUPPORTED_FRAMEWORKS}")
        
        # Validar output_path
        output_path = config.get("output_path")
        if output_path:
            try:
                path = Path(output_path)
                if path.exists() and not path.is_dir():
                    result.add_error(f"output_path no es un directorio: {output_path}")
                elif path.exists() and any(path.iterdir()):
                    result.add_warning(f"Directorio de salida no está vacío: {output_path}")
            except Exception as e:
                result.add_error(f"output_path inválido: {e}")
    
    def _validate_framework_config(self, framework: str, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración específica del framework"""
        if framework == "nextjs":
            self._validate_nextjs_config(config, result)
        elif framework == "react":
            self._validate_react_config(config, result)
        elif framework == "vue":
            self._validate_vue_config(config, result)
        elif framework == "ui":
            self._validate_ui_config(config, result)
    
    def _validate_nextjs_config(self, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración específica de Next.js"""
        # Validar versión de Next.js
        next_version = config.get("next_version")
        if next_version and not self._is_valid_version(next_version):
            result.add_error(f"Versión de Next.js inválida: {next_version}")
        
        # Validar app_router
        app_router = config.get("app_router")
        if app_router is not None and not isinstance(app_router, bool):
            result.add_error("app_router debe ser un booleano")
        
        # Validar src_directory
        src_directory = config.get("src_directory")
        if src_directory is not None and not isinstance(src_directory, bool):
            result.add_error("src_directory debe ser un booleano")
        
        # Advertencia sobre compatibilidad
        if app_router is False:
            result.add_warning("Pages Router está en modo legacy, se recomienda App Router")
    
    def _validate_react_config(self, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración específica de React"""
        # Validar build tool
        build_tool = config.get("build_tool")
        if build_tool and build_tool not in ["vite", "webpack", "parcel"]:
            result.add_error(f"Build tool no soportado para React: {build_tool}")
        
        # Validar state management
        state_mgmt = config.get("state_management")
        react_state_options = ["redux_toolkit", "zustand", "context_api", "mobx"]
        if state_mgmt and state_mgmt not in react_state_options:
            result.add_error(f"State management no soportado para React: {state_mgmt}")
        
        # Validar routing
        routing = config.get("routing")
        if routing is not None and not isinstance(routing, bool):
            result.add_error("routing debe ser un booleano")
    
    def _validate_vue_config(self, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración específica de Vue"""
        # Validar versión de Vue
        vue_version = config.get("vue_version", "3")
        if vue_version not in ["2", "3"]:
            result.add_error(f"Versión de Vue no soportada: {vue_version}")
        
        if vue_version == "2":
            result.add_warning("Vue 2 está en modo legacy, se recomienda Vue 3")
        
        # Validar Composition API
        composition_api = config.get("composition_api")
        if composition_api is not None and not isinstance(composition_api, bool):
            result.add_error("composition_api debe ser un booleano")
        
        # Validar state management para Vue
        state_mgmt = config.get("state_management")
        vue_state_options = ["pinia", "vuex", "composition_api"]
        if state_mgmt and state_mgmt not in vue_state_options:
            result.add_error(f"State management no soportado para Vue: {state_mgmt}")
    
    def _validate_ui_config(self, config: Dict[str, Any], result: ValidationResult):
        """Validar configuración específica de UI"""
        # Validar design system
        design_system = config.get("design_system")
        valid_design_systems = ["material_design", "apple_hig", "fluent", "carbon", "custom"]
        if design_system and design_system not in valid_design_systems:
            result.add_error(f"Design system no soportado: {design_system}")
        
        # Validar color palette
        color_palette = config.get("color_palette")
        valid_palettes = ["blue", "green", "purple", "orange", "monochrome", "custom"]
        if color_palette and color_palette not in valid_palettes:
            result.add_error(f"Color palette no soportado: {color_palette}")
        
        # Validar accessibility
        accessibility = config.get("accessibility")
        if accessibility is not None and not isinstance(accessibility, bool):
            result.add_error("accessibility debe ser un booleano")
        
        if accessibility is False:
            result.add_warning("Se recomienda habilitar accesibilidad")
    
    def _validate_compatibility(self, config: Dict[str, Any], result: ValidationResult):
        """Validar compatibilidades entre opciones"""
        framework = config.get("framework", "").lower()
        build_tool = config.get("build_tool")
        
        # Validar compatibilidad framework + build tool
        if framework and build_tool:
            compatible_tools = FRAMEWORK_BUILD_TOOL_COMPATIBILITY.get(framework, [])
            if build_tool not in compatible_tools:
                result.add_error(f"Build tool '{build_tool}' no compatible con {framework}")
        
        # Validar TypeScript + framework
        typescript = config.get("typescript", False)
        if framework == "nextjs" and not typescript:
            result.add_warning("Se recomienda TypeScript para Next.js")
        
        # Validar UI library + framework
        ui_library = config.get("ui_library")
        if ui_library == "vuetify" and framework != "vue":
            result.add_error("Vuetify solo es compatible con Vue")
        elif ui_library == "material_ui" and framework not in ["react", "nextjs"]:
            result.add_error("Material UI solo es compatible con React/Next.js")
    
    def _validate_names_and_paths(self, config: Dict[str, Any], result: ValidationResult):
        """Validar nombres y rutas"""
        # Validar nombre del proyecto
        project_name = config.get("project_name", "")
        if project_name:
            name_errors = self.validate_project_name(project_name)
            for error in name_errors:
                result.add_error(error)
        
        # Validar nombres de componentes
        components = config.get("components", [])
        for component in components:
            component_name = component.get("name", "")
            if component_name and not self.validate_component_name(component_name):
                result.add_error(f"Nombre de componente inválido: {component_name}")
    
    def _validate_dependencies(self, config: Dict[str, Any], result: ValidationResult):
        """Validar dependencias del proyecto"""
        dependencies = config.get("dependencies", {})
        dev_dependencies = config.get("devDependencies", {})
        
        # Validar versiones de dependencias
        all_deps = {**dependencies, **dev_dependencies}
        for package, version in all_deps.items():
            if not self._is_valid_version(version):
                result.add_warning(f"Versión posiblemente inválida para {package}: {version}")
        
        # Verificar dependencias conflictivas
        conflicting_pairs = [
            ("styled-components", "emotion"),
            ("redux", "zustand"),
            ("vuex", "pinia")
        ]
        
        for dep1, dep2 in conflicting_pairs:
            if dep1 in all_deps and dep2 in all_deps:
                result.add_warning(f"Dependencias potencialmente conflictivas: {dep1} y {dep2}")
    
    def validate_project_name(self, name: str) -> List[str]:
        """
        Validar nombre de proyecto frontend
        
        Args:
            name: Nombre del proyecto
            
        Returns:
            Lista de errores
        """
        errors = []
        
        if not name:
            errors.append("El nombre del proyecto es requerido")
            return errors
        
        # Validar formato
        if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name):
            errors.append("El nombre debe empezar con letra minúscula, contener solo letras, números y guiones, y no terminar en guión")
        
        # Validar longitud
        if len(name) < 3:
            errors.append("El nombre debe tener al menos 3 caracteres")
        elif len(name) > 50:
            errors.append("El nombre no puede exceder 50 caracteres")
        
        # Palabras reservadas de Node.js/npm
        reserved_words = [
            'node_modules', 'public', 'src', 'build', 'dist', 'test', 'tests',
            'next', 'react', 'vue', 'angular', 'svelte', 'vite', 'webpack',
            'main', 'index', 'app', 'www', 'static', 'assets', 'config'
        ]
        
        if name.lower() in reserved_words:
            errors.append(f"'{name}' es una palabra reservada")
        
        # Validar que no empiece con punto o guión
        if name.startswith('.') or name.startswith('-'):
            errors.append("El nombre no puede empezar con punto o guión")
        
        # Validar caracteres válidos para npm
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append("El nombre solo puede contener letras minúsculas, números y guiones")
        
        return errors
    
    def validate_component_name(self, name: str) -> bool:
        """
        Validar nombre de componente frontend
        
        Args:
            name: Nombre del componente
            
        Returns:
            True si es válido
        """
        if not name:
            return False
        
        # Debe ser PascalCase
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
            return False
        
        # No debe ser palabra reservada de React/Vue
        reserved_words = [
            'React', 'Component', 'Element', 'Fragment', 'StrictMode',
            'Suspense', 'Provider', 'Consumer', 'Context', 'Ref',
            'Vue', 'VueComponent', 'App', 'Router', 'Store'
        ]
        
        return name not in reserved_words
    
    def validate_package_json(self, package_json_path: Path) -> ValidationResult:
        """
        Validar archivo package.json
        
        Args:
            package_json_path: Ruta al package.json
            
        Returns:
            Resultado de validación
        """
        result = ValidationResult(valid=True, errors=[], warnings=[], info=[])
        
        if not package_json_path.exists():
            result.add_error("package.json no encontrado")
            return result
        
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"package.json inválido: {e}")
            return result
        except Exception as e:
            result.add_error(f"Error leyendo package.json: {e}")
            return result
        
        # Validar campos requeridos
        required_fields = ["name", "version"]
        for field in required_fields:
            if field not in data:
                result.add_error(f"Campo requerido faltante en package.json: {field}")
        
        # Validar nombre del paquete
        if "name" in data:
            name_errors = self.validate_project_name(data["name"])
            for error in name_errors:
                result.add_error(f"Nombre en package.json: {error}")
        
        # Validar scripts
        scripts = data.get("scripts", {})
        expected_scripts = ["dev", "build"]
        for script in expected_scripts:
            if script not in scripts:
                result.add_warning(f"Script recomendado faltante: {script}")
        
        # Validar dependencias
        dependencies = data.get("dependencies", {})
        dev_dependencies = data.get("devDependencies", {})
        
        # Verificar dependencias duplicadas
        duplicate_deps = set(dependencies.keys()) & set(dev_dependencies.keys())
        for dep in duplicate_deps:
            result.add_warning(f"Dependencia duplicada en dependencies y devDependencies: {dep}")
        
        # Validar versiones
        all_deps = {**dependencies, **dev_dependencies}
        for package, version in all_deps.items():
            if not self._is_valid_version(version):
                result.add_warning(f"Versión posiblemente inválida: {package}@{version}")
        
        return result
    
    def validate_typescript_config(self, tsconfig_path: Path) -> ValidationResult:
        """
        Validar configuración de TypeScript
        
        Args:
            tsconfig_path: Ruta al tsconfig.json
            
        Returns:
            Resultado de validación
        """
        result = ValidationResult(valid=True, errors=[], warnings=[], info=[])
        
        if not tsconfig_path.exists():
            result.add_warning("tsconfig.json no encontrado")
            return result
        
        try:
            with open(tsconfig_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            result.add_error(f"tsconfig.json inválido: {e}")
            return result
        
        # Validar estructura básica
        if "compilerOptions" not in data:
            result.add_error("compilerOptions faltante en tsconfig.json")
            return result
        
        compiler_options = data["compilerOptions"]
        
        # Validar opciones recomendadas
        recommended_options = {
            "strict": True,
            "noEmit": True,
            "jsx": ["react-jsx", "preserve"]
        }
        
        for option, expected in recommended_options.items():
            if option not in compiler_options:
                result.add_warning(f"Opción recomendada faltante: {option}")
            elif isinstance(expected, list):
                if compiler_options[option] not in expected:
                    result.add_info(f"Opción {option} tiene valor no estándar: {compiler_options[option]}")
            elif compiler_options[option] != expected:
                result.add_info(f"Opción {option} no tiene valor recomendado: {compiler_options[option]}")
        
        return result
    
    def validate_project_structure(self, project_path: Path, framework: str) -> ValidationResult:
        """
        Validar estructura de directorios del proyecto
        
        Args:
            project_path: Ruta del proyecto
            framework: Framework utilizado
            
        Returns:
            Resultado de validación
        """
        result = ValidationResult(valid=True, errors=[], warnings=[], info=[])
        
        if not project_path.exists():
            result.add_error(f"Directorio del proyecto no existe: {project_path}")
            return result
        
        # Validar archivos base
        base_files = ["package.json"]
        for file_name in base_files:
            file_path = project_path / file_name
            if not file_path.exists():
                result.add_error(f"Archivo base faltante: {file_name}")
        
        # Validar estructura específica por framework
        if framework == "nextjs":
            self._validate_nextjs_structure(project_path, result)
        elif framework == "react":
            self._validate_react_structure(project_path, result)
        elif framework == "vue":
            self._validate_vue_structure(project_path, result)
    
        return result
    
    def _validate_nextjs_structure(self, project_path: Path, result: ValidationResult):
        """Validar estructura específica de Next.js"""
        # Verificar estructura App Router vs Pages Router
        app_dir = project_path / "app"
        pages_dir = project_path / "pages"
        
        if app_dir.exists() and pages_dir.exists():
            result.add_warning("Ambos directorios 'app' y 'pages' existen - puede causar conflictos")
        elif not app_dir.exists() and not pages_dir.exists():
            result.add_error("Falta directorio 'app' o 'pages' para Next.js")
        
        # Verificar archivos de configuración
        config_files = ["next.config.js", "next.config.mjs", "next.config.ts"]
        if not any((project_path / config).exists() for config in config_files):
            result.add_info("No se encontró archivo de configuración de Next.js")
    
    def _validate_react_structure(self, project_path: Path, result: ValidationResult):
        """Validar estructura específica de React"""
        # Verificar directorio src
        src_dir = project_path / "src"
        if not src_dir.exists():
            result.add_warning("Directorio 'src' no encontrado - no sigue convención estándar")
        
        # Verificar archivos principales
        main_files = ["src/main.tsx", "src/main.ts", "src/index.tsx", "src/index.ts"]
        if not any((project_path / main_file).exists() for main_file in main_files):
            result.add_error("Archivo principal (main.tsx/index.tsx) no encontrado")
        
        # Verificar configuración de build
        build_configs = ["vite.config.ts", "vite.config.js", "webpack.config.js"]
        if not any((project_path / config).exists() for config in build_configs):
            result.add_warning("No se encontró archivo de configuración de build")
    
    def _validate_vue_structure(self, project_path: Path, result: ValidationResult):
        """Validar estructura específica de Vue"""
        # Verificar directorio src
        src_dir = project_path / "src"
        if not src_dir.exists():
            result.add_error("Directorio 'src' es requerido para Vue")
        
        # Verificar App.vue
        app_vue = project_path / "src" / "App.vue"
        if not app_vue.exists():
            result.add_error("App.vue no encontrado en src/")
        
        # Verificar main.ts/js
        main_files = ["src/main.ts", "src/main.js"]
        if not any((project_path / main_file).exists() for main_file in main_files):
            result.add_error("Archivo principal (main.ts) no encontrado")
    
    def _is_valid_version(self, version: str) -> bool:
        """Validar formato de versión semántica"""
        if not version:
            return False
        
        # Remover prefijos comunes
        clean_version = version.lstrip('^~>=<')
        
        # Validar formato semver básico
        semver_pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$'
        return bool(re.match(semver_pattern, clean_version))
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Cargar reglas de validación"""
        return {
            "min_node_version": "16.0.0",
            "recommended_node_version": "18.0.0",
            "max_project_name_length": 50,
            "min_project_name_length": 3,
            "allowed_special_chars": ["-", "_"],
            "forbidden_prefixes": [".", "-", "_"],
            "reserved_words": [
                "node_modules", "public", "src", "build", "dist",
                "test", "tests", "main", "index", "app"
            ]
        }


class FrontendCodeValidator:
    """
    Validador de código frontend específico
    
    Valida sintaxis, patrones y mejores prácticas en código frontend.
    """
    
    def validate_typescript_code(self, code: str) -> ValidationResult:
        """
        Validar código TypeScript básico
        
        Args:
            code: Código TypeScript
            
        Returns:
            Resultado de validación
        """
        result = ValidationResult(valid=True, errors=[], warnings=[], info=[])
        
        if not code.strip():
            result.add_error("Código vacío")
            return result
        
        # Validar balance de llaves
        open_braces = code.count('{')
        close_braces = code.count('}')
        if open_braces != close_braces:
            result.add_error("Llaves no balanceadas")
        
        # Validar balance de paréntesis
        open_parens = code.count('(')
        close_parens = code.count(')')
        if open_parens != close_parens:
            result.add_error("Paréntesis no balanceados")
        
        # Verificar sintaxis básica de React/Vue
        self._validate_component_syntax(code, result)
        
        return result
    
    def _validate_component_syntax(self, code: str, result: ValidationResult):
        """Validar sintaxis básica de componentes"""
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Verificar importaciones
            if line.startswith('import') and 'from' in line:
                if not re.search(r'from\s+[\'"][^\'"]+[\'"]', line):
                    result.add_warning(f"Línea {i}: Importación posiblemente malformada")
            
            # Verificar declaraciones de función
            if 'function' in line or '=>' in line:
                if 'function' in line and not re.search(r'function\s+\w+', line):
                    result.add_info(f"Línea {i}: Función anónima detectada")
            
            # Verificar JSX básico
            if '<' in line and '>' in line:
                if not self._is_valid_jsx_line(line):
                    result.add_warning(f"Línea {i}: JSX posiblemente malformado")
    
    def _is_valid_jsx_line(self, line: str) -> bool:
        """Validar línea JSX básica"""
        # Verificaciones básicas de JSX
        jsx_patterns = [
            r'<\w+[^>]*>',  # Tag de apertura
            r'</\w+>',      # Tag de cierre
            r'<\w+[^>]*/>', # Tag auto-cerrado
        ]
        
        return any(re.search(pattern, line) for pattern in jsx_patterns)


# Instancias globales de validadores
project_validator = FrontendProjectValidator()
code_validator = FrontendCodeValidator()


def validate_frontend_project(config: Dict[str, Any]) -> ValidationResult:
    """
    Función conveniente para validar proyecto frontend
    
    Args:
        config: Configuración del proyecto
        
    Returns:
        Resultado de validación
    """
    return project_validator.validate_project_config(config)


def validate_frontend_project_name(name: str) -> List[str]:
    """
    Función conveniente para validar nombre de proyecto
    
    Args:
        name: Nombre del proyecto
        
    Returns:
        Lista de errores
    """
    return project_validator.validate_project_name(name)


def validate_frontend_component_name(name: str) -> bool:
    """
    Función conveniente para validar nombre de componente
    
    Args:
        name: Nombre del componente
        
    Returns:
        True si es válido
    """
    return project_validator.validate_component_name(name)


def validate_frontend_typescript(code: str) -> ValidationResult:
    """
    Función conveniente para validar código TypeScript
    
    Args:
        code: Código TypeScript
        
    Returns:
        Resultado de validación
    """
    return code_validator.validate_typescript_code(code)
