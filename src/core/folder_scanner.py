# core/folder_scanner.py
"""
Escáner de carpetas para encontrar archivos XEX.
"""
import os
from typing import Optional, List


def find_xex_in_folder(folder_path: str) -> Optional[str]:
    """
    Busca el XEX principal en una carpeta de juego.
    
    Prioridad:
    1. default.xex en raíz
    2. Cualquier .xex en raíz
    3. default.xex en subcarpetas (1 nivel)
    4. Cualquier .xex en subcarpetas (1 nivel)
    
    :param folder_path: Ruta a la carpeta del juego
    :return: Ruta al XEX encontrado o None
    """
    if not os.path.isdir(folder_path):
        return None
    
    # 1. Buscar default.xex en raíz
    default_xex = os.path.join(folder_path, "default.xex")
    if os.path.isfile(default_xex):
        return default_xex
    
    # 2. Buscar cualquier .xex en raíz
    for item in os.listdir(folder_path):
        if item.lower().endswith(".xex"):
            return os.path.join(folder_path, item)
    
    # 3. Buscar en subcarpetas (1 nivel)
    for subdir in os.listdir(folder_path):
        subdir_path = os.path.join(folder_path, subdir)
        if os.path.isdir(subdir_path):
            # Buscar default.xex
            default_xex = os.path.join(subdir_path, "default.xex")
            if os.path.isfile(default_xex):
                return default_xex
            
            # Buscar cualquier .xex
            for item in os.listdir(subdir_path):
                if item.lower().endswith(".xex"):
                    return os.path.join(subdir_path, item)
    
    return None


def list_xex_in_folder(folder_path: str, recursive: bool = False) -> List[str]:
    """
    Lista todos los archivos XEX en una carpeta.
    
    :param folder_path: Ruta a la carpeta
    :param recursive: Si True, busca recursivamente
    :return: Lista de rutas a archivos XEX
    """
    xex_files = []
    
    if not os.path.isdir(folder_path):
        return xex_files
    
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(".xex"):
                    xex_files.append(os.path.join(root, file))
    else:
        for item in os.listdir(folder_path):
            if item.lower().endswith(".xex"):
                xex_files.append(os.path.join(folder_path, item))
    
    return xex_files


def get_drive_letters() -> List[str]:
    """
    Obtiene las letras de unidades disponibles en Windows.
    
    :return: Lista de letras de unidad (ej: ["C:", "D:", "E:"])
    """
    import string
    drives = []
    
    for letter in string.ascii_uppercase:
        drive = f"{letter}:"
        if os.path.exists(drive):
            drives.append(drive)
    
    return drives


def get_optical_drives() -> List[str]:
    """
    Intenta detectar unidades ópticas.
    
    :return: Lista de letras de unidades ópticas
    """
    import subprocess
    
    try:
        # Usar wmic para detectar unidades CD/DVD
        result = subprocess.run(
            ["wmic", "cdrom", "get", "drive"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        drives = []
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if line and line != "Drive" and ":" in line:
                drives.append(line)
        
        return drives
    except Exception:
        # Fallback: retornar unidades comunes
        return ["D:", "E:", "F:"]
