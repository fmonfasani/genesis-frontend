"""
Configuración y fixtures para tests de Genesis Frontend

Este archivo contiene las configuraciones comunes y fixtures 
para todos los tests del ecosistema genesis-frontend.
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, AsyncMock
from typing import Dict, Any, Generator

from genesis_frontend.config import FrontendConfig
from genesis_frontend.agents.base_agent import FrontendAgent
from genesis_frontend.agents.nextjs_agent import NextJSAgent
from genesis_frontend.agents.react_agent import ReactAgent
from genesis_frontend.agents.vue_agent import VueAgent
from genesis_frontend.agents.ui_agent import UIAgent


# ===== CONFIGURACIÓN PYTEST =====

def pytest_configure(config):
    """Configuración global de pytest"""
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "slow: marks tests as slow running"
    )
    config.addinivalue_line(
        "markers", "agent: marks tests related to agents"
    )
    config.addinivalue_line(
        "markers", "llm: marks tests that require LLM integration"
    )


@pytest.fixture(scope="session")
def event_loop():
    """Crear event loop para tests asyncio"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ===== FIXTURES DE CONFIGURACIÓN =====

@pytest.fixture
def frontend_config():
    """Fixture para configuración frontend"""
    return FrontendConfig()


@pytest.fixture
def mock_template_engine():
    """Fixture para mock del template engine"""
    template_engine = Mock()
    template_engine.render_template = Mock(return_value="<!-- Mock template content -->")
    return template_engine


@pytest.fixture
def mock_mcp_client():
    """Fixture para mock del cliente MCP"""
    mcp_client = Mock()
    mcp_client.call_llm = AsyncMock(return_value={
        "content": "// Mock LLM generated code",
        "success": True
    })
    return mcp_client


# ===== FIXTURES DE DIRECTORIOS TEMPORALES =====

