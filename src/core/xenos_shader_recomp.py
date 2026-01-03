# core/xenos_shader_recomp.py
"""
Módulo para conversión de shaders Xbox 360 a HLSL usando XenosRecomp.
Convierte shaders binarios de Xenos GPU a HLSL compatible con DX12/Vulkan.
"""
import subprocess
import os
from typing import Optional, Callable, List, Tuple
from dataclasses import dataclass, field
from pathlib import Path

from core.config import XENOS_RECOMP_PATH, SHADER_COMMON_PATH


@dataclass
class ShaderRecompResult:
    """Resultado de la conversión de shaders."""
    success: bool
    hlsl_files: List[str] = field(default_factory=list)
    error: Optional[str] = None
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""


def check_xenos_recomp_available() -> bool:
    """
    Verifica si XenosRecomp está disponible en el sistema.
    
    :return: True si está disponible
    """
    return os.path.isfile(XENOS_RECOMP_PATH)


def check_shader_common_available() -> bool:
    """
    Verifica si shader_common.h está disponible.
    
    :return: True si está disponible
    """
    return os.path.isfile(SHADER_COMMON_PATH)


def convert_shader(
    input_shader: str,
    output_hlsl: str,
    log: Callable[[str], None] = None,
    timeout: int = 60
) -> ShaderRecompResult:
    """
    Convierte un shader binario de Xbox 360 a HLSL.
    
    :param input_shader: Ruta al archivo de shader binario
    :param output_hlsl: Ruta de salida para el HLSL
    :param log: Función de logging
    :param timeout: Timeout en segundos
    :return: ShaderRecompResult con estado y archivos
    """
    if log:
        log(f"🎨 Convirtiendo shader: {os.path.basename(input_shader)}")
    
    # Verificar disponibilidad
    if not check_xenos_recomp_available():
        error_msg = f"XenosRecomp no encontrado en: {XENOS_RECOMP_PATH}"
        if log:
            log(f"❌ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)
    
    if not check_shader_common_available():
        error_msg = f"shader_common.h no encontrado en: {SHADER_COMMON_PATH}"
        if log:
            log(f"❌ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)
    
    if not os.path.isfile(input_shader):
        error_msg = f"Shader de entrada no encontrado: {input_shader}"
        if log:
            log(f"❌ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)
    
    # Crear directorio de salida
    os.makedirs(os.path.dirname(output_hlsl), exist_ok=True)
    
    # Comando: XenosRecomp [input] [output] [shader_common.h]
    cmd = [
        XENOS_RECOMP_PATH,
        input_shader,
        output_hlsl,
        SHADER_COMMON_PATH
    ]
    
    if log:
        log(f"📋 Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            if log:
                log(f"✅ Shader convertido: {os.path.basename(output_hlsl)}")
            
            return ShaderRecompResult(
                success=True,
                hlsl_files=[output_hlsl],
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )
        else:
            error_msg = f"XenosRecomp falló con código: {result.returncode}"
            if log:
                log(f"❌ {error_msg}")
                if result.stderr:
                    log(f"STDERR: {result.stderr[:500]}")
            
            return ShaderRecompResult(
                success=False,
                error=error_msg,
                return_code=result.returncode,
                stdout=result.stdout,
                stderr=result.stderr
            )
    
    except subprocess.TimeoutExpired:
        error_msg = f"Timeout después de {timeout} segundos"
        if log:
            log(f"⏰ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)
    
    except Exception as e:
        error_msg = f"Error al ejecutar XenosRecomp: {e}"
        if log:
            log(f"❌ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)


def convert_shader_archive(
    shader_archive: str,
    output_dir: str,
    log: Callable[[str], None] = None,
    timeout: int = 300
) -> ShaderRecompResult:
    """
    Convierte todos los shaders de un archivo .ar (shader archive).
    
    :param shader_archive: Ruta al archivo shader.ar
    :param output_dir: Directorio de salida para los HLSL
    :param log: Función de logging
    :param timeout: Timeout en segundos
    :return: ShaderRecompResult con todos los archivos generados
    """
    if log:
        log(f"📦 Procesando shader archive: {os.path.basename(shader_archive)}")
    
    if not os.path.isfile(shader_archive):
        error_msg = f"Shader archive no encontrado: {shader_archive}"
        if log:
            log(f"❌ {error_msg}")
        return ShaderRecompResult(success=False, error=error_msg)
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Para archivos .ar, XenosRecomp puede necesitar procesamiento especial
    # Por ahora, convertimos el archivo completo
    output_hlsl = os.path.join(output_dir, "shaders.hlsl")
    
    result = convert_shader(shader_archive, output_hlsl, log, timeout)
    
    if result.success and log:
        log(f"📊 Shaders convertidos en: {output_dir}")
    
    return result


def find_shader_files(game_dir: str) -> List[str]:
    """
    Busca archivos de shaders en un directorio de juego.
    
    :param game_dir: Directorio del juego extraído
    :return: Lista de rutas a archivos de shader
    """
    shader_files = []
    
    # Extensiones comunes de shaders Xbox 360
    extensions = ['.ar', '.xps', '.xvs', '.xsh']
    
    for root, _, files in os.walk(game_dir):
        for file in files:
            # shader.ar es el archivo típico
            if file.lower() == 'shader.ar':
                shader_files.append(os.path.join(root, file))
            elif any(file.lower().endswith(ext) for ext in extensions):
                shader_files.append(os.path.join(root, file))
    
    return shader_files


def batch_convert_shaders(
    shader_files: List[str],
    output_dir: str,
    log: Callable[[str], None] = None
) -> Tuple[int, int, List[str]]:
    """
    Convierte múltiples archivos de shader.
    
    :param shader_files: Lista de rutas a shaders
    :param output_dir: Directorio de salida
    :param log: Función de logging
    :return: (éxitos, fallos, lista de archivos generados)
    """
    success_count = 0
    fail_count = 0
    generated_files = []
    
    if log:
        log(f"🎨 Iniciando conversión batch de {len(shader_files)} shaders...")
    
    for shader_path in shader_files:
        shader_name = os.path.splitext(os.path.basename(shader_path))[0]
        output_hlsl = os.path.join(output_dir, f"{shader_name}.hlsl")
        
        result = convert_shader(shader_path, output_hlsl, log)
        
        if result.success:
            success_count += 1
            generated_files.extend(result.hlsl_files)
        else:
            fail_count += 1
    
    if log:
        log(f"📊 Conversión batch completada: {success_count} éxitos, {fail_count} fallos")
    
    return success_count, fail_count, generated_files
