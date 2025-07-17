"""
Tests para agentes frontend especializados
Siguiendo la doctrina del ecosistema genesis-frontend
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any

from genesis_frontend.agents.base_agent import FrontendAgent, AgentTask, TaskResult
from genesis_frontend.agents.nextjs_agent import NextJSAgent
from genesis_frontend.agents.react_agent import ReactAgent
from genesis_frontend.agents.vue_agent import VueAgent
from genesis_frontend.agents.ui_agent import UIAgent


class TestFrontendAgent:
    """Tests para la clase base FrontendAgent"""
    
    def test_agent_initialization(self):
        """Test inicialización básica del agente"""
        agent = NextJSAgent()
        
        assert agent.agent_id == "nextjs_agent"
        assert agent.name == "NextJSAgent"
        assert agent.specialization == "nextjs"
        assert agent.version == "1.0.0"
        assert isinstance(agent.capabilities, list)
        assert isinstance(agent.handlers, dict)
    
    def test_capability_management(self):
        """Test gestión de capacidades"""
        agent = NextJSAgent()
        
        # Verificar capacidades iniciales
        assert "nextjs_app_generation" in agent.capabilities
        
        # Agregar nueva capacidad
        agent.add_capability("test_capability")
        assert "test_capability" in agent.capabilities
        
        # No duplicar capacidades
        agent.add_capability("test_capability")
        assert agent.capabilities.count("test_capability") == 1
    
    def test_metadata_management(self):
        """Test gestión de metadata"""
        agent = NextJSAgent()
        
        # Establecer metadata
        agent.set_metadata("test_key", "test_value")
        assert agent.get_metadata("test_key") == "test_value"
        
        # Valor por defecto
        assert agent.get_metadata("non_existent", "default") == "default"
    
    def test_can_handle_framework(self):
        """Test verificación de framework compatible"""
        nextjs_agent = NextJSAgent()
        react_agent = ReactAgent()
        
        assert nextjs_agent.can_handle_framework("nextjs")
        assert nextjs_agent.can_handle_framework("NEXTJS")
        assert not nextjs_agent.can_handle_framework("react")
        
        assert react_agent.can_handle_framework("react")
        assert not react_agent.can_handle_framework("vue")
    
    def test_validate_frontend_request(self):
        """Test validación de requests frontend"""
        agent = NextJSAgent()
        
        # Request válido
        valid_params = {
            "output_path": "./test-project",
            "framework": "nextjs"
        }
        errors = agent.validate_frontend_request(valid_params)
        assert len(errors) == 0
        
        # Request inválido - sin output_path
        invalid_params = {"framework": "nextjs"}
        errors = agent.validate_frontend_request(invalid_params)
        assert "output_path es requerido" in errors
        
        # Request inválido - framework incompatible
        invalid_params = {
            "output_path": "./test",
            "framework": "react"
        }
        errors = agent.validate_frontend_request(invalid_params)
        assert any("no soportado" in error for error in errors)


class TestNextJSAgent:
    """Tests específicos para NextJSAgent"""
    
    @pytest.fixture
    def nextjs_agent(self):
        """Fixture para crear instancia de NextJSAgent"""
        agent = NextJSAgent()
        return agent
    
    @pytest.mark.asyncio
    async def test_initialization(self, nextjs_agent):
        """Test inicialización del agente NextJS"""
        await nextjs_agent.initialize()
        
        assert nextjs_agent.get_metadata("nextjs_version") == "14.0.0"
        assert nextjs_agent.get_metadata("typescript_support") is True
        assert nextjs_agent.get_metadata("app_router_support") is True
    
    def test_nextjs_capabilities(self, nextjs_agent):
        """Test capacidades específicas de NextJS"""
        required_capabilities = [
            "nextjs_app_generation",
            "app_router_setup", 
            "typescript_configuration",
            "tailwind_integration",
            "server_components"
        ]
        
        for capability in required_capabilities:
            assert capability in nextjs_agent.capabilities
    
    def test_nextjs_handlers(self, nextjs_agent):
        """Test handlers registrados para NextJS"""
        required_handlers = [
            "generate_nextjs_app",
            "generate_component",
            "generate_page",
            "generate_layout"
        ]
        
        for handler in required_handlers:
            assert handler in nextjs_agent.handlers
    
    @pytest.mark.asyncio
    async def test_execute_task_generate_app(self, nextjs_agent, tmp_path):
        """Test ejecución de tarea de generación de app"""
        task = AgentTask(
            task_id="test_task",
            name="generate_nextjs_app",
            params={
                "output_path": str(tmp_path),
                "framework": "nextjs",
                "schema": {
                    "project_name": "test-app",
                    "description": "Test application"
                }
            }
        )
        
        # Mock del template engine
        nextjs_agent.template_engine = Mock()
        nextjs_agent.template_engine.render_template = Mock(return_value="mock content")
        
        result = await nextjs_agent.execute_task(task)
        
        assert isinstance(result, TaskResult)
        assert result.success is True
        assert result.task_id == "test_task"
        assert "framework" in result.result
        assert result.result["framework"] == "nextjs"


class TestReactAgent:
    """Tests específicos para ReactAgent"""
    
    @pytest.fixture
    def react_agent(self):
        """Fixture para crear instancia de ReactAgent"""
        return ReactAgent()
    
    @pytest.mark.asyncio
    async def test_initialization(self, react_agent):
        """Test inicialización del agente React"""
        await react_agent.initialize()
        
        assert react_agent.get_metadata("react_version") == "18.2.0"
        assert react_agent.get_metadata("vite_version") == "5.0.0"
        assert react_agent.get_metadata("typescript_support") is True
    
    def test_react_capabilities(self, react_agent):
        """Test capacidades específicas de React"""
        required_capabilities = [
            "react_app_generation",
            "vite_configuration",
            "react_router_setup",
            "redux_toolkit_setup",
            "component_generation"
        ]
        
        for capability in required_capabilities:
            assert capability in react_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_execute_task_generate_component(self, react_agent):
        """Test generación de componente React"""
        task = AgentTask(
            task_id="test_component",
            name="generate_component",
            params={
                "component_name": "TestComponent",
                "component_type": "functional"
            }
        )
        
        result = await react_agent.execute_task(task)
        
        assert isinstance(result, TaskResult)
        assert result.success is True
        assert "component_name" in result.result


class TestVueAgent:
    """Tests específicos para VueAgent"""
    
    @pytest.fixture
    def vue_agent(self):
        """Fixture para crear instancia de VueAgent"""
        return VueAgent()
    
    @pytest.mark.asyncio
    async def test_initialization(self, vue_agent):
        """Test inicialización del agente Vue"""
        await vue_agent.initialize()
        
        assert vue_agent.get_metadata("vue_version") == "3.4.0"
        assert vue_agent.get_metadata("composition_api_support") is True
        assert vue_agent.get_metadata("pinia_support") is True
    
    def test_vue_capabilities(self, vue_agent):
        """Test capacidades específicas de Vue"""
        required_capabilities = [
            "vue3_app_generation",
            "composition_api_setup",
            "vue_router_setup",
            "pinia_setup",
            "vue_component_generation"
        ]
        
        for capability in required_capabilities:
            assert capability in vue_agent.capabilities


class TestUIAgent:
    """Tests específicos para UIAgent"""
    
    @pytest.fixture
    def ui_agent(self):
        """Fixture para crear instancia de UIAgent"""
        return UIAgent()
    
    @pytest.mark.asyncio
    async def test_initialization(self, ui_agent):
        """Test inicialización del agente UI"""
        await ui_agent.initialize()
        
        assert ui_agent.get_metadata("design_systems_supported") is not None
        assert ui_agent.get_metadata("accessibility_compliant") is True
        assert ui_agent.get_metadata("dark_mode_support") is True
    
    def test_ui_capabilities(self, ui_agent):
        """Test capacidades específicas de UI"""
        required_capabilities = [
            "design_system_creation",
            "color_palette_generation",
            "component_library_creation",
            "dark_mode_implementation",
            "accessibility_optimization"
        ]
        
        for capability in required_capabilities:
            assert capability in ui_agent.capabilities
    
    @pytest.mark.asyncio
    async def test_execute_task_create_design_system(self, ui_agent, tmp_path):
        """Test creación de sistema de diseño"""
        task = AgentTask(
            task_id="test_design",
            name="create_design_system",
            params={
                "output_path": str(tmp_path),
                "design_system": "custom",
                "color_palette": "blue",
                "dark_mode": True
            }
        )
        
        # Mock del template engine
        ui_agent.template_engine = Mock()
        ui_agent.template_engine.render_template = Mock(return_value="mock design tokens")
        
        result = await ui_agent.execute_task(task)
        
        assert isinstance(result, TaskResult)
        assert result.success is True
        assert "design_system" in result.result


class TestMCPIntegration:
    """Tests para integración MCP"""
    
    @pytest.fixture
    def agent_with_mcp(self):
        """Fixture para agente con MCP mock"""
        agent = NextJSAgent()
        agent.mcp_client = Mock()
        return agent
    
    @pytest.mark.asyncio
    async def test_mcp_request_handling(self, agent_with_mcp):
        """Test manejo de requests MCP"""
        from genesis_frontend.agents.base_agent import MCPRequest, MCPResponse
        
        # Mock request
        request = MCPRequest(
            request_id="test_req",
            action="generate_nextjs_app",
            data={"framework": "nextjs"}
        )
        
        # Mock handler
        async def mock_handler(req):
            return {"status": "success"}
        
        agent_with_mcp.register_handler("generate_nextjs_app", mock_handler)
        
        response = await agent_with_mcp.handle_mcp_request(request)
        
        assert isinstance(response, MCPResponse)
        assert response.success is True
        assert response.result["status"] == "success"
    
    @pytest.mark.asyncio
    async def test_llm_integration(self, agent_with_mcp):
        """Test integración con LLMs"""
        # Mock LLM response
        agent_with_mcp.mcp_client.call_llm = AsyncMock(
            return_value={"content": "Generated component code"}
        )
        
        result = await agent_with_mcp.call_llm_for_generation(
            "Generate a React component", 
            {"component_name": "TestComponent"}
        )
        
        assert "Generated component code" in result
        agent_with_mcp.mcp_client.call_llm.assert_called_once()


class TestAgentEcosystemCompliance:
    """Tests para verificar cumplimiento de la doctrina del ecosistema"""
    
    def test_no_cli_functionality(self):
        """Verificar que no hay funcionalidad CLI (doctrina)"""
        # Verificar que no existen imports o referencias a CLI
        agent = NextJSAgent()
        
        # Los agentes no deben tener métodos CLI
        assert not hasattr(agent, 'cli')
        assert not hasattr(agent, 'main')
        assert not hasattr(agent, 'run_cli')
    
    def test_no_orchestration_logic(self):
        """Verificar que no hay lógica de orquestación (doctrina)"""
        agent = NextJSAgent()
        
        # Los agentes no deben orquestar workflows
        assert not hasattr(agent, 'orchestrate')
        assert not hasattr(agent, 'coordinate_agents')
        assert not hasattr(agent, 'manage_workflow')
    
    def test_frontend_only_capabilities(self):
        """Verificar que solo tiene capacidades frontend (doctrina)"""
        agents = [NextJSAgent(), ReactAgent(), VueAgent(), UIAgent()]
        
        forbidden_capabilities = [
            "backend_generation",
            "database_setup", 
            "server_deployment",
            "devops_configuration"
        ]
        
        for agent in agents:
            for forbidden in forbidden_capabilities:
                assert forbidden not in agent.capabilities
    
    def test_mcpturbo_compatibility(self):
        """Verificar compatibilidad con MCPturbo (doctrina)"""
        agent = NextJSAgent()
        
        # Debe tener métodos MCP
        assert hasattr(agent, 'handle_mcp_request')
        assert hasattr(agent, 'set_mcp_client')
        
        # Debe poder manejar AgentTask
        assert hasattr(agent, 'execute_task')
    
    def test_llm_integration_capability(self):
        """Verificar capacidad de integración LLM (doctrina)"""
        agent = NextJSAgent()
        
        # Debe poder llamar LLMs
        assert hasattr(agent, 'call_llm_for_generation')
        
        # Debe tener fallback para placeholders
        assert hasattr(agent, '_generate_placeholder_code')
    
    def test_template_collaboration(self):
        """Verificar colaboración con templates (doctrina)"""
        agent = NextJSAgent()
        
        # Debe poder usar template engine
        assert hasattr(agent, 'render_template')
        assert hasattr(agent, 'set_template_engine')
        
        # Debe tener fallback a LLM si no hay templates
        assert agent.template_engine is None  # Inicialmente None


class TestAgentSpecializations:
    """Tests para verificar especializaciones correctas"""
    
    def test_nextjs_specialization(self):
        """Test especialización NextJS"""
        agent = NextJSAgent()
        info = agent.get_specialization_info()
        
        assert info["specialization"] == "nextjs"
        assert "nextjs" in info["frameworks_supported"]
        assert "App Router" in info["features"]
    
    def test_react_specialization(self):
        """Test especialización React"""
        agent = ReactAgent()
        info = agent.get_specialization_info()
        
        assert info["specialization"] == "react"
        assert "react" in info["frameworks_supported"]
        assert "SPA development" in info["features"]
    
    def test_vue_specialization(self):
        """Test especialización Vue"""
        agent = VueAgent()
        info = agent.get_specialization_info()
        
        assert info["specialization"] == "vue"
        assert "vue" in info["frameworks_supported"]
        assert "Composition API" in info["features"]
    
    def test_ui_specialization(self):
        """Test especialización UI"""
        agent = UIAgent()
        info = agent.get_specialization_info()
        
        assert info["specialization"] == "ui"
        assert "design" in info["frameworks_supported"]
        assert "Design systems" in info["features"]


@pytest.mark.integration
class TestIntegrationScenarios:
    """Tests de integración para escenarios reales"""
    
    @pytest.mark.asyncio
    async def test_full_nextjs_app_generation(self, tmp_path):
        """Test generación completa de app NextJS"""
        agent = NextJSAgent()
        await agent.initialize()
        
        # Mock dependencies
        agent.template_engine = Mock()
        agent.template_engine.render_template = Mock(return_value="mock content")
        
        task = AgentTask(
            task_id="integration_test",
            name="generate_nextjs_app",
            params={
                "output_path": str(tmp_path),
                "framework": "nextjs",
                "typescript": True,
                "tailwind_css": True,
                "schema": {
                    "project_name": "test-integration-app",
                    "description": "Integration test application"
                }
            }
        )
        
        result = await agent.execute_task(task)
        
        # Verificar resultado
        assert result.success is True
        assert result.result["framework"] == "nextjs"
        assert result.result["typescript"] is True
        assert result.result["tailwind_css"] is True
        assert len(result.result["generated_files"]) > 0
    
    @pytest.mark.asyncio 
    async def test_agent_collaboration_scenario(self):
        """Test escenario de colaboración entre agentes"""
        # Simular colaboración UI Agent -> NextJS Agent
        ui_agent = UIAgent()
        nextjs_agent = NextJSAgent()
        
        await ui_agent.initialize()
        await nextjs_agent.initialize()
        
        # Mock MCP communication
        ui_agent.mcp_client = Mock()
        nextjs_agent.mcp_client = Mock()
        
        # UI Agent genera sistema de diseño
        design_task = AgentTask(
            task_id="design_task",
            name="create_design_system",
            params={
                "design_system": "custom",
                "color_palette": "blue"
            }
        )
        
        ui_agent.template_engine = Mock()
        ui_agent.template_engine.render_template = Mock(return_value="design tokens")
        
        design_result = await ui_agent.execute_task(design_task)
        
        # NextJS Agent usa el sistema de diseño
        app_task = AgentTask(
            task_id="app_task", 
            name="generate_nextjs_app",
            params={
                "framework": "nextjs",
                "design_system": design_result.result
            }
        )
        
        nextjs_agent.template_engine = Mock()
        nextjs_agent.template_engine.render_template = Mock(return_value="app content")
        
        app_result = await nextjs_agent.execute_task(app_task)
        
        # Verificar colaboración exitosa
        assert design_result.success is True
        assert app_result.success is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
