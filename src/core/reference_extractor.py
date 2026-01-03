# core/reference_extractor.py
"""
Reference Extractor - Herramienta para extraer patrones de proyectos existentes.
Analiza Unleashed Recompiled y otros proyectos para identificar funciones comunes.
"""
import os
import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable, Tuple
from pathlib import Path


@dataclass
class FunctionStub:
    """Representa una función stub de xboxkrnl/xam."""
    name: str
    module: str  # "xboxkrnl" o "xam"
    export_id: Optional[int] = None
    signature: str = ""
    implementation_status: str = "stub"  # stub, partial, full
    source_file: Optional[str] = None
    line_number: int = 0


@dataclass
class RendererPattern:
    """Patrón de implementación de renderer."""
    backend: str  # "dx12", "vulkan"
    features: List[str] = field(default_factory=list)
    shader_model: str = ""
    source_files: List[str] = field(default_factory=list)


@dataclass
class ExtractionResult:
    """Resultado de la extracción de referencias."""
    success: bool
    xboxkrnl_functions: List[FunctionStub] = field(default_factory=list)
    xam_functions: List[FunctionStub] = field(default_factory=list)
    renderer_patterns: List[RendererPattern] = field(default_factory=list)
    audio_patterns: List[str] = field(default_factory=list)
    input_patterns: List[str] = field(default_factory=list)
    error: Optional[str] = None


# Patrones regex para detectar funciones de xboxkrnl
XBOXKRNL_PATTERNS = [
    # Patrón: DECLARE_XBOXKRNL_EXPORT(FunctionName, 0xID)
    r'DECLARE_XBOXKRNL_EXPORT\s*\(\s*(\w+)\s*,\s*(0x[0-9A-Fa-f]+)\s*\)',
    # Patrón: XboxkrnlFunction(...)
    r'(?:DWORD|BOOL|VOID|HRESULT|NTSTATUS)\s+(X[a-zA-Z]+)\s*\(',
    # Patrón: GUEST_FUNCTION_HOOK(addr, FunctionName)
    r'GUEST_FUNCTION_HOOK\s*\(\s*\w+\s*,\s*(\w+)\s*\)',
]

XAM_PATTERNS = [
    r'DECLARE_XAM_EXPORT\s*\(\s*(\w+)\s*,\s*(0x[0-9A-Fa-f]+)\s*\)',
    r'(?:DWORD|BOOL|VOID|HRESULT)\s+(Xam[a-zA-Z]+)\s*\(',
]


def extract_from_repository(
    repo_path: str,
    log: Callable[[str], None] = None
) -> ExtractionResult:
    """
    Extrae patrones de un repositorio de recompilación.
    
    :param repo_path: Ruta al repositorio
    :param log: Función de logging
    :return: ExtractionResult con patrones encontrados
    """
    result = ExtractionResult(success=False)
    
    if not os.path.isdir(repo_path):
        result.error = f"Directorio no encontrado: {repo_path}"
        return result
    
    if log:
        log(f"🔍 Analizando repositorio: {repo_path}")
    
    try:
        # Buscar archivos de código
        cpp_files = _find_source_files(repo_path, [".cpp", ".cc", ".h", ".hpp"])
        
        if log:
            log(f"📄 Archivos encontrados: {len(cpp_files)}")
        
        # Extraer funciones xboxkrnl
        for file_path in cpp_files:
            _extract_xboxkrnl_functions(file_path, result)
            _extract_xam_functions(file_path, result)
            _detect_renderer_patterns(file_path, result)
        
        if log:
            log(f"📊 Funciones xboxkrnl: {len(result.xboxkrnl_functions)}")
            log(f"📊 Funciones xam: {len(result.xam_functions)}")
            log(f"📊 Patrones renderer: {len(result.renderer_patterns)}")
        
        result.success = True
        
    except Exception as e:
        result.error = str(e)
        if log:
            log(f"❌ Error: {e}")
    
    return result


def _find_source_files(directory: str, extensions: List[str]) -> List[str]:
    """Encuentra archivos de código fuente recursivamente."""
    files = []
    for root, _, filenames in os.walk(directory):
        # Ignorar directorios de build
        if any(skip in root for skip in ["build", ".git", "node_modules", "__pycache__"]):
            continue
        for filename in filenames:
            if any(filename.endswith(ext) for ext in extensions):
                files.append(os.path.join(root, filename))
    return files


def _extract_xboxkrnl_functions(file_path: str, result: ExtractionResult):
    """Extrae funciones de xboxkrnl de un archivo."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        for pattern in XBOXKRNL_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                func_name = match.group(1)
                export_id = None
                if len(match.groups()) > 1:
                    try:
                        export_id = int(match.group(2), 16)
                    except:
                        pass
                
                # Evitar duplicados
                if not any(f.name == func_name for f in result.xboxkrnl_functions):
                    stub = FunctionStub(
                        name=func_name,
                        module="xboxkrnl",
                        export_id=export_id,
                        source_file=file_path,
                        line_number=content[:match.start()].count('\n') + 1
                    )
                    result.xboxkrnl_functions.append(stub)
    except:
        pass


def _extract_xam_functions(file_path: str, result: ExtractionResult):
    """Extrae funciones de XAM de un archivo."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        for pattern in XAM_PATTERNS:
            matches = re.finditer(pattern, content)
            for match in matches:
                func_name = match.group(1)
                export_id = None
                if len(match.groups()) > 1:
                    try:
                        export_id = int(match.group(2), 16)
                    except:
                        pass
                
                if not any(f.name == func_name for f in result.xam_functions):
                    stub = FunctionStub(
                        name=func_name,
                        module="xam",
                        export_id=export_id,
                        source_file=file_path,
                        line_number=content[:match.start()].count('\n') + 1
                    )
                    result.xam_functions.append(stub)
    except:
        pass


