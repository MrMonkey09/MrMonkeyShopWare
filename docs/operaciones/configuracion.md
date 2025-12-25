# ⚙️ Configuración

Guía de opciones de configuración.

---

## 📁 Archivo Principal

`src/core/config.py`

---

## 🔧 Variables de Entorno

| Variable | Descripción | Default |
|----------|-------------|---------|
| `XENON_ANALYSE_PATH` | Ruta a XenonAnalyse.exe | `C:\tools\XenonRecompUnlimited\XenonAnalyse.exe` |
| `XEXTOOL_PATH` | Ruta a xextool.exe | `C:\tools\XexTool\xextool.exe` |
| `EXTRACT_XISO_PATH` | Ruta a extract-xiso.exe | `C:\tools\extract-xiso\extract-xiso.exe` |
| `DISC_IMAGE_CREATOR_PATH` | Ruta a DiscImageCreator.exe | `C:\tools\DiscImageCreator\DiscImageCreator.exe` |
| `XENON_RECOMP_PATH` | Ruta a XenonRecomp.exe | `C:\tools\...\XenonRecomp.exe` |
| `PPC_CONTEXT_PATH` | Ruta a ppc_context.h | `C:\tools\XenonRecomp\XenonUtils\ppc_context.h` |
| `X360_TEMP_BASE` | Carpeta base para temporales | `%TEMP%\x360dump` |

---

## 🔧 Configurar Variables

### Windows (PowerShell)

```powershell
# Temporal (solo sesión actual)
$env:XENON_ANALYSE_PATH = "D:\tools\XenonAnalyse.exe"

# Permanente (usuario)
[Environment]::SetEnvironmentVariable("XENON_ANALYSE_PATH", "D:\tools\XenonAnalyse.exe", "User")
```

### Windows (CMD)

```cmd
set XENON_ANALYSE_PATH=D:\tools\XenonAnalyse.exe
```

### Archivo .env (con python-dotenv)

```env
XENON_ANALYSE_PATH=D:\tools\XenonAnalyse.exe
XEXTOOL_PATH=D:\tools\xextool.exe
```

---

## 📂 Estructura de Tools Recomendada

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
    └── build\
        └── XenonRecomp\
            └── Debug\
                └── XenonRecomp.exe
```

---

## 🔍 Verificar Configuración

```python
from src.core.config import *

print(f"XenonAnalyse: {XENON_ANALYSE_PATH}")
print(f"xextool: {XEXTOOL_PATH}")
print(f"extract-xiso: {EXTRACT_XISO_PATH}")
print(f"DiscImageCreator: {DISC_IMAGE_CREATOR_PATH}")
```

---

## 📚 Ver también

- [Primeros Pasos](./primeros-pasos.md)
- [Requisitos](./requisitos.md)
