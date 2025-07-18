# agents/component_types.py
"""
Generación granular de componentes con tipología atómica
Extiende agentes existentes sin romper arquitectura
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

class ComponentType(str, Enum):
    """Tipos de componentes según metodología atómica"""
    ATOM = "atom"           # Button, Input, Icon
    MOLECULE = "molecule"   # SearchBox, Card
    ORGANISM = "organism"   # Header, ProductList
    TEMPLATE = "template"   # PageLayout
    PAGE = "page"          # HomePage, ContactPage

@dataclass
class ComponentSpec:
    """Especificación detallada del componente"""
    name: str
    type: ComponentType
    props: List[Dict[str, Any]]
    variants: List[str] = None
    states: List[str] = None
    accessibility: bool = True
    storybook: bool = True
    tests: bool = True

class AtomicComponentGenerator:
    """Generador de componentes con metodología atómica"""
    
    def __init__(self, agent):
        self.agent = agent
        self.component_templates = self._load_atomic_templates()
    
    async def generate_component(self, spec: ComponentSpec) -> Dict[str, Any]:
        """Generar componente con especificación atómica"""
        
        # LLM prompt específico para tipo atómico
        prompt = self._build_atomic_prompt(spec)
        
        # Generar código del componente
        component_code = await self.agent.call_llm_for_generation(prompt, {
            "spec": spec,
            "component_type": spec.type.value
        })
        
        results = {
            "component": component_code,
            "files": []
        }
        
        # Generar archivos adicionales
        if spec.storybook:
            results["storybook"] = await self._generate_storybook(spec)
            results["files"].append(f"{spec.name}.stories.tsx")
        
        if spec.tests:
            results["tests"] = await self._generate_tests(spec)
            results["files"].append(f"{spec.name}.test.tsx")
        
        return results
    
    def _build_atomic_prompt(self, spec: ComponentSpec) -> str:
        """Construir prompt específico para tipo atómico"""
        type_guidelines = {
            ComponentType.ATOM: "Componente simple, sin dependencias, reutilizable",
            ComponentType.MOLECULE: "Combinación de átomos, funcionalidad específica",
            ComponentType.ORGANISM: "Sección compleja, múltiples moléculas",
            ComponentType.TEMPLATE: "Layout structure, placement guidelines",
            ComponentType.PAGE: "Instancia específica del template"
        }
        
        return f"""
        Genera un componente {spec.type.value} llamado {spec.name}.
        
        Guías para {spec.type.value}: {type_guidelines[spec.type]}
        
        Props: {spec.props}
        Variants: {spec.variants or ['default']}
        States: {spec.states or ['default']}
        
        Requisitos:
        - TypeScript con tipos estrictos
        - Accessibility: {spec.accessibility}
        - Composable y reutilizable
        - Siguiendo design system
        """

# Extender agentes existentes
class EnhancedReactAgent:
    """Extensión del ReactAgent con generación granular"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.atomic_generator = AtomicComponentGenerator(base_agent)
    
    async def generate_atomic_component(self, component_type: str, name: str, **kwargs) -> Dict[str, Any]:
        """Nuevo método para generación granular"""
        
        spec = ComponentSpec(
            name=name,
            type=ComponentType(component_type),
            props=kwargs.get('props', []),
            variants=kwargs.get('variants'),
            states=kwargs.get('states'),
            accessibility=kwargs.get('accessibility', True),
            storybook=kwargs.get('storybook', True),
            tests=kwargs.get('tests', True)
        )
        
        return await self.atomic_generator.generate_component(spec)
