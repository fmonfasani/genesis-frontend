"""
Base Agent para agentes frontend especializados
Compatible con MCPturbo y genesis-templates
"""

import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

# Importar desde MCPturbo (protocolo central)
try:
    from mcpturbo import MCPAgent, MCPRequest, MCPResponse
    from mcpturbo.types import AgentTask, TaskResult
except ImportError:
    # Fallback si MCPturbo no está disponible
    class MCPAgent:
        pass
    
    class MCPRequest:
        pass
    
    class MCPResponse:
        pass
    
    class AgentTask:
        def __init__(self, task_id: str, name: str, params: Dict[str, Any]):
            self.id = task_id
            self.name = name
            self.params = params
    
    class TaskResult:
        def __init__(self, task_id: str, success: bool, result: Any = None, error: str = None):
            self.task_id = task_id
            self.success = success
            self.result = result
            self.error = error

logger = logging.getLogger(__name__)

class FrontendAgent(MCPAgent, ABC):
    """
    Base class para todos los agentes frontend especializados
    
    Siguiendo la doctrina del ecosistema genesis-frontend:
    - Se especializa solo en frontend
    - Usa MCPturbo para comunicación
    - Colabora con genesis-templates
    - No coordina workflows generales
    """
    
    def __init__(self, agent_id: str, name: str, specialization: str):
        super().__init__()
        self.agent_id = agent_id
        self.name = name
        self.specialization = specialization  # 'nextjs', 'react', 'vue', 'ui'
        self.version = "1.0.0"
        self.created_at = datetime.now()
        self.capabilities: List[str] = []
        self.handlers: Dict[str, callable] = {}
        self.metadata: Dict[str, Any] = {}
        
        # Logger específico para frontend
        self.logger = logging.getLogger(f"genesis_frontend.{self.specialization}")
        
        # Template engine (colabora con genesis-templates)
        self.template_engine = None
        
    def add_capability(self, capability: str):
        """Agregar capacidad del agente"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def register_handler(self, action: str, handler: callable):
        """Registrar handler para acción específica"""
        self.handlers[action] = handler
    
    def set_metadata(self, key: str, value: Any):
        """Establecer metadata del agente"""
        self.metadata[key] = value
    
    def get_metadata(self, key: str) -> Any:
        """Obtener metadata del agente"""
        return self.metadata.get(key)
    
    @abstractmethod
    async def initialize(self):
        """Inicializar agente - debe ser implementado por cada agente"""
        pass
    
    @abstractmethod
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica - debe ser implementado por cada agente"""
        pass
    
    async def handle_mcp_request(self, request: MCPRequest) -> MCPResponse:
        """
        Manejar solicitud MCP
        
        Args:
            request: Solicitud MCP
            
        Returns:
            Respuesta MCP
        """
        action = request.action
        
        if action in self.handlers:
            try:
                result = await self.handlers[action](request)
                return MCPResponse(
                    request_id=request.id,
                    success=True,
                    result=result
                )
            except Exception as e:
                self.logger.error(f"Error en handler {action}: {e}")
                return MCPResponse(
                    request_id=request.id,
                    success=False,
                    error=str(e)
                )
        else:
            return MCPResponse(
                request_id=request.id,
                success=False,
                error=f"Acción no soportada: {action}"
            )
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Obtener información del agente"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "specialization": self.specialization,
            "version": self.version,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }
    
    def can_handle_framework(self, framework: str) -> bool:
        """Verificar si el agente puede manejar el framework"""
        return framework.lower() in self.specialization.lower()
    
    def validate_frontend_request(self, params: Dict[str, Any]) -> List[str]:
        """
        Validar solicitud frontend
        
        Args:
            params: Parámetros de la solicitud
            
        Returns:
            Lista de errores de validación
        """
        errors = []
        
        # Validaciones básicas para frontend
        if not params.get("output_path"):
            errors.append("output_path es requerido")
        
        if not params.get("framework"):
            errors.append("framework es requerido")
        
        # Validar que el framework es compatible
        framework = params.get("framework", "").lower()
        if framework and not self.can_handle_framework(framework):
            errors.append(f"Framework '{framework}' no soportado por {self.specialization}")
        
        return errors
    
    async def call_llm_for_generation(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        Llamar a LLM para generación inteligente de código
        
        Args:
            prompt: Prompt para el LLM
            context: Contexto adicional
            
        Returns:
            Código generado por el LLM
        """
        # Aquí se integraría con MCPturbo para llamar a LLMs
        # Por ahora, placeholder
        self.logger.info(f"Llamando LLM para generación: {prompt[:50]}...")
        
        # En implementación real, usar MCPturbo para llamar a OpenAI, Claude, etc.
        # return await self.mcp_client.call_llm("claude", prompt, context)
        
        return "// Código generado por LLM placeholder"
    
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Renderizar template usando genesis-templates
        
        Args:
            template_name: Nombre del template
            context: Contexto para el template
            
        Returns:
            Contenido renderizado
        """
        if not self.template_engine:
            raise RuntimeError("Template engine no configurado")
        
        return self.template_engine.render_template(template_name, context)
    
    def log_frontend_action(self, action: str, framework: str, details: Dict[str, Any] = None):
        """Log específico para acciones frontend"""
        self.logger.info(
            f"[{self.specialization.upper()}] {action} para {framework}",
            extra={"details": details}
        )
