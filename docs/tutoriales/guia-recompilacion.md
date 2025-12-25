# 🔄 Tutorial: Recompilación

Guía para recompilar código Xbox 360 a C++ con XenonRecomp.

---

## 📋 Requisitos

- `analysis.toml` generado por XenonAnalyse
- XenonRecomp compilado
- `ppc_context.h` (parte de XenonUtils)

---

## 🚀 Pasos

### 1. Generar project.toml

```bash
python -m src.cli.tomlgen --out ./output
```

Esto copia `analysis.toml` como `project.toml`.

### 2. Validar TOML

```bash
# El comando tomlgen ya valida automáticamente
# Si ves "✅ project.toml válido", está listo
```

### 3. Ejecutar XenonRecomp

```bash
XenonRecomp.exe ./output/project.toml C:\tools\XenonRecomp\XenonUtils\ppc_context.h
```

### 4. Compilar código C++

El código generado estará en `output/build/`.

Necesitarás un compilador C++ (MSVC, clang, gcc) para compilar.

---

## 📂 Salida

```
output/
├── project.toml       # Configuración
└── build/
    ├── functions.cpp  # Código recompilado
    ├── functions.h    # Headers
    └── ...
```

---

## ⚠️ Problemas Comunes

### "XenonRecomp crashea"
→ Verificar rutas absolutas en project.toml
→ Ejecutar desde la carpeta del TOML

### "Código no compila"
→ El código generado puede necesitar ajustes manuales

---

## 🔧 Siguiente Paso

Después de tener el código C++, necesitas:

1. Crear un proyecto con un runtime básico
2. Implementar llamadas a sistema/librerías
3. Linkear con un motor gráfico (para shaders)

Este paso está fuera del alcance actual del proyecto.

---

## 📚 Ver también

- [XenonRecomp](../herramientas/xenon-recomp.md)
- [Docker](../docker.md) (para compilar XenonRecomp)
