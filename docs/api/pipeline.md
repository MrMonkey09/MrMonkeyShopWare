# 📦 API del Pipeline

## Visión General

El módulo `pipeline` proporciona una forma automatizada de encadenar todas las operaciones de MrMonkeyShopWare en un solo flujo.

---

## Módulo: `core.pipeline`

### Importación

```python
from core.pipeline import full_pipeline, find_main_xex, PipelineResult
```

---

## 📊 PipelineResult

Dataclass que contiene el resultado estructurado del pipeline.

```python
@dataclass
class PipelineResult:
    success: bool
    iso_path: Optional[str] = None
    extracted_dir: Optional[str] = None
    main_xex: Optional[str] = None
    analysis_json: Optional[str] = None
    analysis_toml: Optional[str] = None
    project_toml: Optional[str] = None
    error: Optional[str] = None
    steps_completed: list = field(default_factory=list)
    xex_info: Optional[XexInfo] = None  # 🆕 Metadata del juego
    game_id: Optional[int] = None       # 🆕 ID en base de datos
```

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `success` | `bool` | `True` si el pipeline completó sin errores |
| `iso_path` | `str` | Ruta al ISO generado (solo modo disco) |
| `extracted_dir` | `str` | Directorio con contenido extraído |
| `main_xex` | `str` | Ruta al XEX principal |
| `analysis_json` | `str` | Ruta al JSON de análisis |
| `analysis_toml` | `str` | Ruta al TOML de análisis |
| `project_toml` | `str` | Ruta al project.toml generado |
| `error` | `str` | Mensaje de error (si falló) |
| `steps_completed` | `list` | Pasos completados |
| `xex_info` | `XexInfo` | 🆕 Metadata extraída del juego |
| `game_id` | `int` | 🆕 ID del juego guardado en BD |

> [!NOTE]
> El pipeline ahora auto-guarda el juego en la base de datos con estado `ANALYSED`.
> Ver sección "Paso 5" abajo.

---

## 🔧 full_pipeline()

Ejecuta el pipeline completo encadenando todos los pasos.

```python
def full_pipeline(
    drive_letter: str = None,
    iso_path: str = None,
    xex_path: str = None,
    output_dir: str = None,
    log: Callable[[str], None] = None
) -> PipelineResult
```

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `drive_letter` | `str` | Letra de unidad (ej: `"E:"`). Inicia desde dump. |
| `iso_path` | `str` | Ruta a ISO existente. Inicia desde extracción. |
| `xex_path` | `str` | Ruta a XEX existente. Inicia desde análisis. |
| `output_dir` | `str` | Directorio de salida (opcional). |
| `log` | `Callable` | Función de logging (opcional). |

> [!NOTE]
> Los parámetros `drive_letter`, `iso_path` y `xex_path` son mutuamente excluyentes.
> Se procesa en orden de prioridad: drive > iso > xex.

### Ejemplos

**Desde disco físico:**
```python
result = full_pipeline(drive_letter="E:")
if result.success:
    print(f"Project TOML: {result.project_toml}")
```

**Desde ISO:**
```python
result = full_pipeline(iso_path="C:/games/mygame.iso")
```

**Desde XEX:**
```python
result = full_pipeline(
    xex_path="C:/extracted/default.xex",
    output_dir="C:/output"
)
```

**Con logging personalizado:**
```python
import logging
log = logging.getLogger("pipeline")

result = full_pipeline(
    xex_path="default.xex",
    log=log.info
)
```

---

## 🔍 find_main_xex()

Busca el ejecutable principal en un directorio extraído.

```python
def find_main_xex(extracted_dir: str) -> Optional[str]
```

### Parámetros

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `extracted_dir` | `str` | Directorio con contenido extraído del ISO |

### Retorno

- Ruta absoluta al XEX principal si se encuentra
- `None` si no hay archivos `.xex`

### Lógica de prioridad

1. Busca `default.xex` (nombre estándar de ejecutable principal)
2. Si no existe, retorna el primer `.xex` encontrado

### Ejemplo

```python
from core.pipeline import find_main_xex

xex = find_main_xex("C:/extracted/mygame")
if xex:
    print(f"XEX principal: {xex}")
else:
    print("No se encontraron archivos XEX")
```

---

## 🖥️ CLI

El pipeline está disponible como comando CLI:

```bash
# Desde disco
python -m src.cli.pipeline -d E:

# Desde ISO
python -m src.cli.pipeline -i game.iso -o ./output

# Desde XEX
python -m src.cli.pipeline -x default.xex
```

### Argumentos

| Argumento | Descripción |
|-----------|-------------|
| `-d`, `--drive` | Letra de unidad óptica |
| `-i`, `--iso` | Ruta a archivo ISO |
| `-x`, `--xex` | Ruta a archivo XEX |
| `-o`, `--output` | Directorio de salida |

---

## Véase También

- [dumper.md](./dumper.md) - API de volcado
- [extractor.md](./extractor.md) - API de extracción
- [analyser.md](./analyser.md) - API de análisis
- [toml-generator.md](./toml-generator.md) - API de TOML
