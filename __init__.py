"""
Genesis Frontend - Generación especializada de código frontend

Este paquete forma parte del ecosistema Genesis Engine y se especializa
exclusivamente en la generación de código frontend usando agentes de IA.

Características principales:
- Agentes especializados por framework (Next.js, React, Vue.js)
- Integración con MCPturbo para comunicación entre agentes
- Colaboración con genesis-templates para renderizado
- Generación inteligente usando LLMs
- Soporte para TypeScript, Tailwind CSS, testing, y más

Siguiendo la doctrina del ecosistema:
- ❌ No coordina workflows generales
- ❌ No interactúa directamente con usuarios
- ❌ No conoce backend ni DevOps
- ✅ Se especializa solo en frontend
- ✅ Usa MCPturbo para comunicación
- ✅ Colabora con genesis-templates
"""

from .agents import (
    FrontendAgent,
    NextJSAgent,
    ReactAgent,
    VueAgent,
    UIAgent,
    get_agent_for_framework,
    create_agent,
    get_supported_frameworks,
    AVAILABLE_AGENTS,
    FRAMEWORK_SUPPORT,
)

from .config import (
    config,
    SupportedFramework,
    BuildTool,
    PackageManager,
    StateManagement,
    UILibrary,
    SUPPORTED_FRAMEWORKS,
    SUPPORTED_BUILD_TOOLS,
    SUPPORTED_UI_LIBRARIES,
    DEV_SERVER_DEFAULTS,
)

from .utils import (
    validate_project_name,
    validate_framework_config,
    generate_file_hash,
    ensure_directory_exists,
    safe_file_write,
    read_json_file,
    write_json_file,
    merge_package_json,
    check_node_version,
    check_package_manager,
    format_dependency_version,
    generate_gitignore,
    create_directory_structure,
    get_dev_server_config,
    generate_env_template,
    sanitize_component_name,
    format_file_size,
    is_valid_npm_package_name,
    extract_schema_entities,
)

from .exceptions import (
    FrontendError,
    FrontendValidationError,
    FrontendGenerationError,
    FrameworkNotSupportedError,
    TemplateNotFoundError,
    TemplateRenderError,
    AgentCommunicationError,
    DependencyError,
    ConfigurationError,
    BuildToolError,
    FileSystemError,
    LLMIntegrationError,
    ComponentGenerationError,
    StateManagementError,
    UILibraryError,
    RoutingError,
    TestingConfigurationError,
    format_validation_errors,
    collect_generation_errors,
    create_error_report,
)

# Información del paquete
__version__ = "1.0.0"
__author__ = "Genesis Engine Team"
__description__ = "Agentes frontend especializados para Genesis Engine"
__license__ = "MIT"

# Compatibilidad con el ecosistema
__ecosystem__ = "genesis-engine"
__role__ = "frontend-generation"
__dependencies__ = ["mcpturbo", "genesis-templates"]


def get_version() -> str:
    """Obtener versión del paquete"""
    return __version__


def get_ecosystem_info() -> dict:
    """Obtener información del ecosistema"""
    return {
        "name": "genesis-frontend",
        "version": __version__,
        "ecosystem": __ecosystem__,
        "role": __role__,
        "dependencies": __dependencies__,
        "supported_frameworks": get_supported_frameworks(),
        "available_agents": list(AVAILABLE_AGENTS.keys()),
    }


def quick_start(framework: str, project_name: str, output_path: str = "./", **kwargs) -> dict:
    """
    Inicio rápido para generar proyecto frontend
    
    Args:
        framework: Framework a usar (nextjs, react, vue)
        project_name: Nombre del proyecto
        output_path: Ruta de salida
        **kwargs: Configuración adicional
        
    Returns:
        Resultado de la generación
        
    Example:
        >>> from genesis_frontend import quick_start
        >>> result = quick_start(
        ...     framework="nextjs",
        ...     project_name="my-app",
        ...     output_path="./projects/",
        ...     typescript=True,
        ...     tailwind_css=True
        ... )
    """
    try:
        # Validar entrada
        name_errors = validate_project_name(project_name)
        if name_errors:
            raise FrontendValidationError("Nombre de proyecto inválido", name_errors)
        
        # Crear agente
        agent = create_agent(framework)
        
        # Preparar parámetros
        params = {
            "output_path": output_path,
            "framework": framework,
            "schema": {
                "project_name": project_name,
                "description": f"Proyecto {framework} generado por Genesis Frontend"
            },
            **kwargs
        }
        
        # Validar configuración
        config_errors = validate_framework_config(framework, params)
        if config_errors:
            raise FrontendValidationError("Configuración inválida", config_errors)
        
        # Generar proyecto (esto requeriría implementación async)
        # En un uso real, esto se haría a través de MCPturbo
        return {
            "success": True,
            "framework": framework,
            "project_name": project_name,
            "output_path": output_path,
            "agent_used": agent.agent_id,
            "message": f"Proyecto {framework} '{project_name}' listo para generación"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "framework": framework,
            "project_name": project_name
        }


