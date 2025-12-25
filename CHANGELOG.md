# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [No Publicado]

### Añadido
- Estructura de proyecto profesional reorganizada
- Documentación completa en español
- Configuración de CI/CD con GitHub Actions
- Plantillas de issues y pull requests
- Configuración de pyproject.toml para herramientas modernas

### Cambiado
- Código fuente movido a `src/`
- Configuración Docker movida a `docker/`
- Scripts de utilidad movidos a `scripts/`

---

## [0.1.0] - 2024-XX-XX

### Añadido
- Módulo `core/dumper.py` - Volcado de discos Xbox 360
- Módulo `core/extractor.py` - Extracción de ISOs
- Módulo `core/analyser.py` - Análisis de archivos XEX
- Módulo `core/cleaner_xex.py` - Limpieza de XEX
- Módulo `core/toml_generator.py` - Generación de TOML
- Interfaz CLI básica
- Interfaz GUI con Tkinter
- Soporte Docker para XenonRecomp

---

## Tipos de cambios

- **Añadido** para nuevas funcionalidades.
- **Cambiado** para cambios en funcionalidades existentes.
- **Obsoleto** para funcionalidades que serán eliminadas.
- **Eliminado** para funcionalidades eliminadas.
- **Corregido** para correcciones de bugs.
- **Seguridad** para vulnerabilidades corregidas.
