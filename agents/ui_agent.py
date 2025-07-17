"""
UI Agent - Especialista en diseño de interfaz de usuario
Parte del ecosistema genesis-frontend
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .base_agent import FrontendAgent, AgentTask, TaskResult


class DesignSystem(str, Enum):
    """Sistemas de diseño soportados"""
    MATERIAL_DESIGN = "material_design"
    APPLE_HUMAN_INTERFACE = "apple_hig"
    FLUENT_DESIGN = "fluent"
    CARBON_DESIGN = "carbon"
    CUSTOM = "custom"


class ColorPalette(str, Enum):
    """Paletas de colores predefinidas"""
    BLUE_THEME = "blue"
    GREEN_THEME = "green"
    PURPLE_THEME = "purple"
    ORANGE_THEME = "orange"
    MONOCHROME = "monochrome"
    CUSTOM = "custom"


class ComponentLibrary(str, Enum):
    """Librerías de componentes soportadas"""
    MATERIAL_UI = "material_ui"
    CHAKRA_UI = "chakra_ui"
    MANTINE = "mantine"
    HEADLESS_UI = "headless_ui"
    SHADCN_UI = "shadcn_ui"
    CUSTOM = "custom"


@dataclass
class UIDesignConfig:
    """Configuración de diseño UI"""
    design_system: DesignSystem = DesignSystem.CUSTOM
    color_palette: ColorPalette = ColorPalette.BLUE_THEME
    component_library: ComponentLibrary = ComponentLibrary.CUSTOM
    typography_scale: str = "modern"
    spacing_scale: str = "8px"
    border_radius: str = "8px"
    shadows: bool = True
    animations: bool = True
    dark_mode: bool = True
    responsive: bool = True
    accessibility: bool = True


class UIAgent(FrontendAgent):
    """
    Agente UI - Especialista en diseño de interfaz de usuario
    
    Responsabilidades:
    - Generar sistemas de diseño completos
    - Crear paletas de colores consistentes
    - Diseñar componentes UI reutilizables
    - Configurar tipografía y espaciado
    - Implementar dark mode y temas
    - Asegurar accesibilidad (a11y)
    - Crear design tokens y variables CSS
    - Generar guías de estilo
    """
    
    def __init__(self):
        super().__init__(
            agent_id="ui_agent",
            name="UIAgent",
            specialization="ui_design"
        )
        
        # Capacidades específicas de UI
        self.add_capability("design_system_creation")
        self.add_capability("color_palette_generation")
        self.add_capability("typography_system")
        self.add_capability("component_library_creation")
        self.add_capability("design_token_generation")
        self.add_capability("theme_system")
        self.add_capability("dark_mode_implementation")
        self.add_capability("accessibility_optimization")
        self.add_capability("responsive_design")
        self.add_capability("animation_system")
        self.add_capability("style_guide_generation")
        
        # Registrar handlers específicos
        self.register_handler("create_design_system", self._handle_create_design_system)
        self.register_handler("generate_color_palette", self._handle_generate_color_palette)
        self.register_handler("create_component_library", self._handle_create_component_library)
        self.register_handler("setup_typography", self._handle_setup_typography)
        self.register_handler("implement_dark_mode", self._handle_implement_dark_mode)
        self.register_handler("generate_design_tokens", self._handle_generate_design_tokens)
        self.register_handler("optimize_accessibility", self._handle_optimize_accessibility)
        self.register_handler("create_style_guide", self._handle_create_style_guide)
        
    async def initialize(self):
        """Inicializar agente UI"""
        self.logger.info("Inicializando UI Agent")
        
        # Configurar metadata específica de UI
        self.set_metadata("version", "1.0.0")
        self.set_metadata("design_systems_supported", [ds.value for ds in DesignSystem])
        self.set_metadata("color_palettes_available", [cp.value for cp in ColorPalette])
        self.set_metadata("component_libraries_supported", [cl.value for cl in ComponentLibrary])
        self.set_metadata("accessibility_compliant", True)
        self.set_metadata("responsive_design", True)
        self.set_metadata("dark_mode_support", True)
        
        self.logger.info("UI Agent inicializado correctamente")
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica de UI"""
        task_name = task.name.lower()
        
        try:
            if "create_design_system" in task_name:
                result = await self._create_complete_design_system(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_color_palette" in task_name:
                result = await self._generate_color_palette(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "create_component_library" in task_name:
                result = await self._create_component_library(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "setup_typography" in task_name:
                result = await self._setup_typography_system(task.params)
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
    
    async def _create_complete_design_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Crear sistema de diseño completo"""
        self.log_frontend_action("create_design_system", "ui", params)
        
        # Extraer configuración
        config = self._extract_ui_config(params)
        output_path = Path(params.get("output_path", "./"))
        schema = params.get("schema", {})
        
        # Crear estructura de directorios para UI
        self._create_ui_directory_structure(output_path, config)
        
        generated_files = []
        
        # 1. Generar design tokens
        design_tokens = await self._generate_design_tokens(config, output_path)
        generated_files.extend(design_tokens)
        
        # 2. Generar paleta de colores
        color_palette = await self._generate_color_palette({"config": config, "output_path": output_path})
        generated_files.extend(color_palette.get("files", []))
        
        # 3. Configurar sistema de tipografía
        typography_files = await self._setup_typography_system({"config": config, "output_path": output_path})
        generated_files.extend(typography_files.get("files", []))
        
        # 4. Crear biblioteca de componentes
        component_library = await self._create_component_library({"config": config, "output_path": output_path})
        generated_files.extend(component_library.get("files", []))
        
        # 5. Implementar dark mode
        if config.dark_mode:
            dark_mode_files = await self._implement_dark_mode({"config": config, "output_path": output_path})
            generated_files.extend(dark_mode_files.get("files", []))
        
        # 6. Crear sistema de animaciones
        if config.animations:
            animation_files = await self._create_animation_system(config, output_path)
            generated_files.extend(animation_files)
        
        # 7. Optimizar accesibilidad
        if config.accessibility:
            accessibility_files = await self._optimize_accessibility({"config": config, "output_path": output_path})
            generated_files.extend(accessibility_files.get("files", []))
        
        # 8. Generar guía de estilo
        style_guide = await self._create_style_guide({"config": config, "output_path": output_path, "schema": schema})
        generated_files.extend(style_guide.get("files", []))
        
        return {
            "design_system": config.design_system.value,
            "color_palette": config.color_palette.value,
            "component_library": config.component_library.value,
            "dark_mode": config.dark_mode,
            "accessibility": config.accessibility,
            "generated_files": generated_files,
            "output_path": str(output_path),
            "design_tokens_path": "src/styles/tokens",
            "components_path": "src/components/ui",
            "style_guide_path": "src/styles/guide"
        }
    
    def _extract_ui_config(self, params: Dict[str, Any]) -> UIDesignConfig:
        """Extraer configuración UI de los parámetros"""
        return UIDesignConfig(
            design_system=DesignSystem(params.get("design_system", "custom")),
            color_palette=ColorPalette(params.get("color_palette", "blue")),
            component_library=ComponentLibrary(params.get("component_library", "custom")),
            typography_scale=params.get("typography_scale", "modern"),
            spacing_scale=params.get("spacing_scale", "8px"),
            border_radius=params.get("border_radius", "8px"),
            shadows=params.get("shadows", True),
            animations=params.get("animations", True),
            dark_mode=params.get("dark_mode", True),
            responsive=params.get("responsive", True),
            accessibility=params.get("accessibility", True)
        )
    
    def _create_ui_directory_structure(self, base_path: Path, config: UIDesignConfig):
        """Crear estructura de directorios para UI"""
        directories = [
            "src/styles",
            "src/styles/tokens",
            "src/styles/themes",
            "src/styles/components",
            "src/styles/utilities",
            "src/components/ui",
            "src/components/ui/forms",
            "src/components/ui/feedback",
            "src/components/ui/navigation",
            "src/components/ui/layout",
            "src/components/ui/typography",
            "src/hooks/ui",
            "src/utils/ui",
            "docs/design-system",
        ]
        
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    async def _generate_design_tokens(self, config: UIDesignConfig, output_path: Path) -> List[str]:
        """Generar design tokens"""
        files = []
        
        # Usar LLM para generar tokens inteligentes
        prompt = f"""
        Genera design tokens para un sistema de diseño con:
        - Paleta de colores: {config.color_palette.value}
        - Escala tipográfica: {config.typography_scale}
        - Espaciado: {config.spacing_scale}
        - Border radius: {config.border_radius}
        - Sombras: {config.shadows}
        - Dark mode: {config.dark_mode}
        
        Incluye tokens para colores, tipografía, espaciado, y efectos.
        """
        
        tokens_content = await self.call_llm_for_generation(prompt, {"config": config})
        
        # Fallback si LLM no está disponible
        if "placeholder" in tokens_content:
            tokens_content = self._generate_fallback_design_tokens(config)
        
        tokens_file = output_path / "src" / "styles" / "tokens" / "index.ts"
        tokens_file.write_text(tokens_content)
        files.append(str(tokens_file))
        
        return files
    
    def _generate_fallback_design_tokens(self, config: UIDesignConfig) -> str:
        """Generar design tokens fallback"""
        colors = self._get_color_palette_values(config.color_palette)
        
        return f"""// Design Tokens
export const designTokens = {{
  colors: {{
    primary: {{
      50: '{colors["primary"]["50"]}',
      100: '{colors["primary"]["100"]}',
      200: '{colors["primary"]["200"]}',
      300: '{colors["primary"]["300"]}',
      400: '{colors["primary"]["400"]}',
      500: '{colors["primary"]["500"]}',
      600: '{colors["primary"]["600"]}',
      700: '{colors["primary"]["700"]}',
      800: '{colors["primary"]["800"]}',
      900: '{colors["primary"]["900"]}',
    }},
    gray: {{
      50: '#f9fafb',
      100: '#f3f4f6',
      200: '#e5e7eb',
      300: '#d1d5db',
      400: '#9ca3af',
      500: '#6b7280',
      600: '#4b5563',
      700: '#374151',
      800: '#1f2937',
      900: '#111827',
    }},
    success: {{
      50: '#ecfdf5',
      500: '#10b981',
      600: '#059669',
    }},
    warning: {{
      50: '#fffbeb',
      500: '#f59e0b',
      600: '#d97706',
    }},
    error: {{
      50: '#fef2f2',
      500: '#ef4444',
      600: '#dc2626',
    }},
  }},
  spacing: {{
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    '2xl': '48px',
    '3xl': '64px',
  }},
  typography: {{
    fontFamily: {{
      sans: ['Inter', 'sans-serif'],
      mono: ['Monaco', 'monospace'],
    }},
    fontSize: {{
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '30px',
      '4xl': '36px',
    }},
    fontWeight: {{
      light: '300',
      normal: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    }},
    lineHeight: {{
      tight: '1.2',
      normal: '1.5',
      relaxed: '1.75',
    }},
  }},
  borderRadius: {{
    none: '0px',
    sm: '4px',
    md: '{config.border_radius}',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  }},
  shadows: {{
    sm: '0 1px 2px 0 rgb(0 0 0 / 0.05)',
    md: '0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)',
    lg: '0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)',
    xl: '0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)',
  }},
  animations: {{
    duration: {{
      fast: '150ms',
      normal: '300ms',
      slow: '500ms',
    }},
    easing: {{
      easeInOut: 'cubic-bezier(0.4, 0, 0.2, 1)',
      easeOut: 'cubic-bezier(0, 0, 0.2, 1)',
      easeIn: 'cubic-bezier(0.4, 0, 1, 1)',
    }},
  }},
}}

export default designTokens
"""
    
    def _get_color_palette_values(self, palette: ColorPalette) -> Dict[str, Dict[str, str]]:
        """Obtener valores de paleta de colores"""
        palettes = {
            ColorPalette.BLUE_THEME: {
                "primary": {
                    "50": "#eff6ff",
                    "100": "#dbeafe",
                    "200": "#bfdbfe",
                    "300": "#93c5fd",
                    "400": "#60a5fa",
                    "500": "#3b82f6",
                    "600": "#2563eb",
                    "700": "#1d4ed8",
                    "800": "#1e40af",
                    "900": "#1e3a8a",
                }
            },
            ColorPalette.GREEN_THEME: {
                "primary": {
                    "50": "#ecfdf5",
                    "100": "#d1fae5",
                    "200": "#a7f3d0",
                    "300": "#6ee7b7",
                    "400": "#34d399",
                    "500": "#10b981",
                    "600": "#059669",
                    "700": "#047857",
                    "800": "#065f46",
                    "900": "#064e3b",
                }
            },
            ColorPalette.PURPLE_THEME: {
                "primary": {
                    "50": "#faf5ff",
                    "100": "#f3e8ff",
                    "200": "#e9d5ff",
                    "300": "#d8b4fe",
                    "400": "#c084fc",
                    "500": "#a855f7",
                    "600": "#9333ea",
                    "700": "#7c3aed",
                    "800": "#6b21a8",
                    "900": "#581c87",
                }
            },
        }
        
        return palettes.get(palette, palettes[ColorPalette.BLUE_THEME])
    
    async def _generate_color_palette(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar paleta de colores"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Usar LLM para generar paleta inteligente
        prompt = f"""
        Genera una paleta de colores para tema {config.color_palette.value} con:
        - Colores primarios, secundarios y neutros
        - Variaciones de 50 a 900
        - Colores de estado (success, warning, error)
        - Soporte para dark mode: {config.dark_mode}
        - Accesibilidad garantizada
        """
        
        palette_content = await self.call_llm_for_generation(prompt, {"config": config})
        
        # Fallback si LLM no está disponible
        if "placeholder" in palette_content:
            palette_content = self._generate_fallback_color_palette(config)
        
        palette_file = output_path / "src" / "styles" / "tokens" / "colors.ts"
        palette_file.write_text(palette_content)
        files.append(str(palette_file))
        
        return {"files": files}
    
    def _generate_fallback_color_palette(self, config: UIDesignConfig) -> str:
        """Generar paleta de colores fallback"""
        colors = self._get_color_palette_values(config.color_palette)
        
        return f"""// Color Palette
export const colors = {{
  primary: {json.dumps(colors["primary"], indent=4)},
  gray: {{
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
  }},
  success: {{
    50: '#ecfdf5',
    100: '#d1fae5',
    500: '#10b981',
    600: '#059669',
    700: '#047857',
  }},
  warning: {{
    50: '#fffbeb',
    100: '#fef3c7',
    500: '#f59e0b',
    600: '#d97706',
    700: '#b45309',
  }},
  error: {{
    50: '#fef2f2',
    100: '#fee2e2',
    500: '#ef4444',
    600: '#dc2626',
    700: '#b91c1c',
  }},
}}

export default colors
"""
    
    async def _setup_typography_system(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar sistema de tipografía"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Usar LLM para generar sistema tipográfico inteligente
        prompt = f"""
        Genera un sistema tipográfico para escala {config.typography_scale} con:
        - Jerarquía clara de tamaños
        - Familias tipográficas apropiadas
        - Espaciado y altura de línea optimizados
        - Responsive typography
        - Accesibilidad garantizada
        """
        
        typography_content = await self.call_llm_for_generation(prompt, {"config": config})
        
        # Fallback si LLM no está disponible
        if "placeholder" in typography_content:
            typography_content = self._generate_fallback_typography(config)
        
        typography_file = output_path / "src" / "styles" / "tokens" / "typography.ts"
        typography_file.write_text(typography_content)
        files.append(str(typography_file))
        
        return {"files": files}
    
    def _generate_fallback_typography(self, config: UIDesignConfig) -> str:
        """Generar sistema tipográfico fallback"""
        return """// Typography System
export const typography = {
  fontFamily: {
    sans: ['Inter', 'system-ui', 'sans-serif'],
    mono: ['Monaco', 'Consolas', 'monospace'],
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem', // 30px
    '4xl': '2.25rem',  // 36px
    '5xl': '3rem',     // 48px
    '6xl': '3.75rem',  // 60px
  },
  fontWeight: {
    light: '300',
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700',
    extrabold: '800',
  },
  lineHeight: {
    tight: '1.2',
    normal: '1.5',
    relaxed: '1.75',
  },
  letterSpacing: {
    tight: '-0.025em',
    normal: '0',
    wide: '0.025em',
  },
}

export default typography
"""
    
    async def _create_component_library(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Crear biblioteca de componentes"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Generar componentes base
        base_components = [
            "Button",
            "Input",
            "Select",
            "Checkbox",
            "Radio",
            "Switch",
            "Card",
            "Modal",
            "Alert",
            "Badge",
            "Avatar",
            "Spinner",
            "Progress",
            "Tooltip",
            "Dropdown",
        ]
        
        for component_name in base_components:
            component_file = await self._generate_ui_component(component_name, config, output_path)
            files.append(component_file)
        
        # Generar archivo de índice
        index_file = await self._generate_component_index(base_components, output_path)
        files.append(index_file)
        
        return {"files": files}
    
    async def _generate_ui_component(self, component_name: str, config: UIDesignConfig, output_path: Path) -> str:
        """Generar componente UI específico"""
        # Usar LLM para generar componente inteligente
        prompt = f"""
        Genera un componente React {component_name} con:
        - TypeScript
        - Accesibilidad (ARIA)
        - Variantes y tamaños
        - Dark mode support: {config.dark_mode}
        - Animaciones: {config.animations}
        - Design tokens integrados
        - Props bien tipadas
        - Documentación JSDoc
        """
        
        component_content = await self.call_llm_for_generation(prompt, {
            "component_name": component_name,
            "config": config
        })
        
        # Fallback si LLM no está disponible
        if "placeholder" in component_content:
            component_content = self._generate_fallback_component(component_name, config)
        
        component_file = output_path / "src" / "components" / "ui" / f"{component_name}.tsx"
        component_file.write_text(component_content)
        
        return str(component_file)
    
    def _generate_fallback_component(self, component_name: str, config: UIDesignConfig) -> str:
        """Generar componente fallback"""
        if component_name == "Button":
            return """import React from 'react'
import { designTokens } from '../../styles/tokens'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  className?: string
}

const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  type = 'button',
  className = '',
}) => {
  const baseStyles = `
    inline-flex items-center justify-center font-medium rounded-md
    transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2
    disabled:opacity-50 disabled:cursor-not-allowed
  `
  
  const variants = {
    primary: `bg-primary-600 text-white hover:bg-primary-700 focus:ring-primary-500`,
    secondary: `bg-gray-600 text-white hover:bg-gray-700 focus:ring-gray-500`,
    outline: `border border-gray-300 text-gray-700 hover:bg-gray-50 focus:ring-gray-500`,
    ghost: `text-gray-700 hover:bg-gray-100 focus:ring-gray-500`,
  }
  
  const sizes = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }
  
  const classes = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`
  
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={classes}
      aria-disabled={disabled}
    >
      {children}
    </button>
  )
}

export default Button
"""
        
        return f"""import React from 'react'

interface {component_name}Props {{
  children?: React.ReactNode
  className?: string
}}

const {component_name}: React.FC<{component_name}Props> = ({{
  children,
  className = '',
}}) => {{
  return (
    <div className={{`{component_name.lower()} ${{className}}`}}>
      {{children}}
    </div>
  )
}}

export default {component_name}
"""
    
    async def _generate_component_index(self, components: List[str], output_path: Path) -> str:
        """Generar archivo de índice para componentes"""
        exports = []
        for component in components:
            exports.append(f"export {{ default as {component} }} from './{component}'")
        
        index_content = "\n".join(exports)
        
        index_file = output_path / "src" / "components" / "ui" / "index.ts"
        index_file.write_text(index_content)
        
        return str(index_file)
    
    async def _implement_dark_mode(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Implementar dark mode"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Theme provider
        theme_provider = """import React, { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark'

interface ThemeContextType {
  theme: Theme
  toggleTheme: () => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider')
  }
  return context
}

interface ThemeProviderProps {
  children: React.ReactNode
}

export const ThemeProvider: React.FC<ThemeProviderProps> = ({ children }) => {
  const [theme, setTheme] = useState<Theme>('light')
  
  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') as Theme
    if (savedTheme) {
      setTheme(savedTheme)
    } else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setTheme('dark')
    }
  }, [])
  
  useEffect(() => {
    localStorage.setItem('theme', theme)
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [theme])
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }
  
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}
"""
        
        theme_file = output_path / "src" / "components" / "ui" / "ThemeProvider.tsx"
        theme_file.write_text(theme_provider)
        files.append(str(theme_file))
        
        return {"files": files}
    
    async def _create_animation_system(self, config: UIDesignConfig, output_path: Path) -> List[str]:
        """Crear sistema de animaciones"""
        files = []
        
        # Animations CSS
        animations_css = """/* Animation System */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideInUp {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes slideInDown {
  from {
    transform: translateY(-100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

@keyframes scaleIn {
  from {
    transform: scale(0.9);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

/* Animation Classes */
.animate-fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

.animate-slide-in-up {
  animation: slideInUp 0.3s ease-out;
}

.animate-slide-in-down {
  animation: slideInDown 0.3s ease-out;
}

.animate-scale-in {
  animation: scaleIn 0.2s ease-out;
}

.animate-spin {
  animation: spin 1s linear infinite;
}

/* Transition Classes */
.transition-fast {
  transition: all 0.15s ease;
}

.transition-normal {
  transition: all 0.3s ease;
}

.transition-slow {
  transition: all 0.5s ease;
}
"""
        
        animations_file = output_path / "src" / "styles" / "animations.css"
        animations_file.write_text(animations_css)
        files.append(str(animations_file))
        
        return files
    
    async def _optimize_accessibility(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Optimizar accesibilidad"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Accessibility utilities
        a11y_utils = """// Accessibility Utilities
export const screenReaderOnly = {
  position: 'absolute',
  width: '1px',
  height: '1px',
  padding: '0',
  margin: '-1px',
  overflow: 'hidden',
  clip: 'rect(0, 0, 0, 0)',
  whiteSpace: 'nowrap',
  border: '0',
} as const

export const focusRing = {
  outline: '2px solid transparent',
  outlineOffset: '2px',
  boxShadow: '0 0 0 2px rgba(59, 130, 246, 0.5)',
} as const

export const announceToScreenReader = (message: string) => {
  const announcement = document.createElement('div')
  announcement.setAttribute('aria-live', 'polite')
  announcement.setAttribute('aria-atomic', 'true')
  announcement.setAttribute('style', Object.entries(screenReaderOnly).map(([key, value]) => `${key}: ${value}`).join('; '))
  announcement.textContent = message
  
  document.body.appendChild(announcement)
  
  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

export const trapFocus = (element: HTMLElement) => {
  const focusableElements = element.querySelectorAll(
    'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
  )
  
  const firstFocusableElement = focusableElements[0] as HTMLElement
  const lastFocusableElement = focusableElements[focusableElements.length - 1] as HTMLElement
  
  const handleTabKey = (e: KeyboardEvent) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstFocusableElement) {
          lastFocusableElement.focus()
          e.preventDefault()
        }
      } else {
        if (document.activeElement === lastFocusableElement) {
          firstFocusableElement.focus()
          e.preventDefault()
        }
      }
    }
  }
  
  element.addEventListener('keydown', handleTabKey)
  
  return () => {
    element.removeEventListener('keydown', handleTabKey)
  }
}
"""
        
        a11y_file = output_path / "src" / "utils" / "ui" / "accessibility.ts"
        a11y_file.write_text(a11y_utils)
        files.append(str(a11y_file))
        
        return {"files": files}
    
    async def _create_style_guide(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Crear guía de estilo"""
        config = params.get("config")
        output_path = params.get("output_path")
        schema = params.get("schema", {})
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        project_name = schema.get("project_name", "Design System")
        
        # Style guide documentation
        style_guide_md = f"""# {project_name} Design System

## Overview

This design system provides a comprehensive set of guidelines, components, and patterns for creating consistent user interfaces.

## Design Principles

1. **Consistency**: Use standardized patterns and components
2. **Accessibility**: Ensure all components meet WCAG 2.1 AA standards
3. **Performance**: Optimize for fast loading and smooth interactions
4. **Scalability**: Design for growth and maintainability

## Color Palette

### Primary Colors
- Primary 500: `{self._get_color_palette_values(config.color_palette)["primary"]["500"]}`
- Primary 600: `{self._get_color_palette_values(config.color_palette)["primary"]["600"]}`

### Semantic Colors
- Success: `#10b981`
- Warning: `#f59e0b`
- Error: `#ef4444`

