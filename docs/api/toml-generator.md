# 📝 API: TOML Generator

Módulo para generación de archivos project.toml para XenonRecomp.

**Ubicación**: `src/core/toml_generator.py`

---

## generate_project_toml

```python
def generate_project_toml(
    xex_path: str,
    analysis_json: str,
    output_dir: str
) -> str
```

Genera un project.toml con estructura válida para XenonRecomp.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `xex_path` | `str` | Ruta al archivo XEX |
| `analysis_json` | `str` | Ruta al analysis.json |
| `output_dir` | `str` | Directorio de salida |

### Retorna

- `str`: Ruta al project.toml generado

### Ejemplo

```python
from src.core import generate_project_toml

toml_path = generate_project_toml(
    "./default.xex",
    "./analysis.json",
    "./output"
)
print(f"TOML generado: {toml_path}")
```

---

## validate_project_toml

```python
def validate_project_toml(
    toml_path: str,
    log: callable = None
) -> bool
```

Valida un project.toml ejecutando XenonRecomp.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `toml_path` | `str` | Ruta al project.toml |
| `log` | `callable` | Opcional. Función de logging |

### Retorna

- `True`: TOML válido
- `False`: TOML inválido o XenonRecomp falló

### Ejemplo

```python
from src.core import validate_project_toml

is_valid = validate_project_toml("./output/project.toml", log=print)

if is_valid:
    print("✅ TOML válido")
else:
    print("❌ TOML inválido")
```

---

## Estructura del TOML generado

```toml
[project]
title_id = "00000000"
game_name = "default"

[input]
xex_path = "C:/path/to/default.xex"
analysis_json = "C:/path/to/analysis.json"

[output]
target_dir = "build/"
```

---

## Códigos de error especiales

| Código | Significado |
|--------|-------------|
| 0 | Éxito |
| 3221226505 | XenonRecomp crasheó (problema de CWD o TOML) |

---

## 📚 Ver también

- [XenonRecomp](../herramientas/xenon-recomp.md)
- [Guía de Recompilación](../tutoriales/guia-recompilacion.md)
