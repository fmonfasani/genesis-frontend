# agents/ai_powered_features.py
"""
AI-Powered Features y PWA Generation
Extiende integración LLM existente con capacidades inteligentes
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import re

@dataclass
class AIGenerationConfig:
    """Configuración para generación con AI"""
    creativity_level: float = 0.7  # 0-1
    code_style: str = "modern"     # modern, conservative, experimental
    optimization_focus: str = "performance"  # performance, readability, size
    accessibility_priority: bool = True

class IntelligentComponentGenerator:
    """Generador inteligente de componentes con descripción natural"""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def generate_from_description(self, description: str, config: AIGenerationConfig) -> Dict[str, Any]:
        """Generar componente desde descripción natural"""
        
        # Analizar descripción con AI
        analysis = await self._analyze_description(description)
        
        # Generar código optimizado
        component_code = await self._generate_optimized_component(analysis, config)
        
        # Sugerir mejoras automáticas
        suggestions = await self._suggest_improvements(component_code, config)
        
        return {
            "component": component_code,
            "analysis": analysis,
            "suggestions": suggestions,
            "variants": await self._generate_variants(component_code, config)
        }
    
    async def _analyze_description(self, description: str) -> Dict[str, Any]:
        """Analizar descripción para extraer requisitos"""
        
        prompt = f"""
        Analiza esta descripción de componente y extrae:
        
        "{description}"
        
        Devuelve JSON con:
        {{
          "component_type": "button|card|form|etc",
          "main_purpose": "descripción clara",
          "required_props": [list of props],
          "states": [list of states],
          "interactions": [list of interactions],
          "accessibility_needs": [list of a11y requirements],
          "complexity_level": "simple|medium|complex",
          "suggested_patterns": [design patterns to use]
        }}
        """
        
        analysis_json = await self.agent.call_llm_for_generation(prompt, {"description": description})
        
        try:
            return json.loads(analysis_json)
        except:
            return {"component_type": "unknown", "complexity_level": "medium"}
    
    async def _generate_optimized_component(self, analysis: Dict[str, Any], config: AIGenerationConfig) -> str:
        """Generar componente optimizado basado en análisis"""
        
        prompt = f"""
        Genera componente React TypeScript optimizado:
        
        Análisis: {json.dumps(analysis, indent=2)}
        
        Optimizaciones requeridas:
        - Focus: {config.optimization_focus}
        - Style: {config.code_style}
        - Creativity: {config.creativity_level}
        - A11y Priority: {config.accessibility_priority}
        
        Incluye:
        - Memoización inteligente
        - Custom hooks si necesario
        - Error boundaries
        - TypeScript estricto
        - Performance optimizations
        - Modern React patterns
        """
        
        return await self.agent.call_llm_for_generation(prompt, {"analysis": analysis, "config": config})
    
    async def _suggest_improvements(self, code: str, config: AIGenerationConfig) -> List[str]:
        """Sugerir mejoras automáticas"""
        
        prompt = f"""
        Analiza este código y sugiere mejoras específicas:
        
        ```typescript
        {code}
        ```
        
        Focus en {config.optimization_focus}. Devuelve lista de mejoras concretas.
        """
        
        suggestions_text = await self.agent.call_llm_for_generation(prompt, {"code": code})
        
        # Parsear sugerencias
        suggestions = re.findall(r'[-•]\s*(.+)', suggestions_text)
        return suggestions[:5]  # Top 5 suggestions
    
    async def _generate_variants(self, base_code: str, config: AIGenerationConfig) -> List[Dict[str, str]]:
        """Generar variantes del componente"""
        
        variants = []
        variant_types = ["size", "color", "state", "layout"]
        
        for variant_type in variant_types:
            prompt = f"""
            Genera variante {variant_type} del componente:
            
            {base_code}
            
            Crea variación creativa manteniendo funcionalidad core.
            """
            
            variant_code = await self.agent.call_llm_for_generation(prompt, {"base": base_code, "type": variant_type})
            
            variants.append({
                "type": variant_type,
                "code": variant_code
            })
        
        return variants

class PWAGenerator:
    """Generador automático de PWA"""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def generate_pwa_setup(self, project_path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generar configuración PWA completa"""
        
        # 1. Manifest
        manifest = await self._generate_manifest(config)
        
        # 2. Service Worker
        service_worker = await self._generate_service_worker(config)
        
        # 3. Offline strategies
        offline_strategies = await self._generate_offline_strategies(project_path)
        
        # 4. Push notifications
        push_setup = await self._generate_push_notifications(config)
        
        return {
            "manifest": manifest,
            "service_worker": service_worker,
            "offline_strategies": offline_strategies,
            "push_notifications": push_setup,
            "installation_prompt": await self._generate_install_prompt()
        }
    
    async def _generate_manifest(self, config: Dict[str, Any]) -> str:
        """Generar manifest.json"""
        
        app_name = config.get("app_name", "Genesis PWA")
        theme_color = config.get("theme_color", "#3B82F6")
        
        manifest = {
            "name": app_name,
            "short_name": app_name[:12],
            "description": config.get("description", f"{app_name} - Progressive Web App"),
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": theme_color,
            "orientation": "portrait-primary",
            "scope": "/",
            "icons": [
                {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
                {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
                {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
            ],
            "categories": ["productivity", "utilities"],
            "shortcuts": [
                {"name": "Home", "url": "/", "icons": [{"src": "/icons/home.png", "sizes": "96x96"}]},
                {"name": "Profile", "url": "/profile", "icons": [{"src": "/icons/profile.png", "sizes": "96x96"}]}
            ]
        }
        
        return json.dumps(manifest, indent=2)
    
    async def _generate_service_worker(self, config: Dict[str, Any]) -> str:
        """Generar service worker inteligente"""
        
        cache_strategy = config.get("cache_strategy", "network_first")
        offline_pages = config.get("offline_pages", ["/", "/offline"])
        
        prompt = f"""
        Genera service worker moderno con:
        
        - Estrategia de cache: {cache_strategy}
        - Páginas offline: {offline_pages}
        - Background sync
        - Push notifications support
        - Automatic updates
        - Performance optimizations
        
        Incluye comentarios explicativos y error handling.
        """
        
        return await self.agent.call_llm_for_generation(prompt, {"config": config})
    
    async def _generate_offline_strategies(self, project_path: Path) -> Dict[str, Any]:
        """Generar estrategias offline inteligentes"""
        
        # Analizar tipos de contenido
        content_types = await self._analyze_content_types(project_path)
        
        strategies = {}
        
        for content_type in content_types:
            if content_type == "static_assets":
                strategies[content_type] = "cache_first"
            elif content_type == "api_data":
                strategies[content_type] = "network_first_with_fallback"
            elif content_type == "user_content":
                strategies[content_type] = "background_sync"
        
        return strategies
    
    async def _analyze_content_types(self, project_path: Path) -> List[str]:
        """Analizar tipos de contenido en el proyecto"""
        
        content_types = ["static_assets"]
        
        # Buscar llamadas API
        for tsx_file in project_path.glob("**/*.tsx"):
            try:
                content = tsx_file.read_text()
                if "fetch(" in content or "axios." in content:
                    content_types.append("api_data")
                    break
            except:
                continue
        
        # Buscar forms
        for tsx_file in project_path.glob("**/*.tsx"):
            try:
                content = tsx_file.read_text()
                if "<form" in content or "onSubmit" in content:
                    content_types.append("user_content")
                    break
            except:
                continue
        
        return list(set(content_types))
    
    async def _generate_install_prompt(self) -> str:
        """Generar prompt de instalación PWA"""
        
        prompt = """
        Genera componente React para install prompt PWA:
        
        - Detectar si PWA es instalable
        - UI atractiva para instalación
        - Manejo de beforeinstallprompt
        - Analytics de instalación
        - Responsive design
        - Accesibilidad completa
        """
        
        return await self.agent.call_llm_for_generation(prompt, {})

class LayoutOptimizer:
    """Optimizador inteligente de layouts"""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def optimize_layout(self, layout_code: str, target_devices: List[str]) -> Dict[str, Any]:
        """Optimizar layout para múltiples dispositivos"""
        
        prompt = f"""
        Optimiza este layout para dispositivos {target_devices}:
        
        {layout_code}
        
        Aplica:
        - CSS Grid/Flexbox moderno
        - Responsive breakpoints
        - Performance optimizations
        - Accessibility improvements
        - Modern CSS features (container queries, aspect-ratio)
        
        Devuelve código optimizado y explicación de cambios.
        """
        
        optimized = await self.agent.call_llm_for_generation(prompt, {"code": layout_code, "devices": target_devices})
        
        return {
            "optimized_code": optimized,
            "improvements": await self._analyze_layout_improvements(layout_code, optimized)
        }
    
    async def _analyze_layout_improvements(self, original: str, optimized: str) -> List[str]:
        """Analizar mejoras aplicadas al layout"""
        
        improvements = []
        
        if "grid" in optimized and "grid" not in original:
            improvements.append("Migrado a CSS Grid para mejor control de layout")
        
        if "@container" in optimized:
            improvements.append("Agregado container queries para responsive avanzado")
        
        if "aspect-ratio" in optimized:
            improvements.append("Usado aspect-ratio para mejores proporciones")
        
        return improvements

# Extender agentes existentes con AI features
class AIEnhancedAgent:
    """Agente con capacidades AI avanzadas"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.intelligent_generator = IntelligentComponentGenerator(base_agent)
        self.pwa_generator = PWAGenerator(base_agent)
        self.layout_optimizer = LayoutOptimizer(base_agent)
    
    async def ai_generate_component(self, description: str, config: AIGenerationConfig = None) -> Dict[str, Any]:
        """Generación inteligente desde descripción"""
        config = config or AIGenerationConfig()
        return await self.intelligent_generator.generate_from_description(description, config)
    
    async def create_pwa(self, project_path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
        """Crear PWA completa"""
        return await self.pwa_generator.generate_pwa_setup(project_path, config)
    
    async def optimize_layout_ai(self, layout_code: str, devices: List[str]) -> Dict[str, Any]:
        """Optimizar layout con AI"""
        return await self.layout_optimizer.optimize_layout(layout_code, devices)