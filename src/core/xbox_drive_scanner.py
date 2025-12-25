# core/xbox_drive_scanner.py
"""
Escáner de discos USB con estructura Xbox 360.
Detecta juegos instalados en formato Xbox 360.
"""
import os
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class XboxGameInfo:
    """Información de un juego Xbox 360 en USB."""
    title_id: str
    folder_name: str
    folder_path: str
    xex_path: Optional[str] = None
    display_name: str = ""


def is_xbox_usb(drive_or_folder: str) -> bool:
    """
    Detecta si un disco/carpeta tiene estructura Xbox 360.
    
    Estructura típica:
        Content/
        └── 0000000000000000/
            └── [Title ID]/
    
    :param drive_or_folder: Letra de unidad (ej: "E:") o ruta a carpeta
    :return: True si tiene estructura Xbox 360
    """
    content_path = os.path.join(drive_or_folder, "Content")
    if os.path.isdir(content_path):
        return True
    
    # También verificar si es la carpeta Content directamente
    if os.path.basename(drive_or_folder).lower() == "content":
        return True
    
    # Verificar estructura de juego extraído (carpeta con default.xex)
    games_path = os.path.join(drive_or_folder, "Games")
    if os.path.isdir(games_path):
        return True
    
    return False


def list_games_on_drive(drive_or_folder: str) -> List[XboxGameInfo]:
    """
    Lista todos los juegos en un disco USB Xbox 360.
    
    :param drive_or_folder: Ruta al disco o carpeta
    :return: Lista de juegos encontrados
    """
    games = []
    
    # Buscar en Content/0000000000000000/
    content_path = os.path.join(drive_or_folder, "Content")
    if os.path.isdir(content_path):
        games.extend(_scan_content_folder(content_path))
    
    # Buscar en Games/ (estructura alternativa)
    games_path = os.path.join(drive_or_folder, "Games")
    if os.path.isdir(games_path):
        games.extend(_scan_games_folder(games_path))
    
    # Buscar en raíz (juegos extraídos directamente)
    root_games = _scan_root_folder(drive_or_folder)
    games.extend(root_games)
    
    return games


def _scan_content_folder(content_path: str) -> List[XboxGameInfo]:
    """Escanea estructura Content/"""
    games = []
    
    # Buscar carpetas de perfil (0000000000000000, etc.)
    for profile in os.listdir(content_path):
        profile_path = os.path.join(content_path, profile)
        if not os.path.isdir(profile_path):
            continue
        
        # Buscar title IDs
        for title_id in os.listdir(profile_path):
            title_path = os.path.join(profile_path, title_id)
            if not os.path.isdir(title_path):
                continue
            
            # Buscar XEX en subcarpetas
            xex = _find_xex_recursive(title_path, max_depth=3)
            
            game = XboxGameInfo(
                title_id=title_id.upper(),
                folder_name=title_id,
                folder_path=title_path,
                xex_path=xex,
                display_name=_derive_name_from_path(title_path) or title_id
            )
            games.append(game)
    
    return games


def _scan_games_folder(games_path: str) -> List[XboxGameInfo]:
    """Escanea estructura Games/"""
    games = []
    
    for folder in os.listdir(games_path):
        folder_path = os.path.join(games_path, folder)
        if not os.path.isdir(folder_path):
            continue
        
        # Buscar XEX
        xex = _find_xex_recursive(folder_path, max_depth=2)
        
        # Extraer title ID del nombre si está entre corchetes
        title_id = _extract_title_id(folder)
        
        game = XboxGameInfo(
            title_id=title_id or "UNKNOWN",
            folder_name=folder,
            folder_path=folder_path,
            xex_path=xex,
            display_name=_clean_folder_name(folder)
        )
        games.append(game)
    
    return games


def _scan_root_folder(root_path: str) -> List[XboxGameInfo]:
    """Escanea juegos en la raíz."""
    games = []
    
    for folder in os.listdir(root_path):
        folder_path = os.path.join(root_path, folder)
        
        # Ignorar carpetas especiales
        if folder.lower() in ["content", "games", "cache", "$recycle.bin", "system volume information"]:
            continue
        
        if not os.path.isdir(folder_path):
            continue
        
        # Ver si tiene XEX directamente
        xex = _find_xex_recursive(folder_path, max_depth=1)
        if xex:
            title_id = _extract_title_id(folder)
            game = XboxGameInfo(
                title_id=title_id or "UNKNOWN",
                folder_name=folder,
                folder_path=folder_path,
                xex_path=xex,
                display_name=_clean_folder_name(folder)
            )
            games.append(game)
    
    return games


def _find_xex_recursive(folder: str, max_depth: int = 2) -> Optional[str]:
    """Busca XEX en una carpeta recursivamente."""
    if max_depth < 0:
        return None
    
    # Primero buscar default.xex
    default_xex = os.path.join(folder, "default.xex")
    if os.path.isfile(default_xex):
        return default_xex
    
    # Buscar cualquier .xex en este nivel
    try:
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            if item.lower().endswith(".xex") and os.path.isfile(item_path):
                return item_path
    except PermissionError:
        return None
    
    # Buscar en subcarpetas
    if max_depth > 0:
        try:
            for item in os.listdir(folder):
                item_path = os.path.join(folder, item)
                if os.path.isdir(item_path):
                    result = _find_xex_recursive(item_path, max_depth - 1)
                    if result:
                        return result
        except PermissionError:
            pass
    
    return None


def _extract_title_id(folder_name: str) -> Optional[str]:
    """Extrae Title ID de un nombre de carpeta."""
    import re
    
    # Buscar patrón [XXXXXXXX] o (XXXXXXXX)
    match = re.search(r'[\[\(]([A-Fa-f0-9]{8})[\]\)]', folder_name)
    if match:
        return match.group(1).upper()
    
    # Verificar si el nombre es directamente un Title ID
    if re.match(r'^[A-Fa-f0-9]{8}$', folder_name):
        return folder_name.upper()
    
    return None


def _clean_folder_name(folder_name: str) -> str:
    """Limpia un nombre de carpeta para mostrar."""
    import re
    
    # Remover Title ID entre corchetes
    name = re.sub(r'\s*[\[\(][A-Fa-f0-9]{8}[\]\)]\s*', '', folder_name)
    
    # Reemplazar guiones bajos
    name = name.replace('_', ' ')
    
    return name.strip() or folder_name


def _derive_name_from_path(path: str) -> Optional[str]:
    """Intenta derivar un nombre del path."""
    # Buscar archivo con nombre descriptivo
    for item in os.listdir(path):
        if item.lower().endswith(('.xex', '.xexp')):
            name = os.path.splitext(item)[0]
            if name.lower() != 'default':
                return name.replace('_', ' ')
    
    return None
