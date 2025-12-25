# 🔄 XenonRecomp

Suite de herramientas para recompilar código Xbox 360 a C++.

---

## 📦 Componentes

| Herramienta | Descripción |
|-------------|-------------|
| **XenonAnalyse** | Analiza XEX y genera TOML con metadata |
| **XenonRecomp** | Recompila código PowerPC a C++ |

---

## 📥 Instalación

### Precompilado
Buscar releases en repositorios de la comunidad.

### Compilar desde código

> [!IMPORTANT]
> XenonRecomp **requiere ClangCL**. Debes instalarlo en Visual Studio antes de compilar.

#### Requisitos Previos

1. **Visual Studio 2022** con estos componentes:
   - ✅ Desarrollo para escritorio con C++
   - ✅ Windows 10/11 SDK
   - ✅ C++ Clang Compiler for Windows
   - ✅ C++ Clang-cl for v143 build tools
   - ✅ MSBuild support for LLVM (clang-cl) toolset

2. **CMake** (descarga de [cmake.org](https://cmake.org/download/))

3. **Git** (descarga de [git-scm.com](https://git-scm.com/))

#### Instalar componentes de Clang en Visual Studio

1. Abre **Visual Studio Installer**
2. Busca tu instalación y haz clic en **"Modificar"**
3. Ve a **"Componentes individuales"**
4. Busca y marca los componentes de Clang listados arriba
5. Haz clic en **"Modificar"** y espera

#### Compilar con Visual Studio (Recomendado)

```powershell
# Clonar repositorio
git clone --recursive https://github.com/hedge-dev/XenonRecomp.git
cd XenonRecomp

# Crear directorio build
mkdir build
cd build

# Configurar con CMake (¡ClangCL es obligatorio!)
cmake .. -G "Visual Studio 17 2022" -T ClangCL -A x64

# Compilar
cmake --build . --config Release
```

Los ejecutables estarán en: `build/Release/`

#### Compilar con Ninja (Alternativo)

```bash
mkdir build && cd build
cmake .. -G Ninja -DCMAKE_BUILD_TYPE=Release
ninja
```

#### Usar Docker (Sin necesidad de configurar nada)

```bash
cd docker
docker-compose up -d
```

> [!TIP]
> Para una guía completa de CMake, consulta [Guía de CMake](../tutoriales/guia-cmake.md)

---

## 🔧 XenonAnalyse

```bash
XenonAnalyse.exe <input.xex> <output.toml>
```

**Entrada**: XEX limpio (desencriptado/descomprimido)
**Salida**: TOML con información del ejecutable

---

## 🔧 XenonRecomp

```bash
XenonRecomp.exe <project.toml> <ppc_context.h>
```

**Entrada**: TOML de configuración
**Salida**: Código C++ recompilado

---

## 📂 ppc_context.h

Archivo header necesario para la recompilación, ubicado en:
```
XenonRecomp/XenonUtils/ppc_context.h
```

---

## ⚠️ Problemas Comunes

### Crash con código 3221226505
→ Verificar rutas absolutas en TOML
→ Ejecutar desde el directorio del TOML

### Error de compilación "lzxDecompress"
→ Aplicar parche (ver Dockerfile)

---

## 📚 Recursos

- [GitHub](https://github.com/hedge-dev/XenonRecomp)
- [Docker](../docker.md)
- [Guía de Recompilación](../tutoriales/guia-recompilacion.md)
