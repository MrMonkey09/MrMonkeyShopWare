# 🔧 Módulo Utilidades

El módulo `utils` contiene funciones auxiliares compartidas.

---

## 📁 Archivos

| Archivo | Descripción |
|---------|-------------|
| `getDrives.py` | Detección de unidades en Windows |

---

## 💾 getDrives.py

### `get_drives_with_types()`

Detecta todas las unidades disponibles y sus tipos.

**Retorna**: Diccionario `{unidad: tipo}`

```python
from src.utils import get_drives_with_types

drives = get_drives_with_types()
# {
#     'C:\\': 3,  # DRIVE_FIXED
#     'D:\\': 5,  # DRIVE_CDROM
#     'E:\\': 2,  # DRIVE_REMOVABLE
# }
```

---

## 📋 Tipos de Unidad (Windows)

| Valor | Constante | Descripción |
|-------|-----------|-------------|
| 0 | DRIVE_UNKNOWN | Tipo desconocido |
| 1 | DRIVE_NO_ROOT_DIR | Sin directorio raíz |
| 2 | DRIVE_REMOVABLE | Removible (USB, etc.) |
| 3 | DRIVE_FIXED | Disco fijo (HDD, SSD) |
| 4 | DRIVE_REMOTE | Unidad de red |
| 5 | DRIVE_CDROM | CD/DVD/Blu-ray |
| 6 | DRIVE_RAMDISK | RAM disk |

---

## 🎯 Uso Típico

### Encontrar unidades ópticas

```python
from src.utils import get_drives_with_types

DRIVE_CDROM = 5

drives = get_drives_with_types()
optical_drives = [d for d, t in drives.items() if t == DRIVE_CDROM]

print(f"Unidades ópticas: {optical_drives}")
# Unidades ópticas: ['D:\\', 'E:\\']
```

---

## ⚠️ Requisitos

Este módulo requiere `pywin32` para acceder a la API de Windows:

```bash
pip install pywin32
```

---

## 📚 Ver también

- [Requisitos del Sistema](../requisitos.md)
- [Módulo Core](./core.md)