@pytest.fixture
def temp_project_dir():
    """Fixture para directorio temporal de proyecto"""
    temp_dir = tempfile.mkdtemp(prefix="genesis_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_project_structure(temp_project_dir):
    """Fixture para estructura de proyecto de ejemplo"""
    # Crear estructura básica
    directories = [
        "src/components",
        "src/pages", 
        "src/utils",
        "public",
        "docs"
    ]
    
    for directory in directories:
        (temp_project_dir / directory).mkdir(parents=True, exist_ok=True)
    
    # Crear archivos de ejemplo
    files = {
        "package.json": '{"name": "test-project", "version": "1.0.0"}',
        "src/App.tsx": "export default function App() { return <div>Test</div> }",
        "README.md": "# Test Project"
    }
    
    for file_path, content in files.items():
        (temp_project_dir / file_path).write_text(content)
    
    return temp_project_dir


# ===== FIXTURES DE AGENTES =====

@pytest.fixture
def base_frontend_agent(mock_template_engine, mock_mcp_client):
    """Fixture para agente frontend base configurado"""
    # Crear agente simple para testing
    class TestFrontendAgent(FrontendAgent):
        def __init__(self):
            super().__init__("test_agent", "TestAgent", "test")
        
        async def initialize(self):
            pass
        
        async def execute_task(self, task):
            from genesis_frontend.agents.base_agent import TaskResult
            return TaskResult(
                task_id=task.id,
                success=True,
                result={"status": "test_completed"}
            )
    
    agent = TestFrontendAgent()
    agent.set_template_engine(mock_template_engine)
    agent.set_mcp_client(mock_mcp_client)
    return agent


@pytest.fixture
async def nextjs_agent(mock_template_engine, mock_mcp_client):
    """Fixture para agente NextJS configurado"""
    agent = NextJSAgent()
    agent.set_template_engine(mock_template_engine)
    agent.set_mcp_client(mock_mcp_client)
    await agent.initialize()
    return agent


@pytest.fixture
async def react_agent(mock_template_engine, mock_mcp_client):
    """Fixture para agente React configurado"""
    agent = ReactAgent()
    agent.set_template_engine(mock_template_engine)
    agent.set_mcp_client(mock_mcp_client)
    await agent.initialize()
    return agent


@pytest.fixture
async def vue_agent(mock_template_engine, mock_mcp_client):
    """Fixture para agente Vue configurado"""
    agent = VueAgent()
    agent.set_template_engine(mock_template_engine)
    agent.set_mcp_client(mock_mcp_client)
    await agent.initialize()
    return agent


@pytest.fixture
async def ui_agent(mock_template_engine, mock_mcp_client):
    """Fixture para agente UI configurado"""
    agent = UIAgent()
    agent.set_template_engine(mock_template_engine)
    agent.set_mcp_client(mock_mcp_client)
    await agent.initialize()
    return agent


@pytest.fixture
def all_agents(nextjs_agent, react_agent, vue_agent, ui_agent):
    """Fixture con todos los agentes configurados"""
    return {
        "nextjs": nextjs_agent,
        "react": react_agent,
        "vue": vue_agent,
        "ui": ui_agent
    }


# ===== FIXTURES DE DATOS DE PRUEBA =====

@pytest.fixture
def sample_project_schema():
    """Fixture para schema de proyecto de ejemplo"""
    return {
        "project_name": "test-frontend-app",
        "description": "Test application for Genesis Frontend",
        "version": "1.0.0",
        "stack": {
            "frontend": "nextjs",
            "styling": "tailwindcss",
            "state_management": "redux_toolkit",
            "ui_library": "custom"
        },
        "features": [
            "authentication",
            "responsive_design",
            "dark_mode",
            "accessibility"
        ],
        "entities": [
            {
                "name": "User",
                "fields": [
                    {"name": "id", "type": "string"},
                    {"name": "email", "type": "string"},
                    {"name": "name", "type": "string"}
                ]
            },
            {
                "name": "Post",
                "fields": [
                    {"name": "id", "type": "string"},
                    {"name": "title", "type": "string"},
                    {"name": "content", "type": "text"},
                    {"name": "userId", "type": "string"}
                ]
            }
        ]
    }


@pytest.fixture
def sample_nextjs_config():
    """Fixture para configuración NextJS de ejemplo"""
    return {
        "framework": "nextjs",
        "typescript": True,
        "app_router": True,
        "tailwind_css": True,
        "state_management": "redux_toolkit",
        "ui_library": "tailwindcss",
        "features": ["authentication", "dark_mode"],
        "testing": True,
        "eslint": True
    }


@pytest.fixture
def sample_react_config():
    """Fixture para configuración React de ejemplo"""
    return {
        "framework": "react",
        "typescript": True,
        "build_tool": "vite",
        "state_management": "redux_toolkit",
        "ui_library": "tailwindcss",
        "routing": True,
        "testing": True,
        "pwa": False
    }


@pytest.fixture
def sample_vue_config():
    """Fixture para configuración Vue de ejemplo"""
    return {
        "framework": "vue",
        "vue_version": "3",
        "typescript": True,
        "composition_api": True,
        "state_management": "pinia",
        "ui_library": "custom",
        "router": True,
        "testing": True
    }


@pytest.fixture
def sample_ui_config():
    """Fixture para configuración UI de ejemplo"""
    return {
        "design_system": "custom",
        "color_palette": "blue",
        "dark_mode": True,
        "accessibility": True,
        "component_library": "custom",
        "design_tokens": True
    }


# ===== FIXTURES DE TASKS Y REQUESTS =====

@pytest.fixture
def sample_agent_task(sample_project_schema, temp_project_dir):
    """Fixture para tarea de agente de ejemplo"""
    from genesis_frontend.agents.base_agent import AgentTask
    
    return AgentTask(
        task_id="test_task_123",
        name="generate_frontend_app",
        params={
            "output_path": str(temp_project_dir),
            "framework": "nextjs",
            "schema": sample_project_schema,
            "typescript": True,
            "tailwind_css": True
        }
    )


@pytest.fixture
def sample_mcp_request():
    """Fixture para request MCP de ejemplo"""
    from genesis_frontend.agents.base_agent import MCPRequest
    
    return MCPRequest(
        request_id="mcp_req_123",
        action="generate_nextjs_app",
        data={
            "framework": "nextjs",
            "typescript": True,
            "output_path": "/tmp/test-project"
        }
    )


# ===== FIXTURES DE VALIDACIÓN =====

@pytest.fixture
def validator_functions():
    """Fixture con funciones de validación comunes"""
    def validate_agent_compliance(agent: FrontendAgent) -> Dict[str, bool]:
        """Validar cumplimiento de doctrina del ecosistema"""
        return {
            "has_mcp_handlers": hasattr(agent, 'handle_mcp_request'),
            "has_llm_integration": hasattr(agent, 'call_llm_for_generation'),
            "has_template_collaboration": hasattr(agent, 'render_template'),
            "no_cli_functionality": not hasattr(agent, 'cli'),
            "no_orchestration": not hasattr(agent, 'orchestrate'),
            "frontend_only": agent.specialization in ['nextjs', 'react', 'vue', 'ui']
        }
    
    def validate_generated_files(file_paths: list, expected_extensions: list) -> bool:
        """Validar archivos generados"""
        for file_path in file_paths:
            path = Path(file_path)
            if not path.exists():
                return False
            if path.suffix not in expected_extensions:
                return False
        return True
    
    def validate_package_json(package_json_path: Path) -> Dict[str, Any]:
        """Validar package.json generado"""
        import json
        
        if not package_json_path.exists():
            return {"valid": False, "error": "File not found"}
        
        try:
            with open(package_json_path) as f:
                data = json.load(f)
            
            required_fields = ["name", "version", "dependencies", "scripts"]
            missing_fields = [field for field in required_fields if field not in data]
            
            return {
                "valid": len(missing_fields) == 0,
                "missing_fields": missing_fields,
                "data": data
            }
        except json.JSONDecodeError as e:
            return {"valid": False, "error": f"Invalid JSON: {e}"}
    
    return {
        "validate_agent_compliance": validate_agent_compliance,
        "validate_generated_files": validate_generated_files,
        "validate_package_json": validate_package_json
    }


# ===== FIXTURES DE PERFORMANCE =====

@pytest.fixture
def performance_monitor():
    """Fixture para monitorear performance de tests"""
    import time
    
    class PerformanceMonitor:
        def __init__(self):
            self.start_time = None
            self.end_time = None
        
        def start(self):
            self.start_time = time.time()
        
        def stop(self):
            self.end_time = time.time()
        
        @property
        def duration(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
        
        def assert_faster_than(self, max_seconds):
            assert self.duration is not None, "Monitor not stopped"
            assert self.duration < max_seconds, f"Test took {self.duration}s, expected < {max_seconds}s"
    
    return PerformanceMonitor()


# ===== FIXTURES DE INTEGRACIÓN =====

@pytest.fixture
def integration_environment(temp_project_dir, all_agents, sample_project_schema):
    """Fixture para entorno de integración completo"""
    return {
        "project_dir": temp_project_dir,
        "agents": all_agents,
        "schema": sample_project_schema,
        "configs": {
            "nextjs": sample_nextjs_config(),
            "react": sample_react_config(),
            "vue": sample_vue_config(),
            "ui": sample_ui_config()
        }
    }


# ===== HELPERS PARA TESTS =====

@pytest.fixture
def test_helpers():
    """Fixture con funciones helper para tests"""
    
    def create_mock_llm_response(content: str, success: bool = True) -> Dict[str, Any]:
        """Crear respuesta mock de LLM"""
        return {
            "content": content,
            "success": success,
            "model": "mock-model",
            "tokens": len(content.split())
        }
    
    def create_mock_template_content(template_type: str) -> str:
        """Crear contenido mock de template"""
        templates = {
            "package_json": '{"name": "mock-project", "version": "1.0.0"}',
            "component": "export default function MockComponent() { return <div>Mock</div> }",
            "page": "export default function MockPage() { return <main>Mock Page</main> }",
            "config": "module.exports = { mock: true }"
        }
        return templates.get(template_type, "// Mock template content")
    
    async def wait_for_agent_task(agent, task, timeout: float = 5.0):
        """Esperar que un agente complete una tarea"""
        return await asyncio.wait_for(agent.execute_task(task), timeout=timeout)
    
    return {
        "create_mock_llm_response": create_mock_llm_response,
        "create_mock_template_content": create_mock_template_content,
        "wait_for_agent_task": wait_for_agent_task
    }


# ===== CONFIGURACIÓN DE MOCKS GLOBALES =====

@pytest.fixture(autouse=True)
def mock_external_dependencies(monkeypatch):
    """Mock automático de dependencias externas"""
    # Mock subprocess calls
    def mock_subprocess_run(*args, **kwargs):
        # Simular respuestas exitosas para comandos comunes
        if args[0] and args[0][0] == 'node':
            return Mock(returncode=0, stdout="v18.17.0")
        elif args[0] and args[0][0] == 'npm':
            return Mock(returncode=0, stdout="9.8.1")
        return Mock(returncode=0, stdout="")
    
    monkeypatch.setattr("subprocess.run", mock_subprocess_run)
    
    # Mock file system operations que podrían fallar
    original_mkdir = Path.mkdir
    def safe_mkdir(self, *args, **kwargs):
        try:
            return original_mkdir(self, *args, **kwargs)
        except Exception:
            pass
    
    monkeypatch.setattr(Path, "mkdir", safe_mkdir)


# ===== FIXTURES DE CLEANUP =====

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """Cleanup automático después de cada test"""
    yield
    # Cualquier cleanup necesario se hace aquí
    # Por ejemplo, limpiar archivos temporales, resetear estado global, etc.
    pass
