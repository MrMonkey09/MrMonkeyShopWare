# 📐 Guía de Estilo

Convenciones de código para el proyecto.

---

## 🐍 Python

### Estilo base: PEP 8 + Black

```python
# ✅ Bien
def dump_disc(drive_letter: str, output_path: str = None) -> bool:
    """Hace dump de un disco Xbox 360."""
    pass

# ❌ Mal
def dumpDisc(driveLetter, outputPath=None):
    pass
```

### Formato

| Aspecto | Regla |
|---------|-------|
| Indentación | 4 espacios |
| Línea máxima | 88 caracteres |
| Comillas | Dobles `"string"` |
| Trailing comma | Sí, en listas multilinea |

### Nombres

| Tipo | Convención | Ejemplo |
|------|------------|---------|
| Variables | snake_case | `file_path` |
| Funciones | snake_case | `dump_disc()` |
| Clases | PascalCase | `LauncherGUI` |
| Constantes | UPPER_SNAKE | `TEMP_BASE` |
| Privados | _prefijo | `_sanitize_path()` |

---

## 📝 Docstrings

Estilo Google:

```python
def extract_iso(iso_path: str, output_dir: str = None) -> str | None:
    """
    Extrae contenido de un ISO Xbox 360.
    
    Args:
        iso_path: Ruta al archivo ISO.
        output_dir: Directorio de salida. Si no se especifica,
            se usa el directorio del ISO.
    
    Returns:
        Ruta al directorio con contenido extraído, o None si falla.
    
    Raises:
        FileNotFoundError: Si el ISO no existe.
    
    Example:
        >>> extract_iso("game.iso")
        "C:/temp/game"
    """
```

---

## 📦 Imports

Orden (isort lo hace automático):

```python
# 1. Stdlib
import os
import subprocess
from pathlib import Path

# 2. Third-party
import toml
from win32file import GetDriveType

# 3. Local
from src.core.config import TEMP_BASE
from src.utils import get_drives_with_types
```

---

## 💬 Comentarios

```python
# ✅ Explica el POR QUÉ
# Usamos cwd para workaround del bug en extract-xiso
subprocess.run(cmd, cwd=final_output)

# ❌ No expliques el QUÉ (ya es obvio)
# Ejecutar subprocess
subprocess.run(cmd)
```

---

## 🔧 Type Hints

```python
# Siempre en firmas de funciones públicas
def analyse_xex(
    xex_path: str,
    out_dir: str | None = None,
    log: callable | None = None
) -> tuple[str, str] | None:
```

---

## 📋 Herramientas

```bash
# Formatear
black src/ tests/

# Ordenar imports
isort src/ tests/

# Lint
flake8 src/

# Type check
mypy src/
```

---

## ✅ Checklist Pre-Commit

- [ ] `black .` sin cambios
- [ ] `isort .` sin cambios
- [ ] `flake8 .` sin errores
- [ ] `mypy .` sin errores críticos
- [ ] Tests pasan

---

## 📚 Ver también

- [DESARROLLO.md](./DESARROLLO.md)
- [CONTRIBUIR.md](./CONTRIBUIR.md)
