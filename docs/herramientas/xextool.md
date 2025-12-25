# 🔧 xextool

Herramienta para manipular archivos XEX de Xbox 360.

---

## 📥 Instalación

1. Buscar en comunidades de Xbox homebrew
2. Extraer en `C:\tools\XexTool\`

---

## 🔧 Comandos Principales

### Listar información
```bash
xextool.exe -l default.xex
```

### Desencriptar
```bash
xextool.exe -e d default.xex
```

### Descomprimir
```bash
xextool.exe -c u default.xex
```

### Combinar operaciones
```bash
xextool.exe -e d -c u -o clean.xex default.xex
```

---

## 📋 Flags

| Flag | Descripción |
|------|-------------|
| `-l` | Listar información |
| `-e d` | Desencriptar |
| `-c u` | Descomprimir |
| `-o` | Archivo de salida |

---

## 📊 Información de XEX

La salida de `-l` incluye:
- Estado de encriptación
- Estado de compresión
- Media ID
- Title ID
- Base address

---

## 📚 Recursos

- [Guía de Análisis](../tutoriales/guia-analisis.md)
- [API Cleaner](../api/cleaner.md)
