# 📀 API: Dumper

Módulo para volcado de discos Xbox 360.

**Ubicación**: `src/core/dumper.py`

---

## dump_disc

```python
def dump_disc(
    drive_letter: str,
    gui_ref: object = None,
    out_path: str = None
) -> bool
```

Hace dump de un disco Xbox 360 usando DiscImageCreator.

### Parámetros

| Nombre | Tipo | Descripción |
|--------|------|-------------|
| `drive_letter` | `str` | Letra de unidad óptica (ej: `"E:"` o `"E:\\"`) |
| `gui_ref` | `object` | Opcional. Objeto con método `.log()` para logging |
| `out_path` | `str` | Opcional. Ruta de salida para el ISO |

### Retorna

- `True`: Dump completado exitosamente
- `False`: Error durante el dump

### Ejemplo

```python
from src.core import dump_disc

# Uso básico
success = dump_disc("E:")

# Con ruta personalizada
success = dump_disc("E:", out_path="./mi_juego.iso")

# Con logging personalizado
class MiLogger:
    def log(self, msg):
        print(f"[LOG] {msg}")

logger = MiLogger()
success = dump_disc("E:", gui_ref=logger)
```

### Ruta por defecto

Si no se especifica `out_path`, el ISO se guarda en:
```
%TEMP%/x360dump/game.iso
```

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| "No se encontró DiscImageCreator" | Herramienta no instalada | Configurar ruta en config.py |
| "Error en dump (rc=X)" | Fallo de DiscImageCreator | Verificar disco y unidad |

### Dependencias

- `DiscImageCreator.exe` (configurado en `config.py`)

---

## 📚 Ver también

- [Guía de Dump](../tutoriales/guia-dump.md)
- [DiscImageCreator](../herramientas/disc-image-creator.md)
