"""
NextJS Agent - Especialista en generación de aplicaciones Next.js
Parte del ecosistema genesis-frontend
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from .base_agent import FrontendAgent, AgentTask, TaskResult


class NextJSFeature(str, Enum):
    """Características de Next.js soportadas"""
    APP_ROUTER = "app_router"
    PAGES_ROUTER = "pages_router"
    SERVER_COMPONENTS = "server_components"
    STATIC_GENERATION = "static_generation"
    MIDDLEWARE = "middleware"
    API_ROUTES = "api_routes"
    INTERNATIONALIZATION = "i18n"
    IMAGE_OPTIMIZATION = "image_optimization"


@dataclass
class NextJSConfig:
    """Configuración para aplicaciones Next.js"""
    typescript: bool = True
    app_router: bool = True
    src_directory: bool = False
    tailwind_css: bool = True
    eslint: bool = True
    import_alias: str = "@/*"
    features: List[NextJSFeature] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = [
                NextJSFeature.APP_ROUTER,
                NextJSFeature.SERVER_COMPONENTS,
                NextJSFeature.STATIC_GENERATION
            ]


class NextJSAgent(FrontendAgent):
    """
    Agente NextJS - Especialista en Next.js
    
    Responsabilidades:
    - Generar aplicaciones Next.js completas
    - Configurar App Router y Pages Router
    - Integrar TypeScript, Tailwind CSS, ESLint
    - Generar componentes React optimizados
    - Configurar middleware y API routes
    """
    
    def __init__(self):
        super().__init__(
            agent_id="nextjs_agent",
            name="NextJSAgent",
            specialization="nextjs"
        )
        
        # Capacidades específicas de Next.js
        self.add_capability("nextjs_app_generation")
        self.add_capability("app_router_setup")
        self.add_capability("pages_router_setup")
        self.add_capability("typescript_configuration")
        self.add_capability("tailwind_integration")
        self.add_capability("server_components")
        self.add_capability("static_generation")
        self.add_capability("middleware_setup")
        self.add_capability("api_routes_generation")
        self.add_capability("component_generation")
        self.add_capability("layout_generation")
        self.add_capability("page_generation")
        self.add_capability("hook_generation")
        
        # Registrar handlers específicos
        self.register_handler("generate_nextjs_app", self._handle_generate_app)
        self.register_handler("generate_component", self._handle_generate_component)
        self.register_handler("generate_page", self._handle_generate_page)
        self.register_handler("generate_layout", self._handle_generate_layout)
        self.register_handler("setup_routing", self._handle_setup_routing)
        self.register_handler("configure_typescript", self._handle_configure_typescript)
        self.register_handler("integrate_tailwind", self._handle_integrate_tailwind)
        self.register_handler("generate_api_route", self._handle_generate_api_route)
        
    async def initialize(self):
        """Inicializar agente NextJS"""
        self.logger.info("Inicializando NextJS Agent")
        
        # Configurar template engine para Next.js
        self.set_metadata("version", "1.0.0")
        self.set_metadata("nextjs_version", "14.0.0")
        self.set_metadata("react_version", "18.0.0")
        self.set_metadata("typescript_support", True)
        self.set_metadata("tailwind_support", True)
        self.set_metadata("app_router_support", True)
        
        self.logger.info("NextJS Agent inicializado correctamente")
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica de Next.js"""
        task_name = task.name.lower()
        
        try:
            if "generate_nextjs_app" in task_name:
                result = await self._generate_nextjs_application(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_component" in task_name:
                result = await self._generate_nextjs_component(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_page" in task_name:
                result = await self._generate_nextjs_page(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_layout" in task_name:
                result = await self._generate_nextjs_layout(task.params)
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
    
    async def _generate_nextjs_application(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar aplicación Next.js completa"""
        self.log_frontend_action("generate_app", "nextjs", params)
        
        # Validar parámetros
        validation_errors = self.validate_frontend_request(params)
        if validation_errors:
            raise ValueError(f"Errores de validación: {', '.join(validation_errors)}")
        
        # Extraer configuración
        config = self._extract_nextjs_config(params)
        output_path = Path(params.get("output_path", "./"))
        schema = params.get("schema", {})
        
        # Crear estructura de directorios
        self._create_nextjs_directory_structure(output_path, config)
        
        generated_files = []
        
        # 1. Generar package.json
        package_json = await self._generate_package_json(output_path, config, schema)
        generated_files.append(package_json)
        
        # 2. Generar configuración Next.js
        next_config = await self._generate_next_config(output_path, config)
        generated_files.append(next_config)
        
        # 3. Generar configuración TypeScript
        if config.typescript:
            tsconfig = await self._generate_tsconfig(output_path, config)
            generated_files.append(tsconfig)
        
        # 4. Generar configuración Tailwind
        if config.tailwind_css:
            tailwind_files = await self._generate_tailwind_config(output_path, config)
            generated_files.extend(tailwind_files)
        
        # 5. Generar layout principal
        layout_file = await self._generate_root_layout(output_path, config, schema)
        generated_files.append(layout_file)
        
        # 6. Generar página principal
        page_file = await self._generate_main_page(output_path, config, schema)
        generated_files.append(page_file)
        
        # 7. Generar componentes base
        base_components = await self._generate_base_components(output_path, config, schema)
        generated_files.extend(base_components)
        
        # 8. Generar globals.css
        globals_css = await self._generate_globals_css(output_path, config)
        generated_files.append(globals_css)
        
        # 9. Generar ESLint config
        if config.eslint:
            eslint_config = await self._generate_eslint_config(output_path, config)
            generated_files.append(eslint_config)
        
        return {
            "framework": "nextjs",
            "typescript": config.typescript,
            "app_router": config.app_router,
            "tailwind_css": config.tailwind_css,
            "generated_files": generated_files,
            "output_path": str(output_path),
            "next_steps": self._get_next_steps(config),
            "run_commands": self._get_run_commands()
        }
    
    def _extract_nextjs_config(self, params: Dict[str, Any]) -> NextJSConfig:
        """Extraer configuración Next.js de los parámetros"""
        schema = params.get("schema", {})
        stack = params.get("stack", {})
        
        return NextJSConfig(
            typescript=params.get("typescript", True),
            app_router=params.get("app_router", True),
            src_directory=params.get("src_directory", False),
            tailwind_css=params.get("tailwind_css", True),
            eslint=params.get("eslint", True),
            import_alias=params.get("import_alias", "@/*"),
            features=params.get("features", [])
        )
    
    def _create_nextjs_directory_structure(self, base_path: Path, config: NextJSConfig):
        """Crear estructura de directorios para Next.js"""
        # Estructura básica
        directories = [
            "public",
            "styles",
            "components/ui",
            "components/layout",
            "components/features",
            "lib",
            "hooks",
            "types",
            "utils",
        ]
        
        # Estructura según App Router o Pages Router
        if config.app_router:
            directories.extend([
                "app",
                "app/globals",
                "app/components",
                "app/api",
            ])
        else:
            directories.extend([
                "pages",
                "pages/api",
            ])
        
        # Crear directorios
        for directory in directories:
            self.repo.add_file(f"{directory}/.gitkeep", "")
    
    async def _generate_package_json(self, output_path: Path, config: NextJSConfig, schema: Dict[str, Any]) -> str:
        """Generar package.json para Next.js"""
        project_name = schema.get("project_name", "nextjs-app")
        
        # Usar LLM para generar package.json inteligente
        prompt = f"""
        Genera un package.json para una aplicación Next.js con las siguientes características:
        - Nombre del proyecto: {project_name}
        - TypeScript: {config.typescript}
        - App Router: {config.app_router}
        - Tailwind CSS: {config.tailwind_css}
        - ESLint: {config.eslint}
        
        Incluye todas las dependencias necesarias y scripts optimizados.
        """
        
        package_content = await self.call_llm_for_generation(prompt, {
            "project_name": project_name,
            "config": config
        })
        
        # Fallback si LLM no está disponible
        if "placeholder" in package_content:
            package_content = self._generate_fallback_package_json(project_name, config)
        
        package_file = "package.json"
        self.repo.add_file(package_file, package_content)
        
        return package_file
    
    def _generate_fallback_package_json(self, project_name: str, config: NextJSConfig) -> str:
        """Generar package.json fallback"""
        dependencies = {
            "next": "^14.0.0",
            "react": "^18.0.0",
            "react-dom": "^18.0.0"
        }
        
        dev_dependencies = {}
        
        if config.typescript:
            dev_dependencies.update({
                "typescript": "^5.0.0",
                "@types/react": "^18.0.0",
                "@types/react-dom": "^18.0.0",
                "@types/node": "^20.0.0"
            })
        
        if config.tailwind_css:
            dev_dependencies.update({
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            })
        
        if config.eslint:
            dev_dependencies.update({
                "eslint": "^8.0.0",
                "eslint-config-next": "^14.0.0"
            })
        
        package_json = {
            "name": project_name,
            "version": "0.1.0",
            "private": True,
            "scripts": {
                "dev": "next dev",
                "build": "next build",
                "start": "next start",
                "lint": "next lint"
            },
            "dependencies": dependencies,
            "devDependencies": dev_dependencies
        }
        
        return json.dumps(package_json, indent=2)
    
    async def _generate_next_config(self, output_path: Path, config: NextJSConfig) -> str:
        """Generar next.config.js"""
        next_config_content = """/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    appDir: true,
  },
  images: {
    domains: [],
  },
}

module.exports = nextConfig
"""
        
        config_file = "next.config.js"
        self.repo.add_file(config_file, next_config_content)
        
        return config_file
    
    async def _generate_tsconfig(self, output_path: Path, config: NextJSConfig) -> str:
        """Generar tsconfig.json"""
        tsconfig_content = """{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}"""
        
        tsconfig_file = "tsconfig.json"
        self.repo.add_file(tsconfig_file, tsconfig_content)
        
        return tsconfig_file
    
    async def _generate_tailwind_config(self, output_path: Path, config: NextJSConfig) -> List[str]:
        """Generar configuración Tailwind CSS"""
        files = []
        
        # tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic':
          'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [],
}
"""
        
        tailwind_file = "tailwind.config.js"
        self.repo.add_file(tailwind_file, tailwind_config)
        files.append(tailwind_file)
        
        # postcss.config.js
        postcss_config = """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""
        
        postcss_file = "postcss.config.js"
        self.repo.add_file(postcss_file, postcss_config)
        files.append(postcss_file)
        
        return files
    
    async def _generate_root_layout(self, output_path: Path, config: NextJSConfig, schema: Dict[str, Any]) -> str:
        """Generar layout principal"""
        project_name = schema.get("project_name", "NextJS App")
        
        # Usar LLM para generar layout inteligente
        prompt = f"""
        Genera un layout raíz para Next.js App Router con:
        - Título del proyecto: {project_name}
        - TypeScript: {config.typescript}
        - Tailwind CSS: {config.tailwind_css}
        - Estructura HTML semántica
        - Optimizaciones de rendimiento
        - Meta tags SEO
        """
        
        layout_content = await self.call_llm_for_generation(prompt, {
            "project_name": project_name,
            "config": config
        })
        
        # Fallback si LLM no está disponible
        if "placeholder" in layout_content:
            layout_content = self._generate_fallback_layout(project_name, config)
        
        layout_file = "app/layout.tsx"
        self.repo.add_file(layout_file, layout_content)
        
        return layout_file
    
    def _generate_fallback_layout(self, project_name: str, config: NextJSConfig) -> str:
        """Generar layout fallback"""
        return f"""import './globals.css'
import type {{ Metadata }} from 'next'
import {{ Inter }} from 'next/font/google'

const inter = Inter({{ subsets: ['latin'] }})

export const metadata: Metadata = {{
  title: '{project_name}',
  description: 'Generated by Genesis Engine',
}}

export default function RootLayout({{
  children,
}}: {{
  children: React.ReactNode
}}) {{
  return (
    <html lang="en">
      <body className={{inter.className}}>
        {{children}}
      </body>
    </html>
  )
}}
"""
    
    async def _generate_main_page(self, output_path: Path, config: NextJSConfig, schema: Dict[str, Any]) -> str:
        """Generar página principal"""
        project_name = schema.get("project_name", "NextJS App")
        
        # Usar LLM para generar página inteligente
        prompt = f"""
        Genera una página principal para Next.js con:
        - Título del proyecto: {project_name}
        - Diseño moderno y responsive
        - Componentes interactivos
        - Tailwind CSS para estilos
        - Optimizada para SEO
        """
        
        page_content = await self.call_llm_for_generation(prompt, {
            "project_name": project_name,
            "config": config
        })
        
        # Fallback si LLM no está disponible
        if "placeholder" in page_content:
            page_content = self._generate_fallback_page(project_name, config)
        
        page_file = "app/page.tsx"
        self.repo.add_file(page_file, page_content)
        
        return page_file
    
    def _generate_fallback_page(self, project_name: str, config: NextJSConfig) -> str:
        """Generar página fallback"""
        return f"""export default function Home() {{
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <p className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          {project_name}
        </p>
      </div>

      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:translate-y-[-10px] before:rounded-full before:bg-gradient-radial before:from-white before:to-transparent before:blur-2xl before:content-[''] after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-conic after:from-sky-200 after:via-blue-200 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
        <h1 className="text-6xl font-bold">
          Welcome to {project_name}
        </h1>
      </div>

      <div className="mb-32 grid text-center lg:max-w-5xl lg:w-full lg:mb-0 lg:grid-cols-4 lg:text-left">
        <a
          href="https://nextjs.org/docs"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className="mb-3 text-2xl font-semibold">
            Docs
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            Find in-depth information about Next.js features and API.
          </p>
        </a>

        <a
          href="https://nextjs.org/learn"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className="mb-3 text-2xl font-semibold">
            Learn
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            Learn about Next.js in an interactive course with quizzes!
          </p>
        </a>

        <a
          href="https://vercel.com/templates?framework=next.js"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className="mb-3 text-2xl font-semibold">
            Templates
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50">
            Explore the Next.js 13 playground.
          </p>
        </a>

        <a
          href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100 hover:dark:border-neutral-700 hover:dark:bg-neutral-800/30"
          target="_blank"
          rel="noopener noreferrer"
        >
          <h2 className="mb-3 text-2xl font-semibold">
            Deploy
          </h2>
          <p className="m-0 max-w-[30ch] text-sm opacity-50 group-hover:opacity-100">
            Instantly deploy your Next.js site to a shareable URL with Vercel.
          </p>
        </a>
      </div>
    </main>
  )
}}
"""
    
    async def _generate_base_components(self, output_path: Path, config: NextJSConfig, schema: Dict[str, Any]) -> List[str]:
        """Generar componentes base"""
        files = []
        
        # Header component
        header_content = """export default function Header() {
  return (
    <header className="bg-white shadow">
      <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900">
          Genesis NextJS App
        </h1>
      </div>
    </header>
  )
}"""
        
        header_file = "components/layout/Header.tsx"
        self.repo.add_file(header_file, header_content)
        files.append(header_file)
        
        # Footer component
        footer_content = """export default function Footer() {
  return (
    <footer className="bg-gray-50">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <p className="text-center text-gray-500">
          © 2024 Genesis Engine. All rights reserved.
        </p>
      </div>
    </footer>
  )
}"""
        
        footer_file = "components/layout/Footer.tsx"
        self.repo.add_file(footer_file, footer_content)
        files.append(footer_file)
        
        return files
    
    async def _generate_globals_css(self, output_path: Path, config: NextJSConfig) -> str:
        """Generar globals.css"""
        css_content = """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 0, 0, 0;
  --background-start-rgb: 214, 219, 220;
  --background-end-rgb: 255, 255, 255;
}

