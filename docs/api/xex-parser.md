# 🔧 API: XexParser

Módulo para parsear la salida de XexTool y extraer metadata de juegos Xbox 360.

**Ubicación**: `src/core/xex_parser.py`

---

## Importación

```python
from core.xex_parser import parse_xextool_output, XexInfo
```

---

## 📊 XexInfo (Dataclass)

Contiene toda la metadata extraída de un archivo XEX.

```python
@dataclass
class XexInfo:
    title_id: str = ""          # Ej: "4E4D07F5"
    original_pe_name: str = ""  # Ej: "Dead To Rights.exe"
    display_name: str = ""      # Nombre limpio del juego
    media_id: str = ""
    version: str = ""           # Ej: "v0.0.0.1"
    base_version: str = ""
    disc_number: int = 1
    total_discs: int = 1
    regions: str = ""           # Ej: "All Regions"
    esrb_rating: str = ""       # Ej: "ESRB_M"
    entry_point: str = ""       # Dirección de entrada
    load_address: str = ""
    xex_flags: str = ""
    static_libraries: list = field(default_factory=list)
    is_retail: bool = True
    is_encrypted: bool = False
```

---

## 🔍 parse_xextool_output()

```python
def parse_xextool_output(output: str) -> XexInfo
```

Parsea la salida de `xextool -l` y extrae metadata.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `output` | `str` | Salida de texto de `xextool -l archivo.xex` |

### Retorna

- `XexInfo`: Objeto con toda la metadata extraída

### Ejemplo

```python
from core.xex_parser import parse_xextool_output
import subprocess

# Obtener salida de XexTool
proc = subprocess.run(
    ["xextool.exe", "-l", "default.xex"],
    capture_output=True, text=True
)

# Parsear
info = parse_xextool_output(proc.stdout)

print(f"Juego: {info.display_name}")
print(f"Title ID: {info.title_id}")
print(f"Versión: {info.version}")
print(f"Regiones: {info.regions}")
print(f"Rating: {info.esrb_rating}")
```

---

## 📋 Campos Extraídos

| Campo | Fuente en XexTool | Ejemplo |
|-------|-------------------|---------|
| `title_id` | `Title ID:` | `"4E4D07F5"` |
| `original_pe_name` | `Original PE Name:` | `"Dead To Rights.exe"` |
| `display_name` | Derivado de PE Name | `"Dead To Rights"` |
| `media_id` | `Media ID:` | `"12345678"` |
| `version` | `Version:` | `"v0.0.0.1"` |
| `disc_number` | `Disc Number:` | `1` |
| `total_discs` | `Disc Count:` | `1` |
| `regions` | `Allowed Regions:` | `"All Regions"` |
| `esrb_rating` | `Rating Value:` | `"ESRB_M"` |
| `entry_point` | `Entry Point:` | `"0x82000000"` |
| `static_libraries` | `Static Libraries:` | `["xapilib", "d3d9"]` |

---

## 🧹 Limpieza de Nombre

El `display_name` se genera automáticamente limpiando el `original_pe_name`:

- Elimina extensión `.exe`
- Reemplaza guiones bajos con espacios
- Limpia caracteres especiales

```python
# Entrada:  "Dead_To_Rights.exe"
# Salida:   "Dead To Rights"
```

---

## 📚 Ver también

- [API Analyser](./analyser.md) - Usa XexParser internamente
- [API Database](./database.md) - Almacena XexInfo en la BD
