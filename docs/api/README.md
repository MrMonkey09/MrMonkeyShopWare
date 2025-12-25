# 📘 Referencia de API

Documentación técnica de todas las funciones públicas del proyecto.

---

## 📂 Módulos

| Módulo | Descripción |
|--------|-------------|
| [dumper](./dumper.md) | Volcado de discos Xbox 360 |
| [extractor](./extractor.md) | Extracción de ISOs |
| [analyser](./analyser.md) | Análisis de archivos XEX |
| [cleaner](./cleaner.md) | Limpieza de XEX |
| [toml-generator](./toml-generator.md) | Generación de TOML |
| [pipeline](./pipeline.md) | Pipeline automatizado |
| [database](./database.md) | Base de datos de juegos |
| [shader-recomp](./shader-recomp.md) | Recompilación con XenonRecomp |
| [game-profiles](./game-profiles.md) | Perfiles de configuración por juego |
| [logger](./logger.md) | Sistema de logging avanzado |

---

## 🚀 Uso Rápido

```python
from src.core import (
    dump_disc,
    extract_iso,
    list_xex_files,
    analyse_xex,
    clean_xex,
    generate_project_toml,
    validate_project_toml,
    full_pipeline,  # ⚡ Nuevo
    PipelineResult
)

# Dump
success = dump_disc("E:", out_path="./game.iso")

# Extracción
folder = extract_iso("./game.iso")
xex_files = list_xex_files(folder)

# Análisis
result = analyse_xex(xex_files[0])
json_file, toml_file = result

# Generación TOML
project_toml = generate_project_toml(xex_files[0], json_file, "./output")
```

---

## 📋 Convenciones

### Parámetros Opcionales

- `log`: Función de logging, por defecto `print`
- `gui_ref`: Referencia a objeto GUI con método `.log()`
- `out_path` / `output_dir`: Rutas de salida personalizadas

### Valores de Retorno

- **Éxito**: Ruta al archivo/carpeta generado, o `True`
- **Error**: `None` o `False`

### Manejo de Errores

```python
result = extract_iso("game.iso")
if result is None:
    print("Error en extracción")
else:
    print(f"Extraído en: {result}")
```

---

## 📚 Ver también

- [Arquitectura](../arquitectura.md)
- [Flujo de Datos](../flujo-datos.md)
- [Módulo Core](../modulos/core.md)