def _detect_renderer_patterns(file_path: str, result: ExtractionResult):
    """Detecta patrones de renderer en un archivo."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        
        # Detectar DirectX 12
        if "d3d12" in content.lower() or "ID3D12" in content:
            if not any(r.backend == "dx12" for r in result.renderer_patterns):
                pattern = RendererPattern(backend="dx12")
                
                # Detectar features
                if "CreateComputePipelineState" in content:
                    pattern.features.append("compute_shaders")
                if "CreateRenderTargetView" in content:
                    pattern.features.append("render_targets")
                if "CreateDepthStencilView" in content:
                    pattern.features.append("depth_stencil")
                
                pattern.source_files.append(file_path)
                result.renderer_patterns.append(pattern)
        
        # Detectar Vulkan
        if "vulkan" in content.lower() or "VkDevice" in content:
            if not any(r.backend == "vulkan" for r in result.renderer_patterns):
                pattern = RendererPattern(backend="vulkan")
                pattern.source_files.append(file_path)
                result.renderer_patterns.append(pattern)
    except:
        pass


def compare_game_requirements(
    game_a_functions: List[FunctionStub],
    game_b_functions: List[FunctionStub]
) -> Dict[str, List[str]]:
    """
    Compara funciones requeridas entre dos juegos.
    
    :return: Dict con funciones comunes, solo_a, solo_b
    """
    names_a = {f.name for f in game_a_functions}
    names_b = {f.name for f in game_b_functions}
    
    return {
        "common": list(names_a & names_b),
        "only_a": list(names_a - names_b),
        "only_b": list(names_b - names_a),
    }


def generate_stubs_header(functions: List[FunctionStub], module: str = "xboxkrnl") -> str:
    """
    Genera un header C++ con declaraciones de stubs.
    
    :param functions: Lista de funciones
    :param module: Nombre del módulo
    :return: Contenido del header
    """
    header = f'''// {module}_stubs.h
// Generado por MrMonkeyShopWare Reference Extractor

#pragma once

#include <cstdint>
#include <windows.h>

namespace xbox::{module} {{

'''
    
    for func in sorted(functions, key=lambda f: f.name):
        header += f'''// {func.name}
// Export ID: {hex(func.export_id) if func.export_id else "Unknown"}
// Status: {func.implementation_status}
// DWORD {func.name}(...);

'''
    
    header += f'''}}  // namespace xbox::{module}
'''
    
    return header


def generate_stubs_implementation(functions: List[FunctionStub], module: str = "xboxkrnl") -> str:
    """
    Genera implementación C++ de stubs.
    
    :param functions: Lista de funciones
    :param module: Nombre del módulo
    :return: Contenido del archivo .cpp
    """
    impl = f'''// {module}_stubs.cpp
// Generado por MrMonkeyShopWare Reference Extractor

#include "{module}_stubs.h"
#include <cstdio>

namespace xbox::{module} {{

'''
    
    for func in sorted(functions, key=lambda f: f.name):
        impl += f'''// {func.name}
DWORD {func.name}() {{
    // TODO: Implementar
    printf("[{module.upper()}] STUB: {func.name}\\n");
    return 0;
}}

'''
    
    impl += f'''}}  // namespace xbox::{module}
'''
    
    return impl


def extract_function_list_from_xenia(xenia_path: str, log: Callable[[str], None] = None) -> List[FunctionStub]:
    """
    Extrae lista de funciones de xboxkrnl desde el código de Xenia.
    
    :param xenia_path: Ruta al repositorio de Xenia
    :param log: Función de logging
    :return: Lista de FunctionStub
    """
    functions = []
    
    xboxkrnl_dir = os.path.join(xenia_path, "src", "xenia", "kernel", "xboxkrnl")
    
    if not os.path.isdir(xboxkrnl_dir):
        if log:
            log(f"❌ Directorio no encontrado: {xboxkrnl_dir}")
        return functions
    
    if log:
        log(f"📂 Analizando Xenia: {xboxkrnl_dir}")
    
    result = ExtractionResult(success=False)
    
    for filename in os.listdir(xboxkrnl_dir):
        if filename.endswith(".cc") or filename.endswith(".h"):
            file_path = os.path.join(xboxkrnl_dir, filename)
            _extract_xboxkrnl_functions(file_path, result)
    
    if log:
        log(f"✅ Funciones encontradas: {len(result.xboxkrnl_functions)}")
    
    return result.xboxkrnl_functions
