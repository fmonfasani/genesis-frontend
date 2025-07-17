"""
Base Agent para agentes frontend especializados
Compatible con MCPturbo y genesis-templates
Siguiendo la doctrina del ecosistema genesis-frontend
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
    HAS_MCPTURBO = True
except ImportError:
    # Fallback si MCPturbo no está disponible
    HAS_MCPTURBO = False
    
    class MCPAgent:
        pass
    
    class MCPRequest:
        def __init__(self, request_id: str, action: str, data: Dict[str, Any]):
            self.id = request_id
            self.action = action
            self.data = data
    
    class MCPResponse:
        def __init__(self, request_id: str, success: bool, result: Any = None, error: str = None):
            self.request_id = request_id
            self.success = success
            self.result = result
            self.error = error
    
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
    - Usa LLMs para generación inteligente
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
        
        # MCPturbo integration
        self.mcp_client = None
        
    def add_capability(self, capability: str):
        """Agregar capacidad del agente"""
        if capability not in self.capabilities:
            self.capabilities.append(capability)
    
    def register_handler(self, action: str, handler: callable):
        """Registrar handler para acción específica"""
        self.handlers[action] = handler
        self.logger.debug(f"Registrado handler para acción: {action}")
    
    def set_metadata(self, key: str, value: Any):
        """Establecer metadata del agente"""
        self.metadata[key] = value
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Obtener metadata del agente"""
        return self.metadata.get(key, default)
    
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
            "created_at": self.created_at.isoformat(),
            "has_mcpturbo": HAS_MCPTURBO
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
        
        if not params.get("framework") and self.specialization != "ui":
            errors.append("framework es requerido")
        
        # Validar que el framework es compatible
        framework = params.get("framework", "").lower()
        if framework and not self.can_handle_framework(framework):
            errors.append(f"Framework '{framework}' no soportado por {self.specialization}")
        
        return errors
    
    async def call_llm_for_generation(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        Llamar a LLM para generación inteligente de código
        
        Según la doctrina: "Usarás LLMs para generación inteligente"
        
        Args:
            prompt: Prompt para el LLM
            context: Contexto adicional
            
        Returns:
            Código generado por el LLM
        """
        self.logger.info(f"Generando código con LLM: {prompt[:50]}...")
        
        # Intentar usar MCPturbo para llamar a LLMs
        if self.mcp_client and HAS_MCPTURBO:
            try:
                # En implementación real, usar MCPturbo para llamar a OpenAI, Claude, etc.
                response = await self.mcp_client.call_llm("claude", {
                    "prompt": prompt,
                    "context": context,
                    "specialization": self.specialization
                })
                return response.get("content", "// Código generado")
            except Exception as e:
                self.logger.warning(f"Error llamando LLM via MCPturbo: {e}")
        
        # Fallback placeholder (en desarrollo)
        return self._generate_placeholder_code(context)
    
    def _generate_placeholder_code(self, context: Dict[str, Any]) -> str:
        """Generar código placeholder para desarrollo"""
        framework = context.get("framework", self.specialization)
        component_name = context.get("component_name", "Component")
        
        if framework in ["nextjs", "react"]:
            return f"""// Generated by Genesis Frontend - {self.name}
import React from 'react'

interface {component_name}Props {{
  // TODO: Define props
}}

const {component_name}: React.FC<{component_name}Props> = () => {{
  return (
    <div className="genesis-component">
      <h1>{component_name}</h1>
      {{/* TODO: Implement component logic */}}
    </div>
  )
}}

export default {component_name}
"""
        elif framework == "vue":
            return f"""<!-- Generated by Genesis Frontend - {self.name} -->
<template>
  <div class="genesis-component">
    <h1>{component_name}</h1>
    <!-- TODO: Implement component logic -->
  </div>
</template>

<script setup lang="ts">
// TODO: Define props and logic
</script>

<style scoped>
.genesis-component {{
  /* TODO: Add styles */
}}
</style>
"""
        else:
            return f"// Generated by Genesis Frontend - {self.name}\n// TODO: Implement for {framework}"
    
    async def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Renderizar template usando genesis-templates
        
        Según la doctrina: "Colaborarás con genesis-templates"
        
        Args:
            template_name: Nombre del template
            context: Contexto para el template
            
        Returns:
            Contenido renderizado
        """
        if not self.template_engine:
            self.logger.warning("Template engine no configurado, usando LLM")
            # Fallback: usar LLM para generar el contenido
            prompt = f"Genera {template_name} con el contexto: {context}"
            return await self.call_llm_for_generation(prompt, context)
        
        try:
            return self.template_engine.render_template(template_name, context)
        except Exception as e:
            self.logger.error(f"Error renderizando template {template_name}: {e}")
            # Fallback: usar LLM
            prompt = f"Genera contenido para {template_name} con el contexto: {context}"
            return await self.call_llm_for_generation(prompt, context)
    
    def log_frontend_action(self, action: str, framework: str, details: Dict[str, Any] = None):
        """Log específico para acciones frontend"""
        self.logger.info(
            f"[{self.specialization.upper()}] {action} para {framework}",
            extra={"details": details or {}}
        )
    
    def set_template_engine(self, template_engine):
        """Configurar template engine (inyección de dependencia)"""
        self.template_engine = template_engine
        self.logger.debug("Template engine configurado")
    
    def set_mcp_client(self, mcp_client):
        """Configurar cliente MCP (inyección de dependencia)"""
        self.mcp_client = mcp_client
        self.logger.debug("Cliente MCP configurado")
    
    async def validate_generated_code(self, code: str, language: str) -> Dict[str, Any]:
        """
        Validar código generado
        
        Args:
            code: Código a validar
            language: Lenguaje del código (typescript, javascript, vue, etc.)
            
        Returns:
            Resultado de validación
        """
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "suggestions": []
        }
        
        # Validaciones básicas
        if not code.strip():
            validation_result["valid"] = False
            validation_result["errors"].append("Código vacío")
            return validation_result
        
        # Validaciones específicas por lenguaje
        if language in ["typescript", "tsx"]:
            # Verificar sintaxis TypeScript básica
            if "interface" in code and not code.count("{") >= code.count("interface"):
                validation_result["warnings"].append("Posible problema de sintaxis en interfaces")
        
        elif language in ["javascript", "jsx"]:
            # Verificar sintaxis JavaScript básica
            if code.count("{") != code.count("}"):
                validation_result["warnings"].append("Posible problema de llaves no balanceadas")
        
        elif language == "vue":
            # Verificar estructura Vue
            if "<template>" not in code:
                validation_result["warnings"].append("Componente Vue sin template")
        
        return validation_result
    
    def get_specialization_info(self) -> Dict[str, Any]:
        """Obtener información sobre la especialización del agente"""
        return {
            "specialization": self.specialization,
            "frameworks_supported": self._get_supported_frameworks(),
            "capabilities": self.capabilities,
            "features": self._get_features(),
            "use_cases": self._get_use_cases()
        }
    
    def _get_supported_frameworks(self) -> List[str]:
        """Obtener frameworks soportados por el agente"""
        framework_map = {
            "nextjs": ["nextjs", "next"],
            "react": ["react", "cra"],
            "vue": ["vue", "vue3"],
            "ui": ["design", "ui", "components"]
        }
        return framework_map.get(self.specialization, [])
    
    def _get_features(self) -> List[str]:
        """Obtener características del agente"""
        base_features = [
            "Code generation with LLMs",
            "Template collaboration",
            "MCPturbo integration",
            "TypeScript support"
        ]
        
        specialization_features = {
            "nextjs": ["App Router", "Server Components", "Static Generation"],
            "react": ["SPA development", "State management", "Component libraries"],
            "vue": ["Composition API", "Single File Components", "Reactive state"],
            "ui": ["Design systems", "Color palettes", "Component libraries"]
        }
        
        return base_features + specialization_features.get(self.specialization, [])
    
    def _get_use_cases(self) -> List[str]:
        """Obtener casos de uso del agente"""
        use_cases_map = {
            "nextjs": [
                "Generate full Next.js applications",
                "Create pages and layouts",
                "Setup routing and navigation",
                "Configure TypeScript and Tailwind"
            ],
            "react": [
                "Generate React SPAs",
                "Create reusable components", 
                "Setup state management",
                "Configure build tools"
            ],
            "vue": [
                "Generate Vue 3 applications",
                "Create Vue components",
                "Setup Pinia stores",
                "Configure Vue Router"
            ],
            "ui": [
                "Create design systems",
                "Generate color palettes",
                "Build component libraries",
                "Setup design tokens"
            ]
        }
        
        return use_cases_map.get(self.specialization, [])
