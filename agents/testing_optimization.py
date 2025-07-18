# agents/testing_optimization.py
"""
Testing avanzado y optimización automática
Extiende PerformanceAgent existente
"""

from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path
import json

@dataclass
class TestConfig:
    """Configuración de testing avanzado"""
    e2e: bool = True
    visual_regression: bool = True
    performance: bool = True
    accessibility: bool = True
    coverage_threshold: float = 80.0

class AdvancedTestGenerator:
    """Generador de tests avanzados"""
    
    def __init__(self, agent):
        self.agent = agent
    
    async def generate_test_suite(self, component_path: Path, config: TestConfig) -> Dict[str, Any]:
        """Generar suite completa de tests"""
        
        results = {}
        
        if config.e2e:
            results["e2e"] = await self._generate_e2e_tests(component_path)
        
        if config.visual_regression:
            results["visual"] = await self._generate_visual_tests(component_path)
        
        if config.performance:
            results["performance"] = await self._generate_performance_tests(component_path)
        
        if config.accessibility:
            results["a11y"] = await self._generate_a11y_tests(component_path)
        
        return results
    
    async def _generate_e2e_tests(self, component_path: Path) -> str:
        """Generar tests E2E con Playwright"""
        
        prompt = f"""
        Genera tests E2E para componente en {component_path} usando Playwright:
        
        - Page Object Model
        - Test scenarios críticos
        - Mobile y desktop
        - Cross-browser compatibility
        - Data-testid selectors
        
        Incluye setup y teardown.
        """
        
        return await self.agent.call_llm_for_generation(prompt, {"path": component_path})
    
    async def _generate_visual_tests(self, component_path: Path) -> str:
        """Generar tests de regresión visual"""
        
        prompt = f"""
        Genera tests de regresión visual para {component_path}:
        
        - Screenshot comparisons
        - Multiple viewports
        - Different states (hover, focus, disabled)
        - Theme variations (light/dark)
        - Percy.io integration
        """
        
        return await self.agent.call_llm_for_generation(prompt, {"path": component_path})

class BundleOptimizer:
    """Optimizador automático de bundles"""
    
    def __init__(self, performance_agent):
        self.performance_agent = performance_agent
    
    async def analyze_and_optimize(self, project_path: Path) -> Dict[str, Any]:
        """Análisis y optimización completa"""
        
        # 1. Análisis de bundle
        bundle_analysis = await self._analyze_bundle(project_path)
        
        # 2. Code splitting automático
        splitting_suggestions = await self._suggest_code_splitting(project_path)
        
        # 3. Tree shaking optimization
        tree_shaking = await self._optimize_tree_shaking(project_path)
        
        # 4. Image optimization
        image_opts = await self._optimize_images(project_path)
        
        return {
            "bundle_analysis": bundle_analysis,
            "code_splitting": splitting_suggestions,
            "tree_shaking": tree_shaking,
            "image_optimization": image_opts,
            "recommendations": self._generate_optimization_plan(bundle_analysis)
        }
    
    async def _analyze_bundle(self, project_path: Path) -> Dict[str, Any]:
        """Análisis detallado del bundle"""
        
        # Buscar webpack-bundle-analyzer o similar
        package_json = project_path / "package.json"
        
        if package_json.exists():
            with open(package_json) as f:
                data = json.load(f)
            
            dependencies = data.get("dependencies", {})
            
            # Calcular impacto de dependencias
            heavy_deps = []
            total_estimated_size = 0
            
            size_estimates = {
                "react": 45, "react-dom": 130, "lodash": 70,
                "moment": 230, "three": 600, "chart.js": 200
            }
            
            for dep, version in dependencies.items():
                size = size_estimates.get(dep, 30)
                total_estimated_size += size
                
                if size > 100:
                    heavy_deps.append({"name": dep, "size": size, "version": version})
            
            return {
                "total_size_kb": total_estimated_size,
                "heavy_dependencies": heavy_deps,
                "dependency_count": len(dependencies),
                "optimization_score": min(100, max(0, 100 - (total_estimated_size / 10)))
            }
        
        return {"error": "package.json not found"}
    
    async def _suggest_code_splitting(self, project_path: Path) -> List[Dict[str, str]]:
        """Sugerir puntos de code splitting"""
        
        suggestions = []
        
        # Buscar páginas grandes
        pages_dir = project_path / "pages" or project_path / "src" / "pages"
        if pages_dir.exists():
            for page_file in pages_dir.glob("**/*.tsx"):
                size = page_file.stat().st_size
                if size > 50000:  # > 50KB
                    suggestions.append({
                        "file": str(page_file),
                        "type": "route_splitting",
                        "reason": f"Large page file ({size//1000}KB)",
                        "solution": "React.lazy() + Suspense"
                    })
        
        return suggestions
    
    def _generate_optimization_plan(self, analysis: Dict[str, Any]) -> List[str]:
        """Generar plan de optimización"""
        
        recommendations = []
        
        if analysis.get("total_size_kb", 0) > 500:
            recommendations.append("Bundle size crítico - implementar code splitting urgente")
        
        heavy_deps = analysis.get("heavy_dependencies", [])
        for dep in heavy_deps:
            if dep["name"] == "moment":
                recommendations.append("Reemplazar moment.js con date-fns (-200KB)")
            elif dep["name"] == "lodash":
                recommendations.append("Usar imports específicos de lodash")
        
        score = analysis.get("optimization_score", 0)
        if score < 50:
            recommendations.append("Score bajo - revisar dependencias y implementar lazy loading")
        
        return recommendations

