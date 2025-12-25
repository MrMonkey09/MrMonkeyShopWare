# core/xex_parser.py
"""
Parser para extraer metadata de la salida de XexTool.
"""
import re
from dataclasses import dataclass, field
from typing import Optional, Dict, List


@dataclass
class XexInfo:
    """Información extraída de un archivo XEX."""
    # Información básica
    original_pe_name: str = ""
    title_id: str = ""
    media_id: str = ""
    
    # Versión
    version: str = ""
    base_version: str = ""
    
    # Disco
    disc_number: int = 1
    total_discs: int = 1
    
    # Región y clasificación
    regions: str = ""
    esrb_rating: str = ""
    pegi_rating: str = ""
    
    # Información técnica
    load_address: str = ""
    entry_point: str = ""
    image_size: str = ""
    
    # Tipo de ejecutable
    is_retail: bool = True
    is_encrypted: bool = True
    is_compressed: bool = False
    
    # Librerías estáticas
    static_libraries: List[str] = field(default_factory=list)
    
    # Metadata adicional (JSON)
    raw_data: Dict = field(default_factory=dict)
    
    @property
    def display_name(self) -> str:
        """Retorna un nombre legible para mostrar."""
        if self.original_pe_name:
            # Limpiar nombre: "DeadToRights_xenon.exe" -> "Dead To Rights"
            name = self.original_pe_name
            name = re.sub(r'_xenon\.exe$', '', name, flags=re.IGNORECASE)
            name = re.sub(r'\.exe$', '', name, flags=re.IGNORECASE)
            # Separar CamelCase y underscores
            name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
            name = name.replace('_', ' ')
            return name.strip()
        return ""


def parse_xextool_output(output: str) -> XexInfo:
    """
    Parsea la salida de xextool para extraer metadata del XEX.
    
    :param output: Salida completa de xextool
    :return: Objeto XexInfo con la información extraída
    """
    info = XexInfo()
    info.raw_data = {"raw_output": output}
    
    lines = output.split('\n')
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # === Información del ejecutable ===
        if line.startswith("Original PE Name:"):
            info.original_pe_name = _extract_value(line)
        
        elif line.startswith("Load Address:"):
            info.load_address = _extract_value(line)
        
        elif line.startswith("Entry Point:"):
            info.entry_point = _extract_value(line)
        
        elif line.startswith("Image Size:"):
            info.image_size = _extract_value(line)
        
        # === Tipo de XEX ===
        elif "Retail" in line and not ":" in line:
            info.is_retail = True
        elif "Devkit" in line and not ":" in line:
            info.is_retail = False
        elif "Encrypted" in line and not ":" in line:
            info.is_encrypted = True
        elif "Unencrypted" in line and not ":" in line:
            info.is_encrypted = False
        elif "Compressed" in line and not ":" in line:
            info.is_compressed = True
        elif "Uncompressed" in line and not ":" in line:
            info.is_compressed = False
        
        # === Execution ID ===
        elif line.startswith("Media Id:") and "Execution Id" in '\n'.join(lines[max(0, i-5):i]):
            info.media_id = _extract_value(line)
        elif line.startswith("Title Id:"):
            # Extraer solo el código hex, ej: "4E4D07F5" de "4E4D07F5  (NM-2037)"
            value = _extract_value(line)
            match = re.match(r'^([A-Fa-f0-9]+)', value)
            if match:
                info.title_id = match.group(1)
        elif line.startswith("Version:"):
            info.version = _extract_value(line)
        elif line.startswith("Base Version:"):
            info.base_version = _extract_value(line)
        elif line.startswith("Disc Number:"):
            try:
                info.disc_number = int(_extract_value(line))
            except ValueError:
                pass
        elif line.startswith("Number of Discs:"):
            try:
                info.total_discs = int(_extract_value(line))
            except ValueError:
                pass
        
        # === Regiones ===
        elif line.startswith("Regions"):
            # La siguiente línea contiene las regiones
            if i + 1 < len(lines):
                info.regions = lines[i + 1].strip()
        
        # === Ratings ===
        elif line.startswith("ESRB:"):
            # "ESRB:      ESRB_M            08"
            parts = line.split()
            if len(parts) >= 2:
                info.esrb_rating = parts[1]
        elif line.startswith("PEGI:") and not info.pegi_rating:
            parts = line.split()
            if len(parts) >= 2:
                info.pegi_rating = parts[1]
        
        # === Librerías estáticas ===
        elif line and re.match(r'^\d+\)', line):
            # "0) XMP            v2.0.9328.0"
            match = re.match(r'^\d+\)\s+(\S+)\s+v?(\S+)', line)
            if match:
                lib_name = match.group(1)
                lib_version = match.group(2)
                info.static_libraries.append(f"{lib_name} {lib_version}")
    
    return info


def _extract_value(line: str) -> str:
    """Extrae el valor después de los dos puntos."""
    if ':' in line:
        return line.split(':', 1)[1].strip()
    return ""


def parse_media_id_line(output: str) -> Optional[str]:
    """
    Extrae el Media ID del bloque específico.
    El Media ID está en un formato especial con bytes separados.
    """
    # Buscar sección "Media Id" con el formato de bytes
    match = re.search(
        r'Media Id\s*\n\s*([A-Fa-f0-9\s]+)',
        output,
        re.MULTILINE
    )
    if match:
        # Limpiar espacios y unir bytes
        return match.group(1).replace(' ', '').strip()
    return None


# Función de conveniencia para uso directo
def extract_game_info(xextool_output: str) -> dict:
    """
    Extrae información del juego en formato diccionario.
    Útil para serialización JSON.
    """
    info = parse_xextool_output(xextool_output)
    return {
        "title_id": info.title_id,
        "original_pe_name": info.original_pe_name,
        "display_name": info.display_name,
        "media_id": info.media_id,
        "version": info.version,
        "disc_number": info.disc_number,
        "total_discs": info.total_discs,
        "regions": info.regions,
        "esrb_rating": info.esrb_rating,
        "entry_point": info.entry_point,
        "load_address": info.load_address,
        "is_retail": info.is_retail,
        "static_libraries": info.static_libraries[:5],  # Solo primeras 5
    }
