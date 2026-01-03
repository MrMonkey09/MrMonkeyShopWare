# CMakeLists.txt - Xbox 360 Runtime Library
# Librería compartida para proyectos de recompilación
# Generado por MrMonkeyShopWare

cmake_minimum_required(VERSION 3.20)
project(xbox_runtime VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# ═══════════════════════════════════════════════════════════════
# OPCIONES
# ═══════════════════════════════════════════════════════════════

option(RUNTIME_USE_DX12 "Enable DirectX 12 renderer" ON)
option(RUNTIME_USE_VULKAN "Enable Vulkan renderer" OFF)
option(RUNTIME_USE_XMA "Enable XMA audio decoder" ON)

# ═══════════════════════════════════════════════════════════════
# ARCHIVOS FUENTE
# ═══════════════════════════════════════════════════════════════

set(KERNEL_SOURCES
    src/xboxkrnl/threading.cpp
    src/xboxkrnl/memory.cpp
    src/xboxkrnl/sync.cpp
    src/xboxkrnl/io.cpp
    src/xboxkrnl/crypto.cpp
)

set(XAM_SOURCES
    src/xam/content.cpp
    src/xam/ui.cpp
    src/xam/user.cpp
)

set(RENDERER_SOURCES
    src/renderer/renderer_base.cpp
)

if(RUNTIME_USE_DX12)
    list(APPEND RENDERER_SOURCES
        src/renderer/dx12/dx12_renderer.cpp
    )
endif()

if(RUNTIME_USE_VULKAN)
    list(APPEND RENDERER_SOURCES
        src/renderer/vulkan/vulkan_renderer.cpp
    )
endif()

set(AUDIO_SOURCES
    src/audio/audio_system.cpp
)

if(RUNTIME_USE_XMA)
    list(APPEND AUDIO_SOURCES
        src/audio/xma_decoder.cpp
    )
endif()

set(INPUT_SOURCES
    src/input/input_handler.cpp
)

# ═══════════════════════════════════════════════════════════════
# LIBRERÍA
# ═══════════════════════════════════════════════════════════════

add_library(${PROJECT_NAME} STATIC
    ${KERNEL_SOURCES}
    ${XAM_SOURCES}
    ${RENDERER_SOURCES}
    ${AUDIO_SOURCES}
    ${INPUT_SOURCES}
)

target_include_directories(${PROJECT_NAME} PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# ═══════════════════════════════════════════════════════════════
# DEPENDENCIAS
# ═══════════════════════════════════════════════════════════════

if(RUNTIME_USE_DX12)
    target_compile_definitions(${PROJECT_NAME} PRIVATE RUNTIME_DX12=1)
    target_link_libraries(${PROJECT_NAME} PRIVATE d3d12 dxgi)
endif()

if(RUNTIME_USE_VULKAN)
    find_package(Vulkan REQUIRED)
    target_compile_definitions(${PROJECT_NAME} PRIVATE RUNTIME_VULKAN=1)
    target_link_libraries(${PROJECT_NAME} PRIVATE Vulkan::Vulkan)
endif()

# ═══════════════════════════════════════════════════════════════
# INSTALACIÓN
# ═══════════════════════════════════════════════════════════════

install(TARGETS ${PROJECT_NAME}
    ARCHIVE DESTINATION lib
)

install(DIRECTORY include/
    DESTINATION include
)

message(STATUS "Xbox Runtime Library configurada")
message(STATUS "  DirectX 12: ${RUNTIME_USE_DX12}")
message(STATUS "  Vulkan: ${RUNTIME_USE_VULKAN}")
message(STATUS "  XMA Audio: ${RUNTIME_USE_XMA}")
