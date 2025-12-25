# 🤝 Contribuir a MrMonkeyShopWare

Antes que nada, ¡gracias por considerar contribuir a MrMonkeyShopWare! 🎮

Este documento proporciona las guías y pasos para contribuir. Seguir estas guías ayuda a comunicar que respetas el tiempo de los desarrolladores que gestionan este proyecto.

---

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Primeros Pasos](#primeros-pasos)
- [¿Cómo Puedo Contribuir?](#cómo-puedo-contribuir)
- [Proceso de Desarrollo](#proceso-de-desarrollo)
- [Guías de Estilo](#guías-de-estilo)
- [Mensajes de Commit](#mensajes-de-commit)
- [Proceso de Pull Request](#proceso-de-pull-request)

---

## 📜 Código de Conducta

Este proyecto y todos los que participan en él están gobernados por nuestro [Código de Conducta](./CODIGO_DE_CONDUCTA.md). Al participar, se espera que respetes este código.

---

## 🚀 Primeros Pasos

### Prerrequisitos

- Python 3.11+
- Git
- Conocimiento de formatos de archivo Xbox 360 (útil pero no requerido)

### Configurar Entorno de Desarrollo

```bash
# 1. Haz fork del repositorio en GitHub

# 2. Clona tu fork
git clone https://github.com/TU_USUARIO/MrMonkeyShopWare.git
cd MrMonkeyShopWare

# 3. Añade remote upstream
git remote add upstream https://github.com/MrMonkey/MrMonkeyShopWare.git

# 4. Crea entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 5. Instala dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Dependencias de desarrollo

# 6. Instala pre-commit hooks (opcional pero recomendado)
pre-commit install
```

---

## 💡 ¿Cómo Puedo Contribuir?

### 🐛 Reportar Bugs

Antes de crear reportes de bugs, verifica los issues existentes para evitar duplicados.

Al crear un reporte de bug, incluye:

- **Título claro** describiendo el problema
- **Pasos para reproducir** el comportamiento
- **Comportamiento esperado** vs comportamiento actual
- **Capturas de pantalla** si aplica
- **Info del entorno**: SO, versión de Python, versiones de herramientas

Usa la plantilla de reporte de bugs cuando esté disponible.

### 💡 Sugerir Funcionalidades

¡Las sugerencias de funcionalidades son bienvenidas! Por favor:

1. Verifica si la funcionalidad ya ha sido sugerida
2. Abre un issue con la etiqueta `mejora`
3. Describe la funcionalidad y su caso de uso
4. Explica por qué sería útil para la mayoría de usuarios

### 📝 Documentación

Las mejoras de documentación siempre son bienvenidas:

- Corregir errores tipográficos o explicaciones poco claras
- Añadir ejemplos o tutoriales
- Traducir documentación
- Mejorar comentarios en el código

### 💻 Contribuciones de Código

¿Buscas algo en qué trabajar?

- Revisa issues etiquetados `buen primer issue` para principiantes
- Revisa issues etiquetados `se necesita ayuda` para tareas importantes
- Revisa el [ROADMAP](./ROADMAP.md) para funcionalidades planificadas

---

## 🔄 Proceso de Desarrollo

### Estrategia de Branching

Seguimos **Git Flow**:

```
main          ← Código listo para producción
  │
  └── develop ← Rama de integración
        │
        ├── feature/xxx  ← Nuevas funcionalidades
        ├── bugfix/xxx   ← Corrección de bugs
        └── docs/xxx     ← Documentación
```

### Crear una Rama

```bash
# Sincronizar con upstream
git checkout develop
git pull upstream develop

# Crear rama de feature
git checkout -b feature/nombre-de-tu-feature

# O para un bugfix
git checkout -b bugfix/issue-123-descripcion-fix
```

### Hacer Cambios

1. Haz tus cambios en commits pequeños y lógicos
2. Escribe o actualiza tests según sea necesario
3. Actualiza la documentación si es necesario
4. Asegúrate de que todos los tests pasen
5. Haz push a tu fork

---

## 📐 Guías de Estilo

### Estilo de Código Python

Seguimos **PEP 8** con algunas modificaciones:

```python
# ✅ Bien
def dump_disc(drive_letter: str, output_path: str = None) -> bool:
    """
    Hace dump de un disco Xbox 360 a un archivo ISO.
    
    Args:
        drive_letter: Letra de unidad (ej: 'E:')
        output_path: Ruta de salida opcional para el ISO
        
    Returns:
        True si exitoso, False en caso contrario
    """
    pass

# ❌ Mal
def dumpDisc(driveLetter, outputPath=None):
    pass
```

### Puntos Clave de Estilo

- **Indentación**: 4 espacios (no tabs)
- **Longitud de línea**: Máximo 88 caracteres (default de Black)
- **Nombres**: `snake_case` para funciones/variables, `PascalCase` para clases
- **Imports**: Ordenados con `isort`, agrupados (stdlib, terceros, locales)
- **Type hints**: Usar type hints para firmas de funciones
- **Docstrings**: Estilo Google para docstrings

### Herramientas

Recomendamos usar:

```bash
# Formatear código
black .

# Ordenar imports
isort .

# Lint del código
flake8 .

# Verificación de tipos
mypy .
```

---

## 💬 Mensajes de Commit

Seguimos **Conventional Commits**:

```
<tipo>(<alcance>): <descripción>

[cuerpo opcional]

[pie opcional]
```

### Tipos

| Tipo | Descripción |
|------|-------------|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Solo documentación |
| `style` | Formato, sin cambio de código |
| `refactor` | Cambio de código que no corrige ni añade |
| `test` | Añadir o actualizar tests |
| `chore` | Tareas de mantenimiento |

### Ejemplos

```bash
# Funcionalidad
feat(dumper): añadir soporte de callback de progreso

# Corrección de bug
fix(extractor): manejar espacios en rutas de archivo

# Documentación
docs(readme): añadir instrucciones de instalación

# Con cuerpo
feat(gui): añadir soporte de modo oscuro

Implementado usando temas de tkinter.
Cierra #42
```

---

## 🔀 Proceso de Pull Request

### Antes de Enviar

- [ ] El código sigue las guías de estilo
- [ ] Se realizó auto-revisión del código
- [ ] El código está comentado, particularmente en áreas difíciles
- [ ] Documentación actualizada si es necesario
- [ ] Tests añadidos/actualizados según corresponda
- [ ] Todos los tests pasan localmente

### Enviando

1. Haz push de tu rama a tu fork
2. Abre un Pull Request contra la rama `develop`
3. Completa la plantilla de PR completamente
4. Vincula cualquier issue relacionado

### Formato del Título del PR

```
<tipo>(<alcance>): <descripción>
```

Ejemplo: `feat(core): añadir soporte de procesamiento por lotes`

### Proceso de Revisión

1. Se requiere al menos una revisión de un mantenedor
2. Todos los checks de CI deben pasar
3. Sin conflictos de merge
4. El mantenedor puede solicitar cambios

### Después del Merge

- Elimina tu rama de feature
- Sincroniza tu fork con upstream

---

## 🏷️ Etiquetas de Issues

| Etiqueta | Descripción |
|----------|-------------|
| `bug` | Algo no funciona |
| `mejora` | Solicitud de nueva funcionalidad |
| `documentación` | Mejoras de documentación |
| `buen primer issue` | Bueno para recién llegados |
| `se necesita ayuda` | Se necesita atención extra |
| `pregunta` | Se requiere más información |
| `no se arreglará` | No se trabajará en esto |
| `duplicado` | Ya existe |

---

## 🙏 Reconocimiento

Los colaboradores serán reconocidos en:

- Sección de colaboradores del README.md
- Notas de versión
- Archivo COLABORADORES.md

---

## ❓ ¿Preguntas?

- Abre una [Discusión](https://github.com/MrMonkey/MrMonkeyShopWare/discussions)
- Revisa las [FAQ](./faq.md)
- Contacta a los mantenedores

---

**¡Gracias por contribuir! 🎮✨**
