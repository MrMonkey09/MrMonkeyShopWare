# Guía de Recompilación Xbox 360

Esta guía explica el proceso completo para portar juegos de Xbox 360 a PC usando MrMonkeyShopWare y las herramientas de recompilación estática.

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos](#requisitos)
3. [Pipeline Completo](#pipeline-completo)
4. [Paso a Paso](#paso-a-paso)
5. [Troubleshooting](#troubleshooting)

---

## Introducción

### ¿Qué es la recompilación estática?

La recompilación estática convierte el código PowerPC (PPC) de Xbox 360 a código C++ nativo, permitiendo ejecutar juegos sin emulación. Este proceso:

- **Convierte** instrucciones PPC a C++ equivalente
- **Traduce** shaders de Xenos GPU a HLSL/SPIR-V
- **Genera** un ejecutable nativo para Windows/Linux

### Diferencia con emulación

| Aspecto | Emulación | Recompilación |
|---------|-----------|---------------|
| Velocidad | Menor (interpretación en tiempo real) | Mayor (código nativo) |
| Compatibilidad | Más automática | Requiere trabajo por juego |
| Mejoras posibles | Limitadas | Extensas (4K, 120fps, mods) |

---

## Requisitos

### Herramientas Necesarias

| Herramienta | Propósito | Descarga |
|-------------|-----------|----------|
| **XenonRecomp** | Convierte PPC → C++ | [GitHub](https://github.com/hedge-dev/XenonRecomp) |
| **XenosRecomp** | Convierte shaders → HLSL | [GitHub](https://github.com/hedge-dev/XenosRecomp) |
| **XexTool** | Desencripta XEX | [Digiex](https://digiex.net/threads/xextool-6-3-download.9523/) |
| **XGDTool** | Extrae ISO | [GitHub](https://github.com/wiredopposite/XGDTool) |
| **Clang 18+** | Compila C++ | [LLVM](https://releases.llvm.org/) |
| **CMake 3.20+** | Sistema de build | [CMake](https://cmake.org/) |

### Configuración en MrMonkeyShopWare

Abre la GUI y configura las rutas en **Ajustes → Herramientas**:

```
XENON_RECOMP_PATH = C:\tools\XenonRecomp\XenonRecomp.exe
XENOS_RECOMP_PATH = C:\tools\XenosRecomp\XenosRecomp.exe
XEXTOOL_PATH = C:\tools\XexTool\xextool.exe
PPC_CONTEXT_PATH = C:\tools\XenonRecomp\XenonUtils\ppc_context.h
SHADER_COMMON_PATH = C:\tools\XenosRecomp\shader_common.h
```

---

## Pipeline Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIPELINE DE RECOMPILACIÓN                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. EXTRACCIÓN        ISO Xbox 360 → Archivos del juego        │
│         ↓                                                        │
│  2. PREPARACIÓN       XEX → Desencriptar/Descomprimir           │
│         ↓                                                        │
│  3. ANÁLISIS          XenonAnalyse → Jump tables TOML           │
│         ↓                                                        │
│  4. CONFIGURACIÓN     Crear config.toml con offsets             │
│         ↓                                                        │
│  5. RECOMPILACIÓN     XenonRecomp → Código C++                  │
│         ↓                                                        │
│  6. SHADERS           XenosRecomp → HLSL                        │
│         ↓                                                        │
│  7. RUNTIME           Implementar stubs xboxkrnl/XAM            │
│         ↓                                                        │
│  8. BUILD             CMake + Clang → Ejecutable .exe           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### ¿Qué automatiza MrMonkeyShopWare?

| Fase | Estado | Notas |
|------|--------|-------|
| 1. Extracción | ✅ Automático | `extract_iso()` |
| 2. Preparación | ✅ Automático | `clean_xex()` |
| 3. Análisis | ✅ Automático | `analyse_xex()` |
| 4. Configuración | ⚠️ Semi-auto | Template + ajustes manuales |
| 5. Recompilación | ✅ Automático | `run_recompilation()` |
| 6. Shaders | ✅ Automático | `convert_shader()` |
| 7. Runtime | ❌ Manual | Desarrollo por juego |
| 8. Build | ✅ Automático | `build_with_cmake()` |

---

## Paso a Paso

### Fase 1: Obtener archivos del juego

```python
from core import extract_iso, find_main_xex

# Extraer ISO
extracted = extract_iso("SonicUnleashed.iso", "output/")

# Encontrar XEX principal
xex_path = find_main_xex(extracted)
```

**Resultado:** Carpeta con `default.xex` y assets del juego.

---

### Fase 2: Preparar el XEX

```python
from core import clean_xex

# Desencriptar y descomprimir
clean_path = clean_xex(xex_path, "output/clean/")
```

**Comandos xextool equivalentes:**
```bash
xextool.exe -o default.xex -c u -e u
xextool.exe -i default.xex > info.txt
```

---

### Fase 3: Análisis

```python
from core import analyse_xex

# Ejecutar XenonAnalyse
result = analyse_xex(clean_path, "output/analysis/")
print(f"Jump tables: {result.toml_file}")
print(f"Juego: {result.xex_info.display_name}")
```

**Resultado:** `analysis.toml` con jump tables detectadas.

---

### Fase 4: Configuración TOML

```python
from core import XenonRecompConfig, generate_xenon_toml

config = XenonRecompConfig(
    xex_path="default.xex",
    output_dir="ppc",
    switch_table_path="analysis.toml",
    
    # Direcciones r14 (buscar con Binary Ninja/IDA)
    restgprlr_14=0x831B0B40,
    savegprlr_14=0x831B0AF0,
    # ... más direcciones
)

generate_xenon_toml(config, "config.toml")
```

> **⚠️ IMPORTANTE:** Las direcciones r14 son específicas de cada juego.
> Usa Binary Ninja, IDA o Ghidra para encontrarlas.

---

### Fase 5: Recompilación

```python
from core import run_recompilation

result = run_recompilation("config.toml")

if result.success:
    print(f"Archivos C++ generados: {len(result.cpp_files)}")
else:
    print(f"Error: {result.error}")
```

**Resultado:** Carpeta `ppc/` con archivos `.cpp` y `.h`.

---

### Fase 6: Shaders

```python
from core import find_shader_files, batch_convert_shaders

# Buscar shaders en el juego
shaders = find_shader_files("output/game/")

# Convertir todos
success, fail, files = batch_convert_shaders(shaders, "output/hlsl/")
```

---

### Fase 7: Runtime (Manual)

Esta fase requiere desarrollo específico para cada juego:

1. **Implementar stubs de xboxkrnl** - Funciones del kernel
2. **Implementar stubs de XAM** - Funciones de alto nivel
3. **Crear renderer** - DirectX 12 o Vulkan
4. **Conectar audio** - Sistema de sonido
5. **Manejo de input** - Controles

**Referencia:** Ver [Unleashed Recompiled](https://github.com/hedge-dev/UnleashedRecomp) como ejemplo.

---

### Fase 8: Build

```python
from core import generate_cmakelists, build_with_cmake

# Generar CMakeLists.txt
generate_cmakelists("MiJuego", "ppc/", "CMakeLists.txt")

# Compilar
result = build_with_cmake("proyecto/", build_type="Release")

if result.success:
    print(f"Ejecutable: {result.executable_path}")
```

**O con Clang directo:**
```bash
clang++ -o MiJuego.exe ppc/*.cpp -std=c++20 -O2 -mavx
```

---

## Troubleshooting

### Error: "Unrecognized instruction"

**Causa:** XenonRecomp no implementa esa instrucción PPC.

**Solución:**
1. Buscar en [Issues de XenonRecomp](https://github.com/hedge-dev/XenonRecomp/issues)
2. Revisar forks con implementaciones adicionales
3. Implementar la instrucción en `recompiler.cpp`

---

### Error: "Missing function boundary"

**Causa:** XenonAnalyse no detectó los límites de una función.

**Solución:** Agregar manualmente en `config.toml`:
```toml
functions = [
    { address = 0x824E7EF0, size = 0x98 },
]
```

---

### Error: "r14 addresses not found"

**Causa:** Las direcciones de funciones de registro no están configuradas.

**Solución:**
1. Abrir XEX en Binary Ninja/IDA
2. Buscar patrones: `e9 c1 ff 68` (restgprlr_14)
3. Agregar direcciones al TOML

---

### El juego compila pero crashea

**Causas comunes:**
- Stubs de xboxkrnl faltantes
- Shaders no convertidos
- Endianness incorrecta

**Debug:**
1. Usar build Debug en lugar de Release
2. Agregar logging en funciones críticas
3. Comparar con ejecución en Xenia

---

## Proyectos de Ejemplo

| Proyecto | Estado | Link |
|----------|--------|------|
| Unleashed Recompiled | ✅ Completo | [GitHub](https://github.com/hedge-dev/UnleashedRecomp) |
| Fable2Recomp | 🔧 En desarrollo | [GitHub](https://github.com/Fable2Recomp/Fable2Recomp) |
| MarathonRecomp | 🔧 En desarrollo | [GitHub](https://github.com/ga2mer/MarathonRecomp) |

---

## Recursos Adicionales

- [XenonRecomp Discussion #149](https://github.com/hedge-dev/XenonRecomp/discussions/149) - Tutorial paso a paso
- [Videos tutoriales](https://youtu.be/w-1Pgn5V3wY) - XenonRecomp en video
- [Xenia Emulator](https://github.com/xenia-project/xenia) - Referencia técnica Xbox 360
- [Free60 Wiki](https://free60.org) - Documentación formato XEX
