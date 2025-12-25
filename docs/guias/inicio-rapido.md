# ⚡ Inicio Rápido

Guía de 5 minutos para empezar a usar MrMonkeyShopWare.

---

## 🎯 Objetivo

Al final de esta guía podrás:
1. Hacer dump de un disco Xbox 360
2. Extraer el contenido del ISO
3. Analizar el archivo XEX principal

---

## 📋 Prerrequisitos

- [x] MrMonkeyShopWare instalado ([ver guía](./primeros-pasos.md))
- [x] Herramientas externas configuradas
- [x] Disco original Xbox 360 insertado

---

## 🚀 Flujo Rápido con GUI

### 1. Iniciar la GUI

```bash
python -m src.gui.main
```

### 2. Dump del Disco
1. Haz clic en **"Dump Disc"**
2. Ingresa la letra de tu unidad (ej: `E:`)
3. Espera a que complete el dump
4. El ISO se guardará en `%TEMP%\x360dump\game.iso`

### 3. Extraer ISO
1. Haz clic en **"Extract ISO"**
2. Selecciona el archivo `game.iso`
3. El contenido se extraerá en una carpeta junto al ISO

### 4. Analizar XEX
1. Haz clic en **"Analyse XEX"**
2. Selecciona `default.xex` de la carpeta extraída
3. Se generarán `analysis.toml` y `analysis.json`

---

## 💻 Flujo Rápido con CLI

```bash
# 1. Dump del disco (E: es tu unidad)
python -m src.cli.dump E: --out ./game.iso

# 2. Extraer ISO
python -m src.cli.extract ./game.iso -o ./extracted

# 3. Analizar XEX
python -m src.cli.analyse ./extracted/default.xex
```

---

## 📊 Resultado

Después del análisis tendrás:

```
%TEMP%\x360dump\
├── game.iso              # ISO del disco
├── extracted/            # Contenido extraído
│   ├── default.xex       # Ejecutable principal
│   └── ...               # Otros archivos
└── analysis/
    ├── analysis.toml     # Datos del análisis
    └── analysis.json     # Versión JSON
```

---

## ▶️ Siguiente Paso

- [Tutorial: Pipeline Completo](./tutoriales/pipeline-completo.md)
- [Guía de Dump](./tutoriales/guia-dump.md)
- [Referencia de API](./api/README.md)
