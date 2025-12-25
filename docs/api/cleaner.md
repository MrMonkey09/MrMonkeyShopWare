# 🧹 API: Cleaner

Módulo para limpieza (desencriptar/descomprimir) de archivos XEX.

**Ubicación**: `src/core/cleaner_xex.py`

---

## clean_xex

```python
def clean_xex(
    xex_path: str,
    output_dir: str,
    log: callable = None
) -> str
```

Limpia un XEX (desencripta y/o descomprime) si es necesario.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `xex_path` | `str` | Ruta al archivo XEX original |
| `output_dir` | `str` | Directorio donde guardar el XEX limpio |
| `log` | `callable` | Opcional. Función de logging |

### Retorna

- `str`: Ruta al XEX limpio (o al original si no necesitó limpieza)

### Ejemplo

```python
from src.core.cleaner_xex import clean_xex

clean_path = clean_xex(
    "./default.xex",
    "./output",
    log=print
)
# Si necesitó limpieza: "./output/default_clean.xex"
# Si no: "./default.xex"
```

---

## check_xex_info

```python
def check_xex_info(
    xex_path: str,
    log: callable = None
) -> str
```

Obtiene información de un archivo XEX usando xextool.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `xex_path` | `str` | Ruta al archivo XEX |
| `log` | `callable` | Opcional. Función de logging |

### Retorna

- `str`: Información del XEX (stdout + stderr de xextool)

### Ejemplo

```python
from src.core.cleaner_xex import check_xex_info

info = check_xex_info("./default.xex")
print(info)
# XEX Info:
#   Encrypted: Yes
#   Compressed: Yes
#   ...
```

---

## Operaciones de xextool

| Operación | Flag | Descripción |
|-----------|------|-------------|
| Listar info | `-l` | Muestra información del XEX |
| Desencriptar | `-e d` | Decrypt |
| Descomprimir | `-c u` | Uncompress |

---

## Detección automática

`clean_xex` detecta automáticamente qué operaciones necesita:

```python
info = check_xex_info(xex_path)
needs_decrypt = "encrypted" in info.lower()
needs_uncompress = "compressed" in info.lower()
```

---

## 📚 Ver también

- [API Analyser](./analyser.md)
- [xextool](../herramientas/xextool.md)
