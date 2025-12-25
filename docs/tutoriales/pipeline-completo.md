# 🔄 Tutorial: Pipeline Completo

Guía paso a paso para portar un juego de Xbox 360 a PC.

---

## 🚀 Método Rápido: Pipeline Automatizado

> [!TIP]
> El nuevo comando `pipeline` encadena todos los pasos automáticamente.

### Desde disco físico

```bash
python -m src.cli.pipeline -d E: -o ./output
```

### Desde ISO existente

```bash
python -m src.cli.pipeline -i game.iso -o ./output
```

### Desde XEX existente

```bash
python -m src.cli.pipeline -x ./extracted/default.xex -o ./output
```

**Resultado**: Todo el proceso en un solo comando → `output/project/project.toml`

---

## 📋 Método Manual (Paso a Paso)

### Lo que necesitas

- Disco original Xbox 360
- Unidad óptica compatible
- Herramientas configuradas ([ver requisitos](../guias/requisitos.md))

---

### Paso 1: Dump del Disco

```bash
python -m src.cli.dump E: --out ./game.iso
```

**Tiempo**: 15-30 minutos | **Resultado**: `game.iso`

---

### Paso 2: Extraer ISO

```bash
python -m src.cli.extract ./game.iso -o ./extracted
```

**Tiempo**: 2-5 minutos | **Resultado**: Carpeta `extracted/`

---

### Paso 3: Localizar XEX Principal

```bash
dir extracted\*.xex /s
```

Generalmente el principal es `default.xex`.

---

### Paso 4: Analizar XEX

```bash
python -m src.cli.analyse ./extracted/default.xex
```

**Tiempo**: 1-3 minutos | **Resultado**: `analysis.toml` + `analysis.json`

---

### Paso 5: Generar Project TOML

```bash
python -m src.cli.tomlgen --out ./output
```

**Resultado**: `output/project.toml`

---

### Paso 6: Recompilar (XenonRecomp)

```bash
XenonRecomp.exe ./output/project.toml ./ppc_context.h
```

**Resultado**: Código C++ en `output/build/`

---

## 📊 Resumen del Pipeline

```
Disco → game.iso → extracted/ → default.xex → analysis.toml → project.toml → C++
```

---

## 💡 Tips

1. **Verificar cada paso** antes de continuar al siguiente
2. **Guardar los logs** por si necesitas debug
3. **No eliminar temporales** hasta confirmar que todo funciona

---

## 📚 Ver también

- [API del Pipeline](../api/pipeline.md)
- [Guía de Dump](./guia-dump.md)
- [Guía de Extracción](./guia-extraccion.md)
- [Guía de Análisis](./guia-analisis.md)
