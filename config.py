"""
Configuración y constantes para Genesis Frontend

Este módulo contiene todas las configuraciones, constantes y defaults
específicos para la generación de frontend en el ecosistema Genesis.

Siguiendo la doctrina del ecosistema genesis-frontend:
- Se especializa solo en frontend
- Colabora con genesis-templates
- No coordina workflows generales
"""

import os
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from enum import Enum


class SupportedFramework(str, Enum):
    """Frameworks frontend soportados"""
    NEXTJS = "nextjs"
    REACT = "react"
    VUE = "vue"
    ANGULAR = "angular"
    SVELTE = "svelte"


class BuildTool(str, Enum):
    """Herramientas de build soportadas"""
    VITE = "vite"
    WEBPACK = "webpack"
    PARCEL = "parcel"
    ROLLUP = "rollup"
    TURBOPACK = "turbopack"


class PackageManager(str, Enum):
    """Gestores de paquetes soportados"""
    NPM = "npm"
    YARN = "yarn"
    PNPM = "pnpm"
    BUN = "bun"


class StateManagement(str, Enum):
    """Sistemas de gestión de estado"""
    REDUX_TOOLKIT = "redux_toolkit"
    ZUSTAND = "zustand"
    PINIA = "pinia"
    VUEX = "vuex"
    CONTEXT_API = "context_api"
    MOBX = "mobx"
    RECOIL = "recoil"


class UILibrary(str, Enum):
    """Librerías de UI soportadas"""
    TAILWINDCSS = "tailwindcss"
    STYLED_COMPONENTS = "styled_components"
    MATERIAL_UI = "material_ui"
    CHAKRA_UI = "chakra_ui"
    MANTINE = "mantine"
    VUETIFY = "vuetify"
    QUASAR = "quasar"
    SHADCN_UI = "shadcn_ui"
    CUSTOM = "custom"


@dataclass
class FrontendDefaults:
    """Configuraciones por defecto para frontend"""
    # Versiones por defecto
    node_version: str = "18"
    npm_version: str = "10"
    
    # Framework versions
    nextjs_version: str = "14.0.0"
    react_version: str = "18.2.0"
    vue_version: str = "3.4.0"
    
    # Build tools
    vite_version: str = "5.0.0"
    webpack_version: str = "5.0.0"
    
    # Styling
    tailwind_version: str = "3.3.0"
    postcss_version: str = "8.4.0"
    
    # TypeScript
    typescript_version: str = "5.0.0"
    
    # Testing
    vitest_version: str = "1.0.0"
    jest_version: str = "29.0.0"
    
    # Linting
    eslint_version: str = "8.0.0"
    prettier_version: str = "3.0.0"


@dataclass 
class ProjectStructure:
    """Estructura de directorios por framework"""
    # Directorios comunes
    common_dirs: List[str] = field(default_factory=lambda: [
        "src",
        "public", 
        "docs",
        "tests"
    ])
    
    # Directorios específicos por framework
    nextjs_dirs: List[str] = field(default_factory=lambda: [
        "app",
        "components",
        "lib",
        "hooks",
        "types",
        "styles",
        "public"
    ])
    
    react_dirs: List[str] = field(default_factory=lambda: [
        "src/components",
        "src/hooks", 
        "src/utils",
        "src/types",
        "src/services",
        "src/assets",
        "src/styles",
        "public"
    ])
    
    vue_dirs: List[str] = field(default_factory=lambda: [
        "src/components",
        "src/views",
        "src/router",
        "src/stores",
        "src/composables",
        "src/utils",
        "src/types",
        "src/assets",
        "public"
    ])


@dataclass
class TemplateMapping:
    """Mapeo de templates por framework y característica"""
    # Templates NextJS
    nextjs_templates: Dict[str, str] = field(default_factory=lambda: {
        "package_json": "frontend/nextjs/package.json.j2",
        "next_config": "frontend/nextjs/next.config.js.j2",
        "app_layout": "frontend/nextjs/app/layout.tsx.j2",
        "app_page": "frontend/nextjs/app/page.tsx.j2",
        "dockerfile": "frontend/nextjs/Dockerfile.j2",
        "tsconfig": "frontend/nextjs/tsconfig.json.j2",
    })
    
    # Templates React
    react_templates: Dict[str, str] = field(default_factory=lambda: {
        "package_json": "frontend/react/package.json.j2",
        "vite_config": "frontend/react/vite.config.ts.j2",
        "index_html": "frontend/react/index.html.j2",
        "app_tsx": "frontend/react/src/App.tsx.j2",
        "main_tsx": "frontend/react/src/main.tsx.j2",
        "dockerfile": "frontend/react/Dockerfile.j2",
    })
    
    # Templates Vue
    vue_templates: Dict[str, str] = field(default_factory=lambda: {
        "package_json": "frontend/vue/package.json.j2",
        "vite_config": "frontend/vue/vite.config.ts.j2",
        "app_vue": "frontend/vue/src/App.vue.j2",
        "main_ts": "frontend/vue/src/main.ts.j2",
        "dockerfile": "frontend/vue/Dockerfile.j2",
    })


