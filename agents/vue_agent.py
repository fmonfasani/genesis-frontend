"""
Vue Agent - Especialista en aplicaciones Vue.js
Parte del ecosistema genesis-frontend
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

from .base_agent import FrontendAgent, AgentTask, TaskResult


class VueBuildTool(str, Enum):
    """Herramientas de build soportadas para Vue"""
    VITE = "vite"
    WEBPACK = "webpack"
    VUE_CLI = "vue_cli"


class VueStateManagement(str, Enum):
    """Sistemas de gestión de estado para Vue"""
    PINIA = "pinia"
    VUEX = "vuex"
    COMPOSITION_API = "composition_api"


class VueUILibrary(str, Enum):
    """Librerías de UI para Vue"""
    VUETIFY = "vuetify"
    QUASAR = "quasar"
    ELEMENT_PLUS = "element_plus"
    NAIVE_UI = "naive_ui"
    CUSTOM = "custom"


@dataclass
class VueConfig:
    """Configuración para aplicaciones Vue.js"""
    vue_version: str = "3"
    typescript: bool = True
    build_tool: VueBuildTool = VueBuildTool.VITE
    state_management: VueStateManagement = VueStateManagement.PINIA
    ui_library: VueUILibrary = VueUILibrary.CUSTOM
    router: bool = True
    pwa: bool = False
    ssr: bool = False  # Nuxt.js para SSR
    testing: bool = True
    eslint: bool = True
    prettier: bool = True
    tailwind_css: bool = True
    composition_api: bool = True


class VueAgent(FrontendAgent):
    """
    Agente Vue - Especialista en aplicaciones Vue.js
    
    Responsabilidades:
    - Generar aplicaciones Vue 3 con Composition API
    - Configurar Vue Router para SPA
    - Integrar Pinia para gestión de estado
    - Configurar Vite como build tool
    - Generar componentes Vue reutilizables
    - Configurar testing con Vitest
    - Integrar librerías de UI (Vuetify, Quasar)
    - Configurar PWA con Vue
    """
    
    def __init__(self):
        super().__init__(
            agent_id="vue_agent",
            name="VueAgent",
            specialization="vue"
        )
        
        # Capacidades específicas de Vue
        self.add_capability("vue3_app_generation")
        self.add_capability("composition_api_setup")
        self.add_capability("vue_router_setup")
        self.add_capability("pinia_setup")
        self.add_capability("vuex_setup")
        self.add_capability("vite_configuration")
        self.add_capability("vue_component_generation")
        self.add_capability("composable_generation")
        self.add_capability("vuetify_integration")
        self.add_capability("quasar_integration")
        self.add_capability("pwa_configuration")
        self.add_capability("testing_setup")
        
        # Registrar handlers específicos
        self.register_handler("generate_vue_app", self._handle_generate_app)
        self.register_handler("generate_component", self._handle_generate_component)
        self.register_handler("generate_composable", self._handle_generate_composable)
        self.register_handler("setup_router", self._handle_setup_router)
        self.register_handler("setup_state_management", self._handle_setup_state_management)
        self.register_handler("integrate_ui_library", self._handle_integrate_ui_library)
        self.register_handler("configure_pwa", self._handle_configure_pwa)
        self.register_handler("setup_testing", self._handle_setup_testing)
        
    async def initialize(self):
        """Inicializar agente Vue"""
        self.logger.info("Inicializando Vue Agent")
        
        # Configurar metadata específica de Vue
        self.set_metadata("version", "1.0.0")
        self.set_metadata("vue_version", "3.4.0")
        self.set_metadata("vite_version", "5.0.0")
        self.set_metadata("pinia_support", True)
        self.set_metadata("composition_api_support", True)
        self.set_metadata("typescript_support", True)
        self.set_metadata("pwa_support", True)
        
        self.logger.info("Vue Agent inicializado correctamente")
    
    async def execute_task(self, task: AgentTask) -> TaskResult:
        """Ejecutar tarea específica de Vue"""
        task_name = task.name.lower()
        
        try:
            if "generate_vue_app" in task_name:
                result = await self._generate_vue_application(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_component" in task_name:
                result = await self._generate_vue_component(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "generate_composable" in task_name:
                result = await self._generate_vue_composable(task.params)
                return TaskResult(
                    task_id=task.id,
                    success=True,
                    result=result
                )
            elif "setup_router" in task_name:
                result = await self._setup_vue_router(task.params)
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
    
    async def _generate_vue_application(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar aplicación Vue completa"""
        self.log_frontend_action("generate_app", "vue", params)
        
        # Validar parámetros
        validation_errors = self.validate_frontend_request(params)
        if validation_errors:
            raise ValueError(f"Errores de validación: {', '.join(validation_errors)}")
        
        # Extraer configuración
        config = self._extract_vue_config(params)
        output_path = Path(params.get("output_path", "./"))
        schema = params.get("schema", {})
        
        # Crear estructura de directorios
        self._create_vue_directory_structure(output_path, config)
        
        generated_files = []
        
        # 1. Generar package.json
        package_json = await self._generate_package_json(output_path, config, schema)
        generated_files.append(package_json)
        
        # 2. Generar configuración Vite
        vite_config = await self._generate_vite_config(output_path, config)
        generated_files.append(vite_config)
        
        # 3. Generar configuración TypeScript
        if config.typescript:
            tsconfig = await self._generate_tsconfig(output_path, config)
            generated_files.append(tsconfig)
        
        # 4. Generar index.html
        index_html = await self._generate_index_html(output_path, config, schema)
        generated_files.append(index_html)
        
        # 5. Generar aplicación principal
        app_files = await self._generate_main_app(output_path, config, schema)
        generated_files.extend(app_files)
        
        # 6. Configurar router
        if config.router:
            router_files = await self._setup_vue_router({"config": config, "output_path": output_path})
            generated_files.extend(router_files.get("files", []))
        
        # 7. Configurar gestión de estado
        if config.state_management != VueStateManagement.COMPOSITION_API:
            state_files = await self._setup_state_management({"config": config, "output_path": output_path})
            generated_files.extend(state_files.get("files", []))
        
        # 8. Generar componentes base
        base_components = await self._generate_base_components(output_path, config, schema)
        generated_files.extend(base_components)
        
        # 9. Configurar Tailwind CSS
        if config.tailwind_css:
            tailwind_files = await self._generate_tailwind_config(output_path, config)
            generated_files.extend(tailwind_files)
        
        # 10. Integrar librería de UI
        if config.ui_library != VueUILibrary.CUSTOM:
            ui_files = await self._integrate_ui_library({"config": config, "output_path": output_path})
            generated_files.extend(ui_files.get("files", []))
        
        # 11. Configurar testing
        if config.testing:
            test_files = await self._setup_testing({"config": config, "output_path": output_path})
            generated_files.extend(test_files.get("files", []))
        
        # 12. Generar estilos globales
        styles_file = await self._generate_global_styles(output_path, config)
        generated_files.append(styles_file)
        
        return {
            "framework": "vue",
            "vue_version": config.vue_version,
            "build_tool": config.build_tool.value,
            "state_management": config.state_management.value,
            "ui_library": config.ui_library.value,
            "typescript": config.typescript,
            "generated_files": generated_files,
            "output_path": str(output_path),
            "next_steps": self._get_next_steps(config),
            "run_commands": self._get_run_commands(config)
        }
    
    def _extract_vue_config(self, params: Dict[str, Any]) -> VueConfig:
        """Extraer configuración Vue de los parámetros"""
        return VueConfig(
            vue_version=params.get("vue_version", "3"),
            typescript=params.get("typescript", True),
            build_tool=VueBuildTool(params.get("build_tool", "vite")),
            state_management=VueStateManagement(params.get("state_management", "pinia")),
            ui_library=VueUILibrary(params.get("ui_library", "custom")),
            router=params.get("router", True),
            pwa=params.get("pwa", False),
            ssr=params.get("ssr", False),
            testing=params.get("testing", True),
            eslint=params.get("eslint", True),
            prettier=params.get("prettier", True),
            tailwind_css=params.get("tailwind_css", True),
            composition_api=params.get("composition_api", True)
        )
    
    def _create_vue_directory_structure(self, base_path: Path, config: VueConfig):
        """Crear estructura de directorios para Vue"""
        directories = [
            "src",
            "src/components",
            "src/components/ui",
            "src/components/layout",
            "src/components/features",
            "src/composables",
            "src/utils",
            "src/types",
            "src/assets",
            "src/styles",
            "public",
        ]
        
        if config.router:
            directories.extend([
                "src/views",
                "src/router",
            ])
        
        if config.state_management == VueStateManagement.PINIA:
            directories.append("src/stores")
        elif config.state_management == VueStateManagement.VUEX:
            directories.extend([
                "src/store",
                "src/store/modules",
            ])
        
        if config.testing:
            directories.extend([
                "src/__tests__",
                "src/components/__tests__",
                "src/composables/__tests__",
            ])
        
        # Crear directorios
        for directory in directories:
            (base_path / directory).mkdir(parents=True, exist_ok=True)
    
    async def _generate_package_json(self, output_path: Path, config: VueConfig, schema: Dict[str, Any]) -> str:
        """Generar package.json para Vue"""
        project_name = schema.get("project_name", "vue-app")
        
        # Usar LLM para generar package.json inteligente
        prompt = f"""
        Genera un package.json para una aplicación Vue.js con:
        - Nombre: {project_name}
        - Vue version: {config.vue_version}
        - TypeScript: {config.typescript}
        - Build tool: {config.build_tool.value}
        - State management: {config.state_management.value}
        - UI library: {config.ui_library.value}
        - Router: {config.router}
        - PWA: {config.pwa}
        - Testing: {config.testing}
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
    
    def _generate_fallback_package_json(self, project_name: str, config: VueConfig) -> str:
        """Generar package.json fallback"""
        dependencies = {
            "vue": "^3.4.0"
        }
        
        dev_dependencies = {
            "@vitejs/plugin-vue": "^5.0.0",
            "vite": "^5.0.0"
        }
        
        # TypeScript dependencies
        if config.typescript:
            dev_dependencies.update({
                "typescript": "^5.0.0",
                "vue-tsc": "^1.8.0"
            })
        
        # Router dependencies
        if config.router:
            dependencies["vue-router"] = "^4.2.0"
        
        # State management dependencies
        if config.state_management == VueStateManagement.PINIA:
            dependencies["pinia"] = "^2.1.0"
        elif config.state_management == VueStateManagement.VUEX:
            dependencies["vuex"] = "^4.1.0"
        
        # UI Library dependencies
        if config.ui_library == VueUILibrary.VUETIFY:
            dependencies.update({
                "vuetify": "^3.4.0",
                "@mdi/font": "^7.0.0"
            })
        elif config.ui_library == VueUILibrary.QUASAR:
            dependencies["quasar"] = "^2.14.0"
        elif config.ui_library == VueUILibrary.ELEMENT_PLUS:
            dependencies["element-plus"] = "^2.4.0"
        
        # Styling dependencies
        if config.tailwind_css:
            dev_dependencies.update({
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.0",
                "postcss": "^8.4.0"
            })
        
        # PWA dependencies
        if config.pwa:
            dev_dependencies["vite-plugin-pwa"] = "^0.17.0"
        
        # Testing dependencies
        if config.testing:
            dev_dependencies.update({
                "vitest": "^1.0.0",
                "@vue/test-utils": "^2.4.0",
                "jsdom": "^23.0.0"
            })
        
        # Linting dependencies
        if config.eslint:
            dev_dependencies.update({
                "eslint": "^8.0.0",
                "@vue/eslint-config-typescript": "^12.0.0",
                "eslint-plugin-vue": "^9.0.0"
            })
        
        if config.prettier:
            dev_dependencies["prettier"] = "^3.0.0"
        
        # Scripts
        scripts = {
            "dev": "vite",
            "build": "vue-tsc && vite build",
            "preview": "vite preview"
        }
        
        if config.testing:
            scripts["test"] = "vitest"
        
        if config.eslint:
            scripts["lint"] = "eslint src --ext .vue,.js,.ts"
        
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
    
    async def _generate_vite_config(self, output_path: Path, config: VueConfig) -> str:
        """Generar vite.config.ts"""
        vite_config = """import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'"""
        
        if config.pwa:
            vite_config += "\nimport { VitePWA } from 'vite-plugin-pwa'"
        
        vite_config += """

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),"""
        
        if config.pwa:
            vite_config += """
    VitePWA({
      registerType: 'autoUpdate',
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg}']
      }
    }),"""
        
        vite_config += """
  ],
  resolve: {
    alias: {
      '@': '/src',
    },
  },"""
        
        if config.testing:
            vite_config += """
  test: {
    globals: true,
    environment: 'jsdom',
  },"""
        
        vite_config += """
})
"""
        
        config_file = output_path / "vite.config.ts"
        config_file.write_text(vite_config)
        
        return str(config_file)
    
    async def _generate_tsconfig(self, output_path: Path, config: VueConfig) -> str:
        """Generar tsconfig.json"""
        tsconfig_content = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "module": "ESNext",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "preserve",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.vue"],
  "references": [{ "path": "./tsconfig.node.json" }]
}"""
        
        tsconfig_file = output_path / "tsconfig.json"
        tsconfig_file.write_text(tsconfig_content)
        
        return str(tsconfig_file)
    
    async def _generate_index_html(self, output_path: Path, config: VueConfig, schema: Dict[str, Any]) -> str:
        """Generar index.html"""
        project_name = schema.get("project_name", "Vue App")
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/svg+xml" href="/vite.svg" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{project_name}</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.ts"></script>
  </body>
</html>
"""
        
        html_file = output_path / "index.html"
        html_file.write_text(html_content)
        
        return str(html_file)
    
    async def _generate_main_app(self, output_path: Path, config: VueConfig, schema: Dict[str, Any]) -> List[str]:
        """Generar aplicación principal"""
        files = []
        
        # main.ts
        main_content = """import { createApp } from 'vue'
import './style.css'
import App from './App.vue'"""
        
        if config.router:
            main_content += "\nimport router from './router'"
        
        if config.state_management == VueStateManagement.PINIA:
            main_content += "\nimport { createPinia } from 'pinia'"
        elif config.state_management == VueStateManagement.VUEX:
            main_content += "\nimport store from './store'"
        
        main_content += """

const app = createApp(App)
"""
        
        if config.router:
            main_content += "\napp.use(router)"
        
        if config.state_management == VueStateManagement.PINIA:
            main_content += "\napp.use(createPinia())"
        elif config.state_management == VueStateManagement.VUEX:
            main_content += "\napp.use(store)"
        
        main_content += """
app.mount('#app')
"""
        
        main_file = output_path / "src" / "main.ts"
        main_file.write_text(main_content)
        files.append(str(main_file))
        
        # App.vue
        project_name = schema.get("project_name", "Vue App")
        
        app_content = f"""<template>
  <div id="app">
    <header class="app-header">
      <h1 class="text-4xl font-bold text-blue-600">
        Welcome to {project_name}
      </h1>
      <p class="text-lg text-gray-600 mt-4">
        Generated by Genesis Engine
      </p>
      <div class="mt-8 space-x-4">
        <button 
          @click="incrementCounter"
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Count: {{{{ counter }}}}
        </button>
        <button class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded">
          Learn More
        </button>
      </div>
    </header>"""
        
        if config.router:
            app_content += """
    <main class="mt-8">
      <RouterView />
    </main>"""
        
        app_content += """
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'"""
        
        if config.router:
            app_content += "\nimport { RouterView } from 'vue-router'"
        
        app_content += """

const counter = ref(0)

const incrementCounter = () => {
  counter.value++
}
</script>

<style scoped>
.app-header {
  text-align: center;
  padding: 40px;
  background-color: #f8fafc;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>
"""
        
        app_file = output_path / "src" / "App.vue"
        app_file.write_text(app_content)
        files.append(str(app_file))
        
        return files
    
    async def _generate_base_components(self, output_path: Path, config: VueConfig, schema: Dict[str, Any]) -> List[str]:
        """Generar componentes base"""
        files = []
        
        # Header component
        header_content = """<template>
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-6">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ title }}
        </h1>
        <nav class="hidden md:flex space-x-8">
          <a href="#" class="text-gray-500 hover:text-gray-900">Home</a>
          <a href="#" class="text-gray-500 hover:text-gray-900">About</a>
          <a href="#" class="text-gray-500 hover:text-gray-900">Contact</a>
        </nav>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
interface Props {
  title: string
}

defineProps<Props>()
</script>
"""
        
        header_file = output_path / "src" / "components" / "layout" / "Header.vue"
        header_file.write_text(header_content)
        files.append(str(header_file))
        
        # Button component
        button_content = """<template>
  <button 
    :class="buttonClasses"
    :disabled="disabled"
    @click="handleClick"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'small' | 'medium' | 'large'
  disabled?: boolean
}

interface Emits {
  click: []
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'medium',
  disabled: false
})

const emit = defineEmits<Emits>()

const buttonClasses = computed(() => {
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
  
  const disabledClasses = props.disabled ? 'opacity-50 cursor-not-allowed' : ''
  
  return `${baseClasses} ${variantClasses[props.variant]} ${sizeClasses[props.size]} ${disabledClasses}`
})

const handleClick = () => {
  if (!props.disabled) {
    emit('click')
  }
}
</script>
"""
        
        button_file = output_path / "src" / "components" / "ui" / "Button.vue"
        button_file.write_text(button_content)
        files.append(str(button_file))
        
        return files
    
    async def _generate_tailwind_config(self, output_path: Path, config: VueConfig) -> List[str]:
        """Generar configuración Tailwind CSS"""
        files = []
        
        # tailwind.config.js
        tailwind_config = """/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
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
    
    async def _generate_global_styles(self, output_path: Path, config: VueConfig) -> str:
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

#app {
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
            css_content = """#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
}
"""
        
        css_file = output_path / "src" / "style.css"
        css_file.write_text(css_content)
        
        return str(css_file)
    
    def _get_next_steps(self, config: VueConfig) -> List[str]:
        """Obtener siguientes pasos"""
        steps = [
            "1. Instalar dependencias: npm install",
            "2. Configurar variables de entorno en .env",
            "3. Iniciar servidor de desarrollo: npm run dev",
            "4. Acceder a: http://localhost:5173"
        ]
        
        if config.testing:
            steps.append("5. Ejecutar tests: npm run test")
        
        if config.pwa:
            steps.append("6. Configurar manifest.json para PWA")
        
        return steps
    
    def _get_run_commands(self, config: VueConfig) -> Dict[str, str]:
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
    async def _generate_vue_component(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar componente Vue específico"""
        component_name = params.get("component_name", "MyComponent")
        component_type = params.get("component_type", "composition")
        
        # Usar LLM para generar componente inteligente
        prompt = f"""
        Genera un componente Vue 3 con:
        - Nombre: {component_name}
        - API: Composition API
        - TypeScript
        - Props bien tipadas
        - Eventos tipados
        - Mejores prácticas Vue 3
        - Comentarios útiles
        """
        
        component_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "component_name": component_name,
            "component_content": component_content,
            "file_path": f"src/components/{component_name}.vue"
        }
    
    async def _generate_vue_composable(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Generar composable Vue"""
        composable_name = params.get("composable_name", "useCustom")
        composable_purpose = params.get("composable_purpose", "general")
        
        # Usar LLM para generar composable inteligente
        prompt = f"""
        Genera un composable Vue 3 con:
        - Nombre: {composable_name}
        - Propósito: {composable_purpose}
        - Composition API
        - TypeScript
        - Reactive refs
        - Mejores prácticas
        - Documentación
        """
        
        composable_content = await self.call_llm_for_generation(prompt, params)
        
        return {
            "composable_name": composable_name,
            "composable_content": composable_content,
            "file_path": f"src/composables/{composable_name}.ts"
        }
    
    async def _setup_vue_router(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar Vue Router"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Router configuration
        router_content = """import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
"""
        
        router_file = output_path / "src" / "router" / "index.ts"
        router_file.write_text(router_content)
        files.append(str(router_file))
        
        # Home view
        home_view = """<template>
  <div class="home">
    <h1 class="text-4xl font-bold mb-8">Welcome to Vue 3</h1>
    <p class="text-lg text-gray-600 mb-8">
      This is a home page built with Vue 3 and Composition API
    </p>
    <div class="space-x-4">
      <RouterLink 
        to="/about"
        class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
      >
        About
      </RouterLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
"""
        
        home_file = output_path / "src" / "views" / "HomeView.vue"
        home_file.write_text(home_view)
        files.append(str(home_file))
        
        # About view
        about_view = """<template>
  <div class="about">
    <h1 class="text-4xl font-bold mb-8">About</h1>
    <p class="text-lg text-gray-600 mb-8">
      This is an about page
    </p>
    <RouterLink 
      to="/"
      class="bg-gray-500 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded"
    >
      Back to Home
    </RouterLink>
  </div>
</template>

<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>
"""
        
        about_file = output_path / "src" / "views" / "AboutView.vue"
        about_file.write_text(about_view)
        files.append(str(about_file))
        
        return {"files": files}
    
    async def _setup_state_management(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar gestión de estado"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        if config.state_management == VueStateManagement.PINIA:
            # Pinia store
            store_content = """import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)
  const doubleCount = computed(() => count.value * 2)
  
  function increment() {
    count.value++
  }
  
  function decrement() {
    count.value--
  }
  
  function reset() {
    count.value = 0
  }
  
  return { count, doubleCount, increment, decrement, reset }
})
"""
            
            store_file = output_path / "src" / "stores" / "counter.ts"
            store_file.write_text(store_content)
            files.append(str(store_file))
        
        elif config.state_management == VueStateManagement.VUEX:
            # Vuex store
            store_content = """import { createStore } from 'vuex'