def validate_environment() -> dict:
    """
    Validar entorno para desarrollo frontend
    
    Returns:
        Estado del entorno de desarrollo
    """
    environment = {
        "valid": True,
        "checks": {},
        "recommendations": []
    }
    
    # Verificar Node.js
    node_valid, node_version = check_node_version()
    environment["checks"]["node"] = {
        "valid": node_valid,
        "version": node_version,
        "required": ">=16.0.0"
    }
    
    if not node_valid:
        environment["valid"] = False
        environment["recommendations"].append("Instalar Node.js versión 16 o superior")
    
    # Verificar gestor de paquetes
    pm_available, pm_name = check_package_manager()
    environment["checks"]["package_manager"] = {
        "available": pm_available,
        "manager": pm_name
    }
    
    if not pm_available:
        environment["valid"] = False
        environment["recommendations"].append("Instalar npm, yarn, pnpm o bun")
    
    # Verificar frameworks soportados
    environment["supported_frameworks"] = get_supported_frameworks()
    
    return environment


def get_framework_info(framework: str) -> dict:
    """
    Obtener información detallada de un framework
    
    Args:
        framework: Nombre del framework
        
    Returns:
        Información del framework
    """
    try:
        agent_class = get_agent_for_framework(framework)
        agent = agent_class()
        
        return {
            "framework": framework,
            "agent_id": agent.agent_id,
            "agent_name": agent.name,
            "capabilities": agent.capabilities,
            "metadata": agent.metadata,
            "defaults": config.get_framework_defaults(framework),
            "directory_structure": config.get_directory_structure(framework),
            "templates": config.get_templates_for_framework(framework),
        }
    except Exception as e:
        raise FrameworkNotSupportedError(framework, get_supported_frameworks())


def create_project_structure(framework: str, project_path: str) -> list:
    """
    Crear solo la estructura de directorios para un proyecto
    
    Args:
        framework: Framework a usar
        project_path: Ruta del proyecto
        
    Returns:
        Lista de directorios creados
    """
    from pathlib import Path
    
    try:
        base_path = Path(project_path)
        return create_directory_structure(base_path, framework)
    except Exception as e:
        raise FileSystemError(f"Error creando estructura", "create_directories", project_path, e)


# Exportar principales
__all__ = [
    # Core
    "__version__",
    "get_version", 
    "get_ecosystem_info",
    "quick_start",
    "validate_environment",
    "get_framework_info",
    "create_project_structure",
    
    # Agentes
    "FrontendAgent",
    "NextJSAgent",
    "ReactAgent", 
    "VueAgent",
    "UIAgent",
    "get_agent_for_framework",
    "create_agent",
    "get_supported_frameworks",
    "AVAILABLE_AGENTS",
    "FRAMEWORK_SUPPORT",
    
    # Configuración
    "config",
    "SupportedFramework",
    "BuildTool",
    "PackageManager", 
    "StateManagement",
    "UILibrary",
    "SUPPORTED_FRAMEWORKS",
    "SUPPORTED_BUILD_TOOLS",
    "SUPPORTED_UI_LIBRARIES",
    "DEV_SERVER_DEFAULTS",
    
    # Utilidades
    "validate_project_name",
    "validate_framework_config",
    "generate_file_hash",
    "ensure_directory_exists",
    "safe_file_write",
    "read_json_file",
    "write_json_file",
    "merge_package_json",
    "check_node_version",
    "check_package_manager",
    "format_dependency_version",
    "generate_gitignore",
    "create_directory_structure",
    "get_dev_server_config",
    "generate_env_template",
    "sanitize_component_name",
    "format_file_size",
    "is_valid_npm_package_name",
    "extract_schema_entities",
    
    # Excepciones
    "FrontendError",
    "FrontendValidationError",
    "FrontendGenerationError",
    "FrameworkNotSupportedError",
    "TemplateNotFoundError",
    "TemplateRenderError",
    "AgentCommunicationError",
    "DependencyError",
    "ConfigurationError",
    "BuildToolError",
    "FileSystemError",
    "LLMIntegrationError",
    "ComponentGenerationError",
    "StateManagementError",
    "UILibraryError",
    "RoutingError",
    "TestingConfigurationError",
    "format_validation_errors",
    "collect_generation_errors",
    "create_error_report",
]