## Typography

### Font Families
- **Sans-serif**: Inter, system-ui, sans-serif
- **Monospace**: Monaco, Consolas, monospace

### Font Sizes
- **Small**: 14px
- **Base**: 16px
- **Large**: 18px
- **X-Large**: 24px

## Spacing

Our spacing system is based on an 8px grid:
- **XS**: 4px
- **SM**: 8px
- **MD**: 16px
- **LG**: 24px
- **XL**: 32px

## Components

### Button
- Use primary buttons for main actions
- Use secondary buttons for supporting actions
- Use outline buttons for less prominent actions

### Cards
- Use cards to group related content
- Maintain consistent padding and spacing
- Use shadows appropriately

## Dark Mode

{f"This design system supports dark mode with automatic theme switching." if config.dark_mode else "Dark mode is not enabled in this configuration."}

## Accessibility

- All components meet WCAG 2.1 AA standards
- Proper color contrast ratios
- Keyboard navigation support
- Screen reader compatibility

## Usage Guidelines

1. Always use design tokens for colors, spacing, and typography
2. Follow the component API for consistent behavior
3. Test components in both light and dark modes
4. Ensure proper accessibility attributes
"""
        
        style_guide_file = output_path / "docs" / "design-system" / "README.md"
        style_guide_file.write_text(style_guide_md)
        files.append(str(style_guide_file))
        
        return {"files": files}
    
    # Handlers MCP
    async def _handle_create_design_system(self, request) -> Dict[str, Any]:
        """Handler para crear sistema de diseño"""
        return await self._create_complete_design_system(request.data)
    
    async def _handle_generate_color_palette(self, request) -> Dict[str, Any]:
        """Handler para generar paleta de colores"""
        return await self._generate_color_palette(request.data)
    
    async def _handle_create_component_library(self, request) -> Dict[str, Any]:
        """Handler para crear biblioteca de componentes"""
        return await self._create_component_library(request.data)
    
    async def _handle_setup_typography(self, request) -> Dict[str, Any]:
        """Handler para configurar tipografía"""
        return await self._setup_typography_system(request.data)
    
    async def _handle_implement_dark_mode(self, request) -> Dict[str, Any]:
        """Handler para implementar dark mode"""
        return await self._implement_dark_mode(request.data)
    
    async def _handle_generate_design_tokens(self, request) -> Dict[str, Any]:
        """Handler para generar design tokens"""
        config = self._extract_ui_config(request.data)
        output_path = Path(request.data.get("output_path", "./"))
        
        files = await self._generate_design_tokens(config, output_path)
        
        return {"files": files}
    
    async def _handle_optimize_accessibility(self, request) -> Dict[str, Any]:
        """Handler para optimizar accesibilidad"""
        return await self._optimize_accessibility(request.data)
    
    async def _handle_create_style_guide(self, request) -> Dict[str, Any]:
        """Handler para crear guía de estilo"""
        return await self._create_style_guide(request.data)
