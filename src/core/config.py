# core/config.py
"""
Configuración de rutas a herramientas externas.

Prioridad de lectura:
1. settings.json (configuración de GUI)
2. Variables de entorno
3. Valores por defecto
"""
import os
from pathlib import Path
import json


def _load_settings_value(key: str, default: str) -> str:
    """
    Carga un valor de configuración con la siguiente prioridad:
    1. settings.json
    2. Variable de entorno
    3. Valor por defecto
    """
    # 1. Intentar leer de settings.json
    settings_path = Path.home() / ".mrmonkeyshopware" / "settings.json"
    if settings_path.exists():
        try:
            with open(settings_path, "r", encoding="utf-8") as f:
                settings = json.load(f)
                tools = settings.get("tools", {})
                if key in tools and tools[key]:
                    return tools[key]
        except (json.JSONDecodeError, IOError):
            pass
    
    # 2. Intentar variable de entorno
    env_value = os.environ.get(key)
    if env_value:
        return env_value
    
    # 3. Valor por defecto
    return default


# Rutas de herramientas
XENON_ANALYSE_PATH = _load_settings_value(
    "XENON_ANALYSE_PATH",
    r"C:\tools\XenonRecompUnlimited\XenonAnalyse.exe"
)

XEXTOOL_PATH = _load_settings_value(
    "XEXTOOL_PATH",
    r"C:\tools\XexTool\xextool.exe"
)

EXTRACT_XISO_PATH = _load_settings_value(
    "EXTRACT_XISO_PATH",
    r"C:\tools\extract-xiso\extract-xiso.exe"
)

DISC_IMAGE_CREATOR_PATH = _load_settings_value(
    "DISC_IMAGE_CREATOR_PATH",
    r"C:\tools\DiscImageCreator\DiscImageCreator.exe"
)

XENON_RECOMP_PATH = _load_settings_value(
    "XENON_RECOMP_PATH",
    r"C:\tools\XenonRecompUnlimited\build\XenonRecomp\Debug\XenonRecomp.exe"
)

XENOS_RECOMP_PATH = _load_settings_value(
    "XENOS_RECOMP_PATH",
    r"C:\tools\XenosRecomp\build\XenosRecomp.exe"
)

PPC_CONTEXT_PATH = _load_settings_value(
    "PPC_CONTEXT_PATH",
    r"C:\tools\XenonRecomp\XenonUtils\ppc_context.h"
)

SHADER_COMMON_PATH = _load_settings_value(
    "SHADER_COMMON_PATH",
    r"C:\tools\XenosRecomp\shader_common.h"
)

# Carpeta base para temporales del proyecto
TEMP_BASE = os.environ.get(
    "X360_TEMP_BASE",
    os.path.join(os.environ.get("TEMP", "/tmp"), "x360dump")
)


def reload_config():
    """
    Recarga la configuración desde settings.json.
    Útil después de guardar nuevas configuraciones en la GUI.
    """
    global XENON_ANALYSE_PATH, XEXTOOL_PATH, EXTRACT_XISO_PATH
    global DISC_IMAGE_CREATOR_PATH, XENON_RECOMP_PATH, PPC_CONTEXT_PATH
    global XENOS_RECOMP_PATH, SHADER_COMMON_PATH
    
    XENON_ANALYSE_PATH = _load_settings_value(
        "XENON_ANALYSE_PATH",
        r"C:\tools\XenonRecompUnlimited\XenonAnalyse.exe"
    )
    XEXTOOL_PATH = _load_settings_value(
        "XEXTOOL_PATH",
        r"C:\tools\XexTool\xextool.exe"
    )
    EXTRACT_XISO_PATH = _load_settings_value(
        "EXTRACT_XISO_PATH",
        r"C:\tools\extract-xiso\extract-xiso.exe"
    )
    DISC_IMAGE_CREATOR_PATH = _load_settings_value(
        "DISC_IMAGE_CREATOR_PATH",
        r"C:\tools\DiscImageCreator\DiscImageCreator.exe"
    )
    XENON_RECOMP_PATH = _load_settings_value(
        "XENON_RECOMP_PATH",
        r"C:\tools\XenonRecompUnlimited\build\XenonRecomp\Debug\XenonRecomp.exe"
    )
    XENOS_RECOMP_PATH = _load_settings_value(
        "XENOS_RECOMP_PATH",
        r"C:\tools\XenosRecomp\build\XenosRecomp.exe"
    )
    PPC_CONTEXT_PATH = _load_settings_value(
        "PPC_CONTEXT_PATH",
        r"C:\tools\XenonRecomp\XenonUtils\ppc_context.h"
    )
    SHADER_COMMON_PATH = _load_settings_value(
        "SHADER_COMMON_PATH",
        r"C:\tools\XenosRecomp\shader_common.h"
    )

