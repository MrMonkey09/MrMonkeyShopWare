# 📋 Requisitos del Sistema

## 💻 Hardware

### Mínimo
- **CPU**: Intel Core i3 / AMD Ryzen 3 o superior
- **RAM**: 8 GB
- **Almacenamiento**: 50 GB libres (para ISOs temporales)
- **Unidad óptica**: Compatible con discos DVD-DL (para dump)

### Recomendado
- **CPU**: Intel Core i5 / AMD Ryzen 5 o superior
- **RAM**: 16 GB
- **Almacenamiento**: SSD con 100+ GB libres
- **Unidad óptica**: Unidad verificada por redump.org

---

## 🖥️ Software

### Sistema Operativo
- **Windows 10** (64-bit) - Mínimo
- **Windows 11** (64-bit) - Recomendado

> ⚠️ Linux y macOS tienen soporte parcial (sin dump de discos)

### Python
- **Python 3.11+** requerido
- Tkinter incluido (para GUI)

### Dependencias Python
```
psutil
pywin32
toml
```

---

## 🔧 Herramientas Externas

| Herramienta | Versión | Obligatorio | Fuente |
|-------------|---------|-------------|--------|
| DiscImageCreator | Latest | ✅ Para dump | [redump.org](http://redump.org/discimagecreator/) |
| extract-xiso | Latest | ✅ Para extracción | [GitHub](https://github.com/XboxDev/extract-xiso) |
| xextool | Latest | ✅ Para limpieza XEX | Comunidad Xbox |
| XenonAnalyse | Latest | ✅ Para análisis | [GitHub](https://github.com/hedge-dev/XenonRecomp) |
| XenonRecomp | Latest | 🔶 Para recompilación | [GitHub](https://github.com/hedge-dev/XenonRecomp) |

---

## 📀 Unidades Ópticas Compatibles

Para dump de discos Xbox 360, necesitas una unidad compatible:

### Recomendadas (Verificadas)
- LG GGC-H20L
- Asus BW-16D1HT
- LiteOn iHAS124

### Verificar compatibilidad
Consulta la [lista de unidades verificadas](http://wiki.redump.org/index.php?title=Dumping_Guides/Optical_Disc_Drives) en redump.org.

---

## 🐳 Docker (Opcional)

Para usar Docker con XenonRecomp en Linux:

- Docker Desktop 4.0+
- Docker Compose 2.0+
- 10 GB de espacio para imagen

---

## ⚡ Rendimiento

| Operación | Tiempo estimado |
|-----------|-----------------|
| Dump de disco | 15-30 min |
| Extracción ISO | 2-5 min |
| Análisis XEX | 1-3 min |
| Limpieza XEX | < 1 min |