class A11yEnhancer:
    """Mejorador automático de accesibilidad"""
    
    def __init__(self, ui_agent):
        self.ui_agent = ui_agent
    
    async def enhance_accessibility(self, component_code: str) -> Dict[str, Any]:
        """Mejorar accesibilidad automáticamente"""
        
        prompt = f"""
        Analiza y mejora la accesibilidad de este componente:
        
        {component_code}
        
        Aplica:
        - ARIA labels correctos
        - Focus management
        - Keyboard navigation
        - Screen reader support
        - Color contrast WCAG AA
        - Semantic HTML
        
        Devuelve código mejorado y explicación de cambios.
        """
        
        enhanced_code = await self.ui_agent.call_llm_for_generation(prompt, {"code": component_code})
        
        return {
            "enhanced_code": enhanced_code,
            "improvements": await self._analyze_improvements(component_code, enhanced_code)
        }
    
    async def _analyze_improvements(self, original: str, enhanced: str) -> List[str]:
        """Analizar mejoras aplicadas"""
        
        improvements = []
        
        if "aria-label" in enhanced and "aria-label" not in original:
            improvements.append("Agregado aria-label para screen readers")
        
        if "role=" in enhanced and "role=" not in original:
            improvements.append("Agregado role semántico")
        
        if "tabIndex" in enhanced and "tabIndex" not in original:
            improvements.append("Mejorado keyboard navigation")
        
        return improvements

# Extender PerformanceAgent existente
class EnhancedPerformanceAgent:
    """PerformanceAgent extendido con capacidades avanzadas"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.test_generator = AdvancedTestGenerator(base_agent)
        self.bundle_optimizer = BundleOptimizer(base_agent)
        self.a11y_enhancer = A11yEnhancer(base_agent)
    
    async def full_optimization_suite(self, project_path: Path, config: TestConfig) -> Dict[str, Any]:
        """Suite completa de optimización"""
        
        return {
            "tests": await self.test_generator.generate_test_suite(project_path, config),
            "bundle": await self.bundle_optimizer.analyze_and_optimize(project_path),
            "accessibility": await self._enhance_project_accessibility(project_path)
        }
    
    async def _enhance_project_accessibility(self, project_path: Path) -> Dict[str, Any]:
        """Mejorar accesibilidad del proyecto completo"""
        
        results = {"enhanced_files": [], "summary": []}
        
        # Buscar componentes principales
        components_dir = project_path / "src" / "components"
        if components_dir.exists():
            for component_file in components_dir.glob("**/*.tsx"):
                if component_file.stat().st_size < 100000:  # < 100KB
                    code = component_file.read_text()
                    enhanced = await self.a11y_enhancer.enhance_accessibility(code)
                    results["enhanced_files"].append({
                        "file": str(component_file),
                        "improvements": enhanced["improvements"]
                    })
        
        return results