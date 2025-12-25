# core/virtual_disc.py
"""
Detector de discos virtuales y unidades montadas.
"""
import os
import subprocess
from typing import List, Optional
from dataclasses import dataclass


@dataclass
class VirtualDrive:
    """Información de una unidad virtual."""
    letter: str
    label: str
    drive_type: str  # "Virtual", "Removable", "Fixed", etc.
    is_virtual: bool
    source_file: Optional[str] = None


def get_all_drives_with_type() -> List[VirtualDrive]:
    """
    Obtiene todas las unidades con su tipo.
    
    :return: Lista de VirtualDrive
    """
    drives = []
    
    try:
        # Usar wmic para obtener info de unidades
        result = subprocess.run(
            ["wmic", "logicaldisk", "get", "DeviceID,DriveType,VolumeName"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # DriveType values:
        # 0 = Unknown
        # 1 = No Root Directory
        # 2 = Removable (USB, SD)
        # 3 = Fixed (HDD, SSD)
        # 4 = Network
        # 5 = CD-ROM
        # 6 = RAM Disk
        
        drive_types = {
            "0": "Desconocido",
            "1": "Sin raíz",
            "2": "Extraíble",
            "3": "Fijo",
            "4": "Red",
            "5": "CD-ROM",
            "6": "RAM Disk"
        }
        
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.strip().split()
            if len(parts) >= 2:
                letter = parts[0]
                dtype = parts[1] if len(parts) > 1 else "0"
                label = " ".join(parts[2:]) if len(parts) > 2 else ""
                
                drive = VirtualDrive(
                    letter=letter,
                    label=label,
                    drive_type=drive_types.get(dtype, "Desconocido"),
                    is_virtual=dtype == "5"  # CD-ROM puede ser virtual
                )
                drives.append(drive)
                
    except Exception as e:
        # Fallback: listar unidades básicas
        import string
        for letter in string.ascii_uppercase:
            path = f"{letter}:\\"
            if os.path.exists(path):
                drives.append(VirtualDrive(
                    letter=f"{letter}:",
                    label="",
                    drive_type="Desconocido",
                    is_virtual=False
                ))
    
    return drives


def detect_virtual_drives() -> List[VirtualDrive]:
    """
    Detecta unidades que probablemente sean virtuales (ISOs montadas).
    
    Heurísticas:
    - Tipo CD-ROM sin disco físico
    - Unidad creada por software de montaje
    """
    virtual_drives = []
    all_drives = get_all_drives_with_type()
    
    for drive in all_drives:
        # CD-ROM es probable que sea virtual si no hay DVD físico
        if drive.drive_type == "CD-ROM":
            # Verificar si tiene contenido de Xbox 360
            if _looks_like_xbox_iso(drive.letter):
                drive.is_virtual = True
                virtual_drives.append(drive)
        
        # También verificar unidades extraíbles con estructura Xbox
        elif drive.drive_type == "Extraíble":
            if _looks_like_xbox_iso(drive.letter):
                virtual_drives.append(drive)
    
    return virtual_drives


def _looks_like_xbox_iso(drive_letter: str) -> bool:
    """Verifica si una unidad parece contener un juego Xbox 360."""
    try:
        # Buscar archivos típicos de Xbox 360
        root = drive_letter + "\\"
        
        # Verificar default.xex en raíz
        if os.path.isfile(os.path.join(root, "default.xex")):
            return True
        
        # Verificar carpeta $SystemUpdate (típica de discos Xbox)
        if os.path.isdir(os.path.join(root, "$SystemUpdate")):
            return True
        
        # Buscar cualquier .xex
        for item in os.listdir(root):
            if item.lower().endswith(".xex"):
                return True
                
    except (PermissionError, OSError):
        pass
    
    return False


def find_xex_on_drive(drive_letter: str) -> Optional[str]:
    """
    Busca el XEX principal en una unidad.
    
    :param drive_letter: Letra de unidad (ej: "E:")
    :return: Ruta al XEX o None
    """
    root = drive_letter + "\\"
    
    # Buscar default.xex
    default_xex = os.path.join(root, "default.xex")
    if os.path.isfile(default_xex):
        return default_xex
    
    # Buscar cualquier .xex en raíz
    try:
        for item in os.listdir(root):
            if item.lower().endswith(".xex"):
                return os.path.join(root, item)
    except (PermissionError, OSError):
        pass
    
    return None
