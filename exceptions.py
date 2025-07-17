"""
Excepciones específicas para Genesis Frontend

Este módulo define las excepciones personalizadas para manejar errores
específicos de la generación de frontend en el ecosistema Genesis.
"""

from typing import List, Dict, Any, Optional


class FrontendError(Exception):
    """Excepción base para errores de frontend"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}


class FrontendValidationError(FrontendError):
    """Error de validación en configuración frontend"""
    
    def __init__(self, message: str, validation_errors: List[str], details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.validation_errors = validation_errors
    
    def __str__(self) -> str:
        error_list = "\n".join(f"  - {error}" for error in self.validation_errors)
        return f"{self.message}\nErrores de validación:\n{error_list}"


class FrontendGenerationError(FrontendError):
    """Error durante la generación de código frontend"""
    
    def __init__(self, message: str, file_path: Optional[str] = None, agent_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, details)
        self.file_path = file_path
        self.agent_id = agent_id
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.agent_id:
            parts.append(f"Agente: {self.agent_id}")
        if self.file_path:
            parts.append(f"Archivo: {self.file_path}")
        return " | ".join(parts)


class FrameworkNotSupportedError(FrontendError):
    """Error cuando se solicita un framework no soportado"""
    
    def __init__(self, framework: str, supported_frameworks: List[str]):
        message = f"Framework '{framework}' no soportado"
        super().__init__(message)
        self.framework = framework
        self.supported_frameworks = supported_frameworks
    
    def __str__(self) -> str:
        supported = ", ".join(self.supported_frameworks)
        return f"{self.message}. Frameworks soportados: {supported}"


class TemplateNotFoundError(FrontendError):
    """Error cuando no se encuentra un template"""
    
    def __init__(self, template_name: str, framework: str, search_paths: List[str] = None):
        message = f"Template '{template_name}' no encontrado para framework '{framework}'"
        super().__init__(message)
        self.template_name = template_name
        self.framework = framework
        self.search_paths = search_paths or []
    
    def __str__(self) -> str:
        if self.search_paths:
            paths = "\n".join(f"  - {path}" for path in self.search_paths)
            return f"{self.message}\nRutas buscadas:\n{paths}"
        return self.message


class TemplateRenderError(FrontendError):
    """Error durante el renderizado de templates"""
    
    def __init__(self, template_name: str, error_message: str, missing_variables: List[str] = None):
        message = f"Error renderizando template '{template_name}': {error_message}"
        super().__init__(message)
        self.template_name = template_name
        self.error_message = error_message
        self.missing_variables = missing_variables or []
    
    def __str__(self) -> str:
        if self.missing_variables:
            vars_list = ", ".join(self.missing_variables)
            return f"{self.message}\nVariables faltantes: {vars_list}"
        return self.message


class AgentCommunicationError(FrontendError):
    """Error en comunicación MCP entre agentes"""
    
    def __init__(self, source_agent: str, target_agent: str, action: str, error_message: str):
        message = f"Error en comunicación MCP de {source_agent} a {target_agent} (acción: {action}): {error_message}"
        super().__init__(message)
        self.source_agent = source_agent
        self.target_agent = target_agent
        self.action = action
        self.error_message = error_message


class DependencyError(FrontendError):
    """Error relacionado con dependencias de proyecto"""
    
    def __init__(self, message: str, package_name: Optional[str] = None, required_version: Optional[str] = None, current_version: Optional[str] = None):
        super().__init__(message)
        self.package_name = package_name
        self.required_version = required_version
        self.current_version = current_version
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.package_name:
            parts.append(f"Paquete: {self.package_name}")
        if self.required_version:
            parts.append(f"Versión requerida: {self.required_version}")
        if self.current_version:
            parts.append(f"Versión actual: {self.current_version}")
        return " | ".join(parts)


class ConfigurationError(FrontendError):
    """Error en configuración de proyecto frontend"""
    
    def __init__(self, message: str, config_key: Optional[str] = None, config_file: Optional[str] = None):
        super().__init__(message)
        self.config_key = config_key
        self.config_file = config_file
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.config_file:
            parts.append(f"Archivo: {self.config_file}")
        if self.config_key:
            parts.append(f"Clave: {self.config_key}")
        return " | ".join(parts)


class BuildToolError(FrontendError):
    """Error relacionado con herramientas de build"""
    
    def __init__(self, message: str, build_tool: str, command: Optional[str] = None, exit_code: Optional[int] = None):
        super().__init__(message)
        self.build_tool = build_tool
        self.command = command
        self.exit_code = exit_code
    
    def __str__(self) -> str:
        parts = [self.message, f"Build tool: {self.build_tool}"]
        if self.command:
            parts.append(f"Comando: {self.command}")
        if self.exit_code is not None:
            parts.append(f"Código de salida: {self.exit_code}")
        return " | ".join(parts)


class FileSystemError(FrontendError):
    """Error de sistema de archivos durante generación"""
    
    def __init__(self, message: str, operation: str, file_path: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.operation = operation
        self.file_path = file_path
        self.original_error = original_error
    
    def __str__(self) -> str:
        parts = [self.message, f"Operación: {self.operation}", f"Archivo: {self.file_path}"]
        if self.original_error:
            parts.append(f"Error original: {str(self.original_error)}")
        return " | ".join(parts)


class LLMIntegrationError(FrontendError):
    """Error en integración con LLMs para generación de código"""
    
    def __init__(self, message: str, llm_provider: str, model: Optional[str] = None, prompt_tokens: Optional[int] = None):
        super().__init__(message)
        self.llm_provider = llm_provider
        self.model = model
        self.prompt_tokens = prompt_tokens
    
    def __str__(self) -> str:
        parts = [self.message, f"Proveedor: {self.llm_provider}"]
        if self.model:
            parts.append(f"Modelo: {self.model}")
        if self.prompt_tokens:
            parts.append(f"Tokens: {self.prompt_tokens}")
        return " | ".join(parts)


class ComponentGenerationError(FrontendError):
    """Error específico en generación de componentes"""
    
    def __init__(self, message: str, component_name: str, component_type: str, framework: str):
        super().__init__(message)
        self.component_name = component_name
        self.component_type = component_type
        self.framework = framework
    
    def __str__(self) -> str:
        return f"{self.message} | Componente: {self.component_name} ({self.component_type}) | Framework: {self.framework}"


class StateManagementError(FrontendError):
    """Error en configuración de gestión de estado"""
    
    def __init__(self, message: str, state_library: str, framework: str, configuration: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.state_library = state_library
        self.framework = framework
        self.configuration = configuration
    
    def __str__(self) -> str:
        return f"{self.message} | Librería: {self.state_library} | Framework: {self.framework}"


class UILibraryError(FrontendError):
    """Error en integración de librerías de UI"""
    
    def __init__(self, message: str, ui_library: str, framework: str, version_conflict: bool = False):
        super().__init__(message)
        self.ui_library = ui_library
        self.framework = framework
        self.version_conflict = version_conflict
    
    def __str__(self) -> str:
        parts = [self.message, f"Librería UI: {self.ui_library}", f"Framework: {self.framework}"]
        if self.version_conflict:
            parts.append("Conflicto de versiones detectado")
        return " | ".join(parts)


class RoutingError(FrontendError):
    """Error en configuración de routing"""
    
    def __init__(self, message: str, router_library: str, framework: str, route_config: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.router_library = router_library
        self.framework = framework
        self.route_config = route_config
    
    def __str__(self) -> str:
        return f"{self.message} | Router: {self.router_library} | Framework: {self.framework}"


class TestingConfigurationError(FrontendError):
    """Error en configuración de testing"""
    
    def __init__(self, message: str, testing_framework: str, runner: str, config_file: Optional[str] = None):
        super().__init__(message)
        self.testing_framework = testing_framework
        self.runner = runner
        self.config_file = config_file
    
    def __str__(self) -> str:
        parts = [self.message, f"Framework: {self.testing_framework}", f"Runner: {self.runner}"]
        if self.config_file:
            parts.append(f"Config: {self.config_file}")
        return " | ".join(parts)


# Utilidades para manejo de errores
def format_validation_errors(errors: List[str]) -> str:
    """
    Formatear lista de errores de validación
    
    Args:
        errors: Lista de errores
        
    Returns:
        String formateado con los errores
    """
    if not errors:
        return "No hay errores de validación"
    
    formatted = ["Errores de validación encontrados:"]
    for i, error in enumerate(errors, 1):
        formatted.append(f"  {i}. {error}")
    
    return "\n".join(formatted)


def collect_generation_errors(exceptions: List[Exception]) -> Dict[str, List[str]]:
    """
    Recopilar y categorizar errores de generación
    
    Args:
        exceptions: Lista de excepciones
        
    Returns:
        Diccionario con errores categorizados
    """
    categorized = {
        "validation": [],
        "generation": [],
        "template": [],
        "dependency": [],
        "filesystem": [],
        "other": []
    }
    
    for exc in exceptions:
        if isinstance(exc, FrontendValidationError):
            categorized["validation"].extend(exc.validation_errors)
        elif isinstance(exc, FrontendGenerationError):
            categorized["generation"].append(str(exc))
        elif isinstance(exc, (TemplateNotFoundError, TemplateRenderError)):
            categorized["template"].append(str(exc))
        elif isinstance(exc, DependencyError):
            categorized["dependency"].append(str(exc))
        elif isinstance(exc, FileSystemError):
            categorized["filesystem"].append(str(exc))
        else:
            categorized["other"].append(str(exc))
    
    # Remover categorías vacías
    return {k: v for k, v in categorized.items() if v}


def create_error_report(errors: Dict[str, List[str]]) -> str:
    """
    Crear reporte de errores formateado
    
    Args:
        errors: Errores categorizados
        
    Returns:
        Reporte formateado
    """
    if not errors:
        return "No se encontraron errores"
    
    report_lines = ["=== REPORTE DE ERRORES ===\n"]
    
    category_names = {
        "validation": "Errores de Validación",
        "generation": "Errores de Generación",
        "template": "Errores de Template",
        "dependency": "Errores de Dependencias",
        "filesystem": "Errores de Sistema de Archivos",
        "other": "Otros Errores"
    }
    
    for category, category_errors in errors.items():
        if category_errors:
            report_lines.append(f"\n{category_names.get(category, category.title())}:")
            for i, error in enumerate(category_errors, 1):
                report_lines.append(f"  {i}. {error}")
    
    return "\n".join(report_lines)
