# 🚀 Primeros Pasos

Esta guía te ayudará a instalar y configurar MrMonkeyShopWare en tu sistema.

---

## 📋 Prerrequisitos

Antes de comenzar, asegúrate de tener:

- **Windows 10/11** (requerido para algunas herramientas)
- **Python 3.11+** ([Descargar](https://www.python.org/downloads/))
- **Git** ([Descargar](https://git-scm.com/downloads))
- **Unidad óptica** compatible con discos Xbox 360 (para dump)

---

## 📥 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MrMonkey09/MrMonkeyShopWare.git
cd MrMonkeyShopWare
```

### 2. Crear entorno virtual

```bash
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
# Dependencias principales
pip install -r requirements.txt

# (Opcional) Dependencias de desarrollo
pip install -r requirements-dev.txt
```

---

## 🔧 Configurar Herramientas Externas

El proyecto requiere herramientas externas. Descárgalas y configura sus rutas.

### Opción A: Rutas por defecto

Coloca las herramientas en `C:\tools\`:

```
C:\tools\
├── DiscImageCreator\
│   └── DiscImageCreator.exe
├── extract-xiso\
│   └── extract-xiso.exe
├── XexTool\
│   └── xextool.exe
└── XenonRecompUnlimited\
    ├── XenonAnalyse.exe
    └── build\XenonRecomp\Debug\XenonRecomp.exe
```

### Opción B: Variables de entorno

Configura las rutas personalizadas:

```powershell
# PowerShell
$env:DISC_IMAGE_CREATOR_PATH = "D:\mis-tools\DiscImageCreator.exe"
$env:EXTRACT_XISO_PATH = "D:\mis-tools\extract-xiso.exe"
$env:XEXTOOL_PATH = "D:\mis-tools\xextool.exe"
$env:XENON_ANALYSE_PATH = "D:\mis-tools\XenonAnalyse.exe"
$env:XENON_RECOMP_PATH = "D:\mis-tools\XenonRecomp.exe"
```

### Opción C: Editar config.py

Edita directamente `src/core/config.py` con tus rutas.

---

## ✅ Verificar Instalación

```bash
# Verificar que Python está configurado
python --version

# Verificar dependencias
pip list

# Ejecutar GUI para probar
python -m src.gui.main
```

Si la GUI se abre correctamente, ¡la instalación fue exitosa!

---

## ▶️ Siguiente Paso

- [Inicio Rápido](./inicio-rapido.md) - Tutorial de 5 minutos
- [Requisitos del Sistema](./requisitos.md) - Requisitos detallados
- [FAQ](./faq.md) - Preguntas frecuentes
