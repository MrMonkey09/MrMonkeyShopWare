# 🖥️ Módulo GUI

El módulo `gui` proporciona una interfaz gráfica moderna usando **CustomTkinter**.

---

## 📁 Estructura

```
gui/
├── app.py              # Aplicación principal (ModernApp)
└── components/
    ├── sidebar.py      # Barra lateral de navegación
    ├── dropzone.py     # Zona de arrastrar y soltar
    ├── logview.py      # Vista de logs con timestamps
    ├── gamelist.py     # Lista de juegos con filtros
    ├── gamedetail.py   # Vista de detalle de juego
    └── settings.py     # Panel de configuración
```

---

## 🚀 Iniciar GUI

```bash
python -m gui.app
```

---

## 🎨 Interfaz

### Layout Principal

```
┌─────────────────────────────────────────────────────────┐
│ 🎮 MrMonkey                                         🌙 │
│ ShopWare        ┌────────────────────────────────────┐ │
├─────────────────┤   Contenido Principal               │ │
│ 🚀 Pipeline     │                                    │ │
│ 📀 Dump Disc    │   [DropZone / GameList / etc.]     │ │
│ 📂 Extraer ISO  │                                    │ │
│ 🔬 Analizar XEX │                                    │ │
│ 📝 Generar TOML ├────────────────────────────────────┤ │
│ ─────────────── │ 📋 Log                             │ │
│ 📚 Historial    │ [13:30:01] ℹ️ Mensaje...           │ │
│ ⚙️ Configuración│ [13:30:02] ✅ Completado           │ │
└─────────────────┴────────────────────────────────────┘ │
│ Listo                                        v0.1.0   │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Componentes

### ModernApp (`app.py`)

Aplicación principal con:
- Sidebar de navegación
- Área de contenido dinámico
- LogView persistente
- Barra de estado

```python
from gui.app import ModernApp

app = ModernApp()
app.mainloop()
```

### DropZone

Zona para arrastrar y soltar archivos ISO/XEX:
- Soporte drag & drop (tkinterdnd2)
- Click para seleccionar archivo
- Validación de extensiones

### GameList

Lista scrollable de juegos con:
- Filtro por estado
- Tarjetas con icono y status
- Callback para selección

### GameDetailView 🆕

Vista de detalle del juego con:
- Pestañas: Info, Archivos, Notas
- Metadata de XexTool
- Cambio de estado
- Edición de notas
- Eliminación de juego

### SettingsView

Panel de configuración con pestañas:
- 🔧 Herramientas (rutas)
- 🎨 Apariencia (tema)
- 💾 Base de Datos
- 📜 Logs

---

## 🎨 Características

| Característica | Estado |
|----------------|--------|
| Tema oscuro/claro | ✅ |
| Drag & drop | ✅ |
| Persistencia de configuración | ✅ |
| Vista de historial | ✅ |
| Vista de detalle de juego | ✅ |
| Responsive | ✅ |

---

## ⚙️ Threading

Las operaciones largas se ejecutan en threads separados:

```python
def _start_analyse(self, file_path: str):
    def job():
        result = analyse_xex(file_path, log=self._log)
        # Guardar en BD, mostrar resumen...
    threading.Thread(target=job, daemon=True).start()
```

---

## 📚 Ver también

- [Catálogo de Vistas](./gui-catalogo-vistas.md)
- [Tutorial Pipeline](../tutoriales/pipeline-completo.md)
