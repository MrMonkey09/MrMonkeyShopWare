# 🛠️ Guía de Desarrollo

Guía para configurar tu entorno de desarrollo.

---

## 📋 Prerrequisitos

- Python 3.11+
- Git
- VS Code (recomendado) u otro editor

---

## 🚀 Configuración Inicial

### 1. Clonar y preparar

```bash
git clone https://github.com/TU_USUARIO/MrMonkeyShopWare.git
cd MrMonkeyShopWare
```

### 2. Crear entorno virtual

```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Instalar pre-commit hooks

```bash
pre-commit install
```

---

## 🔧 Herramientas de Desarrollo

### Formateo de código

```bash
# Formatear con Black
black src/

# Ordenar imports
isort src/
```

### Linting

```bash
# Verificar estilo
flake8 src/

# Verificar tipos
mypy src/
```

### Tests

```bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=src

# Tests específicos
pytest tests/unit/test_dumper.py -v
```

---

## 📁 Estructura para Desarrollo

```
MrMonkeyShopWare/
├── src/              # Código fuente (editar aquí)
├── tests/            # Tests (añadir tests aquí)
├── docs/             # Documentación (mantener actualizada)
└── scripts/          # Scripts auxiliares
```

---

## 🔄 Flujo de Trabajo

### 1. Crear rama

```bash
git checkout develop
git pull origin develop
git checkout -b feature/mi-feature
```

### 2. Desarrollar

- Editar código en `src/`
- Añadir tests en `tests/`
- Actualizar docs si es necesario

### 3. Verificar

```bash
black src/
isort src/
flake8 src/
pytest
```

### 4. Commit

```bash
git add .
git commit -m "feat(modulo): descripción del cambio"
```

### 5. Push y PR

```bash
git push origin feature/mi-feature
# Abrir PR en GitHub
```

---

## 🐛 Debugging

### VS Code launch.json

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "GUI",
            "type": "python",
            "request": "launch",
            "module": "src.gui.main"
        },
        {
            "name": "CLI Dump",
            "type": "python",
            "request": "launch",
            "module": "src.cli.dump",
            "args": ["E:"]
        }
    ]
}
```

---

## 📚 Ver también

- [CONTRIBUIR.md](./CONTRIBUIR.md)
- [PRUEBAS.md](./PRUEBAS.md)
- [GUIA_DE_ESTILO.md](./GUIA_DE_ESTILO.md)
