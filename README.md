# 🐵 MrMonkeyShopWare

> **Kit de Herramientas para Portar Juegos de Xbox 360 a PC Nativo**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![Platform: Windows](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

---

## 📖 Descripción

**MrMonkeyShopWare** es una suite de herramientas diseñada para facilitar el proceso de portar juegos de Xbox 360 a PC nativo. Proporciona una interfaz gráfica moderna y una línea de comandos completa para gestionar todo el flujo de trabajo: desde el dump del disco hasta la organización de archivos para recompilación.

### ¿Para quién es?

- 🎮 **Desarrolladores de ports** que trabajan en proyectos de recompilación
- 🔬 **Investigadores** que analizan ejecutables XEX
- 📦 **Preservacionistas** que mantienen backups organizados de sus juegos

---

## ✨ Características Principales

| Característica | Descripción |
|----------------|-------------|
| 📀 **Dump de Discos** | Crea imágenes ISO desde discos Xbox 360 físicos |
| 📦 **Extracción de ISOs** | Extrae el contenido completo de imágenes ISO |
| 🔬 **Análisis de XEX** | Detecta metadata, librerías y entry points |
| 📁 **Workspaces Organizados** | Carpeta por juego con estructura estandarizada |
| 🔄 **Sincronización** | Centraliza archivos dispersos en el workspace |
| 💾 **Base de Datos** | Registro de todos los juegos procesados |
| 💿 **USB Xbox 360** | Detecta juegos en pendrives formateados para Xbox |
| 🖥️ **Disco Virtual** | Trabaja con ISOs montadas directamente |

---

## 🚀 Instalación

### Requisitos

- **Python 3.11+**
- **Windows 10/11**
- **Herramientas externas** (opcionales):
  - [DiscImageCreator](https://github.com/saramibreak/DiscImageCreator) - Para dump de discos
  - [extract-xiso](https://github.com/XboxDev/extract-xiso) - Para extracción de ISOs
  - [XexTool](https://github.com/) - Para análisis de XEX

### Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/MrMonkey09/MrMonkeyShopWare.git
cd MrMonkeyShopWare

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Uso

### Interfaz Gráfica (GUI)

```bash
cd src
python -m gui.app
```

La GUI ofrece:
- Selector de tipo de entrada (Disco, ISO, Carpeta, USB)
- Vista de historial de juegos procesados
- Detalle de juego con checklist de archivos
- Visor de estructura de archivos TOML/JSON
- Configuración de herramientas externas

### Línea de Comandos (CLI)

```bash
cd src
python -m cli.main --help
```

#### Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `analyse <xex>` | Analiza un archivo XEX y crea workspace |
| `extract <iso>` | Extrae contenido de un ISO |
| `dump <drive>` | Crea ISO desde disco físico |
| `pipeline <drive>` | Pipeline completo (dump → extract → analyse) |
| `scan-usb <drive>` | Detecta juegos en USB Xbox 360 |
| `list` | Lista todos los workspaces |
| `info <title_id>` | Muestra información de un juego |
| `sync <title_id>` | Sincroniza archivos al workspace |
| `db list` | Lista juegos en base de datos |

#### Ejemplos

```bash
# Analizar un XEX
python -m cli.main analyse "C:/Games/default.xex"

# Listar workspaces
python -m cli.main list

# Ver info de un juego
python -m cli.main info 4E4D07F5

# Escanear USB Xbox 360
python -m cli.main scan-usb E:
```

---

## 📁 Estructura de Workspaces

Cada juego procesado se organiza automáticamente:

```
~/MrMonkeyShopWare/ports/
└── GameName [TitleID]/
    ├── info.json          # Metadata del juego
    ├── notes.md           # Notas del port
    ├── default.xex        # XEX principal (si sincronizado)
    ├── game.iso           # ISO original (si sincronizado)
    ├── analysis/          # Archivos de análisis
    │   ├── analysis.toml
    │   └── analysis.json
    ├── extracted/         # Contenido del ISO
    ├── cleaned/           # XEX limpios
    └── recompiled/        # Código recompilado
```

---

## 📚 Documentación

Para documentación completa, visita:

- 📖 [Índice de Documentación](docs/index.md)
- 🚀 [Primeros Pasos](docs/guias/primeros-pasos.md)
- 🏗️ [Arquitectura](docs/arquitectura/arquitectura.md)
- 📘 [Referencia API](docs/api/README.md)
- 📝 [Tutoriales](docs/tutoriales/)

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor lee nuestra guía:

- 📋 [Guía de Contribución](docs/desarrollo/CONTRIBUIR.md)
- 📜 [Código de Conducta](docs/desarrollo/CODIGO_DE_CONDUCTA.md)
- 🎨 [Guía de Estilo](docs/desarrollo/GUIA_DE_ESTILO.md)

### Cómo Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

---

## 📊 Estado del Proyecto

| Componente | Estado |
|------------|--------|
| Core | ✅ Estable |
| CLI | ✅ Completo |
| GUI | ✅ Funcional |
| Documentación | 🔄 En progreso |
| Tests | 🔄 Básicos |

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- Comunidad de Xbox 360 modding
- Desarrolladores de herramientas como XexTool, extract-xiso, DiscImageCreator
- Todos los colaboradores del proyecto

---

<p align="center">
  <strong>Hecho con ❤️ por MrMonkey y la comunidad</strong>
</p>
