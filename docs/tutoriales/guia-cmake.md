# 🛠️ Tutorial: Compilar Proyectos con CMake

Guía completa para principiantes sobre cómo compilar proyectos C++ usando CMake en Windows.

---

## 📋 ¿Qué es CMake?

**CMake** es un sistema de construcción multiplataforma que genera archivos de proyecto nativos (como los de Visual Studio) a partir de archivos de configuración simples (`CMakeLists.txt`).

```
┌──────────────────────────────────────────────────────────────┐
│  CMakeLists.txt  →  CMake  →  Visual Studio Project  →  EXE │
└──────────────────────────────────────────────────────────────┘
```

---

## 📦 Requisitos Previos

### 1. Visual Studio 2022

Descarga desde: [visualstudio.microsoft.com](https://visualstudio.microsoft.com/es/downloads/)

**Componentes requeridos:**
- ✅ Desarrollo para escritorio con C++
- ✅ Windows 10/11 SDK
- ✅ C++ Clang Compiler for Windows *(si el proyecto lo requiere)*
- ✅ C++ Clang-cl for v143 build tools
- ✅ MSBuild support for LLVM (clang-cl) toolset

### 2. CMake

Descarga desde: [cmake.org/download](https://cmake.org/download/)

> [!TIP]
> Durante la instalación, selecciona **"Add CMake to the system PATH"** para poder usarlo desde la terminal.

### 3. Git

Descarga desde: [git-scm.com](https://git-scm.com/downloads)

---

## 🚀 Proceso de Compilación General

### Paso 1: Clonar el Repositorio

```powershell
git clone --recursive https://github.com/usuario/proyecto.git
cd proyecto
```

> [!IMPORTANT]
> El flag `--recursive` es importante para proyectos que usan submódulos de Git.

### Paso 2: Crear Carpeta de Compilación

```powershell
mkdir build
cd build
```

### Paso 3: Configurar con CMake

**Usando Visual Studio (MSVC):**
```powershell
cmake .. -G "Visual Studio 17 2022" -A x64
```

**Usando Clang (si el proyecto lo requiere):**
```powershell
cmake .. -G "Visual Studio 17 2022" -T ClangCL -A x64
```

**Usando Ninja (más rápido):**
```powershell
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
```

### Paso 4: Compilar

**Con CMake (recomendado):**
```powershell
cmake --build . --config Release
```

**O con Ninja:**
```powershell
ninja
```

---

## 📂 Ejemplo Práctico: Compilar XenonRecomp

### Requisitos Especiales

XenonRecomp **requiere ClangCL**, por lo que debes tener instalados los componentes de Clang en Visual Studio.

### Instalación de ClangCL

1. Abre **Visual Studio Installer**
2. Haz clic en **"Modificar"** junto a tu instalación
3. Ve a **"Componentes individuales"**
4. Busca y selecciona:
   - ✅ C++ Clang Compiler for Windows
   - ✅ C++ Clang-cl for v143 build tools
   - ✅ MSBuild support for LLVM (clang-cl) toolset
5. Haz clic en **"Modificar"** y espera

### Compilación Paso a Paso

```powershell
# 1. Clonar
git clone --recursive https://github.com/hedge-dev/XenonRecomp.git
cd XenonRecomp

# 2. Crear carpeta build
mkdir build
cd build

# 3. Configurar (CON ClangCL)
cmake .. -G "Visual Studio 17 2022" -T ClangCL -A x64

# 4. Compilar
cmake --build . --config Release
```

### Ubicación de los Ejecutables

Después de compilar, encontrarás:
```
XenonRecomp/build/Release/
├── XenonAnalyse.exe
└── XenonRecomp.exe
```

---

## 📖 Referencia de Parámetros CMake

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-G` | Generador (Visual Studio, Ninja, etc.) | `-G "Visual Studio 17 2022"` |
| `-T` | Toolset (MSVC, ClangCL) | `-T ClangCL` |
| `-A` | Arquitectura | `-A x64` o `-A Win32` |
| `-DCMAKE_BUILD_TYPE` | Tipo de build (para Ninja) | `-DCMAKE_BUILD_TYPE=Release` |
| `--config` | Configuración al compilar | `--config Release` |

---

## ⚠️ Errores Comunes y Soluciones

### Error: "No se pueden encontrar las herramientas de compilación para ClangCL"

**Causa:** Falta el toolset ClangCL en Visual Studio.

**Solución:**
1. Abre Visual Studio Installer
2. Modifica tu instalación
3. Añade los componentes de Clang (ver arriba)
4. Borra la carpeta `build` y vuelve a configurar

```powershell
Remove-Item -Recurse -Force build
mkdir build
cd build
cmake .. -G "Visual Studio 17 2022" -T ClangCL -A x64
```

---

### Error: "CMake no encontrado" o "cmake is not recognized"

**Causa:** CMake no está en el PATH.

**Solución:**
1. Reinstala CMake seleccionando "Add to PATH"
2. O añade manualmente: `C:\Program Files\CMake\bin` al PATH del sistema

---

### Error: "MSBuild not found"

**Causa:** Visual Studio no tiene la carga de trabajo de C++.

**Solución:**
1. Abre Visual Studio Installer
2. Modifica tu instalación
3. Selecciona "Desarrollo para escritorio con C++"
4. Instala y reinicia la terminal

---

### Error: "git clone --recursive" falla

**Causa:** Submódulos no accesibles o Git no configurado.

**Solución:**
```powershell
# Si ya clonaste sin --recursive:
git submodule update --init --recursive
```

---

## 🔧 Comandos Útiles

### Limpiar y reconfigurar
```powershell
# Desde la carpeta del proyecto
Remove-Item -Recurse -Force build
mkdir build
cd build
cmake ..
```

### Ver opciones disponibles del proyecto
```powershell
cmake -L ..
```

### Compilar en paralelo (más rápido)
```powershell
cmake --build . --config Release -j 8
```
*(el número 8 es la cantidad de núcleos a usar)*

---

## 📚 Recursos Adicionales

- [Documentación oficial de CMake](https://cmake.org/documentation/)
- [Visual Studio C++ Downloads](https://visualstudio.microsoft.com/vs/features/cplusplus/)
- [XenonRecomp](../herramientas/xenon-recomp.md)
- [Guía de Recompilación](./guia-recompilacion.md)

---

## 🤝 ¿Necesitas Ayuda?

Si tienes problemas:
1. Verifica que todos los requisitos estén instalados
2. Borra la carpeta `build` y reconfigura
3. Abre un issue en GitHub con el error completo

---

<div align="center">

**¡Buena suerte compilando! 🚀**

</div>
