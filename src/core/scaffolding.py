# core/scaffolding.py
"""
Scaffolding Manager para proyectos de recompilación Xbox 360.
Genera y gestiona la estructura de directorios y archivos base.
"""
import os
import shutil
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Callable
from pathlib import Path
import json


@dataclass
class ProjectConfig:
    """Configuración para crear un proyecto de recompilación."""
    name: str
    output_dir: str
    title_id: str = ""
    game_name: str = ""
    
    # Rutas opcionales de archivos del juego
    xex_path: Optional[str] = None
    analysis_toml: Optional[str] = None
    ppc_dir: Optional[str] = None
    shaders_dir: Optional[str] = None
    
    # Opciones
    use_dx12: bool = True
    use_vulkan: bool = False
    include_runtime_submodule: bool = True


@dataclass
class ScaffoldResult:
    """Resultado de la operación de scaffolding."""
    success: bool
    project_dir: str
    created_files: List[str] = field(default_factory=list)
    created_dirs: List[str] = field(default_factory=list)
    error: Optional[str] = None


# Estructura base de un proyecto de recompilación
PROJECT_STRUCTURE = {
    "src": {
        "main.cpp": None,  # None = crear archivo con template
        "ppc": {},         # Directorio vacío para código recompilado
        "patches": {},     # Parches específicos del juego
    },
    "shaders": {},
    "assets": {},
    "config": {
        "game.toml": None,
        "hooks.toml": None,
    },
    "include": {},
    "lib": {},
}


def create_project_scaffold(
    config: ProjectConfig,
    log: Callable[[str], None] = None
) -> ScaffoldResult:
    """
    Crea la estructura de directorios para un nuevo proyecto de recompilación.
    
    :param config: Configuración del proyecto
    :param log: Función de logging
    :return: ScaffoldResult con información del proyecto creado
    """
    result = ScaffoldResult(success=False, project_dir="")
    
    # Crear directorio principal
    project_dir = os.path.join(config.output_dir, f"{config.name}_Recomp")
    result.project_dir = project_dir
    
    if log:
        log(f"📁 Creando proyecto: {project_dir}")
    
    try:
        os.makedirs(project_dir, exist_ok=True)
        result.created_dirs.append(project_dir)
        
        # Crear estructura recursivamente
        _create_structure(project_dir, PROJECT_STRUCTURE, result, log)
        
        # Generar archivos con contenido
        _generate_main_cpp(project_dir, config, result, log)
        _generate_cmakelists(project_dir, config, result, log)
        _generate_game_toml(project_dir, config, result, log)
        _generate_hooks_toml(project_dir, config, result, log)
        _generate_gitignore(project_dir, result, log)
        _generate_readme(project_dir, config, result, log)
        
        # Copiar archivos si existen
        if config.ppc_dir and os.path.isdir(config.ppc_dir):
            _copy_directory(config.ppc_dir, os.path.join(project_dir, "src", "ppc"), log)
        
        if config.shaders_dir and os.path.isdir(config.shaders_dir):
            _copy_directory(config.shaders_dir, os.path.join(project_dir, "shaders"), log)
        
        result.success = True
        if log:
            log(f"✅ Proyecto creado: {len(result.created_dirs)} carpetas, {len(result.created_files)} archivos")
        
    except Exception as e:
        result.error = str(e)
        if log:
            log(f"❌ Error creando proyecto: {e}")
    
    return result


