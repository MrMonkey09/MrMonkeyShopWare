# Tablón de Operaciones - Bitácora del Proyecto

Este documento centraliza el seguimiento de tareas, vinculando cada actividad con sus Historias de Usuario, Epicas y Sprints correspondientes.

---

## 📋 Tablón Kanban

### 🟠 Tareas Pendientes

*  **Ninguna**

---

### 🟢 Tareas Finalizadas (Done)

#### [TASK-001] Visor de Estructura de Archivos ✅
*   **Estado**: `Finalizado`
*   **Épica**: GUI - Gestión de Juegos
*   **Descripción**: Vista en detalle del juego para visualizar estructura de archivos TOML/JSON.
*   **Archivos**: `gui/components/file_viewer.py`, `gui/components/gamedetail.py`
*   **Fecha/Hora Finalización**: 2025-12-25 16:28

#### [TASK-002] Actualizar CLI acorde al GUI ✅
*   **Estado**: `Finalizado`
*   **Épica**: CLI - Paridad de Funcionalidades
*   **Descripción**: Actualizar el módulo CLI con subcomandos y paridad con GUI.
*   **Archivos**: `cli/main.py` - REESCRITO
*   **Comandos**: analyse, scan-usb, list, info, extract, dump, pipeline, db
*   **Fecha/Hora Finalización**: 2025-12-25 16:36

#### [TASK-003] Sincronización de Rutas al Workspace 🎄 ✅
*   **Estado**: `Finalizado`
*   **Épica**: Core - Estabilidad y Organización
*   **Descripción**: Detectar cuando los archivos de un juego están fuera del workspace y ofrecer sincronización.
*   **Archivos modificados**:
    - `core/game_workspace.py` - +ExternalFile, +check_external_files(), +sync_all_files()
    - `gui/components/gamedetail.py` - +Banner ⚠️, +Botón Sincronizar
    - `cli/main.py` - +Comando `sync`
*   **Funcionalidades implementadas**:
    - [x] Detectar archivos fuera del workspace
    - [x] Mostrar advertencia visual ⚠️ en checklist
    - [x] Botón "🔄 Sincronizar" para copiar al workspace
    - [x] Comando CLI `mrmonkey sync`
    - [x] Actualizar rutas en BD después de sincronizar
*   **Fecha/Hora Creación**: 2025-12-25 16:42
*   **Fecha/Hora Finalización**: 2025-12-25 16:50

#### [TASK-004] Crear README.md Completo 🔴 ✅
*   **Estado**: `Finalizado`
*   **Épica**: Documentación - Publicación
*   **Prioridad**: 🔴 CRÍTICA
*   **Descripción**: Crear un README.md profesional y completo para la publicación del repositorio.
*   **Archivos creados**:
    - `README.md` - ✅ CREADO completo
    - `CONTRIBUTING.md` - ✅ CREADO en raíz
*   **Contenido incluido**:
    - [x] Badges (License, Python, Platform)
    - [x] Descripción clara del proyecto
    - [x] Lista de features principales
    - [x] Instrucciones de instalación
    - [x] Ejemplos de uso (CLI y GUI)
    - [x] Estructura de workspaces
    - [x] Links a documentación
    - [x] Sección de contribución
*   **Fecha/Hora Creación**: 2025-12-25 17:06
*   **Fecha/Hora Finalización**: 2025-12-25 17:13

#### [TASK-005] Eliminar Archivos Obsoletos y CLI Legacy 🟠 ✅
*   **Estado**: `Finalizado`
*   **Épica**: Mantenimiento - Limpieza
*   **Prioridad**: 🟠 Alta
*   **Descripción**: Eliminar archivos obsoletos y marcar módulos CLI legacy como deprecated.
*   **Archivos ELIMINADOS (raíz)**:
    - [x] `analisis_auditoria_old-project.md`
    - [x] `analisis_auditoria_proyecto.md`
*   **Archivos CLI marcados DEPRECATED**:
    - [x] `cli/analyse.py`
    - [x] `cli/dump.py`
    - [x] `cli/extract.py`
    - [x] `cli/pipeline.py`
    - [x] `cli/tomlgen.py`
*   **Duplicados corregidos en docs**:
    - [x] `docs/index.md` - Eliminadas líneas duplicadas en tutoriales
*   **Fecha/Hora Creación**: 2025-12-25 17:06
*   **Fecha/Hora Finalización**: 2025-12-25 17:18

#### [TASK-006] Actualizar Documentación y Screenshots 🟡 ✅
*   **Estado**: `Finalizado`
*   **Épica**: Documentación - Actualización
*   **Prioridad**: 🟡 Media
*   **Descripción**: Actualizar documentación para reflejar nuevas funcionalidades.
*   **Archivos actualizados**:
    - [x] `docs/index.md` - Corregidos duplicados en tutoriales
    - [x] `docs/modulos/cli.md` - Añadidos todos los comandos nuevos + deprecated
    - [x] `docs/modulos/core.md` - Añadidos 4 nuevos módulos
    - [x] `docs/api/game-workspace.md` - CREADO documentación completa
*   **Fecha/Hora Creación**: 2025-12-25 17:06
*   **Fecha/Hora Finalización**: 2025-12-25 17:25

---

## 📝 Plantilla para Nueva Tarea
Copia y pega este bloque para agregar una nueva tarea:

```markdown
#### [TASK-ID] Título Descriptivo
*   **Estado**: `[Pendiente / En Curso / Finalizado]`
*   **Epica**: [Nombre Epica]
*   **Descripción**: ...
*   **Fecha/Hora Creacion**: [Fecha/Hora]
*   **Fecha/Hora Actualizacion**: [Fecha/Hora]
```
```

---


