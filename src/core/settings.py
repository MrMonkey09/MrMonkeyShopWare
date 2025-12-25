# core/settings.py
"""
Sistema de persistencia de configuración.
"""
import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


def _get_settings_path() -> Path:
    """Retorna la ruta al archivo de configuración."""
    settings_dir = Path.home() / ".mrmonkeyshopware"
    settings_dir.mkdir(parents=True, exist_ok=True)
    return settings_dir / "settings.json"


def load_settings() -> Dict[str, Any]:
    """
    Carga la configuración desde el archivo.
    
    :return: Diccionario con la configuración
    """
    settings_path = _get_settings_path()
    
    if not settings_path.exists():
        return get_default_settings()
    
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return get_default_settings()


def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Guarda la configuración en el archivo.
    
    :param settings: Diccionario con la configuración
    :return: True si se guardó correctamente
    """
    settings_path = _get_settings_path()
    
    try:
        with open(settings_path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def get_default_settings() -> Dict[str, Any]:
    """Retorna la configuración por defecto."""
    return {
        "tools": {
            "XENON_ANALYSE_PATH": "",
            "XENON_RECOMP_PATH": "",
            "XEXTOOL_PATH": "",
            "EXTRACT_XISO_PATH": "",
            "DISC_IMAGE_CREATOR_PATH": "",
            "PPC_CONTEXT_PATH": ""
        },
        "appearance": {
            "theme": "Dark",
            "window_size": "1100x750",
            "ui_scale": 1.0
        },
        "database": {
            "path": str(Path.home() / ".mrmonkeyshopware" / "games.db")
        },
        "logging": {
            "level": "INFO",
            "log_dir": str(Path.home() / ".mrmonkeyshopware" / "logs"),
            "max_size_mb": 5
        }
    }


def get_setting(key: str, default: Any = None) -> Any:
    """
    Obtiene un valor de configuración.
    
    :param key: Clave en formato "section.key" (ej: "tools.XENON_ANALYSE_PATH")
    :param default: Valor por defecto si no existe
    :return: Valor de la configuración
    """
    settings = load_settings()
    
    parts = key.split(".")
    value = settings
    
    for part in parts:
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return default
    
    return value


def set_setting(key: str, value: Any) -> bool:
    """
    Establece un valor de configuración.
    
    :param key: Clave en formato "section.key"
    :param value: Valor a guardar
    :return: True si se guardó correctamente
    """
    settings = load_settings()
    
    parts = key.split(".")
    current = settings
    
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    current[parts[-1]] = value
    
    return save_settings(settings)


def apply_tool_settings():
    """
    Aplica las rutas de herramientas a las variables de entorno.
    Esto hace que core/config.py las use.
    """
    settings = load_settings()
    tools = settings.get("tools", {})
    
    for key, value in tools.items():
        if value:  # Solo si tiene valor
            os.environ[key] = value
