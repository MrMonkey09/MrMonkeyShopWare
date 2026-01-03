# core/build_automation.py
"""
Módulo para automatizar la compilación del código C++ generado por XenonRecomp.
Genera CMakeLists.txt y ejecuta builds con Clang.
"""
import subprocess
import os
import shutil
from typing import Optional, Callable, List, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass 
class BuildResult:
    """Resultado de la compilación."""
    success: bool
    executable_path: Optional[str] = None
    error: Optional[str] = None
    return_code: int = 0
    stdout: str = ""
    stderr: str = ""


def check_clang_available() -> Tuple[bool, Optional[str]]:
    """
    Verifica si Clang está disponible en el sistema.
    
    :return: (disponible, versión)
    """
    try:
        result = subprocess.run(
            ["clang", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            return True, version
    except Exception:
        pass
    
    # Intentar con clang++
    try:
        result = subprocess.run(
            ["clang++", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            return True, version
    except Exception:
        pass
    
    return False, None


def check_cmake_available() -> Tuple[bool, Optional[str]]:
    """
    Verifica si CMake está disponible en el sistema.
    
    :return: (disponible, versión)
    """
    try:
        result = subprocess.run(
            ["cmake", "--version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            version = result.stdout.split('\n')[0]
            return True, version
    except Exception:
        pass
    
    return False, None


def generate_cmakelists(
    project_name: str,
    ppc_dir: str,
    output_path: str,
    additional_sources: List[str] = None,
    log: Callable[[str], None] = None
) -> str:
    """
    Genera un CMakeLists.txt para compilar el código recompilado.
    
    :param project_name: Nombre del proyecto
    :param ppc_dir: Directorio con archivos PPC generados
    :param output_path: Ruta donde guardar el CMakeLists.txt
    :param additional_sources: Archivos fuente adicionales
    :param log: Función de logging
    :return: Ruta al CMakeLists.txt generado
    """
    
    cmake_content = f'''# CMakeLists.txt - Generado por MrMonkeyShopWare
# Proyecto de recompilación Xbox 360

cmake_minimum_required(VERSION 3.20)
project({project_name} VERSION 1.0 LANGUAGES CXX)

# Requerir C++20 y Clang
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Verificar compilador Clang
if(NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(WARNING "Se recomienda usar Clang para este proyecto")
endif()

# Flags de optimización
set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} -O2 -mavx -msse4.1 -mssse3")

# Archivos PPC recompilados
file(GLOB PPC_SOURCES 
    "${{CMAKE_SOURCE_DIR}}/{os.path.basename(ppc_dir)}/*.cpp"
)

# Crear ejecutable
add_executable(${{PROJECT_NAME}}
    ${{PPC_SOURCES}}
)

# Incluir headers
target_include_directories(${{PROJECT_NAME}} PRIVATE
    ${{CMAKE_SOURCE_DIR}}/{os.path.basename(ppc_dir)}
    ${{CMAKE_SOURCE_DIR}}/include
)

# Configuración de build
set_target_properties(${{PROJECT_NAME}} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${{CMAKE_BINARY_DIR}}/bin"
)

# Mensaje de estado
message(STATUS "Configurando proyecto: {project_name}")
message(STATUS "Archivos PPC: ${{PPC_SOURCES}}")
'''
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cmake_content)
    
    if log:
        log(f"✅ CMakeLists.txt generado: {output_path}")
    
    return output_path


def build_with_cmake(
    project_dir: str,
    build_type: str = "Release",
    generator: str = None,
    log: Callable[[str], None] = None,
    timeout: int = 600
) -> BuildResult:
    """
    Compila el proyecto usando CMake.
    
    :param project_dir: Directorio del proyecto
    :param build_type: Tipo de build (Debug/Release/RelWithDebInfo)
    :param generator: Generador de CMake (opcional)
    :param log: Función de logging
    :param timeout: Timeout en segundos
    :return: BuildResult con estado
    """
    if log:
        log(f"🔧 Iniciando build CMake en: {project_dir}")
    
    # Verificar CMake
    cmake_available, cmake_version = check_cmake_available()
    if not cmake_available:
        return BuildResult(
            success=False,
            error="CMake no encontrado en el sistema"
        )
    
    if log:
        log(f"📋 CMake: {cmake_version}")
    
    build_dir = os.path.join(project_dir, "build")
    os.makedirs(build_dir, exist_ok=True)
    
    # Configurar
    configure_cmd = [
        "cmake",
        "-S", project_dir,
        "-B", build_dir,
        f"-DCMAKE_BUILD_TYPE={build_type}"
    ]
    
    if generator:
        configure_cmd.extend(["-G", generator])
    
    if log:
        log(f"📋 Configurando: {' '.join(configure_cmd)}")
    
    try:
        config_result = subprocess.run(
            configure_cmd,
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if config_result.returncode != 0:
            error_msg = f"Configuración CMake falló: {config_result.stderr}"
            if log:
                log(f"❌ {error_msg}")
            return BuildResult(
                success=False,
                error=error_msg,
                return_code=config_result.returncode,
                stdout=config_result.stdout,
                stderr=config_result.stderr
            )
        
        if log:
            log("✅ Configuración completada")
        
        # Compilar
        build_cmd = [
            "cmake",
            "--build", build_dir,
            "--config", build_type,
            "--parallel"
        ]
        
        if log:
            log(f"📋 Compilando: {' '.join(build_cmd)}")
        
        build_result = subprocess.run(
            build_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if build_result.returncode != 0:
            error_msg = f"Build falló: {build_result.stderr}"
            if log:
                log(f"❌ {error_msg}")
            return BuildResult(
                success=False,
                error=error_msg,
                return_code=build_result.returncode,
                stdout=build_result.stdout,
                stderr=build_result.stderr
            )
        
        # Buscar ejecutable generado
        exe_path = find_executable(build_dir)
        
        if log:
            if exe_path:
                log(f"✅ Ejecutable generado: {exe_path}")
            else:
                log("✅ Build completado (ejecutable no encontrado)")
        
        return BuildResult(
            success=True,
            executable_path=exe_path,
            return_code=0,
            stdout=build_result.stdout,
            stderr=build_result.stderr
        )
    
    except subprocess.TimeoutExpired:
        error_msg = f"Timeout después de {timeout} segundos"
        if log:
            log(f"⏰ {error_msg}")
        return BuildResult(success=False, error=error_msg)
    
    except Exception as e:
        error_msg = f"Error durante build: {e}"
        if log:
            log(f"❌ {error_msg}")
        return BuildResult(success=False, error=error_msg)


def build_with_clang_direct(
    cpp_files: List[str],
    output_exe: str,
    include_dirs: List[str] = None,
    log: Callable[[str], None] = None,
    timeout: int = 600
) -> BuildResult:
    """
    Compila directamente con Clang sin CMake.
    Útil para builds rápidos o cuando CMake no está disponible.
    
    :param cpp_files: Lista de archivos .cpp
    :param output_exe: Ruta del ejecutable de salida
    :param include_dirs: Directorios de includes
    :param log: Función de logging
    :param timeout: Timeout en segundos
    :return: BuildResult con estado
    """
    if log:
        log(f"🔧 Compilando {len(cpp_files)} archivos con Clang...")
    
    # Verificar Clang
    clang_available, clang_version = check_clang_available()
    if not clang_available:
        return BuildResult(
            success=False,
            error="Clang no encontrado en el sistema"
        )
    
    if log:
        log(f"📋 Clang: {clang_version}")
    
    # Construir comando
    # Similar al usado en Fable2Recomp
    cmd = [
        "clang++",
        "-o", output_exe,
        "-std=c++20",
        "-O2",
        "-mssse3",
        "-msse4.1",
        "-mavx",
        "-pthread"
    ]
    
    # Agregar includes
    if include_dirs:
        for inc in include_dirs:
            cmd.extend(["-I", inc])
    
    # Agregar archivos fuente
    cmd.extend(cpp_files)
    
    if log:
        log(f"📋 Comando: clang++ -o {os.path.basename(output_exe)} [archivos...]")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            if log:
                log(f"✅ Ejecutable generado: {output_exe}")
            
            return BuildResult(
                success=True,
                executable_path=output_exe,
                return_code=0,
                stdout=result.stdout,
                stderr=result.stderr
            )
        else:
            error_msg = f"Clang falló con código: {result.returncode}"
            if log:
                log(f"❌ {error_msg}")
                if result.stderr:
                    # Mostrar primeros errores
                    log(f"STDERR: {result.stderr[:1000]}")
            
            return BuildResult(
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
        return BuildResult(success=False, error=error_msg)
    
    except Exception as e:
        error_msg = f"Error durante compilación: {e}"
        if log:
            log(f"❌ {error_msg}")
        return BuildResult(success=False, error=error_msg)


def find_executable(directory: str) -> Optional[str]:
    """
    Busca un archivo ejecutable en un directorio.
    
    :param directory: Directorio donde buscar
    :return: Ruta al ejecutable o None
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".exe") or (os.name != "nt" and os.access(os.path.join(root, file), os.X_OK)):
                return os.path.join(root, file)
    return None


def get_build_requirements() -> dict:
    """
    Obtiene el estado de las herramientas de build.
    
    :return: Diccionario con disponibilidad de herramientas
    """
    clang_ok, clang_ver = check_clang_available()
    cmake_ok, cmake_ver = check_cmake_available()
    
    return {
        "clang": {
            "available": clang_ok,
            "version": clang_ver
        },
        "cmake": {
            "available": cmake_ok,
            "version": cmake_ver
        },
        "ready": clang_ok  # Mínimo requerido
    }
