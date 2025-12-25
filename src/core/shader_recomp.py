# core/shader_recomp.py
"""
Módulo para recompilación de shaders y ejecutables Xbox 360 usando XenonRecomp.
"""
import subprocess
import os
from typing import Optional, Callable, Tuple, List
from dataclasses import dataclass, field
from pathlib import Path

from core.config import XENON_RECOMP_PATH, PPC_CONTEXT_PATH


@dataclass
class RecompResult:
    """Resultado de la recompilación."""
    success: bool
    output_dir: Optional[str] = None
    cpp_files: List[str] = field(default_factory=list)
    header_files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""


def check_xenon_recomp_available() -> bool:
    """
    Verifica si XenonRecomp está disponible en el sistema.
    
    :return: True si está disponible
    """
    return os.path.isfile(XENON_RECOMP_PATH)


def get_recomp_version(log: Callable[[str], None] = None) -> Optional[str]:
    """
    Obtiene la versión de XenonRecomp instalado.
    
    :param log: Función de logging opcional
    :return: Versión como string o None si no está disponible
    """
    if not check_xenon_recomp_available():
        if log:
            log("❌ XenonRecomp no encontrado")
        return None
    
    try:
        result = subprocess.run(
            [XENON_RECOMP_PATH, "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        version = result.stdout.strip() or result.stderr.strip()
        return version if version else "unknown"
    except Exception as e:
        if log:
            log(f"⚠️ No se pudo obtener versión: {e}")
        return None


def run_recompilation(
    toml_path: str,
    output_dir: str = None,
    log: Callable[[str], None] = None,
    timeout: int = 300
) -> RecompResult:
    """
    Ejecuta XenonRecomp para recompilar el XEX.
    
    :param toml_path: Ruta al project.toml
    :param output_dir: Directorio de salida (opcional, usa el del TOML)
    :param log: Función de logging
    :param timeout: Timeout en segundos (default: 5 minutos)
    :return: RecompResult con estado y archivos generados
    """
    if log:
        log("🔧 Iniciando recompilación con XenonRecomp...")
    
    # Verificar que XenonRecomp está disponible
    if not check_xenon_recomp_available():
        error_msg = f"XenonRecomp no encontrado en: {XENON_RECOMP_PATH}"
        if log:
            log(f"❌ {error_msg}")
        return RecompResult(success=False, error=error_msg)
    
    # Verificar que el TOML existe
    if not os.path.isfile(toml_path):
        error_msg = f"Archivo TOML no encontrado: {toml_path}"
        if log:
            log(f"❌ {error_msg}")
        return RecompResult(success=False, error=error_msg)
    
    # Verificar PPC Context
    if not os.path.isfile(PPC_CONTEXT_PATH):
        error_msg = f"PPC Context no encontrado: {PPC_CONTEXT_PATH}"
        if log:
            log(f"❌ {error_msg}")
        return RecompResult(success=False, error=error_msg)
    
    # Determinar directorio de salida
    if output_dir is None:
        output_dir = os.path.dirname(toml_path)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Construir comando
    cmd = [
        XENON_RECOMP_PATH,
        toml_path,
        PPC_CONTEXT_PATH
    ]
    
    if log:
        log(f"📋 Comando: {' '.join(cmd)}")
        log(f"📁 Directorio de trabajo: {os.path.dirname(toml_path)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(toml_path),
            timeout=timeout
        )
        
        if result.returncode == 0:
            if log:
                log("✅ Recompilación completada exitosamente")
            
            # Buscar archivos generados
            cpp_files, header_files = _find_generated_files(output_dir)
            
            if log:
                log(f"📄 Archivos C++ generados: {len(cpp_files)}")
                log(f"📄 Headers generados: {len(header_files)}")
            
            return RecompResult(
                success=True,
                output_dir=output_dir,
                cpp_files=cpp_files,
                header_files=header_files,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )
        else:
            error_msg = f"XenonRecomp falló con código: {result.returncode}"
            if log:
                log(f"❌ {error_msg}")
                if result.stdout:
                    log(f"STDOUT: {result.stdout[:500]}")
                if result.stderr:
                    log(f"STDERR: {result.stderr[:500]}")
            
            return RecompResult(
                success=False,
                output_dir=output_dir,
                error=error_msg,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )
    
    except subprocess.TimeoutExpired:
        error_msg = f"Timeout después de {timeout} segundos"
        if log:
            log(f"⏰ {error_msg}")
        return RecompResult(success=False, error=error_msg)
    
    except Exception as e:
        error_msg = f"Error al ejecutar XenonRecomp: {e}"
        if log:
            log(f"❌ {error_msg}")
        return RecompResult(success=False, error=error_msg)


def _find_generated_files(directory: str) -> Tuple[List[str], List[str]]:
    """
    Busca archivos generados por la recompilación.
    
    :param directory: Directorio donde buscar
    :return: Tupla (cpp_files, header_files)
    """
    cpp_files = []
    header_files = []
    
    build_dir = os.path.join(directory, "build")
    search_dirs = [directory, build_dir] if os.path.isdir(build_dir) else [directory]
    
    for search_dir in search_dirs:
        if not os.path.isdir(search_dir):
            continue
        
        for root, _, files in os.walk(search_dir):
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith(".cpp"):
                    cpp_files.append(full_path)
                elif file.endswith(".h") or file.endswith(".hpp"):
                    header_files.append(full_path)
    
    return cpp_files, header_files


def validate_recomp_output(output_dir: str, log: Callable[[str], None] = None) -> Tuple[bool, List[str]]:
    """
    Valida que la recompilación generó los archivos esperados.
    
    :param output_dir: Directorio de salida
    :param log: Función de logging opcional
    :return: (success, list of all generated files)
    """
    if not os.path.isdir(output_dir):
        if log:
            log(f"❌ Directorio no existe: {output_dir}")
        return False, []
    
    cpp_files, header_files = _find_generated_files(output_dir)
    all_files = cpp_files + header_files
    
    if log:
        log(f"📊 Archivos encontrados: {len(all_files)}")
        for f in all_files[:10]:  # Mostrar máximo 10
            log(f"   - {os.path.basename(f)}")
        if len(all_files) > 10:
            log(f"   ... y {len(all_files) - 10} más")
    
    # Considerar exitoso si hay al menos un archivo .cpp
    success = len(cpp_files) > 0
    
    return success, all_files