class FrontendConfig:
    """Configuración central para Genesis Frontend"""
    
    def __init__(self):
        self.defaults = FrontendDefaults()
        self.structure = ProjectStructure()
        self.templates = TemplateMapping()
        
        # Configuración de entorno
        self.debug = os.getenv("GENESIS_FRONTEND_DEBUG", "false").lower() == "true"
        self.template_cache_enabled = os.getenv("GENESIS_TEMPLATE_CACHE", "true").lower() == "true"
        self.llm_enabled = os.getenv("GENESIS_LLM_ENABLED", "true").lower() == "true"
        
        # Rutas
        self.base_path = Path(__file__).parent
        self.templates_path = self.base_path / "templates"
        
        # Configuración de LLMs
        self.llm_config = {
            "default_provider": os.getenv("GENESIS_LLM_PROVIDER", "claude"),
            "model": os.getenv("GENESIS_LLM_MODEL", "claude-3-sonnet"),
            "max_tokens": int(os.getenv("GENESIS_LLM_MAX_TOKENS", "4000")),
            "temperature": float(os.getenv("GENESIS_LLM_TEMPERATURE", "0.3"))
        }
        
    def get_framework_defaults(self, framework: str) -> Dict[str, Any]:
        """Obtener defaults para un framework específico"""
        framework = framework.lower()
        
        base_defaults = {
            "typescript": True,
            "eslint": True,
            "prettier": True,
            "testing": True,
        }
        
        if framework in ["nextjs", "next"]:
            return {
                **base_defaults,
                "app_router": True,
                "src_directory": False,
                "tailwind_css": True,
                "state_management": "redux_toolkit",
                "ui_library": "tailwindcss",
                "server_components": True,
                "static_generation": True,
            }
        elif framework == "react":
            return {
                **base_defaults,
                "build_tool": "vite",
                "state_management": "redux_toolkit",
                "ui_library": "tailwindcss",
                "routing": True,
                "spa": True,
            }
        elif framework == "vue":
            return {
                **base_defaults,
                "vue_version": "3",
                "composition_api": True,
                "state_management": "pinia",
                "ui_library": "custom",
                "router": True,
                "sfc": True,  # Single File Components
            }
        else:
            return base_defaults
    
    def get_directory_structure(self, framework: str) -> List[str]:
        """Obtener estructura de directorios para un framework"""
        framework = framework.lower()
        
        base_dirs = self.structure.common_dirs.copy()
        
        if framework in ["nextjs", "next"]:
            base_dirs.extend(self.structure.nextjs_dirs)
        elif framework == "react":
            base_dirs.extend(self.structure.react_dirs)
        elif framework == "vue":
            base_dirs.extend(self.structure.vue_dirs)
        
        return base_dirs
    
    def get_templates_for_framework(self, framework: str) -> Dict[str, str]:
        """Obtener templates para un framework específico"""
        framework = framework.lower()
        
        if framework in ["nextjs", "next"]:
            return self.templates.nextjs_templates
        elif framework == "react":
            return self.templates.react_templates
        elif framework == "vue":
            return self.templates.vue_templates
        else:
            return {}
    
    def get_supported_frameworks(self) -> List[str]:
        """Obtener lista de frameworks soportados"""
        return [framework.value for framework in SupportedFramework]
    
    def get_supported_build_tools(self) -> List[str]:
        """Obtener herramientas de build soportadas"""
        return [tool.value for tool in BuildTool]
    
    def get_supported_ui_libraries(self) -> List[str]:
        """Obtener librerías de UI soportadas"""
        return [lib.value for lib in UILibrary]
    
    def validate_framework_compatibility(self, framework: str, config: Dict[str, Any]) -> List[str]:
        """Validar compatibilidad entre framework y configuración"""
        errors = []
        framework = framework.lower()
        
        # Validar build tool
        build_tool = config.get("build_tool")
        if build_tool:
            if framework == "nextjs" and build_tool not in ["webpack", "turbopack"]:
                errors.append(f"Build tool '{build_tool}' no compatible con Next.js")
            elif framework in ["react", "vue"] and build_tool not in ["vite", "webpack", "parcel"]:
                errors.append(f"Build tool '{build_tool}' no compatible con {framework}")
        
        # Validar state management
        state_mgmt = config.get("state_management")
        if state_mgmt:
            if framework == "vue" and state_mgmt not in ["pinia", "vuex", "composition_api"]:
                errors.append(f"State management '{state_mgmt}' no compatible con Vue")
            elif framework in ["nextjs", "react"] and state_mgmt not in ["redux_toolkit", "zustand", "context_api", "mobx"]:
                errors.append(f"State management '{state_mgmt}' no compatible con {framework}")
        
        return errors
    
    def get_llm_prompt_templates(self) -> Dict[str, str]:
        """Obtener templates de prompts para LLMs"""
        return {
            "component_generation": """
Generate a {framework} component with the following specifications:
- Component name: {component_name}
- Props: {props}
- Styling: {styling}
- TypeScript: {typescript}
- Features: {features}

Please follow best practices for {framework} development.
            """.strip(),
            
            "page_generation": """
Generate a {framework} page component with:
- Page name: {page_name}
- Layout: {layout}
- Data fetching: {data_fetching}
- SEO optimization: {seo}
- TypeScript: {typescript}

Include proper error handling and loading states.
            """.strip(),
            
            "config_generation": """
Generate a {config_type} configuration file for {framework}:
- Build tool: {build_tool}
- Features: {features}
- Environment: {environment}
- Optimization: {optimization}

Ensure the configuration follows current best practices.
            """.strip()
        }
    
    def get_optimization_rules(self) -> Dict[str, List[str]]:
        """Obtener reglas de optimización por framework"""
        return {
            "nextjs": [
                "Use App Router for new projects",
                "Implement Server Components where possible",
                "Enable Static Generation for static content",
                "Use Image component for optimization",
                "Implement proper SEO metadata"
            ],
            "react": [
                "Use React.memo for expensive components",
                "Implement code splitting with lazy loading",
                "Use useCallback and useMemo appropriately",
                "Optimize bundle size with tree shaking",
                "Implement proper error boundaries"
            ],
            "vue": [
                "Use Composition API for better reusability",
                "Implement proper reactive patterns",
                "Use defineAsyncComponent for code splitting",
                "Optimize with v-memo directive when needed",
                "Implement proper TypeScript integration"
            ]
        }


