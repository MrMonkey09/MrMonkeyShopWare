# 🔍 Tutorial: Análisis de XEX

Guía para analizar archivos XEX con XenonAnalyse.

---

## 📋 Requisitos

- Archivo XEX (extraído de un ISO)
- xextool instalado (para limpieza)
- XenonAnalyse instalado

---

## 🚀 Pasos

### 1. Localizar XEX

```bash
# Generalmente en la carpeta extraída
dir extracted\default.xex
```

### 2. Analizar

**CLI:**
```bash
python -m src.cli.analyse ./extracted/default.xex
```

**GUI:**
1. Iniciar: `python -m src.gui.main`
2. Click en "Analyse XEX"
3. Seleccionar archivo XEX

### 3. Revisar salida

El proceso:
1. Limpia el XEX (desencripta/descomprime) si es necesario
2. Ejecuta XenonAnalyse
3. Genera TOML y JSON

---

## 📂 Archivos Generados

```
%TEMP%\x360dump\analysis\
├── default_clean.xex    # XEX limpio (si fue necesario)
├── analysis.toml        # Salida de XenonAnalyse
└── analysis.json        # Versión JSON
```

---

## 📊 Contenido del Analysis

```toml
[info]
title = "Nombre del Juego"
media_id = "..."

[functions]
# Lista de funciones detectadas

[switch_tables]
# Tablas de switch
```

---

## ⚠️ Problemas Comunes

### "XenonAnalyse falló"
→ XEX corrupto o no limpio correctamente

### TOML vacío
→ XEX puede no ser compatible

---

## 📚 Ver también

- [xextool](../herramientas/xextool.md)
- [XenonRecomp](../herramientas/xenon-recomp.md)