def _create_structure(base_path: str, structure: dict, result: ScaffoldResult, log=None):
    """Crea estructura de directorios recursivamente."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # Es un directorio
            os.makedirs(path, exist_ok=True)
            result.created_dirs.append(path)
            _create_structure(path, content, result, log)
        elif content is None:
            # Es un archivo placeholder (se genera después)
            pass


def _generate_main_cpp(project_dir: str, config: ProjectConfig, result: ScaffoldResult, log=None):
    """Genera main.cpp base."""
    content = f'''// {config.name} - Recompilación Xbox 360
// Generado por MrMonkeyShopWare

#include <cstdio>

// Incluir runtime compartido
// #include "runtime/xbox/xboxkrnl.h"
// #include "runtime/xbox/xam.h"

// Incluir código PPC recompilado
// #include "ppc/ppc_recomp.h"

int main(int argc, char* argv[]) {{
    printf("{config.name} Recompiled\\n");
    printf("Title ID: {config.title_id}\\n");
    
    // TODO: Inicializar runtime
    // xbox::runtime::Initialize();
    
    // TODO: Inicializar renderer
    // renderer::Initialize();
    
    // TODO: Ejecutar punto de entrada del juego
    // ppc::entry_point();
    
    return 0;
}}
'''
    
    path = os.path.join(project_dir, "src", "main.cpp")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)


def _generate_cmakelists(project_dir: str, config: ProjectConfig, result: ScaffoldResult, log=None):
    """Genera CMakeLists.txt."""
    content = f'''# CMakeLists.txt - {config.name} Recompiled
# Generado por MrMonkeyShopWare

cmake_minimum_required(VERSION 3.20)
project({config.name}Recomp VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Verificar Clang
if(NOT CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    message(WARNING "Se recomienda usar Clang para este proyecto")
endif()

# Flags de optimización
set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} -O2 -mavx -msse4.1")

# Archivos PPC recompilados
file(GLOB PPC_SOURCES "src/ppc/*.cpp")

# Archivos de patches
file(GLOB PATCH_SOURCES "src/patches/*.cpp")

# Ejecutable principal
add_executable(${{PROJECT_NAME}}
    src/main.cpp
    ${{PPC_SOURCES}}
    ${{PATCH_SOURCES}}
)

target_include_directories(${{PROJECT_NAME}} PRIVATE
    include/
    src/ppc/
)

# Runtime compartido (si está disponible)
# add_subdirectory(runtime)
# target_link_libraries(${{PROJECT_NAME}} PRIVATE xbox_runtime)

# Renderer
'''
    
    if config.use_dx12:
        content += '''
# DirectX 12
# find_package(DirectX12 REQUIRED)
# target_link_libraries(${PROJECT_NAME} PRIVATE d3d12 dxgi)
'''
    
    if config.use_vulkan:
        content += '''
# Vulkan
find_package(Vulkan REQUIRED)
target_link_libraries(${PROJECT_NAME} PRIVATE Vulkan::Vulkan)
'''
    
    content += '''
# Output
set_target_properties(${PROJECT_NAME} PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)

message(STATUS "Configurando: ${PROJECT_NAME}")
'''
    
    path = os.path.join(project_dir, "CMakeLists.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)


def _generate_game_toml(project_dir: str, config: ProjectConfig, result: ScaffoldResult, log=None):
    """Genera game.toml con perfil del juego."""
    content = f'''# Perfil del juego - {config.name}
# Generado por MrMonkeyShopWare

[game]
title_id = "{config.title_id}"
name = "{config.game_name or config.name}"

[xboxkrnl]
# Funciones del kernel requeridas por este juego
required_functions = [
    "XCreateThread",
    "XWaitForSingleObject",
    "XMemAlloc",
    "XMemFree",
]

[xam]
# Funciones XAM requeridas
required_functions = [
    # "XamShowMessageBox",
    # "XamContentCreate",
]

[renderer]
# Configuración del renderer
backend = "{"dx12" if config.use_dx12 else "vulkan"}"
shader_model = "6.0"
uses_geometry_shaders = false

[audio]
# Configuración de audio
format = "XMA2"
channels = 2

[input]
# Mapeo de controles
use_xinput = true

[memory]
# Configuración de memoria  
heap_size = 0x10000000  # 256MB
'''
    
    path = os.path.join(project_dir, "config", "game.toml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)


def _generate_hooks_toml(project_dir: str, config: ProjectConfig, result: ScaffoldResult, log=None):
    """Genera hooks.toml para parches del juego."""
    content = f'''# Hooks y parches - {config.name}
# Generado por MrMonkeyShopWare

# Mid-asm hooks para insertar código personalizado
# [[midasm_hook]]
# name = "FrameLimiter"
# address = 0x00000000
# registers = ["r3"]

# Function replacements
# [[function_replace]]
# original_address = 0x00000000
# replacement = "my_custom_function"

# Memory patches
# [[memory_patch]]
# address = 0x00000000
# bytes = [0x60, 0x00, 0x00, 0x00]  # NOP
# description = "Skip intro"
'''
    
    path = os.path.join(project_dir, "config", "hooks.toml")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)


def _generate_gitignore(project_dir: str, result: ScaffoldResult, log=None):
    """Genera .gitignore."""
    content = '''# Build
build/
bin/
out/
*.exe
*.dll
*.so
*.dylib

# IDE
.vs/
.vscode/
*.sln
*.vcxproj*
.idea/

# Game assets (no commitear)
assets/*
!assets/.gitkeep

# Temporal
*.log
*.tmp
__pycache__/
'''
    
    path = os.path.join(project_dir, ".gitignore")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)
    
    # Crear .gitkeep en assets
    gitkeep = os.path.join(project_dir, "assets", ".gitkeep")
    with open(gitkeep, "w") as f:
        pass
    result.created_files.append(gitkeep)


def _generate_readme(project_dir: str, config: ProjectConfig, result: ScaffoldResult, log=None):
    """Genera README.md."""
    content = f'''# {config.name} Recompiled

Recompilación de {config.game_name or config.name} (Xbox 360) a PC nativo.

**Title ID:** `{config.title_id}`

## Requisitos

- CMake 3.20+
- Clang 18+
- {'DirectX 12' if config.use_dx12 else 'Vulkan SDK'}

## Build

```bash
cmake -B build -G "Visual Studio 17 2022" -T ClangCL
cmake --build build --config Release
```

## Archivos del Juego

Coloca los archivos del juego en `assets/`:
- Assets extraídos del ISO

## Estructura

```
{config.name}_Recomp/
├── src/
│   ├── main.cpp          # Punto de entrada
│   ├── ppc/              # Código recompilado
│   └── patches/          # Parches del juego
├── shaders/              # Shaders HLSL
├── assets/               # Assets del juego
├── config/
│   ├── game.toml         # Perfil del juego
│   └── hooks.toml        # Hooks y parches
└── CMakeLists.txt
```

## Créditos

- Generado con [MrMonkeyShopWare](https://github.com/MrMonkey09/MrMonkeyShopWare)
- Herramientas: XenonRecomp, XenosRecomp
'''
    
    path = os.path.join(project_dir, "README.md")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    result.created_files.append(path)


def _copy_directory(src: str, dst: str, log=None):
    """Copia un directorio recursivamente."""
    if log:
        log(f"📋 Copiando: {src} → {dst}")
    shutil.copytree(src, dst, dirs_exist_ok=True)


def update_project_scaffold(
    project_dir: str,
    updates: Dict[str, str],
    log: Callable[[str], None] = None
) -> bool:
    """
    Actualiza archivos de un proyecto existente.
    
    :param project_dir: Directorio del proyecto
    :param updates: Dict de {ruta_relativa: contenido}
    :param log: Función de logging
    :return: True si se actualizó correctamente
    """
    if not os.path.isdir(project_dir):
        if log:
            log(f"❌ Proyecto no encontrado: {project_dir}")
        return False
    
    for rel_path, content in updates.items():
        full_path = os.path.join(project_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        if log:
            log(f"📝 Actualizado: {rel_path}")
    
    return True


def list_project_files(project_dir: str) -> List[str]:
    """
    Lista todos los archivos de un proyecto.
    
    :param project_dir: Directorio del proyecto
    :return: Lista de rutas relativas
    """
    files = []
    for root, _, filenames in os.walk(project_dir):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            rel_path = os.path.relpath(full_path, project_dir)
            files.append(rel_path)
    return files


def validate_project_structure(project_dir: str) -> Dict[str, bool]:
    """
    Valida que un proyecto tenga la estructura esperada.
    
    :param project_dir: Directorio del proyecto
    :return: Dict con {componente: existe}
    """
    required = {
        "CMakeLists.txt": False,
        "src/main.cpp": False,
        "src/ppc": False,
        "config/game.toml": False,
        "config/hooks.toml": False,
    }
    
    for path in required:
        full_path = os.path.join(project_dir, path)
        required[path] = os.path.exists(full_path)
    
    return required
