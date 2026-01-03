# 📚 MrMonkeyShopWare - Índice de Documentación

> **Kit de Herramientas para Portar Juegos de Xbox 360 a PC Nativo**

¡Bienvenido a la documentación oficial de MrMonkeyShopWare! Este índice proporciona una guía completa de toda la documentación del proyecto, organizada para desarrolladores, colaboradores y mantenedores.

---

## 🚀 Navegación Rápida

| Documento | Descripción | Audiencia |
|-----------|-------------|-----------|
| [Primeros Pasos](./guias/primeros-pasos.md) | Instalación y primeros pasos | Nuevos Usuarios |
| [🆕 Recompilación Xbox 360](./guias/recompilacion-xbox360.md) | Pipeline completo de recompilación | Colaboradores |
| [Arquitectura](./arquitectura/arquitectura.md) | Diseño del sistema y componentes | Desarrolladores |
| [Contribuir](./desarrollo/CONTRIBUIR.md) | Cómo contribuir al proyecto | Colaboradores |
| [Referencia API](./api/README.md) | Documentación de módulos | Desarrolladores |
| [Changelog](../CHANGELOG.md) | Historial de versiones | Todos |

---

## � Estructura de la Documentación

```
docs/
├── 📄 index.md                      # Este archivo
│
├── 📂 guias/                        # 👋 Primeros pasos y guías básicas
│   ├── primeros-pasos.md
│   ├── requisitos.md
│   ├── inicio-rapido.md
│   ├── recompilacion-xbox360.md     # 🆕 Pipeline de recompilación
│   └── faq.md
│
├── 📂 arquitectura/                 # 🏗️ Diseño del sistema
│   ├── arquitectura.md
│   ├── decisiones-diseno.md
│   └── flujo-datos.md
│
├── 📂 modulos/                      # 📦 Documentación por módulo
│   ├── core.md
│   ├── cli.md
│   ├── gui.md
│   ├── gui-catalogo-vistas.md
│   └── utilidades.md
│
├── 📂 api/                          # 📘 Referencia de API
│   ├── README.md
│   ├── dumper.md
│   ├── extractor.md
│   ├── analyser.md
│   ├── cleaner.md
│   ├── database.md
│   ├── pipeline.md
│   ├── xex-parser.md                # Parser de metadata XexTool
│   ├── toml-generator.md
│   └── modulos-recompilacion.md     # 🆕 API de recompilación
│
├── 📂 desarrollo/                   # 🛠️ Guías de desarrollo
│   ├── CONTRIBUIR.md
│   ├── CODIGO_DE_CONDUCTA.md
│   ├── DESARROLLO.md
│   ├── FLUJO_GIT.md                 # 🆕 Flujo de trabajo Git
│   ├── PRUEBAS.md
│   └── GUIA_DE_ESTILO.md
│
├── 📂 operaciones/                  # 🚢 Despliegue y operaciones
│   ├── DESPLIEGUE.md
│   ├── docker.md
│   ├── configuracion.md
│   └── solucion-problemas.md
│
├── 📂 proyecto/                     # 📊 Gestión del proyecto
│   ├── ESTUDIO.md                   # 🆕 Guía Maestra de Recompilación
│   ├── VISION.md
│   ├── ROADMAP.md
│   ├── SEGURIDAD.md
│   └── SOPORTE.md
│
├── 📂 tutoriales/                   # 📚 Tutoriales paso a paso
│   ├── pipeline-completo.md
│   ├── guia-dump.md
│   ├── guia-extraccion.md
│   ├── guia-analisis.md
│   ├── guia-recompilacion.md
│   ├── guia-cmake.md
│   ├── guia-respaldos.md            # Usar respaldos existentes (USB/ISO)
│   └── primer-proyecto-recompilacion.md  # 🆕 Tu primer proyecto de recomp
│
└── 📂 herramientas/                 # 🔧 Herramientas externas
│   ├── disc-image-creator.md
│   ├── extract-xiso.md
│   ├── xextool.md
│   ├── xenon-recomp.md
│   └── configuracion-recompilacion.md  # 🆕 Configurar herramientas recomp
│
└── 📂 capturas/                     # 📸 Capturas de pantalla
    └── (imágenes para documentación)
```

---

## 📖 Contenido por Sección

### 1. 👋 Guías de Inicio
- [primeros-pasos.md](./guias/primeros-pasos.md) - Guía completa de instalación
- [requisitos.md](./guias/requisitos.md) - Requisitos del sistema y dependencias
- [inicio-rapido.md](./guias/inicio-rapido.md) - Tutorial de inicio en 5 minutos
- [faq.md](./guias/faq.md) - Preguntas frecuentes
- 🆕 [recompilacion-xbox360.md](./guias/recompilacion-xbox360.md) - **Pipeline de recompilación Xbox 360**

---

### 2. 🏗️ Arquitectura y Diseño
- [arquitectura.md](./arquitectura/arquitectura.md) - Arquitectura de alto nivel
- [decisiones-diseno.md](./arquitectura/decisiones-diseno.md) - ADRs (Decisiones de Arquitectura)
- [flujo-datos.md](./arquitectura/flujo-datos.md) - Diagramas de flujo de datos

