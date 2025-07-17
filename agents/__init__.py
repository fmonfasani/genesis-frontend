"""
Genesis Frontend Agents Module

Este módulo contiene todos los agentes especializados en generación de frontend
para el ecosistema Genesis Engine.

Agentes disponibles:
- NextJSAgent: Especialista en aplicaciones Next.js
- ReactAgent: Especialista en aplicaciones React SPA  
- VueAgent: Especialista en aplicaciones Vue.js
- UIAgent: Especialista en diseño de interfaz de usuario

Siguiendo la doctrina del ecosistema genesis-frontend:
- Solo se enfoca en frontend
- Usa MCPturbo para comunicación
- Colabora con genesis-templates
- No coordina workflows generales
"""

from .base_agent import FrontendAgent
from .nextjs_agent import NextJSAgent
from .react_agent import ReactAgent
from .vue_agent import VueAgent
from .ui_agent import UIAgent

# Registro de agentes disponibles
AVAILABLE_AGENTS = {
    "nextjs": NextJSAgent,
    "react": ReactAgent,
    "vue": VueAgent,
    "ui": UIAgent,
}

# Frameworks soportados por cada agente
FRAMEWORK_SUPPORT = {
    "nextjs": ["nextjs", "next"],
    "react": ["react", "cra"],
    "vue": ["vue", "vue3"],
    "ui": ["design", "ui", "components"],
}

def get_agent_for_framework(framework: str) -> type[FrontendAgent]:
    """
    Obtener el agente apropiado para un framework específico
    
    Args:
        framework: Nombre del framework (nextjs, react, vue, ui)
        
    Returns:
        Clase del agente apropiado
        
    Raises:
        ValueError: Si el framework no es soportado
    """
    framework = framework.lower().strip()
    
    # Buscar coincidencia directa
    if framework in AVAILABLE_AGENTS:
        return AVAILABLE_AGENTS[framework]
    
    # Buscar en aliases
    for agent_name, supported_frameworks in FRAMEWORK_SUPPORT.items():
        if framework in supported_frameworks:
            return AVAILABLE_AGENTS[agent_name]
    
    raise ValueError(f"Framework '{framework}' no soportado. Frameworks disponibles: {list(AVAILABLE_AGENTS.keys())}")

def create_agent(framework: str, **kwargs) -> FrontendAgent:
    """
    Crear instancia del agente apropiado para un framework
    
    Args:
        framework: Nombre del framework
        **kwargs: Argumentos adicionales para el agente
        
    Returns:
        Instancia del agente inicializada
    """
    agent_class = get_agent_for_framework(framework)
    agent = agent_class(**kwargs)
    return agent

def get_supported_frameworks() -> list[str]:
    """
    Obtener lista de frameworks soportados
    
    Returns:
        Lista de nombres de frameworks soportados
    """
    frameworks = set()
    for supported_list in FRAMEWORK_SUPPORT.values():
        frameworks.update(supported_list)
    return sorted(list(frameworks))

def get_agent_capabilities(framework: str) -> list[str]:
    """
    Obtener capacidades de un agente específico
    
    Args:
        framework: Nombre del framework
        
    Returns:
        Lista de capacidades del agente
    """
    agent_class = get_agent_for_framework(framework)
    # Crear instancia temporal para obtener capacidades
    temp_agent = agent_class()
    return temp_agent.capabilities

def validate_framework_config(framework: str, config: dict) -> list[str]:
    """
    Validar configuración para un framework específico
    
    Args:
        framework: Nombre del framework
        config: Configuración a validar
        
    Returns:
        Lista de errores de validación (vacía si no hay errores)
    """
    errors = []
    
    # Validaciones básicas
    if not isinstance(config, dict):
        errors.append("La configuración debe ser un diccionario")
        return errors
    
    # Validaciones específicas por framework
    if framework in ["nextjs", "next"]:
        if "typescript" in config and not isinstance(config["typescript"], bool):
            errors.append("typescript debe ser un booleano")
        if "app_router" in config and not isinstance(config["app_router"], bool):
            errors.append("app_router debe ser un booleano")
    
    elif framework == "react":
        if "build_tool" in config and config["build_tool"] not in ["vite", "webpack", "parcel"]:
            errors.append("build_tool debe ser 'vite', 'webpack' o 'parcel'")
        if "state_management" in config and config["state_management"] not in ["redux_toolkit", "zustand", "context_api", "mobx"]:
            errors.append("state_management no válido para React")
    
    elif framework == "vue":
        if "vue_version" in config and config["vue_version"] not in ["2", "3"]:
            errors.append("vue_version debe ser '2' o '3'")
        if "state_management" in config and config["state_management"] not in ["pinia", "vuex", "composition_api"]:
            errors.append("state_management no válido para Vue")
    
    elif framework == "ui":
        if "design_system" in config and config["design_system"] not in ["material_design", "apple_hig", "fluent", "carbon", "custom"]:
            errors.append("design_system no válido")
    
    return errors

# Información de versión del módulo
__version__ = "1.0.0"
__author__ = "Genesis Engine Team"
__description__ = "Agentes frontend especializados para Genesis Engine"

# Exportar principales
__all__ = [
    "FrontendAgent",
    "NextJSAgent", 
    "ReactAgent",
    "VueAgent",
    "UIAgent",
    "AVAILABLE_AGENTS",
    "FRAMEWORK_SUPPORT",
    "get_agent_for_framework",
    "create_agent",
    "get_supported_frameworks",
    "get_agent_capabilities",
    "validate_framework_config",
]
