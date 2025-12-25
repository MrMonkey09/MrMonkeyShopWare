# 📦 Tutorial: Extracción de ISO

Guía para extraer contenido de un ISO Xbox 360.

---

## 📋 Requisitos

- Archivo ISO de Xbox 360
- extract-xiso instalado

---

## 🚀 Pasos

### 1. Localizar ISO

```bash
dir *.iso
# game.iso
```

### 2. Extraer

**CLI:**
```bash
python -m src.cli.extract ./game.iso -o ./extracted
```

**GUI:**
1. Iniciar: `python -m src.gui.main`
2. Click en "Extract ISO"
3. Seleccionar archivo ISO

### 3. Verificar

```bash
dir extracted
# default.xex
# data/
# ...
```

---

## 📂 Contenido Típico

```
extracted/
├── default.xex       # Ejecutable principal
├── default.xexp      # Patches (opcional)
├── title/            # Contenido del juego
│   ├── content/
│   └── update/
└── ...
```

---

## 🔍 Encontrar XEX

```bash
# Listar todos los XEX
dir extracted\*.xex /s
```

El principal suele ser `default.xex` en la raíz.

---

## ⚠️ Problemas Comunes

### "Error al extraer ISO"
→ ISO corrupto o extract-xiso mal configurado

### La carpeta está vacía
→ Verificar que el ISO sea formato Xbox (XISO)

---

## 📚 Ver también

- [extract-xiso](../herramientas/extract-xiso.md)
- [Guía de Análisis](./guia-analisis.md)
