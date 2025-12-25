# 🔧 API de Recompilación de Shaders

## Visión General

El módulo `shader_recomp` proporciona funciones para ejecutar XenonRecomp y recompilar ejecutables Xbox 360.

---

## Importación

```python
from core.shader_recomp import run_recompilation, RecompResult, validate_recomp_output
```

---

## 📊 RecompResult (Dataclass)

Resultado de la recompilación:

```python
@dataclass
class RecompResult:
    success: bool
    output_dir: Optional[str] = None
    cpp_files: List[str] = []
    header_files: List[str] = []
    error: Optional[str] = None
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""
```

---

## 🔧 Funciones

### run_recompilation()

Ejecuta XenonRecomp para recompilar un XEX.

```python
result = run_recompilation(
    toml_path="path/to/project.toml",
    output_dir="./output",  # opcional
    log=print,  # opcional
    timeout=300  # opcional, 5 min default
)

if result.success:
    print(f"Archivos C++: {len(result.cpp_files)}")
```

---

### validate_recomp_output()

Valida que la recompilación generó archivos.

```python
success, files = validate_recomp_output("./output")
```

---

### check_xenon_recomp_available()

Verifica si XenonRecomp está instalado.

```python
if check_xenon_recomp_available():
    print("XenonRecomp disponible")
```

---

## 🖥️ CLI

```bash
# Recompilar desde TOML
python -m cli.recomp toml -t path/to/project.toml

# Recompilar desde XEX (pipeline completo)
python -m cli.recomp xex -x path/to/game.xex -o ./output

# Ver versión de XenonRecomp
python -m cli.recomp version

# Validar output
python -m cli.recomp validate -d ./output
```

---

## ⚠️ Dependencias

> [!IMPORTANT]
> Requiere `XenonRecomp.exe` instalado en el sistema.
> Configura la ruta en `core/config.py` o via variable de entorno `XENON_RECOMP_PATH`.

---

## Véase También

- [pipeline.md](./pipeline.md)
- [toml-generator.md](./toml-generator.md)
