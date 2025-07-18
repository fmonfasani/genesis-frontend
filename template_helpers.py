"""
Template Helpers para Genesis Frontend

Este módulo proporciona utilidades para colaborar con genesis-templates
siguiendo la doctrina del ecosistema genesis-frontend.

Siguiendo la doctrina:
- ✅ Colabora con genesis-templates
- ✅ Se especializa solo en frontend
- ❌ No coordina workflows generales
"""

from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import re
import json

from .config import config, SUPPORTED_FRAMEWORKS
from .exceptions import TemplateNotFoundError, TemplateRenderError


class FrontendTemplateHelper:
    """
    Helper para colaboración con genesis-templates en contexto frontend
    
    Proporciona métodos específicos para trabajar con templates de frontend,
    validar variables y generar contextos apropiados.
    """
    
    def __init__(self):
        self.template_cache: Dict[str, str] = {}
        self.required_variables_cache: Dict[str, List[str]] = {}
    
    def get_template_path(self, framework: str, template_type: str) -> str:
        """
        Obtener ruta del template para framework específico
        
        Args:
            framework: Framework (nextjs, react, vue)
            template_type: Tipo de template (package.json, component, etc.)
            
        Returns:
            Ruta del template
            
        Raises:
            TemplateNotFoundError: Si el template no existe
        """
        framework = framework.lower()
        
        if framework not in SUPPORTED_FRAMEWORKS:
            raise TemplateNotFoundError(
                template_type, 
                framework, 
                [f"Framework no soportado: {framework}"]
            )
        
        # Mapear templates por framework
        template_paths = {
            "nextjs": {
                "package.json": "frontend/nextjs/package.json.j2",
                "next.config": "frontend/nextjs/next.config.js.j2",
                "tsconfig": "frontend/nextjs/tsconfig.json.j2",
                "layout": "frontend/nextjs/app/layout.tsx.j2",
                "page": "frontend/nextjs/app/page.tsx.j2",
                "component": "frontend/nextjs/components/component.tsx.j2",
                "dockerfile": "frontend/nextjs/Dockerfile.j2",
                "middleware": "frontend/nextjs/middleware.ts.j2"
            },
            "react": {
                "package.json": "frontend/react/package.json.j2",
                "vite.config": "frontend/react/vite.config.ts.j2",
                "index.html": "frontend/react/index.html.j2",
                "app": "frontend/react/src/App.tsx.j2",
                "main": "frontend/react/src/main.tsx.j2",
                "component": "frontend/react/src/components/component.tsx.j2",
                "dockerfile": "frontend/react/Dockerfile.j2"
            },
            "vue": {
                "package.json": "frontend/vue/package.json.j2",
                "vite.config": "frontend/vue/vite.config.ts.j2",
                "app": "frontend/vue/src/App.vue.j2",
                "main": "frontend/vue/src/main.ts.j2",
                "component": "frontend/vue/src/components/component.vue.j2",
                "dockerfile": "frontend/vue/Dockerfile.j2"
            },
            "ui": {
                "design_tokens": "frontend/ui/design_tokens.ts.j2",
                "component": "frontend/ui/component.tsx.j2",
                "theme_provider": "frontend/ui/ThemeProvider.tsx.j2",
                "colors": "frontend/ui/colors.ts.j2"
            }
        }
        
        framework_templates = template_paths.get(framework, {})
        template_path = framework_templates.get(template_type)
        
        if not template_path:
            available_templates = list(framework_templates.keys())
            raise TemplateNotFoundError(
                template_type,
                framework, 
                [f"Templates disponibles para {framework}: {available_templates}"]
            )
        
        return template_path
    
    def prepare_template_context(
        self, 
        framework: str, 
        template_type: str, 
        base_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Preparar contexto completo para renderizado de template
        
        Args:
            framework: Framework objetivo
            template_type: Tipo de template
            base_context: Contexto base proporcionado
            
        Returns:
            Contexto completo con todas las variables requeridas
        """
        # Contexto base con defaults
        context = {
            "framework": framework,
            "template_type": template_type,
            "generated_by": "Genesis Frontend",
            "version": "1.0.0",
            **base_context
        }
        
        # Agregar variables específicas por framework
        framework_defaults = self._get_framework_defaults(framework)
        context.update(framework_defaults)
        
        # Agregar variables específicas por tipo de template
        template_defaults = self._get_template_defaults(framework, template_type)
        context.update(template_defaults)
        
        # Validar variables requeridas
        missing_vars = self._validate_required_variables(framework, template_type, context)
        if missing_vars:
            raise TemplateRenderError(
                template_type,
                f"Variables faltantes: {', '.join(missing_vars)}",
                missing_vars
            )
        
        return context
    
    def _get_framework_defaults(self, framework: str) -> Dict[str, Any]:
        """Obtener defaults específicos del framework"""
        defaults_map = {
            "nextjs": {
                "node_version": "18",
                "next_version": "14.0.0",
                "typescript": True,
                "app_router": True,
                "src_directory": False,
                "tailwind_css": True,
                "port": 3000
            },
            "react": {
                "node_version": "18", 
                "react_version": "18.2.0",
                "vite_version": "5.0.0",
                "typescript": True,
                "build_tool": "vite",
                "port": 3000
            },
            "vue": {
                "node_version": "18",
                "vue_version": "3.4.0",
                "vite_version": "5.0.0",
                "typescript": True,
                "composition_api": True,
                "port": 5173
            },
            "ui": {
                "design_system": "custom",
                "color_palette": "blue",
                "dark_mode": True,
                "accessibility": True
            }
        }
        
        return defaults_map.get(framework, {})
    
    def _get_template_defaults(self, framework: str, template_type: str) -> Dict[str, Any]:
        """Obtener defaults específicos del tipo de template"""
        if template_type == "package.json":
            return {
                "private": True,
                "license": "MIT",
                "engines": {"node": ">=16.0.0"},
                "scripts": self._get_default_scripts(framework)
            }
        elif template_type == "dockerfile":
            return {
                "base_image": "node:18-alpine",
                "working_dir": "/app",
                "expose_port": 3000 if framework == "nextjs" else 80
            }
        elif template_type in ["component", "layout", "page"]:
            return {
                "typescript": True,
                "export_default": True,
                "props_interface": True
            }
        
        return {}
    
    def _get_default_scripts(self, framework: str) -> Dict[str, str]:
        """Obtener scripts por defecto por framework"""
        scripts_map = {
            "nextjs": {
                "dev": "next dev",
                "build": "next build", 
                "start": "next start",
                "lint": "next lint",
                "type-check": "tsc --noEmit"
            },
            "react": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
                "lint": "eslint src --ext .ts,.tsx",
                "type-check": "tsc --noEmit"
            },
            "vue": {
                "dev": "vite",
                "build": "vue-tsc && vite build",
                "preview": "vite preview",
                "lint": "eslint src --ext .vue,.ts",
                "type-check": "vue-tsc --noEmit"
            }
        }
        
        return scripts_map.get(framework, {})
    
    def _validate_required_variables(
        self, 
        framework: str, 
        template_type: str, 
        context: Dict[str, Any]
    ) -> List[str]:
        """Validar que todas las variables requeridas están presentes"""
        cache_key = f"{framework}:{template_type}"
        
        if cache_key not in self.required_variables_cache:
            required_vars = self._get_required_variables(framework, template_type)
            self.required_variables_cache[cache_key] = required_vars
        
        required_vars = self.required_variables_cache[cache_key]
        missing_vars = []
        
        for var in required_vars:
            if var not in context or context[var] is None:
                missing_vars.append(var)
        
        return missing_vars
    
    def _get_required_variables(self, framework: str, template_type: str) -> List[str]:
        """Obtener variables requeridas para un template específico"""
        # Variables base siempre requeridas
        base_required = ["project_name", "description", "framework"]
        
        # Variables específicas por tipo de template
        template_required = {
            "package.json": ["version", "scripts"],
            "dockerfile": ["node_version", "port"],
            "component": ["component_name"],
            "page": ["page_name"],
            "layout": ["layout_name"],
            "app": ["app_name"],
            "main": ["entry_point"]
        }
        
        # Variables específicas por framework
        framework_required = {
            "nextjs": ["next_version", "typescript", "app_router"],
            "react": ["react_version", "build_tool"],
            "vue": ["vue_version", "composition_api"],
            "ui": ["design_system", "color_palette"]
        }
        
        required = base_required.copy()
        required.extend(template_required.get(template_type, []))
        required.extend(framework_required.get(framework, []))
        
        return list(set(required))  # Remover duplicados
    
    def extract_dependencies_from_context(self, context: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
        """
        Extraer dependencias necesarias basado en el contexto
        
        Args:
            context: Contexto del template
            
        Returns:
            Diccionario con dependencies y devDependencies
        """
        framework = context.get("framework", "")
        typescript = context.get("typescript", False)
        ui_library = context.get("ui_library", "")
        state_management = context.get("state_management", "")
        build_tool = context.get("build_tool", "")
        
        dependencies = {}
        dev_dependencies = {}
        
        # Dependencias base por framework
        if framework == "nextjs":
            dependencies.update({
                "next": "^14.0.0",
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            })
        elif framework == "react":
            dependencies.update({
                "react": "^18.2.0",
                "react-dom": "^18.2.0"
            })
        elif framework == "vue":
            dependencies.update({
                "vue": "^3.4.0"
            })
        
        # TypeScript dependencies
        if typescript:
            dev_dependencies.update({
                "typescript": "^5.0.0",
                "@types/node": "^20.0.0"
            })
            
            if framework in ["nextjs", "react"]:
                dev_dependencies.update({
                    "@types/react": "^18.0.0",
                    "@types/react-dom": "^18.0.0"
                })
        
        # Build tool dependencies
        if build_tool == "vite":
            dev_dependencies["vite"] = "^5.0.0"
            if framework == "react":
                dev_dependencies["@vitejs/plugin-react"] = "^4.0.0"
            elif framework == "vue":
                dev_dependencies["@vitejs/plugin-vue"] = "^4.0.0"
        
        # UI Library dependencies
        if ui_library == "tailwindcss":
            dev_dependencies.update({
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            })
        elif ui_library == "styled_components":
            dependencies["styled-components"] = "^5.3.0"
        elif ui_library == "material_ui":
            dependencies["@mui/material"] = "^5.0.0"
        
        # State management dependencies
        if state_management == "redux_toolkit":
            dependencies.update({
                "@reduxjs/toolkit": "^1.9.0",
                "react-redux": "^8.0.0"
            })
        elif state_management == "zustand":
            dependencies["zustand"] = "^4.3.0"
        elif state_management == "pinia":
            dependencies["pinia"] = "^2.1.0"
        elif state_management == "vuex":
            dependencies["vuex"] = "^4.1.0"
        
        return {
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }
    
    def generate_component_props_interface(self, component_name: str, props: List[Dict[str, Any]]) -> str:
        """
        Generar interfaz de props para componente TypeScript
        
        Args:
            component_name: Nombre del componente
            props: Lista de props con tipo y descripción
            
        Returns:
            Código TypeScript de la interfaz
        """
        if not props:
            return f"interface {component_name}Props {{\n  // No props defined\n}}"
        
        interface_lines = [f"interface {component_name}Props {{"]
        
        for prop in props:
            name = prop.get("name", "")
            prop_type = prop.get("type", "any")
            optional = prop.get("optional", False)
            description = prop.get("description", "")
            
            if description:
                interface_lines.append(f"  /** {description} */")
            
            optional_marker = "?" if optional else ""
            interface_lines.append(f"  {name}{optional_marker}: {prop_type}")
        
        interface_lines.append("}")
        
        return "\n".join(interface_lines)
    
    def validate_component_name(self, name: str) -> bool:
        """
        Validar nombre de componente frontend
        
        Args:
            name: Nombre del componente
            
        Returns:
            True si es válido
        """
        # Debe empezar con mayúscula y ser PascalCase
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', name):
            return False
        
        # No debe ser palabra reservada
        reserved_words = [
            'React', 'Component', 'Element', 'Node', 'Props', 
            'State', 'Ref', 'Key', 'Children', 'Fragment'
        ]
        
        return name not in reserved_words
    
    def format_template_variables(self, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Formatear variables para uso en templates
        
        Args:
            variables: Variables originales
            
        Returns:
            Variables formateadas
        """
        formatted = variables.copy()
        
        # Formatear nombres de proyecto
        if "project_name" in formatted:
            project_name = formatted["project_name"]
            formatted.update({
                "project_name_kebab": self._to_kebab_case(project_name),
                "project_name_snake": self._to_snake_case(project_name),
                "project_name_pascal": self._to_pascal_case(project_name),
                "project_name_camel": self._to_camel_case(project_name)
            })
        
        # Formatear booleanos para JavaScript
        for key, value in formatted.items():
            if isinstance(value, bool):
                formatted[f"{key}_js"] = "true" if value else "false"
        
        # Formatear arrays para templates
        for key, value in formatted.items():
            if isinstance(value, list):
                formatted[f"{key}_json"] = json.dumps(value)
                formatted[f"{key}_comma_separated"] = ", ".join(str(v) for v in value)
        
        return formatted
    
    def _to_kebab_case(self, text: str) -> str:
        """Convertir a kebab-case"""
        return re.sub(r'[^a-zA-Z0-9]+', '-', text).lower().strip('-')
    
    def _to_snake_case(self, text: str) -> str:
        """Convertir a snake_case"""
        return re.sub(r'[^a-zA-Z0-9]+', '_', text).lower().strip('_')
    
    def _to_pascal_case(self, text: str) -> str:
        """Convertir a PascalCase"""
        words = re.findall(r'[a-zA-Z0-9]+', text)
        return ''.join(word.capitalize() for word in words)
    
    def _to_camel_case(self, text: str) -> str:
        """Convertir a camelCase"""
        pascal = self._to_pascal_case(text)
        return pascal[0].lower() + pascal[1:] if pascal else ""


# Instancia global del helper
template_helper = FrontendTemplateHelper()


def get_template_path(framework: str, template_type: str) -> str:
    """
    Función conveniente para obtener ruta de template
    
    Args:
        framework: Framework objetivo
        template_type: Tipo de template
        
    Returns:
        Ruta del template
    """
    return template_helper.get_template_path(framework, template_type)


def prepare_frontend_context(
    framework: str,
    template_type: str, 
    **kwargs
) -> Dict[str, Any]:
    """
    Función conveniente para preparar contexto de frontend
    
    Args:
        framework: Framework objetivo
        template_type: Tipo de template
        **kwargs: Variables del contexto
        
    Returns:
        Contexto preparado para renderizado
    """
    return template_helper.prepare_template_context(framework, template_type, kwargs)


def validate_frontend_template_context(
    framework: str,
    template_type: str,
    context: Dict[str, Any]
) -> List[str]:
    """
    Validar contexto para template frontend
    
    Args:
        framework: Framework objetivo
        template_type: Tipo de template
        context: Contexto a validar
        
    Returns:
        Lista de errores de validación
    """
    try:
        template_helper._validate_required_variables(framework, template_type, context)
        return []
    except TemplateRenderError as e:
        return e.missing_variables if hasattr(e, 'missing_variables') else [str(e)]


def generate_frontend_dependencies(context: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    """
    Generar dependencias para proyecto frontend
    
    Args:
        context: Contexto del proyecto
        
    Returns:
        Diccionario con dependencies y devDependencies
    """
    return template_helper.extract_dependencies_from_context(context)
