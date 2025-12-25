# 🔍 API: Analyser

Módulo para análisis de archivos XEX con extracción automática de metadata.

**Ubicación**: `src/core/analyser.py`

---

## AnalysisResult (Dataclass)

```python
@dataclass
class AnalysisResult:
    json_file: Optional[str] = None      # Ruta al analysis.json
    toml_file: Optional[str] = None      # Ruta al analysis.toml
    xex_info: Optional[XexInfo] = None   # 🆕 Metadata del juego
    xextool_output: str = ""             # Salida cruda de XexTool
    success: bool = False
```

---

## analyse_xex

```python
def analyse_xex(
    xex_path: str,
    out_dir: str = None,
    log: callable = None
) -> Optional[AnalysisResult]
```

Analiza un archivo XEX con XenonAnalyse y extrae metadata con XexTool.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `xex_path` | `str` | Ruta al archivo XEX |
| `out_dir` | `str` | Opcional. Directorio de salida |
| `log` | `callable` | Opcional. Función de logging |

### Retorna

- `AnalysisResult`: Objeto con archivos generados y metadata del juego
- `None`: Error durante el análisis

### Ejemplo

```python
from core.analyser import analyse_xex

result = analyse_xex("./default.xex", log=print)

if result and result.success:
    # Archivos generados
    print(f"JSON: {result.json_file}")
    print(f"TOML: {result.toml_file}")
    
    # 🆕 Metadata del juego
    if result.xex_info:
        print(f"Juego: {result.xex_info.display_name}")
        print(f"Title ID: {result.xex_info.title_id}")
        print(f"Versión: {result.xex_info.version}")
```

---

## XexInfo (Dataclass)

Metadata extraída de XexTool. Ver [xex-parser.md](./xex-parser.md) para detalles.

```python
@dataclass
class XexInfo:
    title_id: str               # Ej: "4E4D07F5"
    original_pe_name: str       # Ej: "Dead To Rights.exe"
    display_name: str           # Nombre limpio del juego
    version: str                # Ej: "v0.0.0.1"
    media_id: str
    disc_number: int
    total_discs: int
    regions: str                # Ej: "All Regions"
    esrb_rating: str            # Ej: "ESRB_M"
    entry_point: str
    # ... más campos
```

---

## Proceso interno

1. **Info**: Ejecuta `xextool -l` y parsea metadata
2. **Limpieza**: Si el XEX está encriptado/comprimido, se limpia
3. **Análisis**: Ejecuta XenonAnalyse → `analysis.toml`
4. **Conversión**: Convierte TOML a JSON → `analysis.json`

---

## Archivos generados

| Archivo | Descripción |
|---------|-------------|
| `analysis.toml` | Salida directa de XenonAnalyse |
| `analysis.json` | Versión JSON para procesamiento |
| `*_clean.xex` | XEX limpio (si fue necesario) |

---

## 📚 Ver también

- [API XexParser](./xex-parser.md)
- [API Cleaner](./cleaner.md)
- [Guía de Análisis](../tutoriales/guia-analisis.md)

