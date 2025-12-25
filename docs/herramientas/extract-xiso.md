# 📦 extract-xiso

Herramienta para extraer ISOs de Xbox/Xbox 360.

---

## 📥 Instalación

### Precompilado
1. Descargar de [GitHub Releases](https://github.com/XboxDev/extract-xiso/releases)
2. Extraer en `C:\tools\extract-xiso\`

### Compilar desde código
```bash
git clone https://github.com/XboxDev/extract-xiso.git
cd extract-xiso
# Seguir instrucciones del README
```

---

## 🔧 Uso Básico

```bash
# Extraer ISO
extract-xiso.exe -x game.iso

# Extraer a carpeta específica (workaround: usar cwd)
cd destino
extract-xiso.exe -x C:\path\to\game.iso
```

| Flag | Descripción |
|------|-------------|
| `-x` | Extraer ISO |
| `-l` | Listar contenido |
| `-c` | Crear ISO |

---

## ⚠️ Notas

- El flag `-d` para directorio destino no funciona bien en algunas versiones
- Workaround: cambiar al directorio destino antes de ejecutar

---

## 📚 Recursos

- [GitHub](https://github.com/XboxDev/extract-xiso)
- [Guía de Extracción](../tutoriales/guia-extraccion.md)
