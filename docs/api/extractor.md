# 📦 API: Extractor

Módulo para extracción de ISOs Xbox 360.

**Ubicación**: `src/core/extractor.py`

---

## extract_iso

```python
def extract_iso(
    iso_path: str,
    output_dir: str = None,
    log: callable = None
) -> str | None
```

Extrae contenido de un ISO Xbox 360 usando extract-xiso.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `iso_path` | `str` | Ruta al archivo ISO |
| `output_dir` | `str` | Opcional. Directorio de salida |
| `log` | `callable` | Opcional. Función de logging |

### Retorna

- `str`: Ruta a la carpeta con contenido extraído
- `None`: Error durante la extracción

### Ejemplo

```python
from src.core import extract_iso

# Uso básico
folder = extract_iso("./game.iso")
# Resultado: "./game/" (junto al ISO)

# Con directorio personalizado
folder = extract_iso("./game.iso", output_dir="./extracted")

# Con logging
folder = extract_iso("./game.iso", log=print)
```

---

## list_xex_files

```python
def list_xex_files(output_dir: str) -> list[str]
```

Busca todos los archivos `.xex` en un directorio (recursivo).

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `output_dir` | `str` | Directorio donde buscar |

### Retorna

- `list[str]`: Lista de rutas absolutas a archivos XEX

### Ejemplo

```python
from src.core import extract_iso, list_xex_files

folder = extract_iso("./game.iso")
xex_files = list_xex_files(folder)

for xex in xex_files:
    print(f"Encontrado: {xex}")
# Encontrado: C:\...\default.xex
# Encontrado: C:\...\update.xex
```

---

## Comportamiento especial

### Carpetas incrementales

Si la carpeta de destino ya existe, se genera un nombre incremental:
```
game/      (si existe)
game_1/    (se crea)
```

---

## 📚 Ver también

- [Guía de Extracción](../tutoriales/guia-extraccion.md)
- [extract-xiso](../herramientas/extract-xiso.md)
