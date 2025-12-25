# 🏗️ Arquitectura del Sistema

## Visión General

MrMonkeyShopWare sigue una arquitectura **modular por capas**, separando la lógica principal (core) de las interfaces de usuario (CLI/GUI).

---

## 📊 Diagrama de Arquitectura

```mermaid
graph TB
    subgraph "Capa de Presentación"
        CLI["CLI<br/>src/cli/"]
        GUI["GUI Tkinter<br/>src/gui/"]
    end
    
    subgraph "Capa de Lógica de Negocio"
        CONFIG["config.py<br/>Configuración"]
        DUMPER["dumper.py<br/>Volcado"]
        EXTRACTOR["extractor.py<br/>Extracción"]
        ANALYSER["analyser.py<br/>Análisis"]
        CLEANER["cleaner_xex.py<br/>Limpieza"]
        TOMLGEN["toml_generator.py<br/>TOML"]
    end
    
    subgraph "Capa de Utilidades"
        DRIVES["getDrives.py<br/>Detección"]
    end
    
    subgraph "Capa Externa"
        DIC["DiscImageCreator"]
        XISO["extract-xiso"]
        XEXTOOL["xextool"]
        XENON["XenonAnalyse"]
        RECOMP["XenonRecomp"]
    end
    
    CLI --> DUMPER & EXTRACTOR & ANALYSER
    GUI --> DUMPER & EXTRACTOR & ANALYSER
    
    DUMPER --> CONFIG & DIC
    EXTRACTOR --> CONFIG & XISO
    ANALYSER --> CONFIG & CLEANER & XENON
    CLEANER --> CONFIG & XEXTOOL
    TOMLGEN --> CONFIG & RECOMP
    
    CLI & GUI --> DRIVES
```

---

## 📁 Estructura de Directorios

```
src/
├── __init__.py
├── core/                    # Lógica principal
│   ├── __init__.py
│   ├── config.py           # Configuración y rutas
│   ├── dumper.py           # Volcado de discos
│   ├── extractor.py        # Extracción de ISOs
│   ├── analyser.py         # Análisis de XEX
│   ├── cleaner_xex.py      # Limpieza de XEX
│   └── toml_generator.py   # Generación de TOML
├── cli/                     # Interfaz CLI
│   ├── __init__.py
│   ├── main.py             # Punto de entrada
│   ├── dump.py             # Comando dump
│   ├── extract.py          # Comando extract
│   ├── analyse.py          # Comando analyse
│   └── tomlgen.py          # Comando tomlgen
├── gui/                     # Interfaz GUI
│   ├── __init__.py
│   └── main.py             # Aplicación Tkinter
└── utils/                   # Utilidades
    ├── __init__.py
    └── getDrives.py        # Detección de unidades
```

---

## 🔄 Patrones de Diseño

### 1. Módulos Independientes
Cada módulo del core es independiente y puede usarse por separado.

```python
from src.core import dump_disc, extract_iso, analyse_xex

# Uso individual
dump_disc("E:")
extract_iso("game.iso")
analyse_xex("default.xex")
```

### 2. Configuración Centralizada
Todas las rutas se gestionan desde `config.py` con soporte para variables de entorno.

### 3. Logging Opcional
Cada función acepta un parámetro `log` para inyectar logging personalizado.

```python
def dump_disc(drive, gui_ref=None, out_path=None):
    log = gui_ref.log if gui_ref else print
```

### 4. Manejo de Errores
Funciones retornan `True/False` o `None` en caso de error, permitiendo encadenar operaciones.

---

## 🔌 Puntos de Extensión

| Componente | Cómo Extender |
|------------|---------------|
| Nueva herramienta | Añadir ruta en `config.py`, crear módulo en `core/` |
| Nuevo comando CLI | Crear archivo en `cli/`, seguir patrón existente |
| Nueva funcionalidad GUI | Añadir botón/método en `gui/main.py` |
| Nueva utilidad | Añadir en `utils/`, exportar en `__init__.py` |

---

## 📦 Dependencias

### Internas
- `src.core` → Lógica principal
- `src.utils` → Utilidades compartidas

### Externas (Python)
- `subprocess` → Ejecución de herramientas
- `os`, `tempfile` → Gestión de archivos
- `tkinter` → GUI
- `argparse` → Parsing de CLI
- `psutil`, `pywin32` → Sistema Windows

### Externas (Binarios)
- DiscImageCreator, extract-xiso, xextool, XenonAnalyse, XenonRecomp