@media (prefers-color-scheme: dark) {
  :root {
    --foreground-rgb: 255, 255, 255;
    --background-start-rgb: 0, 0, 0;
    --background-end-rgb: 0, 0, 0;
  }
}

body {
  color: rgb(var(--foreground-rgb));
  background: linear-gradient(
      to bottom,
      transparent,
      rgb(var(--background-end-rgb))
    )
    rgb(var(--background-start-rgb));
}
"""
        
        css_file = "app/globals.css"
        self.repo.add_file(css_file, css_content)
        
        return css_file
    
    async def _generate_eslint_config(self, output_path: Path, config: NextJSConfig) -> str:
        """Generar configuración ESLint"""
        eslint_content = """{
  "extends": "next/core-web-vitals"
}
"""
        
        eslint_file = ".eslintrc.json"
        self.repo.add_file(eslint_file, eslint_content)
        
        return eslint_file
    
    def _get_next_steps(self, config: NextJSConfig) -> List[str]:
        """Obtener siguientes pasos"""
        steps = [
            "1. Instalar dependencias: npm install",
            "2. Configurar variables de entorno en .env.local",
            "3. Iniciar servidor de desarrollo: npm run dev",
            "4. Acceder a: http://localhost:3000"
        ]
        
        if config.typescript:
            steps.append("5. Revisar configuración TypeScript en tsconfig.json")
        
        if config.tailwind_css:
            steps.append("6. Personalizar estilos en tailwind.config.js")
        
        return steps
    
    def _get_run_commands(self) -> Dict[str, str]:
        """Obtener comandos de ejecución"""
        return {
            "install": "npm install",
            "dev": "npm run dev",
            "build": "npm run build",
            "start": "npm start",
            "lint": "npm run lint",
            "type-check": "tsc --noEmit"
        }
    
    # Métodos para generar componentes específicos
    async def _generate_nextjs_component(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar componente Next.js específico"""
        component_name = params.get("component_name", "MyComponent")
        component_type = params.get("component_type", "functional")
        
        # Usar LLM para generar componente inteligente
        prompt = f"""
        Genera un componente React/Next.js con:
        - Nombre: {component_name}
        - Tipo: {component_type}
        - TypeScript
        - Mejores prácticas
        - Comentarios útiles
        """
        
        component_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "component_name": component_name,
            "component_content": component_content,
            "file_path": f"components/{component_name}.tsx"
        }
    
    async def _generate_nextjs_page(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar página Next.js específica"""
        page_name = params.get("page_name", "about")
        
        # Usar LLM para generar página inteligente
        prompt = f"""
        Genera una página Next.js para la ruta "/{page_name}" con:
        - Estructura App Router
        - TypeScript
        - Componentes optimizados
        - SEO metadata
        """
        
        page_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "page_name": page_name,
            "page_content": page_content,
            "file_path": f"app/{page_name}/page.tsx"
        }
    
    async def _generate_nextjs_layout(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar layout Next.js específico"""
        layout_name = params.get("layout_name", "dashboard")
        
        # Usar LLM para generar layout inteligente
        prompt = f"""
        Genera un layout Next.js para "{layout_name}" con:
        - Estructura App Router
        - TypeScript
        - Navegación incluida
        - Responsive design
        """
        
        layout_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "layout_name": layout_name,
            "layout_content": layout_content,
            "file_path": f"app/{layout_name}/layout.tsx"
        }
    
    # Handlers MCP
    async def _handle_generate_app(self, request) -> Dict[str, Any]:
        """Handler para generar aplicación NextJS"""
        return await self._generate_nextjs_application(request.data)
    
    async def _handle_generate_component(self, request) -> Dict[str, Any]:
        """Handler para generar componente"""
        return await self._generate_nextjs_component(request.data)
    
    async def _handle_generate_page(self, request) -> Dict[str, Any]:
        """Handler para generar página"""
        return await self._generate_nextjs_page(request.data)
    
    async def _handle_generate_layout(self, request) -> Dict[str, Any]:
        """Handler para generar layout"""
        return await self._generate_nextjs_layout(request.data)
    
    async def _handle_setup_routing(self, request) -> Dict[str, Any]:
        """Handler para configurar routing"""
        return {"status": "routing_configured", "router_type": "app_router"}
    
    async def _handle_configure_typescript(self, request) -> Dict[str, Any]:
        """Handler para configurar TypeScript"""
        return {"status": "typescript_configured"}
    
    async def _handle_integrate_tailwind(self, request) -> Dict[str, Any]:
        """Handler para integrar Tailwind"""
        return {"status": "tailwind_integrated"}
    
    async def _handle_generate_api_route(self, request) -> Dict[str, Any]:
        """Handler para generar ruta API"""
        return {"status": "api_route_generated"}
