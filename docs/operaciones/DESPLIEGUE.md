# 🚢 Guía de Despliegue

## 📦 Distribución

### Instalación desde PyPI (futuro)

```bash
pip install mrmonkeyshopware
```

### Instalación desde código fuente

```bash
git clone https://github.com/MrMonkey/MrMonkeyShopWare.git
cd MrMonkeyShopWare
pip install -e .
```

---

## 🔨 Build

### Crear paquete distribuible

```bash
pip install build
python -m build
```

Genera:
- `dist/mrmonkeyshopware-X.X.X.tar.gz`
- `dist/mrmonkeyshopware-X.X.X-py3-none-any.whl`

---

## 🖥️ Ejecutable Standalone (futuro)

### Con PyInstaller

```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/gui/main.py
```

---

## 🐳 Despliegue con Docker

Ver [docker.md](./docker.md) para instrucciones detalladas.

```bash
cd docker
docker-compose up -d
```

---

## ✅ Checklist Pre-Release

- [ ] Bumped version in `pyproject.toml`
- [ ] Updated CHANGELOG.md
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Git tag created

---

## 📚 Ver también

- [Docker](./docker.md)
- [Configuración](./configuracion.md)
