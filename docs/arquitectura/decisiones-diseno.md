# 📋 Decisiones de Diseño (ADRs)

Este documento registra las decisiones arquitectónicas importantes del proyecto.

---

## ADR-001: Arquitectura Modular por Capas

**Estado**: Aceptado  
**Fecha**: 2024

### Contexto
Necesitamos una arquitectura que permita:
- Uso independiente de cada componente
- Fácil testing
- Múltiples interfaces (CLI, GUI, API futura)

### Decisión
Adoptar arquitectura de 3 capas:
1. **Core**: Lógica de negocio pura
2. **Interfaces**: CLI y GUI que consumen el core
3. **Utils**: Funciones auxiliares compartidas

### Consecuencias
- ✅ Cada módulo es testeable de forma aislada
- ✅ Nuevas interfaces se añaden fácilmente
- ⚠️ Requiere más archivos y organización

---

## ADR-002: Python como Lenguaje Principal

**Estado**: Aceptado  
**Fecha**: 2024

### Contexto
Opciones consideradas: Python, C#, Go, Rust

### Decisión
Usar Python 3.11+ por:
- Facilidad de uso para contribuidores
- Tkinter incluido para GUI
- Excelente para prototipado
- Comunidad amplia en español

### Consecuencias
- ✅ Bajo barrier de entrada
- ✅ Desarrollo rápido
- ⚠️ Rendimiento inferior a lenguajes compilados
- ⚠️ Dependencia de Python instalado

---

## ADR-003: Herramientas Externas vs Reimplementación

**Estado**: Aceptado  
**Fecha**: 2024

### Contexto
¿Debemos reimplementar DiscImageCreator, xextool, etc. o usarlos como dependencias externas?

### Decisión
Usar herramientas externas existentes y actuar como orquestador.

### Razones
- Herramientas probadas y mantenidas
- Evitar duplicar trabajo complejo
- Actualizaciones independientes

### Consecuencias
- ✅ Menos código a mantener
- ✅ Aprovecha expertise existente
- ⚠️ Dependencia de binarios externos
- ⚠️ Configuración adicional requerida

---

## ADR-004: Configuración por Variables de Entorno

**Estado**: Aceptado  
**Fecha**: 2024

### Contexto
¿Cómo manejar paths configurables de herramientas?

### Decisión
Soportar 3 métodos (en orden de prioridad):
1. Variables de entorno
2. Archivo config.py
3. Rutas por defecto en `C:\tools\`

### Consecuencias
- ✅ Flexible para diferentes configuraciones
- ✅ Compatible con CI/CD
- ⚠️ Más complejidad en config.py

---

## ADR-005: Tkinter para GUI Inicial

**Estado**: Aceptado, sujeto a revisión  
**Fecha**: 2024

### Contexto
Opciones de GUI: Tkinter, PyQt, wxPython, CustomTkinter

### Decisión
Usar Tkinter inicialmente por:
- Incluido en Python (sin dependencias)
- Suficiente para MVP
- Fácil de aprender

### Consecuencias
- ✅ Cero dependencias adicionales
- ✅ Funcional para versión inicial
- ⚠️ Apariencia básica
- 🔄 Planificado migrar a PyQt6/CustomTkinter en Fase 3

---

## ADR-006: Español como Idioma Principal

**Estado**: Aceptado  
**Fecha**: 2024

### Contexto
¿En qué idioma escribir documentación y mensajes?

### Decisión
Español para:
- Documentación
- Mensajes de usuario en GUI/CLI
- Comentarios de código

Inglés para:
- Nombres de variables/funciones
- Commits (Conventional Commits)
- Issues/PRs (opcional bilingüe)

### Consecuencias
- ✅ Accesible para comunidad hispanohablante
- ⚠️ Barrera para contribuidores no hispanohablantes
- 🔄 Traducciones planificadas para Fase 5
