"""
Frontend-specific validation utilities

Validaciones específicas para generación frontend siguiendo la doctrina:
- Se especializa solo en frontend
- No duplica validaciones generales del ecosistema
- Valida aspectos específicos de frameworks frontend
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from ..exceptions import FrontendValidationError, FrameworkNotSupportedError
from ..config import SUPPORTED_FRAMEWORKS, FRAMEWORK_BUILD_TOOL_COMPATIBILITY


class ValidationSeverity(str, Enum):
    """Severidad de validación"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    """Resultado de validación"""
    severity: ValidationSeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    suggestion: Optional[str] = None
    code: Optional[str] = None


class FrontendValidator:
    """
    Validador específico para proyectos frontend
    
    Valida aspectos específicos de frontend como:
    - Configuración de frameworks
    - Estructura de componentes
    - Dependencias y compatibilidad
    - Sintaxis de código frontend
    - Mejores prácticas frontend
    """
    
    def __init__(self):
        self.results: List[ValidationResult] = []
        
        # Patrones de validación
        self.component_patterns = self._load_component_patterns()
        self.dependency_rules = self._load_dependency_rules()
        self.framework_rules = self._load_framework_rules()
    
    def validate_project_config(self, config: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validar configuración de proyecto frontend
        
        Args:
            config: Configuración del proyecto
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        # Validar framework
        framework = config.get("framework")
        if not framework:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Framework no especificado",
                suggestion="Especificar un framework soportado: nextjs, react, vue"
            ))
        elif framework not in SUPPORTED_FRAMEWORKS:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message=f"Framework '{framework}' no soportado",
                suggestion=f"Usar uno de: {', '.join(SUPPORTED_FRAMEWORKS)}"
            ))
        
        # Validar compatibilidad build tool
        build_tool = config.get("build_tool")
        if framework and build_tool:
            compatible_tools = FRAMEWORK_BUILD_TOOL_COMPATIBILITY.get(framework, [])
            if build_tool not in compatible_tools:
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message=f"Build tool '{build_tool}' puede no ser compatible con {framework}",
                    suggestion=f"Considerar usar: {', '.join(compatible_tools)}"
                ))
        
        # Validar TypeScript
        typescript = config.get("typescript", False)
        if framework == "nextjs" and not typescript:
            results.append(ValidationResult(
                severity=ValidationSeverity.WARNING,
                message="TypeScript no habilitado para Next.js",
                suggestion="Se recomienda usar TypeScript con Next.js para mejor DX"
            ))
        
        # Validar nombre del proyecto
        project_name = config.get("project_name") or config.get("name")
        if project_name:
            name_errors = self.validate_project_name(project_name)
            results.extend(name_errors)
        
        return results
    
    def validate_project_name(self, name: str) -> List[ValidationResult]:
        """
        Validar nombre de proyecto frontend
        
        Args:
            name: Nombre del proyecto
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        if not name:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Nombre del proyecto requerido"
            ))
            return results
        
        # Validar caracteres
        if not re.match(r'^[a-z][a-z0-9-]*$', name):
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Nombre debe empezar con letra minúscula y contener solo letras, números y guiones",
                suggestion="Ejemplo: my-awesome-app"
            ))
        
        # Validar longitud
        if len(name) > 50:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Nombre no puede exceder 50 caracteres"
            ))
        
        if len(name) < 3:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Nombre debe tener al menos 3 caracteres"
            ))
        
        # Palabras reservadas
        reserved_words = {
            'node_modules', 'public', 'src', 'build', 'dist', 'test', 'tests',
            'package', 'next', 'react', 'vue', 'components', 'pages', 'app'
        }
        
        if name.lower() in reserved_words:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message=f"'{name}' es una palabra reservada",
                suggestion="Usar un nombre más descriptivo"
            ))
        
        return results
    
    def validate_package_json(self, package_json_path: Path) -> List[ValidationResult]:
        """
        Validar package.json de proyecto frontend
        
        Args:
            package_json_path: Ruta al package.json
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        if not package_json_path.exists():
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="package.json no encontrado",
                file_path=str(package_json_path)
            ))
            return results
        
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message=f"package.json inválido: {e}",
                file_path=str(package_json_path)
            ))
            return results
        
        # Validar campos requeridos
        required_fields = ['name', 'version', 'scripts']
        for field in required_fields:
            if field not in data:
                results.append(ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Campo requerido '{field}' faltante en package.json",
                    file_path=str(package_json_path),
                    suggestion=f"Agregar campo '{field}'"
                ))
        
        # Validar scripts
        scripts = data.get('scripts', {})
        required_scripts = ['dev', 'build']
        for script in required_scripts:
            if script not in scripts:
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message=f"Script '{script}' no encontrado",
                    file_path=str(package_json_path),
                    suggestion=f"Agregar script '{script}' para desarrollo/build"
                ))
        
        # Validar dependencias de desarrollo
        dev_deps = data.get('devDependencies', {})
        if 'typescript' in dev_deps:
            # Si usa TypeScript, verificar dependencias relacionadas
            ts_deps = ['@types/node']
            for dep in ts_deps:
                if dep not in dev_deps:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.INFO,
                        message=f"Dependencia TypeScript '{dep}' no encontrada",
                        file_path=str(package_json_path),
                        suggestion=f"Considerar agregar '{dep}' para mejor soporte TypeScript"
                    ))
        
        return results
    
    def validate_component_file(self, file_path: Path, framework: str) -> List[ValidationResult]:
        """
        Validar archivo de componente frontend
        
        Args:
            file_path: Ruta al archivo del componente
            framework: Framework usado (nextjs, react, vue)
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        if not file_path.exists():
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message="Archivo de componente no encontrado",
                file_path=str(file_path)
            ))
            return results
        
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            results.append(ValidationResult(
                severity=ValidationSeverity.ERROR,
                message=f"Error leyendo archivo: {e}",
                file_path=str(file_path)
            ))
            return results
        
        # Validaciones específicas por framework
        if framework in ['nextjs', 'react']:
            results.extend(self._validate_react_component(content, file_path))
        elif framework == 'vue':
            results.extend(self._validate_vue_component(content, file_path))
        
        return results
    
    def _validate_react_component(self, content: str, file_path: Path) -> List[ValidationResult]:
        """Validar componente React/Next.js"""
        results = []
        lines = content.split('\n')
        
        # Verificar import de React (para archivos .jsx/.tsx)
        if file_path.suffix in ['.jsx', '.tsx']:
            has_react_import = any('import' in line and 'react' in line.lower() for line in lines[:10])
            if not has_react_import and any('jsx' in line.lower() or '<' in line for line in lines):
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message="Posible componente React sin import de React",
                    file_path=str(file_path),
                    suggestion="Agregar: import React from 'react'"
                ))
        
        # Verificar naming convention de componente
        component_name = file_path.stem
        if not component_name[0].isupper():
            results.append(ValidationResult(
                severity=ValidationSeverity.WARNING,
                message="Nombre de componente debería empezar con mayúscula",
                file_path=str(file_path),
                suggestion=f"Renombrar a {component_name.capitalize()}"
            ))
        
        # Verificar export default
        has_default_export = any('export default' in line for line in lines)
        if not has_default_export:
            results.append(ValidationResult(
                severity=ValidationSeverity.INFO,
                message="Componente sin export default",
                file_path=str(file_path),
                suggestion="Considerar agregar export default para mejor reusabilidad"
            ))
        
        # Verificar hooks rules básicas
        for i, line in enumerate(lines, 1):
            if 'useState(' in line or 'useEffect(' in line:
                # Verificar que está dentro de una función componente
                function_context = self._find_function_context(lines, i-1)
                if not function_context:
                    results.append(ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message="Hook usado fuera de componente React",
                        file_path=str(file_path),
                        line_number=i,
                        suggestion="Mover hook dentro de función componente"
                    ))
        
        return results
    
    def _validate_vue_component(self, content: str, file_path: Path) -> List[ValidationResult]:
        """Validar componente Vue"""
        results = []
        
        # Verificar estructura básica de SFC
        has_template = '<template>' in content
        has_script = '<script' in content
        
        if not has_template:
            results.append(ValidationResult(
                severity=ValidationSeverity.WARNING,
                message="Componente Vue sin bloque <template>",
                file_path=str(file_path),
                suggestion="Agregar bloque <template> para renderizado"
            ))
        
        if not has_script:
            results.append(ValidationResult(
                severity=ValidationSeverity.WARNING,
                message="Componente Vue sin bloque <script>",
                file_path=str(file_path),
                suggestion="Agregar bloque <script> para lógica del componente"
            ))
        
        # Verificar Composition API vs Options API
        if '<script setup' in content:
            # Composition API con script setup
            results.append(ValidationResult(
                severity=ValidationSeverity.INFO,
                message="Usando Composition API con <script setup>",
                file_path=str(file_path)
            ))
        elif 'export default {' in content:
            # Options API
            results.append(ValidationResult(
                severity=ValidationSeverity.INFO,
                message="Usando Options API",
                file_path=str(file_path),
                suggestion="Considerar migrar a Composition API para mejor TypeScript support"
            ))
        
        return results
    
    def _find_function_context(self, lines: List[str], line_index: int) -> bool:
        """
        Verificar si una línea está dentro de una función componente
        """
        # Buscar hacia atrás para encontrar definición de función
        for i in range(line_index, max(0, line_index - 20), -1):
            line = lines[i].strip()
            if ('function' in line and any(word in line for word in ['Component', 'const', 'export'])) or \
               ('const' in line and '=>' in line):
                return True
        return False
    
    def validate_project_structure(self, project_path: Path, framework: str) -> List[ValidationResult]:
        """
        Validar estructura de proyecto frontend
        
        Args:
            project_path: Ruta del proyecto
            framework: Framework usado
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        # Validar archivos básicos
        required_files = {
            'nextjs': ['package.json', 'next.config.js', 'tsconfig.json'],
            'react': ['package.json', 'index.html', 'vite.config.ts'],
            'vue': ['package.json', 'vite.config.ts', 'index.html']
        }
        
        framework_files = required_files.get(framework, ['package.json'])
        for file_name in framework_files:
            file_path = project_path / file_name
            if not file_path.exists():
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message=f"Archivo recomendado '{file_name}' no encontrado",
                    file_path=str(file_path),
                    suggestion=f"Crear {file_name} para configuración de {framework}"
                ))
        
        # Validar estructura de directorios
        expected_dirs = {
            'nextjs': ['app', 'components', 'public'],
            'react': ['src', 'public'],
            'vue': ['src', 'public']
        }
        
        framework_dirs = expected_dirs.get(framework, ['src'])
        for dir_name in framework_dirs:
            dir_path = project_path / dir_name
            if not dir_path.exists():
                results.append(ValidationResult(
                    severity=ValidationSeverity.INFO,
                    message=f"Directorio '{dir_name}' no encontrado",
                    suggestion=f"Crear directorio '{dir_name}' para organización de {framework}"
                ))
        
        return results
    
    def validate_dependencies_compatibility(self, dependencies: Dict[str, str], framework: str) -> List[ValidationResult]:
        """
        Validar compatibilidad de dependencias
        
        Args:
            dependencies: Diccionario de dependencias {name: version}
            framework: Framework usado
            
        Returns:
            Lista de resultados de validación
        """
        results = []
        
        # Reglas específicas por framework
        framework_rules = {
            'nextjs': {
                'required': ['next', 'react', 'react-dom'],
                'incompatible': ['create-react-app'],
                'recommended': ['typescript', '@types/react', '@types/node']
            },
            'react': {
                'required': ['react', 'react-dom'],
                'incompatible': ['next'],
                'recommended': ['typescript', '@types/react']
            },
            'vue': {
                'required': ['vue'],
                'incompatible': ['react', 'next'],
                'recommended': ['typescript']
            }
        }
        
        rules = framework_rules.get(framework, {})
        
        # Verificar dependencias requeridas
        for required_dep in rules.get('required', []):
            if required_dep not in dependencies:
                results.append(ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Dependencia requerida '{required_dep}' faltante para {framework}",
                    suggestion=f"Agregar '{required_dep}' a dependencies"
                ))
        
        # Verificar dependencias incompatibles
        for incompatible_dep in rules.get('incompatible', []):
            if incompatible_dep in dependencies:
                results.append(ValidationResult(
                    severity=ValidationSeverity.WARNING,
                    message=f"Dependencia '{incompatible_dep}' puede ser incompatible con {framework}",
                    suggestion=f"Considerar remover '{incompatible_dep}'"
                ))
        
        # Verificar versiones problemáticas conocidas
        version_issues = self._check_known_version_issues(dependencies)
        results.extend(version_issues)
        
        return results
    
    def _check_known_version_issues(self, dependencies: Dict[str, str]) -> List[ValidationResult]:
        """Verificar problemas conocidos de versiones"""
        results = []
        
        # Ejemplos de reglas de versiones
        version_rules = {
            'react': {
                'min_version': '16.8.0',
                'message': 'Versión muy antigua, hooks no soportados'
            },
            'next': {
                'min_version': '12.0.0',
                'message': 'Versión muy antigua, considerar actualizar'
            }
        }
        
        for dep_name, version in dependencies.items():
            if dep_name in version_rules:
                rule = version_rules[dep_name]
                # Aquí iría lógica de comparación de versiones semánticas
                # Por simplicidad, omitimos la implementación completa
                pass
        
        return results
    
    def _load_component_patterns(self) -> Dict[str, Any]:
        """Cargar patrones de validación de componentes"""
        return {
            'react': {
                'naming': r'^[A-Z][a-zA-Z0-9]*$',
                'hooks_rules': ['useState', 'useEffect', 'useContext'],
                'forbidden_patterns': ['document.getElementById', 'window.']
            },
            'vue': {
                'naming': r'^[A-Z][a-zA-Z0-9]*$',
                'composition_api': ['ref', 'reactive', 'computed'],
                'template_syntax': ['v-if', 'v-for', 'v-model']
            }
        }
    
    def _load_dependency_rules(self) -> Dict[str, Any]:
        """Cargar reglas de dependencias"""
        return {
            'security': ['audit', 'vulnerability_check'],
            'performance': ['bundle_size', 'tree_shaking'],
            'compatibility': ['peer_dependencies', 'engine_requirements']
        }
    
    def _load_framework_rules(self) -> Dict[str, Any]:
        """Cargar reglas específicas de frameworks"""
        return {
            'nextjs': {
                'file_based_routing': True,
                'api_routes': True,
                'static_optimization': True
            },
            'react': {
                'component_lifecycle': True,
                'state_management': True,
                'context_api': True
            },
            'vue': {
                'single_file_components': True,
                'composition_api': True,
                'directives': True
            }
        }
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Obtener resumen de validaciones
        
        Returns:
            Resumen con estadísticas de validación
        """
        errors = [r for r in self.results if r.severity == ValidationSeverity.ERROR]
        warnings = [r for r in self.results if r.severity == ValidationSeverity.WARNING]
        info = [r for r in self.results if r.severity == ValidationSeverity.INFO]
        
        return {
            'total_issues': len(self.results),
            'errors': len(errors),
            'warnings': len(warnings),
            'info': len(info),
            'is_valid': len(errors) == 0,
            'details': {
                'errors': [r.message for r in errors],
                'warnings': [r.message for r in warnings],
                'info': [r.message for r in info]
            }
        }
