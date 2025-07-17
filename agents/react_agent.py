"""
React Agent - Especialista en aplicaciones React (SPA)
Parte del ecosistema genesis-frontend
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from .base_agent import FrontendAgent, AgentTask, TaskResult


class ReactBuildTool(str, Enum):
    """Herramientas de build soportadas"""
    VITE = "vite"
    WEBPACK = "webpack"
    PARCEL = "parcel"
    ROLLUP = "rollup"


class ReactStateManagement(str, Enum):
    """Sistemas de gestión de estado"""
    REDUX_TOOLKIT = "redux_toolkit"
    ZUSTAND = "zustand"
    CONTEXT_API = "context_api"
    MOBX = "mobx"
    RECOIL = "recoil"


@dataclass
class ReactConfig:
    """Configuración para aplicaciones React"""
    typescript: bool = True
    build_tool: ReactBuildTool = ReactBuildTool.VITE
    state_management: ReactStateManagement = ReactStateManagement.REDUX_TOOLKIT
    routing: bool = True
    testing: bool = True
    pwa: bool = False
    styled_components: bool = False
    tailwind_css: bool = True
    eslint: bool = True
    prettier: bool = True


class ReactAgent(FrontendAgent):
    """
    Agente React - Especialista en aplicaciones React SPA
    
    Responsabilidades:
    - Generar aplicaciones React con Vite/Webpack
    - Configurar React Router para SPA
    - Integrar sistemas de estado (Redux, Zustand, Context)
    - Configurar testing con Jest/Vitest
    - Generar componentes reutilizables
    - Configurar PWA y service workers
    """
    
    def __init__(self):
        super().__init__(
            agent_id="react_agent",
            name="ReactAgent",
            specialization="react"
        )
        
        # Capacidades específicas de React
        self.add_capability("react_app_generation")
        self.add_capability("vite_configuration")
        self.add_capability("webpack_configuration")
        self.add_capability("react_router_setup")
        self.add_capability("redux_toolkit_setup")
        self.add_capability("zustand_setup")
        self.add_capability("context_api_setup")
        self.add_capability("component_generation")
        self.add_capability("hook_generation")
        self.add_capability("testing_setup")
        self.add_capability("pwa_configuration")
        self.add_capability("styled_components_setup")
        
        # Registrar handlers específicos
        self.register_handler("generate_react_app", self._handle_generate_app)
        self.register_handler("generate_component", self._handle_generate_component)
        self.register_handler("generate_hook", self._handle_generate_hook)
        self.register_handler("setup_routing", self._handle_setup_routing)
        self.register_handler("setup_state_management", self._handle_setup_state_management)
        self.register_handler("setup_testing", self._handle_setup_testing)
        self.register_handler("configure_pwa", self._handle_configure_pwa)
        self.register_handler("setup_build_tool", self._handle_setup_build_tool)
        
    async def initialize(self):
        """Inicializar agente React"""
        self.logger.info("Inicializando React Agent")
        
        # Configurar metadata específica de React
        self.set_metadata("version", "1.0.0")
        self.set_metadata("react_version", "18.2.0")
        self.set_metadata("vite_version", "5.0.0")
        self.set_metadata("typescript_support", True)
        self.set_metadata("router_support", True)
        self.set_metadata("state_management_support", True)
        self.set_metadata("testing_support", True)
        self.set_metadata("pwa_support", True)
        
        self.logger.info("React Agent inicializado correctamente")
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica de React"""
        task_name = task.name.lower()
        
        try:
            if "generate_react_app" in task_name:
                result = await self._generate_react_application(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_component" in task_name:
                result = await self._generate_react_component(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_hook" in task_name:
                result = await self._generate_react_hook(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "setup_routing" in task_name:
                result = await self._setup_react_routing(task.params)
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
    
    async def _generate_react_application(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar aplicación React completa"""
        self.log_frontend_action("generate_app", "react", params)
        
        # Validar parámetros
        validation_errors = self.validate_frontend_request(params)
        if validation_errors:
            raise ValueError(f"Errores de validación: {', '.join(validation_errors)}")
        
        # Extraer configuración
        config = self._extract_react_config(params)
        output_path = Path(params.get("output_path", "./"))
        schema = params.get("schema", {})
        
        # Crear estructura de directorios
        self._create_react_directory_structure(output_path, config)
        
        generated_files = []
        
        # 1. Generar package.json
        package_json = await self._generate_package_json(output_path, config, schema)
        generated_files.append(package_json)
        
        # 2. Generar configuración del build tool
        build_config = await self._generate_build_config(output_path, config)
        generated_files.append(build_config)
        
        # 3. Generar configuración TypeScript
        if config.typescript:
            tsconfig = await self._generate_tsconfig(output_path, config)
            generated_files.append(tsconfig)
        
        # 4. Generar configuración Tailwind
        if config.tailwind_css:
            tailwind_files = await self._generate_tailwind_config(output_path, config)
            generated_files.extend(tailwind_files)
        
        # 5. Generar index.html
        index_html = await self._generate_index_html(output_path, config, schema)
        generated_files.append(index_html)
        
        # 6. Generar App principal
        app_files = await self._generate_main_app(output_path, config, schema)
        generated_files.extend(app_files)
        
        # 7. Generar componentes base
        base_components = await self._generate_base_components(output_path, config, schema)
        generated_files.extend(base_components)
        
        # 8. Configurar routing
        if config.routing:
            routing_files = await self._setup_react_routing({"config": config, "output_path": output_path})
            generated_files.extend(routing_files.get("files", []))
        
        # 9. Configurar gestión de estado
        if config.state_management != ReactStateManagement.CONTEXT_API:
            state_files = await self._setup_state_management({"config": config, "output_path": output_path})
            generated_files.extend(state_files.get("files", []))
        
        # 10. Configurar testing
        if config.testing:
            test_files = await self._setup_testing({"config": config, "output_path": output_path})
            generated_files.extend(test_files.get("files", []))
        
        # 11. Generar estilos globales
        styles_file = await self._generate_global_styles(output_path, config)
        generated_files.append(styles_file)
        
        # 12. Generar configuración ESLint/Prettier
        if config.eslint:
            eslint_config = await self._generate_eslint_config(output_path, config)
            generated_files.append(eslint_config)
        
        if config.prettier:
            prettier_config = await self._generate_prettier_config(output_path, config)
            generated_files.append(prettier_config)
        
        return {
            "framework": "react",
            "build_tool": config.build_tool.value,
            "typescript": config.typescript,
            "state_management": config.state_management.value,
            "routing": config.routing,
            "generated_files": generated_files,
            "output_path": str(output_path),
            "next_steps": self._get_next_steps(config),
            "run_commands": self._get_run_commands(config)
        }
    
    def _extract_react_config(self, params: Dict[str, Any]) -> ReactConfig:
        """Extraer configuración React de los parámetros"""
        return ReactConfig(
            typescript=params.get("typescript", True),
            build_tool=ReactBuildTool(params.get("build_tool", "vite")),
            state_management=ReactStateManagement(params.get("state_management", "redux_toolkit")),
            routing=params.get("routing", True),
            testing=params.get("testing", True),
            pwa=params.get("pwa", False),
            styled_components=params.get("styled_components", False),
            tailwind_css=params.get("tailwind_css", True),
            eslint=params.get("eslint", True),
            prettier=params.get("prettier", True)
        )
    
    def _create_react_directory_structure(self, base_path: Path, config: ReactConfig):
        """Crear estructura de directorios para React"""
        directories = [
            "src",
            "src/components",
            "src/components/ui",
            "src/components/layout",
            "src/components/features",
            "src/hooks",
            "src/utils",
            "src/types",
            "src/assets",
            "src/styles",
            "public",
        ]
        
        if config.routing:
            directories.extend([
                "src/pages",
                "src/router",
            ])
        
        if config.state_management == ReactStateManagement.REDUX_TOOLKIT:
            directories.extend([
                "src/store",
                "src/store/slices",
                "src/store/api",
            ])
        elif config.state_management == ReactStateManagement.ZUSTAND:
            directories.append("src/store")
        
        if config.testing:
            directories.extend([
                "src/__tests__",
                "src/components/__tests__",
                "src/hooks/__tests__",
            ])
        
        # Crear directorios
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    async def _generate_package_json(self, output_path: Path, config: ReactConfig, schema: Dict[str, Any]) -> str:
        """Generar package.json para React"""
        project_name = schema.get("project_name", "react-app")
        
        # Usar LLM para generar package.json inteligente
        prompt = f"""
        Genera un package.json para una aplicación React SPA con:
        - Nombre: {project_name}
        - TypeScript: {config.typescript}
        - Build tool: {config.build_tool.value}
        - State management: {config.state_management.value}
        - Routing: {config.routing}
        - Testing: {config.testing}
        - PWA: {config.pwa}
        - Tailwind CSS: {config.tailwind_css}
        
        Incluye todas las dependencias necesarias y scripts optimizados.
        """
        
        package_content = await self.call_llm_for_generation(prompt, {
            "project_name": project_name,
            "config": config
        })
        
        # Fallback si LLM no está disponible
        if "placeholder" in package_content:
            package_content = self._generate_fallback_package_json(project_name, config)
        
        package_file = output_path / "package.json"
        package_file.write_text(package_content)
        
        return str(package_file)
    
    def _generate_fallback_package_json(self, project_name: str, config: ReactConfig) -> str:
        """Generar package.json fallback"""
        dependencies = {
            "react": "^18.2.0",
            "react-dom": "^18.2.0"
        }
        
        dev_dependencies = {}
        
        # Build tool dependencies
        if config.build_tool == ReactBuildTool.VITE:
            dev_dependencies.update({
                "vite": "^5.0.0",
                "@vitejs/plugin-react": "^4.0.0"
            })
        
        # TypeScript dependencies
        if config.typescript:
            dev_dependencies.update({
                "typescript": "^5.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0"
            })
        
        # Routing dependencies
        if config.routing:
            dependencies["react-router-dom"] = "^6.8.0"
        
        # State management dependencies
        if config.state_management == ReactStateManagement.REDUX_TOOLKIT:
            dependencies.update({
                "@reduxjs/toolkit": "^1.9.0",
                "react-redux": "^8.0.0"
            })
        elif config.state_management == ReactStateManagement.ZUSTAND:
            dependencies["zustand"] = "^4.3.0"
        
        # Styling dependencies
        if config.tailwind_css:
            dev_dependencies.update({
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            })
        
        if config.styled_components:
            dependencies["styled-components"] = "^5.3.0"
        
        # Testing dependencies
        if config.testing:
            if config.build_tool == ReactBuildTool.VITE:
                dev_dependencies.update({
                    "vitest": "^0.34.0",
                    "@testing-library/react": "^13.4.0",
                    "@testing-library/jest-dom": "^5.16.0"
                })
            else:
                dev_dependencies.update({
                    "jest": "^29.0.0",
                    "@testing-library/react": "^13.4.0",
                    "@testing-library/jest-dom": "^5.16.0"
                })
        
        # Scripts
        scripts = {
            "dev": "vite" if config.build_tool == ReactBuildTool.VITE else "webpack serve",
            "build": "vite build" if config.build_tool == ReactBuildTool.VITE else "webpack build",
            "preview": "vite preview" if config.build_tool == ReactBuildTool.VITE else "serve -s build"
        }
        
        if config.testing:
            scripts["test"] = "vitest" if config.build_tool == ReactBuildTool.VITE else "jest"
        
        if config.eslint:
            scripts["lint"] = "eslint src --ext .ts,.tsx"
        
        package_json = {
            "name": project_name,
            "private": True,
            "version": "0.0.0",
            "type": "module",
            "scripts": scripts,
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }
        
        return json.dumps(package_json, indent=2)
    
    async def _generate_build_config(self, output_path: Path, config: ReactConfig) -> str:
        """Generar configuración del build tool"""
        if config.build_tool == ReactBuildTool.VITE:
            return await self._generate_vite_config(output_path, config)
        elif config.build_tool == ReactBuildTool.WEBPACK:
            return await self._generate_webpack_config(output_path, config)
        else:
            raise ValueError(f"Build tool no soportado: {config.build_tool}")
    
    async def _generate_vite_config(self, output_path: Path, config: ReactConfig) -> str:
        """Generar vite.config.ts"""
        vite_config = """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
"""
        
        config_file = output_path / "vite.config.ts"
        config_file.write_text(vite_config)
        
        return str(config_file)
    
    async def _generate_webpack_config(self, output_path: Path, config: ReactConfig) -> str:
        """Generar webpack.config.js"""
        # Implementación básica de webpack config
        webpack_config = """const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: './src/index.tsx',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
  },
  module: {
    rules: [
      {
        test: /\.(ts|tsx)$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader', 'postcss-loader'],
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: './public/index.html',
    }),
  ],
  devServer: {
    contentBase: './dist',
    port: 3000,
  },
};
"""
        
        config_file = output_path / "webpack.config.js"
        config_file.write_text(webpack_config)
        
        return str(config_file)
    
    async def _generate_tsconfig(self, output_path: Path, config: ReactConfig) -> str:
        """Generar tsconfig.json"""
        tsconfig_content = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""
        
        tsconfig_file = output_path / "tsconfig.json"
        tsconfig_file.write_text(tsconfig_content)
        
        return str(tsconfig_file)
    
    async def _generate_tailwind_config(self, output_path: Path, config: ReactConfig) -> List[str]:
        """Generar configuración Tailwind CSS"""
        files = []
        
        # tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        
        tailwind_file = output_path / "tailwind.config.js"
        tailwind_file.write_text(tailwind_config)
        files.append(str(tailwind_file))
        
        # postcss.config.js
        postcss_config = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        
        postcss_file = output_path / "postcss.config.js"
        postcss_file.write_text(postcss_config)
        files.append(str(postcss_file))
        
        return files
    
    async def _generate_index_html(self, output_path: Path, config: ReactConfig, schema: Dict[str, Any]) -> str:
        """Generar index.html"""
        project_name = schema.get("project_name", "React App")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""
        
        html_file = output_path / "index.html"
        html_file.write_text(html_content)
        
        return str(html_file)
    
    async def _generate_main_app(self, output_path: Path, config: ReactConfig, schema: Dict[str, Any]) -> List[str]:
        """Generar aplicación principal"""
        files = []
        
        # main.tsx
        main_content = """import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
"""
        
        main_file = output_path / "src" / "main.tsx"
        main_file.write_text(main_content)
        files.append(str(main_file))
        
        # App.tsx
        project_name = schema.get("project_name", "React App")
        
        app_content = f"""import React from 'react'
import './App.css'

function App() {{
  return (
    <div className="App">
      <header className="App-header">
        <h1 className="text-4xl font-bold text-blue-600">
          Welcome to {project_name}
        </h1>
        <p className="text-lg text-gray-600 mt-4">
          Generated by Genesis Engine
        </p>
        <div className="mt-8 space-x-4">
          <button className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
            Get Started
          </button>
          <button className="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
            Learn More
          </button>
        </div>
      </header>
    </div>
  )
}}

export default App
"""
        
        app_file = output_path / "src" / "App.tsx"
        app_file.write_text(app_content)
        files.append(str(app_file))
        
        # App.css
        app_css = """.App {
  text-align: center;
}

.App-header {
  background-color: #f8fafc;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}
"""
        
        app_css_file = output_path / "src" / "App.css"
        app_css_file.write_text(app_css)
        files.append(str(app_css_file))
        
        return files
    
    async def _generate_base_components(self, output_path: Path, config: ReactConfig, schema: Dict[str, Any]) -> List[str]:
        """Generar componentes base"""
        files = []
        
        # Header component
        header_content = """import React from 'react'

interface HeaderProps {
  title: string
}

const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            {title}
          </h1>
          <nav className="hidden md:flex space-x-8">
            <a href="#" className="text-gray-500 hover:text-gray-900">Home</a>
            <a href="#" className="text-gray-500 hover:text-gray-900">About</a>
            <a href="#" className="text-gray-500 hover:text-gray-900">Contact</a>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header
"""
        
        header_file = output_path / "src" / "components" / "layout" / "Header.tsx"
        header_file.write_text(header_content)
        files.append(str(header_file))
        
        # Button component
        button_content = """import React from 'react'

interface ButtonProps {
  children: React.ReactNode
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'small' | 'medium' | 'large'
  onClick?: () => void
  disabled?: boolean
}

const Button: React.FC<ButtonProps> = ({ 
  children, 
  variant = 'primary', 
  size = 'medium', 
  onClick, 
  disabled = false 
}) => {
  const baseClasses = 'font-bold rounded focus:outline-none focus:ring-2 focus:ring-offset-2 transition-colors'
  
  const variantClasses = {
    primary: 'bg-blue-500 hover:bg-blue-700 text-white focus:ring-blue-500',
    secondary: 'bg-gray-500 hover:bg-gray-700 text-white focus:ring-gray-500',
    danger: 'bg-red-500 hover:bg-red-700 text-white focus:ring-red-500'
  }
  
  const sizeClasses = {
    small: 'py-1 px-2 text-sm',
    medium: 'py-2 px-4 text-base',
    large: 'py-3 px-6 text-lg'
  }
  
  const disabledClasses = 'opacity-50 cursor-not-allowed'
  
  const classes = `${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${disabled ? disabledClasses : ''}`
  
  return (
    <button 
      className={classes}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

export default Button
"""
        
        button_file = output_path / "src" / "components" / "ui" / "Button.tsx"
        button_file.write_text(button_content)
        files.append(str(button_file))
        
        return files
    
    async def _generate_global_styles(self, output_path: Path, config: ReactConfig) -> str:
        """Generar estilos globales"""
        if config.tailwind_css:
            css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;

  color-scheme: light dark;
  color: rgba(255, 255, 255, 0.87);
  background-color: #242424;

  font-synthesis: none;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  -webkit-text-size-adjust: 100%;
}

a {
  font-weight: 500;
  color: #646cff;
  text-decoration: inherit;
}
a:hover {
  color: #535bf2;
}

body {
  margin: 0;
  display: flex;
  place-items: center;
  min-width: 320px;
  min-height: 100vh;
}

h1 {
  font-size: 3.2em;
  line-height: 1.1;
}

#root {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

@media (prefers-color-scheme: light) {
  :root {
    color: #213547;
    background-color: #ffffff;
  }
  a:hover {
    color: #747bff;
  }
}
"""
        else:
            css_content = """body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

code {
  font-family: source-code-pro, Menlo, Monaco, Consolas, 'Courier New',
    monospace;
}

* {
  box-sizing: border-box;
}

#root {
  min-height: 100vh;
}
"""
        
        css_file = output_path / "src" / "index.css"
        css_file.write_text(css_content)
        
        return str(css_file)
    
    async def _generate_eslint_config(self, output_path: Path, config: ReactConfig) -> str:
        """Generar configuración ESLint"""
        eslint_content = """{
  "env": {
    "browser": true,
    "es2020": true
  },
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react-hooks/recommended"
  ],
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": "latest",
    "sourceType": "module"
  },
  "plugins": ["react-refresh"],
  "rules": {
    "react-refresh/only-export-components": "warn"
  }
}
"""
        
        eslint_file = output_path / ".eslintrc.json"
        eslint_file.write_text(eslint_content)
        
        return str(eslint_file)
    
    async def _generate_prettier_config(self, output_path: Path, config: ReactConfig) -> str:
        """Generar configuración Prettier"""
        prettier_content = """{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
"""
        
        prettier_file = output_path / ".prettierrc"
        prettier_file.write_text(prettier_content)
        
        return str(prettier_file)
    
    def _get_next_steps(self, config: ReactConfig) -> List[str]:
        """Obtener siguientes pasos"""
        steps = [
            "1. Instalar dependencias: npm install",
            "2. Configurar variables de entorno en .env",
            "3. Iniciar servidor de desarrollo: npm run dev",
            "4. Acceder a: http://localhost:3000"
        ]
        
        if config.testing:
            steps.append("5. Ejecutar tests: npm run test")
        
        if config.pwa:
            steps.append("6. Configurar service worker para PWA")
        
        return steps
    
    def _get_run_commands(self, config: ReactConfig) -> Dict[str, str]:
        """Obtener comandos de ejecución"""
        commands = {
            "install": "npm install",
            "dev": "npm run dev",
            "build": "npm run build",
            "preview": "npm run preview"
        }
        
        if config.testing:
            commands["test"] = "npm run test"
        
        if config.eslint:
            commands["lint"] = "npm run lint"
        
        return commands
    
    # Métodos para generar elementos específicos
    async def _generate_react_component(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar componente React específico"""
        component_name = params.get("component_name", "MyComponent")
        component_type = params.get("component_type", "functional")
        
        # Usar LLM para generar componente inteligente
        prompt = f"""
        Genera un componente React con:
        - Nombre: {component_name}
        - Tipo: {component_type}
        - TypeScript
        - Props bien tipadas
        - Mejores prácticas
        - Comentarios útiles
        """
        
        component_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "component_name": component_name,
            "component_content": component_content,
            "file_path": f"src/components/{component_name}.tsx"
        }
    
    async def _generate_react_hook(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar hook React personalizado"""
        hook_name = params.get("hook_name", "useCustomHook")
        hook_purpose = params.get("hook_purpose", "general")
        
        # Usar LLM para generar hook inteligente
        prompt = f"""
        Genera un hook React personalizado con:
        - Nombre: {hook_name}
        - Propósito: {hook_purpose}
        - TypeScript
        - Tipado correcto
        - Mejores prácticas
        - Documentación
        """
        
        hook_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "hook_name": hook_name,
            "hook_content": hook_content,
            "file_path": f"src/hooks/{hook_name}.ts"
        }
    
    async def _setup_react_routing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar React Router"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Router configuration
        router_content = """import { createBrowserRouter } from 'react-router-dom'
import App from '../App'
import Home from '../pages/Home'
import About from '../pages/About'
import NotFound from '../pages/NotFound'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      {
        index: true,
        element: <Home />
      },
      {
        path: 'about',
        element: <About />
      }
    ]
  },
  {
    path: '*',
    element: <NotFound />
  }
])
"""
        
        router_file = output_path / "src" / "router" / "index.tsx"
        router_file.write_text(router_content)
        files.append(str(router_file))
        
        return {"files": files}
    
    async def _setup_state_management(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar gestión de estado"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        if config.state_management == ReactStateManagement.REDUX_TOOLKIT:
            # Redux Toolkit store
            store_content = """import { configureStore } from '@reduxjs/toolkit'
import counterReducer from './slices/counterSlice'

export const store = configureStore({
  reducer: {
    counter: counterReducer,
  },
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
"""
            
            store_file = output_path / "src" / "store" / "index.ts"
            store_file.write_text(store_content)
            files.append(str(store_file))
        
        elif config.state_management == ReactStateManagement.ZUSTAND:
            # Zustand store
            store_content = """import { create } from 'zustand'

interface CounterState {
  count: number
  increment: () => void
  decrement: () => void
  reset: () => void
}

export const useCounterStore = create<CounterState>((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
  decrement: () => set((state) => ({ count: state.count - 1 })),
  reset: () => set({ count: 0 }),
}))
"""
            
            store_file = output_path / "src" / "store" / "counterStore.ts"
            store_file.write_text(store_content)
            files.append(str(store_file))
        
        return {"files": files}
    
    async def _setup_testing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar testing"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Test setup
        test_setup = """import '@testing-library/jest-dom'
"""
        
        setup_file = output_path / "src" / "setupTests.ts"
        setup_file.write_text(test_setup)
        files.append(str(setup_file))
        
        # Example test
        test_content = """import { render, screen } from '@testing-library/react'
import App from '../App'

test('renders learn react link', () => {
  render(<App />)
  const linkElement = screen.getByText(/learn react/i)
  expect(linkElement).toBeInTheDocument()
})
"""
        
        test_file = output_path / "src" / "__tests__" / "App.test.tsx"
        test_file.write_text(test_content)
        files.append(str(test_file))
        
        return {"files": files}
    
    # Handlers MCP
    async def _handle_generate_app(self, request) -> Dict[str, Any]:
        """Handler para generar aplicación React"""
        return await self._generate_react_application(request.data)
    
    async def _handle_generate_component(self, request) -> Dict[str, Any]:
        """Handler para generar componente"""
        return await self._generate_react_component(request.data)
    
    async def _handle_generate_hook(self, request) -> Dict[str, Any]:
        """Handler para generar hook"""
        return await self._generate_react_hook(request.data)
    
    async def _handle_setup_routing(self, request) -> Dict[str, Any]:
        """Handler para configurar routing"""
        return await self._setup_react_routing(request.data)
    
    async def _handle_setup_state_management(self, request) -> Dict[str, Any]:
        """Handler para configurar state management"""
        return await self._setup_state_management(request.data)
    
    async def _handle_setup_testing(self, request) -> Dict[str, Any]:
        """Handler para configurar testing"""
        return await self._setup_testing(request.data)
    
    async def _handle_configure_pwa(self, request) -> Dict[str, Any]:
        """Handler para configurar PWA"""
        return {"status": "pwa_configured"}
    
    async def _handle_setup_build_tool(self, request) -> Dict[str, Any]:
        """Handler para configurar build tool"""
        return {"status": "build_tool_configured"}
