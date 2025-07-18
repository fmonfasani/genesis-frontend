# agents/design_system_auto.py
"""
Generación automática de design systems completos
Extiende UIAgent existente con capacidades avanzadas
"""

from dataclasses import dataclass
from typing import Dict, List, Any
import colorsys
import json

@dataclass
class ColorPaletteConfig:
    """Configuración para generación automática de paletas"""
    primary_hue: float
    saturation_range: tuple = (0.6, 0.9)
    lightness_range: tuple = (0.1, 0.95)
    variations: int = 10
    accessibility_compliant: bool = True

class AutoDesignSystemGenerator:
    """Generador automático de design systems"""
    
    def __init__(self, ui_agent):
        self.ui_agent = ui_agent
    
    async def generate_complete_system(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generar design system completo automáticamente"""
        
        # 1. Generar paleta de colores inteligente
        color_palette = await self._generate_intelligent_palette(config)
        
        # 2. Generar tipografía responsiva
        typography = await self._generate_responsive_typography(config)
        
        # 3. Generar espaciado modular
        spacing = self._generate_modular_spacing(config)
        
        # 4. Generar componentes themed
        components = await self._generate_themed_components(color_palette, typography)
        
        return {
            "colors": color_palette,
            "typography": typography,
            "spacing": spacing,
            "components": components,
            "tokens": self._generate_design_tokens(color_palette, typography, spacing)
        }
    
    async def _generate_intelligent_palette(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generar paleta usando teoría del color y AI"""
        
        primary_color = config.get("primary_color", "#3B82F6")
        palette_type = config.get("palette_type", "complementary")
        
        # Usar LLM para generar paleta inteligente
        prompt = f"""
        Genera una paleta de colores {palette_type} partiendo de {primary_color}.
        
        Requisitos:
        - Contraste WCAG AA compliant
        - 50-900 variations por color
        - Colores semánticos (success, warning, error)
        - Dark mode compatible
        - Armonía cromática basada en teoría del color
        
        Devuelve JSON con estructura:
        {{
          "primary": {{"50": "#...", "100": "#...", ..., "900": "#..."}},
          "secondary": {{...}},
          "accent": {{...}},
          "semantic": {{"success": {{...}}, "warning": {{...}}, "error": {{...}}}}
        }}
        """
        
        palette_json = await self.ui_agent.call_llm_for_generation(prompt, config)
        
        try:
            return json.loads(palette_json)
        except:
            return self._fallback_palette(primary_color)
    
    async def _generate_responsive_typography(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generar sistema tipográfico responsivo"""
        
        base_size = config.get("base_font_size", 16)
        scale_ratio = config.get("type_scale", 1.25)  # Perfect fourth
        
        prompt = f"""
        Genera un sistema tipográfico responsivo con:
        - Base size: {base_size}px
        - Scale ratio: {scale_ratio}
        - Breakpoints: mobile, tablet, desktop
        - Fluid typography con clamp()
        - Line heights optimizados
        - Letter spacing ajustado
        
        Devuelve CSS custom properties y clases utilitarias.
        """
        
        typography_css = await self.ui_agent.call_llm_for_generation(prompt, config)
        
        return {
            "css": typography_css,
            "scale": self._calculate_type_scale(base_size, scale_ratio),
            "fluid_sizes": self._generate_fluid_typography(base_size, scale_ratio)
        }
    
    def _generate_modular_spacing(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generar sistema de espaciado modular"""
        base_unit = config.get("spacing_unit", 8)
        
        # Escala basada en secuencia de Fibonacci modificada
        multipliers = [0, 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12, 16, 24]
        
        spacing_system = {}
        for i, mult in enumerate(multipliers):
            size = base_unit * mult
            spacing_system[str(i)] = f"{size}px" if size >= 1 else f"{size * 16}rem"
        
        return {
            "scale": spacing_system,
            "base_unit": base_unit,
            "css_variables": {f"--space-{k}": v for k, v in spacing_system.items()}
        }
    
    async def _generate_themed_components(self, colors: Dict, typography: Dict) -> List[str]:
        """Generar componentes con theming automático"""
        
        components = ["Button", "Input", "Card", "Badge", "Alert"]
        generated = []
        
        for component in components:
            prompt = f"""
            Genera componente {component} con theming completo:
            - Usa color tokens del design system
            - Multiple variants (primary, secondary, etc.)
            - Estados (hover, focus, disabled)
            - Dark mode support
            - Accesibilidad completa
            - TypeScript interfaces
            """
            
            component_code = await self.ui_agent.call_llm_for_generation(prompt, {
                "colors": colors,
                "typography": typography,
                "component": component
            })
            
            generated.append(component_code)
        
        return generated
    
    def _generate_design_tokens(self, colors: Dict, typography: Dict, spacing: Dict) -> str:
        """Generar design tokens en formato estándar"""
        
        tokens = {
            "color": colors,
            "typography": typography.get("scale", {}),
            "spacing": spacing.get("scale", {}),
            "border": {
                "radius": {"sm": "4px", "md": "8px", "lg": "12px", "xl": "16px", "full": "9999px"}
            },
            "shadow": {
                "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
                "md": "0 4px 6px -1px rgb(0 0 0 / 0.1)",
                "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1)",
                "xl": "0 20px 25px -5px rgb(0 0 0 / 0.1)"
            }
        }
        
        return json.dumps(tokens, indent=2)
    
    def _calculate_type_scale(self, base: int, ratio: float) -> Dict[str, str]:
        """Calcular escala tipográfica"""
        sizes = {}
        scale_names = ["xs", "sm", "base", "lg", "xl", "2xl", "3xl", "4xl", "5xl"]
        
        for i, name in enumerate(scale_names):
            size = base * (ratio ** (i - 2))  # base is at index 2
            sizes[name] = f"{size:.1f}px"
        
        return sizes
    
    def _generate_fluid_typography(self, base: int, ratio: float) -> Dict[str, str]:
        """Generar tipografía fluida con clamp()"""
        fluid_sizes = {}
        
        for name, static_size in self._calculate_type_scale(base, ratio).items():
            size_px = float(static_size.replace('px', ''))
            min_size = size_px * 0.8
            max_size = size_px * 1.2
            preferred = f"{size_px / 16}rem + 0.5vw"
            
            fluid_sizes[name] = f"clamp({min_size/16}rem, {preferred}, {max_size/16}rem)"
        
        return fluid_sizes
    
    def _fallback_palette(self, primary: str) -> Dict[str, Any]:
        """Paleta fallback si LLM falla"""
        return {
            "primary": {
                "50": "#eff6ff", "100": "#dbeafe", "500": primary,
                "600": "#2563eb", "900": "#1e3a8a"
            },
            "semantic": {
                "success": {"500": "#10b981"},
                "warning": {"500": "#f59e0b"},
                "error": {"500": "#ef4444"}
            }
        }

# Extender UIAgent existente
class EnhancedUIAgent:
    """UIAgent extendido con generación automática"""
    
    def __init__(self, base_agent):
        self.base_agent = base_agent
        self.auto_generator = AutoDesignSystemGenerator(base_agent)
    
    async def auto_generate_design_system(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Método público para generación automática"""
        return await self.auto_generator.generate_complete_system(config)