interface State {
  count: number
}

export default createStore<State>({
  state: {
    count: 0
  },
  getters: {
    doubleCount: (state) => state.count * 2
  },
  mutations: {
    increment(state) {
      state.count++
    },
    decrement(state) {
      state.count--
    },
    reset(state) {
      state.count = 0
    }
  },
  actions: {
    increment({ commit }) {
      commit('increment')
    },
    decrement({ commit }) {
      commit('decrement')
    },
    reset({ commit }) {
      commit('reset')
    }
  }
})
"""
            
            store_file = output_path / "src" / "store" / "index.ts"
            store_file.write_text(store_content)
            files.append(str(store_file))
        
        return {"files": files}
    
    async def _integrate_ui_library(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Integrar librería de UI"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        if config.ui_library == VueUILibrary.VUETIFY:
            # Vuetify plugin
            vuetify_content = """import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light'
  }
})
"""
            
            vuetify_file = output_path / "src" / "plugins" / "vuetify.ts"
            vuetify_file.parent.mkdir(exist_ok=True)
            vuetify_file.write_text(vuetify_content)
            files.append(str(vuetify_file))
        
        return {"files": files}
    
    async def _setup_testing(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Configurar testing"""
        config = params.get("config")
        output_path = params.get("output_path")
        
        if not config or not output_path:
            return {"files": []}
        
        files = []
        
        # Example test
        test_content = """import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import App from '../App.vue'

describe('App', () => {
  it('renders properly', () => {
    const wrapper = mount(App)
    expect(wrapper.text()).toContain('Welcome to')
  })
})
"""
        
        test_file = output_path / "src" / "__tests__" / "App.spec.ts"
        test_file.write_text(test_content)
        files.append(str(test_file))
        
        return {"files": files}
    
    # Handlers MCP
    async def _handle_generate_app(self, request) -> Dict[str, Any]:
        """Handler para generar aplicación Vue"""
        return await self._generate_vue_application(request.data)
    
    async def _handle_generate_component(self, request) -> Dict[str, Any]:
        """Handler para generar componente"""
        return await self._generate_vue_component(request.data)
    
    async def _handle_generate_composable(self, request) -> Dict[str, Any]:
        """Handler para generar composable"""
        return await self._generate_vue_composable(request.data)
    
    async def _handle_setup_router(self, request) -> Dict[str, Any]:
        """Handler para configurar router"""
        return await self._setup_vue_router(request.data)
    
    async def _handle_setup_state_management(self, request) -> Dict[str, Any]:
        """Handler para configurar state management"""
        return await self._setup_state_management(request.data)
    
    async def _handle_integrate_ui_library(self, request) -> Dict[str, Any]:
        """Handler para integrar UI library"""
        return await self._integrate_ui_library(request.data)
    
    async def _handle_configure_pwa(self, request) -> Dict[str, Any]:
        """Handler para configurar PWA"""
        return {"status": "pwa_configured"}
    
    async def _handle_setup_testing(self, request) -> Dict[str, Any]:
        """Handler para configurar testing"""
        return await self._setup_testing(request.data)