---

### 3. 📦 Documentación de Módulos
- [core.md](./modulos/core.md) - Módulo core
- [cli.md](./modulos/cli.md) - Interfaz CLI
- [gui.md](./modulos/gui.md) - Interfaz GUI
- [utilidades.md](./modulos/utilidades.md) - Utilidades

---

### 4. 📘 Referencia de API
- [README.md](./api/README.md) - Índice de API
- [dumper.md](./api/dumper.md) - API de volcado
- [extractor.md](./api/extractor.md) - API de extracción
- [analyser.md](./api/analyser.md) - API de análisis
- [cleaner.md](./api/cleaner.md) - API de limpieza
- [toml-generator.md](./api/toml-generator.md) - API de TOML
- 🆕 [modulos-recompilacion.md](./api/modulos-recompilacion.md) - **API de recompilación**

---

### 5. 🛠️ Desarrollo
- [CONTRIBUIR.md](./desarrollo/CONTRIBUIR.md) - Guía de contribución
- [CODIGO_DE_CONDUCTA.md](./desarrollo/CODIGO_DE_CONDUCTA.md) - Código de conducta
- [DESARROLLO.md](./desarrollo/DESARROLLO.md) - Configuración de entorno
- [PRUEBAS.md](./desarrollo/PRUEBAS.md) - Guía de testing
- [GUIA_DE_ESTILO.md](./desarrollo/GUIA_DE_ESTILO.md) - Estilo de código

---

### 6. 🚢 Operaciones
- [DESPLIEGUE.md](./operaciones/DESPLIEGUE.md) - Procedimientos de despliegue
- [docker.md](./operaciones/docker.md) - Configuración Docker
- [configuracion.md](./operaciones/configuracion.md) - Opciones de configuración
- [solucion-problemas.md](./operaciones/solucion-problemas.md) - Troubleshooting

---

### 7. 📊 Gestión del Proyecto
- [ESTUDIO.md](./proyecto/ESTUDIO.md) - 🆕 Guía Maestra: Recompilación Estática Xbox 360 → PC
- [VISION.md](./proyecto/VISION.md) - Visión y objetivos
- [ROADMAP.md](./proyecto/ROADMAP.md) - Planes futuros
- [SEGURIDAD.md](./proyecto/SEGURIDAD.md) - Políticas de seguridad
- [SOPORTE.md](./proyecto/SOPORTE.md) - Cómo obtener ayuda

---

### 8. 📚 Tutoriales
- [pipeline-completo.md](./tutoriales/pipeline-completo.md) - Flujo completo
- [guia-dump.md](./tutoriales/guia-dump.md) - Volcado de discos
- [guia-extraccion.md](./tutoriales/guia-extraccion.md) - Extracción de ISO
- [guia-analisis.md](./tutoriales/guia-analisis.md) - Análisis de XEX
- [guia-recompilacion.md](./tutoriales/guia-recompilacion.md) - Recompilación
- [guia-cmake.md](./tutoriales/guia-cmake.md) - Compilar con CMake

---

### 9. 🔧 Herramientas Externas
- [disc-image-creator.md](./herramientas/disc-image-creator.md) - DiscImageCreator
- [extract-xiso.md](./herramientas/extract-xiso.md) - extract-xiso
- [xextool.md](./herramientas/xextool.md) - xextool
- [xenon-recomp.md](./herramientas/xenon-recomp.md) - XenonRecomp

---

## � Estado de la Documentación

| Carpeta | Documentos | Estado |
|---------|------------|--------|
| guias/ | 4 | ✅ Completo |
| arquitectura/ | 3 | ✅ Completo |
| modulos/ | 4 | ✅ Completo |
| api/ | 6 | ✅ Completo |
| desarrollo/ | 5 | ✅ Completo |
| operaciones/ | 4 | ✅ Completo |
| proyecto/ | 5 | ✅ Completo |
| tutoriales/ | 6 | ✅ Completo |
| herramientas/ | 4 | ✅ Completo |

> 📊 **Total: 41 documentos organizados en 9 carpetas**

---

## 🤝 Contribuir a la Documentación

1. **¿Encontraste un error?** Abre un issue con la etiqueta `docs`
2. **¿Quieres escribir?** Revisa [CONTRIBUIR.md](./desarrollo/CONTRIBUIR.md)
3. **¿Sugerencias?** Abre una discusión

---

## 📞 ¿Necesitas Ayuda?

- 💬 [GitHub Discussions](https://github.com/MrMonkey09/MrMonkeyShopWare/discussions)
- 🐛 [Issue Tracker](https://github.com/MrMonkey09/MrMonkeyShopWare/issues)
- � [Soporte](./proyecto/SOPORTE.md)

---

<div align="center">

**Hecho con ❤️ por la Comunidad MrMonkeyShopWare**

[⬆️ Volver Arriba](#-mrmonkeyshopware---índice-de-documentación)

</div>