# Instancia global de configuración
config = FrontendConfig()

# Constantes exportables
SUPPORTED_FRAMEWORKS = config.get_supported_frameworks()
SUPPORTED_BUILD_TOOLS = config.get_supported_build_tools() 
SUPPORTED_UI_LIBRARIES = config.get_supported_ui_libraries()

# Mapas de compatibilidad
FRAMEWORK_BUILD_TOOL_COMPATIBILITY = {
    "nextjs": ["webpack", "turbopack"],
    "react": ["vite", "webpack", "parcel", "rollup"],
    "vue": ["vite", "webpack", "parcel", "rollup"],
    "angular": ["webpack", "esbuild"],
    "svelte": ["vite", "webpack", "rollup"],
}

FRAMEWORK_STATE_MANAGEMENT_COMPATIBILITY = {
    "nextjs": ["redux_toolkit", "zustand", "context_api", "mobx"],
    "react": ["redux_toolkit", "zustand", "context_api", "mobx", "recoil"],
    "vue": ["pinia", "vuex", "composition_api"],
    "angular": ["ngrx", "akita"],
    "svelte": ["svelte_store"],
}

# Configuraciones por defecto de desarrollo local
DEV_SERVER_DEFAULTS = {
    "nextjs": {"port": 3000, "host": "localhost"},
    "react": {"port": 3000, "host": "localhost"},
    "vue": {"port": 5173, "host": "localhost"},
    "angular": {"port": 4200, "host": "localhost"},
    "svelte": {"port": 5173, "host": "localhost"},
}

# Configuraciones de producción
PRODUCTION_DEFAULTS = {
    "minify": True,
    "sourcemaps": False,
    "tree_shaking": True,
    "code_splitting": True,
    "compression": True,
}

# Variables de entorno requeridas por framework
REQUIRED_ENV_VARS = {
    "nextjs": ["NEXT_PUBLIC_API_URL"],
    "react": ["REACT_APP_API_URL"],
    "vue": ["VITE_API_URL"],
}

# Extensiones de archivo por framework
FILE_EXTENSIONS = {
    "nextjs": [".tsx", ".ts", ".jsx", ".js"],
    "react": [".tsx", ".ts", ".jsx", ".js"],
    "vue": [".vue", ".ts", ".js"],
    "angular": [".component.ts", ".service.ts", ".module.ts"],
    "svelte": [".svelte", ".ts", ".js"],
}

# Patrones de código por framework para validación
CODE_PATTERNS = {
    "nextjs": {
        "app_router": r"export\s+default\s+function\s+\w+\(",
        "server_component": r"async\s+function\s+\w+\(",
        "client_component": r"['\"]use\s+client['\"]",
    },
    "react": {
        "functional_component": r"const\s+\w+:\s*React\.FC",
        "hook": r"use[A-Z]\w*\s*=",
        "context": r"createContext\s*\(",
    },
    "vue": {
        "composition_api": r"<script\s+setup",
        "reactive": r"ref\(|reactive\(",
        "computed": r"computed\(",
    }
}

# Configuraciones de calidad de código
CODE_QUALITY_RULES = {
    "typescript": {
        "strict": True,
        "no_any": False,  # Permitir any en casos específicos
        "no_unused_vars": True,
        "prefer_const": True,
    },
    "eslint": {
        "max_lines": 300,
        "max_complexity": 10,
        "prefer_arrow_functions": True,
    },
    "accessibility": {
        "alt_text_required": True,
        "color_contrast": "AA",
        "keyboard_navigation": True,
    }
}
