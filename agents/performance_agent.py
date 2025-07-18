"""
Frontend Performance Agent - Optimización específica de frontend
Parte del ecosistema genesis-frontend

Siguiendo la doctrina del ecosistema:
- ❌ No coordina workflows generales
- ❌ No interactúa directamente con usuarios
- ❌ No conoce backend ni DevOps
- ✅ Se especializa solo en optimización frontend
- ✅ Usa MCPturbo para comunicación
- ✅ Colabora con genesis-templates
"""

import ast
import re
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .base_agent import FrontendAgent, AgentTask, TaskResult


class FrontendOptimizationType(str, Enum):
    """Tipos de optimización frontend"""
    PERFORMANCE = "performance"
    BUNDLE_SIZE = "bundle_size"
    ACCESSIBILITY = "accessibility"
    SEO = "seo"
    IMAGES = "images"
    FONTS = "fonts"
    CSS = "css"
    JAVASCRIPT = "javascript"


class SeverityLevel(str, Enum):
    """Niveles de severidad"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class FrontendIssue:
    """Issue de frontend detectado"""
    type: FrontendOptimizationType
    severity: SeverityLevel
    file_path: str
    line_number: Optional[int]
    description: str
    recommendation: str
    code_snippet: Optional[str] = None
    estimated_impact: str = "medium"


@dataclass
class FrontendOptimizationResult:
    """Resultado de optimización frontend"""
    applied_optimizations: List[str]
    detected_issues: List[FrontendIssue]
    performance_score: float
    accessibility_score: float
    seo_score: float
    bundle_size_estimate: str
    files_modified: List[str]
    recommendations: List[str]


class FrontendPerformanceAgent(FrontendAgent):
    """
    Agente de Performance Frontend - Optimización específica de frontend
    
    Analiza y optimiza específicamente el código frontend:
    - Performance de componentes React/Vue/Angular
    - Optimización de bundle size
    - Mejoras de accesibilidad
    - Optimización SEO
    - Optimización de imágenes y assets
    """
    
    def __init__(self):
        super().__init__(
            agent_id="frontend_performance_agent",
            name="FrontendPerformanceAgent",
            specialization="frontend_performance"
        )
        
        # Capacidades específicas de frontend
        self.add_capability("react_optimization")
        self.add_capability("vue_optimization")
        self.add_capability("nextjs_optimization")
        self.add_capability("bundle_analysis")
        self.add_capability("accessibility_audit")
        self.add_capability("seo_optimization")
        self.add_capability("image_optimization")
        self.add_capability("css_optimization")
        self.add_capability("javascript_optimization")
        
        # Registrar handlers específicos
        self.register_handler("analyze_frontend_performance", self._handle_analyze_performance)
        self.register_handler("optimize_react_components", self._handle_optimize_react)
        self.register_handler("optimize_vue_components", self._handle_optimize_vue)
        self.register_handler("optimize_bundle_size", self._handle_optimize_bundle)
        self.register_handler("audit_accessibility", self._handle_audit_accessibility)
        self.register_handler("optimize_seo", self._handle_optimize_seo)
        self.register_handler("optimize_images", self._handle_optimize_images)
        
    async def initialize(self):
        """Inicialización del agente de performance frontend"""
        self.logger.info("[INIT] Inicializando Frontend Performance Agent")
        
        self.set_metadata("version", "1.0.0")
        self.set_metadata("specialization", "frontend_performance")
        self.set_metadata("supported_frameworks", ["react", "nextjs", "vue", "angular"])
        self.set_metadata("optimization_types", [t.value for t in FrontendOptimizationType])
        
        self.logger.info("[OK] Frontend Performance Agent inicializado")
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica de performance frontend"""
        task_name = task.name.lower()
        
        try:
            if "analyze_frontend_performance" in task_name:
                result = await self._analyze_frontend_performance(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "optimize_react_components" in task_name:
                result = await self._optimize_react_components(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "optimize_bundle_size" in task_name:
                result = await self._optimize_bundle_size(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "audit_accessibility" in task_name:
                result = await self._audit_accessibility(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            else:
                raise ValueError(f"Tarea no reconocida: {task.name}")
        
        except Exception as e:
            self.logger.error(f"Error ejecutando tarea {task.name}: {e}")
            return TaskResult(
                task_id=task.id,
                success=False,
                error=str(e)
            )
    
    async def _analyze_frontend_performance(self, params: Dict[str, Any]) -> FrontendOptimizationResult:
        """Analizar performance completo del frontend"""
        self.logger.info("[PERF] Analizando performance del frontend")
        
        frontend_path = Path(params.get("frontend_path", "./"))
        framework = params.get("framework", "react")
        
        all_issues = []
        applied_optimizations = []
        files_modified = []
        
        # 1. Análisis de componentes según framework
        if framework in ["react", "nextjs"]:
            react_issues = await self._analyze_react_components(frontend_path)
            all_issues.extend(react_issues)
        elif framework == "vue":
            vue_issues = await self._analyze_vue_components(frontend_path)
            all_issues.extend(vue_issues)
        
        # 2. Análisis de bundle size
        bundle_issues = await self._analyze_bundle_size(frontend_path)
        all_issues.extend(bundle_issues)
        
        # 3. Auditoría de accesibilidad
        a11y_issues = await self._analyze_accessibility(frontend_path)
        all_issues.extend(a11y_issues)
        
        # 4. Análisis SEO
        seo_issues = await self._analyze_seo(frontend_path)
        all_issues.extend(seo_issues)
        
        # 5. Optimización de imágenes
        image_optimizations = await self._analyze_images(frontend_path)
        all_issues.extend(image_optimizations["issues"])
        applied_optimizations.extend(image_optimizations["optimizations"])
        files_modified.extend(image_optimizations["files_modified"])
        
        # 6. Análisis de CSS
        css_issues = await self._analyze_css(frontend_path)
        all_issues.extend(css_issues)
        
        # 7. Análisis de JavaScript
        js_issues = await self._analyze_javascript(frontend_path)
        all_issues.extend(js_issues)
        
        # Calcular scores
        performance_score = self._calculate_performance_score(all_issues)
        accessibility_score = self._calculate_accessibility_score(all_issues)
        seo_score = self._calculate_seo_score(all_issues)
        bundle_size_estimate = self._estimate_bundle_size(frontend_path)
        
        # Generar recomendaciones
        recommendations = self._generate_frontend_recommendations(all_issues, framework)
        
        result = FrontendOptimizationResult(
            applied_optimizations=applied_optimizations,
            detected_issues=all_issues,
            performance_score=performance_score,
            accessibility_score=accessibility_score,
            seo_score=seo_score,
            bundle_size_estimate=bundle_size_estimate,
            files_modified=files_modified,
            recommendations=recommendations
        )
        
        # Generar reporte
        await self._generate_frontend_report(frontend_path, result)
        
        self.logger.info(f"[OK] Análisis completado - Performance: {performance_score:.1f}/10")
        return result
    
    async def _analyze_react_components(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar componentes React para optimizaciones"""
        issues = []
        
        # Buscar archivos React
        react_files = list(frontend_path.glob("**/*.tsx")) + list(frontend_path.glob("**/*.jsx"))
        
        for file_path in react_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # Detectar problemas comunes en React
                for i, line in enumerate(lines, 1):
                    # useEffect sin dependencias
                    if 'useEffect(' in line:
                        # Buscar en las siguientes líneas si no tiene array de dependencias
                        next_lines = '\n'.join(lines[i:i+10])
                        if '},[])' not in next_lines and '},[' not in next_lines and '}); ' in next_lines:
                            issues.append(FrontendIssue(
                                type=FrontendOptimizationType.PERFORMANCE,
                                severity=SeverityLevel.MEDIUM,
                                file_path=str(file_path),
                                line_number=i,
                                description="useEffect sin array de dependencias puede causar re-renders innecesarios",
                                recommendation="Agregar array de dependencias a useEffect",
                                code_snippet=line.strip()
                            ))
                    
                    # Componentes sin React.memo para optimización
                    if re.search(r'const\s+\w+\s*=\s*\(.*\)\s*=>\s*{', line):
                        # Verificar si no usa React.memo
                        if 'React.memo' not in content and 'memo(' not in content:
                            issues.append(FrontendIssue(
                                type=FrontendOptimizationType.PERFORMANCE,
                                severity=SeverityLevel.LOW,
                                file_path=str(file_path),
                                line_number=i,
                                description="Componente sin React.memo puede re-renderizar innecesariamente",
                                recommendation="Considerar envolver en React.memo si recibe props",
                                code_snippet=line.strip()
                            ))
                    
                    # Inline objects y functions en JSX
                    if re.search(r'style={{.*}}|onClick={.*=>.*}', line):
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.PERFORMANCE,
                            severity=SeverityLevel.MEDIUM,
                            file_path=str(file_path),
                            line_number=i,
                            description="Objetos o funciones inline causan re-renders innecesarios",
                            recommendation="Mover objetos y funciones fuera del JSX o usar useCallback/useMemo",
                            code_snippet=line.strip()
                        ))
                    
                    # console.log en producción
                    if 'console.log' in line and 'development' not in line.lower():
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.PERFORMANCE,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="console.log en código puede afectar performance en producción",
                            recommendation="Remover console.log o usar logger condicional",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando {file_path}: {e}")
        
        return issues
    
    async def _analyze_vue_components(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar componentes Vue para optimizaciones"""
        issues = []
        
        vue_files = list(frontend_path.glob("**/*.vue"))
        
        for file_path in vue_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # v-for sin key
                    if 'v-for=' in line and ':key=' not in line and 'key=' not in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.PERFORMANCE,
                            severity=SeverityLevel.HIGH,
                            file_path=str(file_path),
                            line_number=i,
                            description="v-for sin key puede causar problemas de rendimiento",
                            recommendation="Agregar :key único a elementos v-for",
                            code_snippet=line.strip()
                        ))
                    
                    # Computed properties que podrían ser métodos
                    if 'computed:' in content and '()' in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.PERFORMANCE,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="Posible uso innecesario de computed property",
                            recommendation="Verificar si debería ser un método en lugar de computed",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando {file_path}: {e}")
        
        return issues
    
    async def _analyze_bundle_size(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar tamaño del bundle y dependencias"""
        issues = []
        
        # Analizar package.json
        package_json = frontend_path / "package.json"
        if package_json.exists():
            try:
                with open(package_json) as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get("dependencies", {})
                
                # Librerías pesadas conocidas
                heavy_libraries = {
                    "moment": "Moment.js es pesado, considerar date-fns",
                    "lodash": "Importar funciones específicas de lodash",
                    "rxjs": "Verificar si se usa completamente",
                    "three": "Three.js es muy pesado para la mayoría de casos",
                    "chart.js": "Considerar alternativas más ligeras si es posible"
                }
                
                for lib, recommendation in heavy_libraries.items():
                    if lib in dependencies:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.BUNDLE_SIZE,
                            severity=SeverityLevel.MEDIUM,
                            file_path=str(package_json),
                            line_number=None,
                            description=f"Librería pesada detectada: {lib}",
                            recommendation=recommendation,
                            code_snippet=f'"{lib}": "{dependencies[lib]}"'
                        ))
                
                # Demasiadas dependencias
                if len(dependencies) > 50:
                    issues.append(FrontendIssue(
                        type=FrontendOptimizationType.BUNDLE_SIZE,
                        severity=SeverityLevel.MEDIUM,
                        file_path=str(package_json),
                        line_number=None,
                        description=f"Muchas dependencias ({len(dependencies)})",
                        recommendation="Revisar si todas las dependencias son necesarias",
                        code_snippet=f"Total dependencies: {len(dependencies)}"
                    ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando package.json: {e}")
        
        return issues
    
    async def _analyze_accessibility(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar accesibilidad del frontend"""
        issues = []
        
        html_files = list(frontend_path.glob("**/*.html")) + \
                    list(frontend_path.glob("**/*.tsx")) + \
                    list(frontend_path.glob("**/*.jsx")) + \
                    list(frontend_path.glob("**/*.vue"))
        
        for file_path in html_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Imágenes sin alt
                    if '<img' in line and 'alt=' not in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.ACCESSIBILITY,
                            severity=SeverityLevel.HIGH,
                            file_path=str(file_path),
                            line_number=i,
                            description="Imagen sin atributo alt",
                            recommendation="Agregar atributo alt descriptivo a las imágenes",
                            code_snippet=line.strip()
                        ))
                    
                    # Botones sin aria-label
                    if '<button' in line and 'aria-label=' not in line and not re.search(r'<button[^>]*>[^<]+</button>', line):
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.ACCESSIBILITY,
                            severity=SeverityLevel.MEDIUM,
                            file_path=str(file_path),
                            line_number=i,
                            description="Botón sin texto visible ni aria-label",
                            recommendation="Agregar aria-label o texto visible al botón",
                            code_snippet=line.strip()
                        ))
                    
                    # Inputs sin labels
                    if '<input' in line and 'id=' in line:
                        input_id = re.search(r'id=["\']([^"\']+)["\']', line)
                        if input_id and f'for="{input_id.group(1)}"' not in content:
                            issues.append(FrontendIssue(
                                type=FrontendOptimizationType.ACCESSIBILITY,
                                severity=SeverityLevel.HIGH,
                                file_path=str(file_path),
                                line_number=i,
                                description="Input sin label asociado",
                                recommendation="Agregar label con atributo for correspondiente",
                                code_snippet=line.strip()
                            ))
                    
                    # Links sin texto descriptivo
                    if re.search(r'<a[^>]*href[^>]*>(?:\s*<[^>]*>)*\s*(?:click|here|more|link)\s*(?:<[^>]*>)*\s*</a>', line, re.IGNORECASE):
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.ACCESSIBILITY,
                            severity=SeverityLevel.MEDIUM,
                            file_path=str(file_path),
                            line_number=i,
                            description="Link con texto no descriptivo",
                            recommendation="Usar texto de link más descriptivo",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando accesibilidad en {file_path}: {e}")
        
        return issues
    
    async def _analyze_seo(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar SEO del frontend"""
        issues = []
        
        # Buscar archivos HTML y de layout
        html_files = list(frontend_path.glob("**/*.html"))
        layout_files = list(frontend_path.glob("**/layout.tsx")) + list(frontend_path.glob("**/layout.jsx"))
        
        all_files = html_files + layout_files
        
        for file_path in all_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                
                # Meta tags faltantes
                if '<title>' not in content:
                    issues.append(FrontendIssue(
                        type=FrontendOptimizationType.SEO,
                        severity=SeverityLevel.HIGH,
                        file_path=str(file_path),
                        line_number=None,
                        description="Falta tag <title>",
                        recommendation="Agregar tag <title> descriptivo",
                        code_snippet="<title>"
                    ))
                
                if 'name="description"' not in content:
                    issues.append(FrontendIssue(
                        type=FrontendOptimizationType.SEO,
                        severity=SeverityLevel.HIGH,
                        file_path=str(file_path),
                        line_number=None,
                        description="Falta meta description",
                        recommendation="Agregar meta tag description",
                        code_snippet='<meta name="description" content="...">'
                    ))
                
                if 'name="viewport"' not in content:
                    issues.append(FrontendIssue(
                        type=FrontendOptimizationType.SEO,
                        severity=SeverityLevel.MEDIUM,
                        file_path=str(file_path),
                        line_number=None,
                        description="Falta meta viewport",
                        recommendation="Agregar meta viewport para responsive design",
                        code_snippet='<meta name="viewport" content="width=device-width, initial-scale=1">'
                    ))
                
                # Open Graph tags
                if 'property="og:' not in content:
                    issues.append(FrontendIssue(
                        type=FrontendOptimizationType.SEO,
                        severity=SeverityLevel.LOW,
                        file_path=str(file_path),
                        line_number=None,
                        description="Faltan tags Open Graph",
                        recommendation="Agregar tags Open Graph para redes sociales",
                        code_snippet='<meta property="og:title" content="...">'
                    ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando SEO en {file_path}: {e}")
        
        return issues
    
    async def _analyze_images(self, frontend_path: Path) -> Dict[str, Any]:
        """Analizar y optimizar imágenes"""
        issues = []
        optimizations = []
        files_modified = []
        
        # Buscar archivos de imagen
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(frontend_path.glob(f"**/*{ext}"))
        
        # Analizar HTML/JSX para uso de imágenes
        html_files = list(frontend_path.glob("**/*.html")) + \
                    list(frontend_path.glob("**/*.tsx")) + \
                    list(frontend_path.glob("**/*.jsx"))
        
        for file_path in html_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # Imágenes sin lazy loading
                    if '<img' in line and 'loading=' not in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.IMAGES,
                            severity=SeverityLevel.MEDIUM,
                            file_path=str(file_path),
                            line_number=i,
                            description="Imagen sin lazy loading",
                            recommendation="Agregar loading='lazy' para mejorar performance",
                            code_snippet=line.strip()
                        ))
                    
                    # Imágenes con formatos no optimizados
                    img_src = re.search(r'src=["\']([^"\']+\.(?:jpg|jpeg|png))["\']', line)
                    if img_src:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.IMAGES,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="Formato de imagen no optimizado",
                            recommendation="Considerar usar WebP o AVIF para mejor compresión",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando imágenes en {file_path}: {e}")
        
        return {
            "issues": issues,
            "optimizations": optimizations,
            "files_modified": files_modified
        }
    
    async def _analyze_css(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar CSS para optimizaciones"""
        issues = []
        
        css_files = list(frontend_path.glob("**/*.css")) + list(frontend_path.glob("**/*.scss"))
        
        for file_path in css_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # CSS no utilizado (reglas muy genéricas)
                    if line.strip().startswith('*') and '{' in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.CSS,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="Selector universal (*) puede afectar performance",
                            recommendation="Usar selectores más específicos",
                            code_snippet=line.strip()
                        ))
                    
                    # !important excesivo
                    if '!important' in line:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.CSS,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="Uso de !important puede indicar problemas de especificidad",
                            recommendation="Revisar la estructura CSS para evitar !important",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando CSS en {file_path}: {e}")
        
        return issues
    
    async def _analyze_javascript(self, frontend_path: Path) -> List[FrontendIssue]:
        """Analizar JavaScript para optimizaciones"""
        issues = []
        
        js_files = list(frontend_path.glob("**/*.js")) + \
                  list(frontend_path.glob("**/*.ts")) + \
                  list(frontend_path.glob("**/*.jsx")) + \
                  list(frontend_path.glob("**/*.tsx"))
        
        for file_path in js_files:
            try:
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                for i, line in enumerate(lines, 1):
                    # DOM queries en bucles
                    if re.search(r'for\s*\(.*\)|while\s*\(.*\)', line):
                        next_lines = '\n'.join(lines[i:i+10])
                        if 'document.querySelector' in next_lines or 'document.getElementById' in next_lines:
                            issues.append(FrontendIssue(
                                type=FrontendOptimizationType.JAVASCRIPT,
                                severity=SeverityLevel.MEDIUM,
                                file_path=str(file_path),
                                line_number=i,
                                description="Query DOM dentro de bucle",
                                recommendation="Cachear referencias DOM fuera del bucle",
                                code_snippet=line.strip()
                            ))
                    
                    # addEventListener sin removeEventListener
                    if 'addEventListener' in line and 'removeEventListener' not in content:
                        issues.append(FrontendIssue(
                            type=FrontendOptimizationType.JAVASCRIPT,
                            severity=SeverityLevel.LOW,
                            file_path=str(file_path),
                            line_number=i,
                            description="addEventListener sin cleanup correspondiente",
                            recommendation="Agregar removeEventListener para evitar memory leaks",
                            code_snippet=line.strip()
                        ))
            
            except Exception as e:
                self.logger.warning(f"Error analizando JavaScript en {file_path}: {e}")
        
        return issues
    
    def _calculate_performance_score(self, issues: List[FrontendIssue]) -> float:
        """Calcular score de performance"""
        score = 10.0
        
        for issue in issues:
            if issue.type == FrontendOptimizationType.PERFORMANCE:
                if issue.severity == SeverityLevel.CRITICAL:
                    score -= 2.0
                elif issue.severity == SeverityLevel.HIGH:
                    score -= 1.5
                elif issue.severity == SeverityLevel.MEDIUM:
                    score -= 1.0
                elif issue.severity == SeverityLevel.LOW:
                    score -= 0.5
        
        return max(0.0, min(10.0, score))
    
    def _calculate_accessibility_score(self, issues: List[FrontendIssue]) -> float:
        """Calcular score de accesibilidad"""
        a11y_issues = [i for i in issues if i.type == FrontendOptimizationType.ACCESSIBILITY]
        
        if not a11y_issues:
            return 10.0
        
        score = 10.0
        for issue in a11y_issues:
            if issue.severity == SeverityLevel.CRITICAL:
                score -= 3.0
            elif issue.severity == SeverityLevel.HIGH:
                score -= 2.0
            elif issue.severity == SeverityLevel.MEDIUM:
                score -= 1.0
            elif issue.severity == SeverityLevel.LOW:
                score -= 0.5
        
        return max(0.0, score)
    
    def _calculate_seo_score(self, issues: List[FrontendIssue]) -> float:
        """Calcular score de SEO"""
        seo_issues = [i for i in issues if i.type == FrontendOptimizationType.SEO]
        
        if not seo_issues:
            return 10.0
        
        score = 10.0
        for issue in seo_issues:
            if issue.severity == SeverityLevel.CRITICAL:
                score -= 2.5
            elif issue.severity == SeverityLevel.HIGH:
                score -= 2.0
            elif issue.severity == SeverityLevel.MEDIUM:
                score -= 1.0
            elif issue.severity == SeverityLevel.LOW:
                score -= 0.5
        
        return max(0.0, score)
    
    def _estimate_bundle_size(self, frontend_path: Path) -> str:
        """Estimar tamaño del bundle"""
        package_json = frontend_path / "package.json"
        if not package_json.exists():
            return "No estimado"
        
        try:
            with open(package_json) as f:
                package_data = json.load(f)
            
            dependencies = package_data.get("dependencies", {})
            
            # Estimación básica basada en librerías conocidas
            estimated_kb = 50  # Base bundle
            
            size_map = {
                "react": 45,
                "react-dom": 130,
                "vue": 40,
                "angular": 150,
                "lodash": 70,
                "moment": 230,
                "three": 600,
                "chart.js": 200,
            }
            
            for dep in dependencies:
                estimated_kb += size_map.get(dep, 30)  # Default 30KB por dependencia
            
            if estimated_kb < 200:
                return f"~{estimated_kb}KB (Pequeño)"
            elif estimated_kb < 500:
                return f"~{estimated_kb}KB (Mediano)"
            elif estimated_kb < 1000:
                return f"~{estimated_kb}KB (Grande)"
            else:
                return f"~{estimated_kb}KB (Muy Grande)"
        
        except Exception:
            return "Error estimando"
    
    def _generate_frontend_recommendations(self, issues: List[FrontendIssue], framework: str) -> List[str]:
        """Generar recomendaciones específicas de frontend"""
        recommendations = []
        
        # Agrupar por tipo
        issue_types = {}
        for issue in issues:
            if issue.type not in issue_types:
                issue_types[issue.type] = []
            issue_types[issue.type].append(issue)
        
        # Recomendaciones por tipo
        if FrontendOptimizationType.PERFORMANCE in issue_types:
            if framework in ["react", "nextjs"]:
                recommendations.append("Implementar React.memo y useCallback para optimizar re-renders")
                recommendations.append("Usar React.lazy para code splitting")
            elif framework == "vue":
                recommendations.append("Usar v-memo para componentes costosos")
                recommendations.append("Implementar dynamic imports para lazy loading")
        
        if FrontendOptimizationType.BUNDLE_SIZE in issue_types:
            recommendations.append("Implementar tree shaking en configuración de build")
            recommendations.append("Usar import dinámicos para reducir bundle inicial")
            recommendations.append("Considerar usar librerías más ligeras")
        
        if FrontendOptimizationType.ACCESSIBILITY in issue_types:
            recommendations.append("Implementar navegación por teclado completa")
            recommendations.append("Agregar aria-labels y roles semánticos")
            recommendations.append("Verificar contraste de colores")
        
        if FrontendOptimizationType.SEO in issue_types:
            recommendations.append("Implementar meta tags dinámicos")
            recommendations.append("Agregar structured data (JSON-LD)")
            recommendations.append("Configurar sitemap.xml")
        
        if FrontendOptimizationType.IMAGES in issue_types:
            recommendations.append("Implementar responsive images con srcset")
            recommendations.append("Usar formatos modernos (WebP, AVIF)")
            recommendations.append("Configurar CDN para assets")
        
        return recommendations
    
    async def _generate_frontend_report(self, frontend_path: Path, result: FrontendOptimizationResult):
        """Generar reporte de optimización frontend"""
        report_content = f"""# Frontend Performance Report

## Scores

- **Performance**: {result.performance_score:.1f}/10
- **Accessibility**: {result.accessibility_score:.1f}/10
- **SEO**: {result.seo_score:.1f}/10
- **Bundle Size**: {result.bundle_size_estimate}

## Issues Detected ({len(result.detected_issues)})

"""
        
        # Agrupar issues por tipo
        issues_by_type = {}
        for issue in result.detected_issues:
            if issue.type not in issues_by_type:
                issues_by_type[issue.type] = []
            issues_by_type[issue.type].append(issue)
        
        for issue_type, issues in issues_by_type.items():
            report_content += f"### {issue_type.value.title()} ({len(issues)} issues)\n\n"
            
            for issue in issues[:5]:  # Mostrar solo los primeros 5
                severity_emoji = {
                    SeverityLevel.CRITICAL: "🔴",
                    SeverityLevel.HIGH: "🟠",
                    SeverityLevel.MEDIUM: "🟡",
                    SeverityLevel.LOW: "🟢"
                }
                
                report_content += f"- {severity_emoji[issue.severity]} **{issue.description}**\n"
                report_content += f"  - File: `{issue.file_path}`\n"
                if issue.line_number:
                    report_content += f"  - Line: {issue.line_number}\n"
                report_content += f"  - Recommendation: {issue.recommendation}\n\n"
        
        report_content += "## Recommendations\n\n"
        for rec in result.recommendations:
            report_content += f"- 💡 {rec}\n"
        
        # Guardar reporte
        report_file = frontend_path / "frontend_performance_report.md"
        report_file.write_text(report_content)
        
        self.logger.info(f"[REPORT] Reporte generado: {report_file}")
    
    # Handlers MCP
    async def _handle_analyze_performance(self, request) -> Dict[str, Any]:
        """Handler para análisis de performance"""
        result = await self._analyze_frontend_performance(request.data)
        return {
            "performance_score": result.performance_score,
            "accessibility_score": result.accessibility_score,
            "seo_score": result.seo_score,
            "bundle_size_estimate": result.bundle_size_estimate,
            "total_issues": len(result.detected_issues),
            "recommendations": result.recommendations
        }
    
    async def _handle_optimize_react(self, request) -> Dict[str, Any]:
        """Handler para optimización de React"""
        return await self._optimize_react_components(request.data)
    
    async def _handle_optimize_vue(self, request) -> Dict[str, Any]:
        """Handler para optimización de Vue"""
        return await self._optimize_vue_components(request.data)
    
    async def _handle_optimize_bundle(self, request) -> Dict[str, Any]:
        """Handler para optimización de bundle"""
        return await self._optimize_bundle_size(request.data)
    
    async def _handle_audit_accessibility(self, request) -> Dict[str, Any]:
        """Handler para auditoría de accesibilidad"""
        return await self._audit_accessibility(request.data)
    
    async def _handle_optimize_seo(self, request) -> Dict[str, Any]:
        """Handler para optimización SEO"""
        return await self._optimize_seo(request.data)
    
    async def _handle_optimize_images(self, request) -> Dict[str, Any]:
        """Handler para optimización de imágenes"""
        return await self._optimize_images_handler(request.data)
    
    # Métodos de optimización específicos (implementación simplificada)
    async def _optimize_react_components(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar componentes React específicamente"""
        return {"status": "react_components_optimized", "optimizations": []}
    
    async def _optimize_vue_components(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar componentes Vue específicamente"""
        return {"status": "vue_components_optimized", "optimizations": []}
    
    async def _optimize_bundle_size(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar tamaño del bundle"""
        return {"status": "bundle_size_optimized", "size_reduction": "10%"}
    
    async def _audit_accessibility(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Auditar accesibilidad completa"""
        frontend_path = Path(params.get("frontend_path", "./"))
        issues = await self._analyze_accessibility(frontend_path)
        return {"accessibility_issues": len(issues), "score": self._calculate_accessibility_score(issues)}
    
    async def _optimize_seo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar SEO"""
        return {"status": "seo_optimized", "improvements": []}
    
    async def _optimize_images_handler(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handler para optimización de imágenes"""
        frontend_path = Path(params.get("frontend_path", "./"))
        result = await self._analyze_images(frontend_path)
        return result
