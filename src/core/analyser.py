# core/analyser.py
"""
Analizador de archivos XEX con extracción de metadata.
"""
import os
import json
import subprocess
from dataclasses import dataclass
from typing import Optional, Tuple

try:
    import tomllib  # Python 3.11+
except ImportError:
    import toml as tomllib  # fallback para 3.10 o anterior

from core.config import XENON_ANALYSE_PATH, TEMP_BASE
from core.cleaner_xex import clean_xex, check_xex_info
from core.xex_parser import parse_xextool_output, XexInfo


@dataclass
class AnalysisResult:
    """Resultado del análisis de un XEX."""
    json_file: Optional[str] = None
    toml_file: Optional[str] = None
    xex_info: Optional[XexInfo] = None
    xextool_output: str = ""
    success: bool = False


def analyse_xex(xex_path, out_dir=None, log=None) -> Optional[AnalysisResult]:
    """
    Limpia el XEX si hace falta (xextool), ejecuta XenonAnalyse y convierte TOML->JSON.
    Ahora también extrae metadata del juego parseando la salida de XexTool.
    
    :param xex_path: Ruta al archivo XEX
    :param out_dir: Directorio de salida (opcional)
    :param log: Función de logging (opcional)
    :return: AnalysisResult con archivos y metadata, o None si falla
    """
    result = AnalysisResult()
    
    if not os.path.exists(xex_path):
        raise FileNotFoundError(f"No existe el archivo XEX: {xex_path}")

    if not os.path.exists(XENON_ANALYSE_PATH):
        raise FileNotFoundError(
            f"No se encontró XenonAnalyse en '{XENON_ANALYSE_PATH}'. "
            "Ajusta core/config.py o define la variable de entorno XENON_ANALYSE_PATH."
        )

    base_dir = out_dir or os.path.join(TEMP_BASE, "analysis")
    os.makedirs(base_dir, exist_ok=True)

    # 1) Obtener info del XEX con xextool -l (para metadata)
    if log:
        log("📋 Obteniendo información del XEX...")
    
    xextool_output = check_xex_info(xex_path, log=log)
    result.xextool_output = xextool_output
    
    # Parsear la salida para extraer metadata
    try:
        result.xex_info = parse_xextool_output(xextool_output)
        if result.xex_info.title_id:
            if log:
                log(f"🎮 Juego detectado: {result.xex_info.display_name}")
                log(f"   Title ID: {result.xex_info.title_id}")
                if result.xex_info.version:
                    log(f"   Versión: {result.xex_info.version}")
    except Exception as e:
        if log:
            log(f"⚠️ No se pudo parsear metadata: {e}")

    # 2) Limpiar XEX si es necesario (desencriptar/descomprimir)
    cleaned_xex = clean_xex(xex_path, base_dir, log=log)

    # 3) Ejecutar XenonAnalyse -> analysis.toml
    toml_file = os.path.join(base_dir, "analysis.toml")
    json_file = os.path.join(base_dir, "analysis.json")

    # Crear archivo vacío para evitar FileNotFound durante el open()
    if not os.path.exists(toml_file):
        with open(toml_file, "w", encoding="utf-8"):
            pass

    cmd = [XENON_ANALYSE_PATH, cleaned_xex, toml_file]
    if log:
        log(f"Ejecutando: {' '.join(cmd)}")

    proc = subprocess.run(cmd, capture_output=True, text=True)
    if log:
        if proc.stdout:
            log(proc.stdout.strip())
        if proc.stderr:
            log(proc.stderr.strip())

    if proc.returncode != 0:
        if log:
            log("❌ XenonAnalyse falló")
        return None

    result.toml_file = toml_file

    # 4) Convertir TOML->JSON (si hay contenido), si no, JSON vacío
    if os.path.exists(toml_file) and os.path.getsize(toml_file) > 0:
        try:
            with open(toml_file, "rb") as f:
                data = tomllib.load(f)
        except Exception as e:
            if log:
                log(f"⚠️ No se pudo parsear TOML: {e}")
            data = {}
    else:
        data = {}

    try:
        with open(json_file, "w", encoding="utf-8") as jf:
            json.dump(data, jf, indent=2)
        result.json_file = json_file
    except Exception as e:
        if log:
            log(f"⚠️ No se pudo escribir JSON: {e}")

    result.success = True
    
    if log:
        log("✅ Análisis completado")

    return result


# Función de compatibilidad con código existente
def analyse_xex_legacy(xex_path, out_dir=None, log=None) -> Optional[Tuple[str, str]]:
    """
    Versión legacy que retorna (json_file, toml_file) para compatibilidad.
    """
    result = analyse_xex(xex_path, out_dir, log)
    if result and result.success:
        return (result.json_file, result.toml_file)
    return None

