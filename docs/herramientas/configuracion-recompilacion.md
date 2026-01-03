# Configuración de Herramientas de Recompilación

Guía para instalar y configurar todas las herramientas necesarias para el pipeline de recompilación Xbox 360.

## Descarga de Herramientas

### 1. XenonRecomp (Recompilador Principal)

```bash
# Clonar con submódulos
git clone --recursive https://github.com/hedge-dev/XenonRecomp.git

# O usar fork con mejoras
git clone --recursive https://github.com/testdriveupgrade/XenonRecompUnlim.git
```

**Compilar:**
```bash
# Windows (Visual Studio 2022 + Clang)
cmake -B build -G "Visual Studio 17 2022" -T ClangCL
cmake --build build --config Release
```

**Resultado:** `build/XenonRecomp/Release/XenonRecomp.exe`

---

### 2. XenosRecomp (Shaders)

```bash
git clone --recursive https://github.com/hedge-dev/XenosRecomp.git
cmake -B build -G "Visual Studio 17 2022"
cmake --build build --config Release
```

**Resultado:** `build/Release/XenosRecomp.exe`

---

### 3. XexTool

1. Descargar de [Digiex](https://digiex.net/threads/xextool-6-3-download.9523/)
2. Extraer a `C:\tools\XexTool\`

---

### 4. XGDTool (Extractor ISO)

```bash
git clone https://github.com/wiredopposite/XGDTool.git
```

O descargar release precompilado.

---

### 5. Clang/LLVM

1. Descargar de [LLVM Releases](https://releases.llvm.org/)
2. Instalar con opción "Add to PATH"
3. Verificar: `clang --version`

---

### 6. CMake

1. Descargar de [cmake.org](https://cmake.org/download/)
2. Instalar con opción "Add to PATH"
3. Verificar: `cmake --version`

---

## Estructura Recomendada

```
C:\tools\
├── XenonRecomp\
│   ├── build\
│   │   └── XenonRecomp\Release\XenonRecomp.exe
│   └── XenonUtils\
│       └── ppc_context.h
├── XenosRecomp\
│   ├── build\Release\XenosRecomp.exe
│   └── shader_common.h
├── XexTool\
│   └── xextool.exe
└── XGDTool\
    └── XGDTool.exe
```

---

## Configuración en MrMonkeyShopWare

### Opción 1: GUI

1. Abrir MrMonkeyShopWare
2. Ir a **Ajustes** (icono engranaje)
3. Pestaña **Herramientas**
4. Configurar rutas:

| Campo | Ruta |
|-------|------|
| XenonRecomp | `C:\tools\XenonRecomp\build\XenonRecomp\Release\XenonRecomp.exe` |
| XenosRecomp | `C:\tools\XenosRecomp\build\Release\XenosRecomp.exe` |
| XexTool | `C:\tools\XexTool\xextool.exe` |
| PPC Context | `C:\tools\XenonRecomp\XenonUtils\ppc_context.h` |
| Shader Common | `C:\tools\XenosRecomp\shader_common.h` |

### Opción 2: settings.json

Editar `~/.mrmonkeyshopware/settings.json`:

```json
{
  "tools": {
    "XENON_RECOMP_PATH": "C:\\tools\\XenonRecomp\\build\\XenonRecomp\\Release\\XenonRecomp.exe",
    "XENOS_RECOMP_PATH": "C:\\tools\\XenosRecomp\\build\\Release\\XenosRecomp.exe",
    "XEXTOOL_PATH": "C:\\tools\\XexTool\\xextool.exe",
    "PPC_CONTEXT_PATH": "C:\\tools\\XenonRecomp\\XenonUtils\\ppc_context.h",
    "SHADER_COMMON_PATH": "C:\\tools\\XenosRecomp\\shader_common.h"
  }
}
```

### Opción 3: Variables de Entorno

```batch
set XENON_RECOMP_PATH=C:\tools\XenonRecomp\build\XenonRecomp\Release\XenonRecomp.exe
set XENOS_RECOMP_PATH=C:\tools\XenosRecomp\build\Release\XenosRecomp.exe
```

---

## Verificación

```python
from core import (
    check_xenon_recomp_available, 
    check_xenos_recomp_available,
    get_build_requirements
)

# Verificar herramientas
print(f"XenonRecomp: {check_xenon_recomp_available()}")
print(f"XenosRecomp: {check_xenos_recomp_available()}")

# Verificar build tools
reqs = get_build_requirements()
print(f"Clang: {reqs['clang']['available']} - {reqs['clang']['version']}")
print(f"CMake: {reqs['cmake']['available']} - {reqs['cmake']['version']}")
```

---

## Herramientas Opcionales

### Binary Ninja / IDA Pro / Ghidra

Para análisis manual de binarios (encontrar direcciones r14, setjmp, etc.):

- **Binary Ninja** (comercial): [binary.ninja](https://binary.ninja/)
- **IDA Pro** (comercial): [hex-rays.com](https://hex-rays.com/)
- **Ghidra** (gratuito): [ghidra-sre.org](https://ghidra-sre.org/)

### DirectX Shader Compiler (DXC)

Para compilar shaders HLSL a DXIL/SPIR-V:

```bash
# Windows SDK incluye DXC
# O descargar de GitHub
git clone https://github.com/microsoft/DirectXShaderCompiler.git
```
