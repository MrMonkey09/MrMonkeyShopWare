# core/logger.py
"""
Sistema de logging avanzado para MrMonkeyShopWare.

Características:
- Niveles: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Rotación de archivos por tamaño
- Salida a consola y archivo
- Formato consistente con timestamps
"""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional, Callable

# Nombre del logger principal
LOGGER_NAME = "MrMonkeyShopWare"

# Directorio de logs por defecto
DEFAULT_LOG_DIR = Path.home() / ".mrmonkeyshopware" / "logs"

# Formato de logs
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Colores para consola (ANSI)
COLORS = {
    "DEBUG": "\033[36m",     # Cyan
    "INFO": "\033[32m",      # Green
    "WARNING": "\033[33m",   # Yellow
    "ERROR": "\033[31m",     # Red
    "CRITICAL": "\033[35m",  # Magenta
    "RESET": "\033[0m"
}


class ColoredFormatter(logging.Formatter):
    """Formatter con colores para consola."""
    
    def __init__(self, use_colors: bool = True):
        super().__init__(LOG_FORMAT, LOG_DATE_FORMAT)
        self.use_colors = use_colors
    
    def format(self, record):
        if self.use_colors and sys.stdout.isatty():
            color = COLORS.get(record.levelname, "")
            reset = COLORS["RESET"]
            record.levelname = f"{color}{record.levelname}{reset}"
        return super().format(record)


class GUILogHandler(logging.Handler):
    """
    Handler que envía logs a una función callback de la GUI.
    
    Uso:
        handler = GUILogHandler(callback=gui.log_message)
        logger.addHandler(handler)
    """
    
    def __init__(self, callback: Callable[[str], None], level=logging.INFO):
        super().__init__(level)
        self.callback = callback
        self.setFormatter(logging.Formatter("%(message)s"))
    
    def emit(self, record):
        try:
            msg = self.format(record)
            # Añadir emoji según nivel
            level_emoji = {
                "DEBUG": "🔍",
                "INFO": "ℹ️",
                "WARNING": "⚠️",
                "ERROR": "❌",
                "CRITICAL": "💀"
            }
            emoji = level_emoji.get(record.levelname, "")
            self.callback(f"{emoji} {msg}")
        except Exception:
            self.handleError(record)


def get_logger(name: str = None) -> logging.Logger:
    """
    Obtiene un logger configurado.
    
    :param name: Nombre del módulo (usa LOGGER_NAME si es None)
    :return: Logger configurado
    
    Uso:
        logger = get_logger(__name__)
        logger.info("Mensaje")
    """
    if name:
        return logging.getLogger(f"{LOGGER_NAME}.{name}")
    return logging.getLogger(LOGGER_NAME)


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    log_dir: str = None,
    max_bytes: int = 5_000_000,  # 5MB
    backup_count: int = 3,
    console_output: bool = True,
    use_colors: bool = True
) -> logging.Logger:
    """
    Configura el sistema de logging.
    
    :param level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    :param log_file: Nombre del archivo de log (default: app.log)
    :param log_dir: Directorio de logs (default: ~/.mrmonkeyshopware/logs)
    :param max_bytes: Tamaño máximo antes de rotar (default: 5MB)
    :param backup_count: Número de archivos de backup (default: 3)
    :param console_output: Si mostrar logs en consola
    :param use_colors: Si usar colores en consola
    :return: Logger principal configurado
    
    Ejemplo:
        setup_logging(level="DEBUG", log_file="debug.log")
    """
    # Obtener nivel
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Logger principal
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(log_level)
    
    # Limpiar handlers existentes
    logger.handlers.clear()
    
    # Crear directorio de logs
    if log_dir:
        logs_path = Path(log_dir)
    else:
        logs_path = DEFAULT_LOG_DIR
    
    logs_path.mkdir(parents=True, exist_ok=True)
    
    # Handler de archivo con rotación
    log_filename = log_file or "app.log"
    file_path = logs_path / log_filename
    
    file_handler = RotatingFileHandler(
        file_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8"
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, LOG_DATE_FORMAT))
    logger.addHandler(file_handler)
    
    # Handler de consola
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(ColoredFormatter(use_colors=use_colors))
        logger.addHandler(console_handler)
    
    # Log inicial
    logger.debug(f"Logging configurado: level={level}, file={file_path}")
    
    return logger


def add_gui_handler(callback: Callable[[str], None], level: str = "INFO") -> GUILogHandler:
    """
    Añade un handler para enviar logs a la GUI.
    
    :param callback: Función que recibe mensajes de log
    :param level: Nivel mínimo de logs a enviar
    :return: Handler creado
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    handler = GUILogHandler(callback, level=log_level)
    
    logger = get_logger()
    logger.addHandler(handler)
    
    return handler


def remove_gui_handler(handler: GUILogHandler) -> None:
    """
    Remueve un handler de GUI.
    
    :param handler: Handler a remover
    """
    logger = get_logger()
    logger.removeHandler(handler)


def get_log_file_path() -> Path:
    """
    Retorna la ruta al archivo de log actual.
    
    :return: Path al archivo de log
    """
    return DEFAULT_LOG_DIR / "app.log"


def clear_logs() -> None:
    """
    Limpia todos los archivos de log.
    """
    if DEFAULT_LOG_DIR.exists():
        for log_file in DEFAULT_LOG_DIR.glob("*.log*"):
            try:
                log_file.unlink()
            except Exception:
                pass
