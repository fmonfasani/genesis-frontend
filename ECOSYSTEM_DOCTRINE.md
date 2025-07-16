<!-- ECOSYSTEM_DOCTRINE: genesis-frontend -->
# 🎨 Ecosystem Doctrine — Genesis-Frontend (Generación Frontend)

Este repositorio forma parte del ecosistema **Genesis Engine**.  
Su rol es el de **generación de código frontend usando agentes especializados**.

## 🧠 Rol Declarado

- Tipo: **Generador Frontend**
- Nombre: `genesis-frontend`
- Dominio: Código frontend (UI, componentes, estado)
- Función: Generar código frontend moderno y funcional

## 🔒 Mandamientos del Proyecto

### 1. **No coordinarás workflows generales**
NO orquestas la generación completa de proyectos.  
Solo generas la parte frontend cuando te lo soliciten.

### 2. **No conocerás backend ni DevOps**
NO contiene lógica de FastAPI, Docker, etc.  
Solo frontend: componentes, páginas, estado, estilos.

### 3. **No interactuarás con el usuario final**
NO tiene CLI ni interfaz gráfica.  
Solo agentes que responden a solicitudes MCPturbo.

### 4. **Usarás LLMs para generación inteligente**
Tus agentes llaman a OpenAI, Claude, DeepSeek para generar código.  
NO código hardcodeado o templates estáticos.

### 5. **Serás especialista en frontend**
Conocimiento profundo de Next.js, React, Vue, TypeScript, estilos.  
Generas código frontend moderno y optimizado.

### 6. **Cada agente tendrá responsabilidad específica**
NextJSAgent: aplicaciones Next.js  
ReactAgent: componentes React  
UIAgent: diseño de interfaz  
StateAgent: gestión de estado

### 7. **Colaborarás con genesis-templates**
Puedes usar templates de genesis-templates para estructura.  
Pero el código lo generas con LLMs.

---

## 🧩 Interfaz esperada por consumidores

Genesis-core y otros componentes usan:

- `NextJSAgent.generate_frontend()`
- `ReactAgent.create_components()`
- `UIAgent.design_interface()`
- `StateAgent.setup_state_management()`

---

## 📦 Separación de capas (importante)

| Capa | Puede importar desde | No puede importar desde |
|------|----------------------|--------------------------|
| genesis-frontend | genesis-agents, mcpturbo, genesis-templates | genesis-core, genesis-cli, genesis-backend, genesis-devops |
| genesis-core | mcpturbo | genesis-frontend |

---

## 🤖 AI Agents, please read:

Este repositorio es el especialista en frontend del ecosistema.

Si estás revisando código, escribiendo tests o generando lógica nueva:
- ❌ No implementes lógica de backend o DevOps.
- ❌ No coordines workflows generales.
- ❌ No interactúes directamente con usuarios.
- ✅ Enfócate en generar código frontend excelente.
- ✅ Usa LLMs para código inteligente.
- ✅ Mantén agentes especializados en frontend.

Toda excepción debe documentarse en `DOCTRINE_CHANGE_REQUEST.md`.

---

## 📎 Referencias

- Genesis Agents → [https://github.com/fmonfasani/genesis-agents](https://github.com/fmonfasani/genesis-agents)
- MCPturbo → [https://github.com/fmonfasani/mcpturbo](https://github.com/fmonfasani/mcpturbo)
- Next.js → [https://nextjs.org/](https://nextjs.org/)