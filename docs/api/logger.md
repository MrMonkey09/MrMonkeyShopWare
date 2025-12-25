# 📜 API de Logging

## Visión General

Sistema de logging profesional con niveles, rotación y soporte GUI.

---

## Importación

```python
from core.logger import get_logger, setup_logging
```

---

## 🔧 Funciones

### setup_logging()

Configura el sistema de logging.

```python
setup_logging(
    level="DEBUG",        # DEBUG, INFO, WARNING, ERROR
    log_file="app.log",   # Nombre del archivo
    max_bytes=5_000_000,  # 5MB antes de rotar
    backup_count=3        # Archivos de backup
)
```

---

### get_logger()

Obtiene un logger configurado.

```python
logger = get_logger(__name__)
logger.info("Operación completada")
logger.warning("Algo inesperado")
logger.error("Algo falló")
```

---

### add_gui_handler()

Envía logs a la GUI.

```python
handler = add_gui_handler(my_gui.log_callback)
```

---

## 📊 Niveles

| Nivel | Emoji | Uso |
|-------|-------|-----|
| DEBUG | 🔍 | Desarrollo |
| INFO | ℹ️ | Normal |
| WARNING | ⚠️ | Inesperado |
| ERROR | ❌ | Fallos |
| CRITICAL | 💀 | Fatal |

---

## 📁 Ubicación

```
~/.mrmonkeyshopware/logs/
├── app.log       # Actual
├── app.log.1     # Backup 1
└── app.log.2     # Backup 2
```
