# 💻 Módulo CLI

El módulo `cli` proporciona una interfaz de línea de comandos unificada para todas las operaciones de MrMonkeyShopWare.

---

## 🚀 Uso Principal

```bash
cd src
python -m cli.main <comando> [opciones]
```

---

## 📋 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `analyse` | Analiza un XEX y crea workspace organizado |
| `extract` | Extrae contenido de un ISO |
| `dump` | Crea ISO desde disco físico |
| `pipeline` | Pipeline completo (dump → extract → analyse) |
| `scan-usb` | Detecta juegos en USB Xbox 360 |
| `list` | Lista todos los workspaces |
| `info` | Muestra información de un juego |
| `sync` | Sincroniza archivos al workspace |
| `db` | Gestiona la base de datos |

---

## 🔬 Análisis de XEX

```bash
python -m cli.main analyse <xex>

# Ejemplo
python -m cli.main analyse "C:/Games/default.xex"
```

**Características**:
- Crea workspace organizado automáticamente
- Guarda `info.json` con metadata
- Copia archivos de análisis al workspace
- Registra en base de datos

---

## 📦 Extracción de ISO

```bash
python -m cli.main extract <iso> [-o <output>]

# Ejemplo
python -m cli.main extract game.iso -o ./extracted
```

---

## 📀 Dump de Disco

```bash
python -m cli.main dump <drive> [-o <output>]

# Ejemplo
python -m cli.main dump E:
```

---

## 🚀 Pipeline Completo

```bash
python -m cli.main pipeline <drive> [-o <output>]

# Ejemplo
python -m cli.main pipeline E:
```

Ejecuta automáticamente: dump → extract → analyse

---

## 💾 Escanear USB Xbox 360

```bash
python -m cli.main scan-usb <drive> [-a]

# Ejemplo
python -m cli.main scan-usb E: -a  # -a para analizar interactivamente
```

Detecta juegos instalados en USB con formato Xbox 360.

---

## 📂 Listar Workspaces

```bash
python -m cli.main list [-v]

# Ejemplo
python -m cli.main list -v  # -v para más detalles
```

Muestra todos los workspaces creados en `~/MrMonkeyShopWare/ports/`.

---

## ℹ️ Info de Juego

```bash
python -m cli.main info <title_id>

# Ejemplo
python -m cli.main info 4E4D07F5
```

Muestra información detallada de un juego por su Title ID.

---

## 🔄 Sincronizar Archivos

```bash
python -m cli.main sync <title_id> [-y]

# Ejemplo
python -m cli.main sync 4E4D07F5 -y  # -y para no pedir confirmación
```

Detecta archivos fuera del workspace y los copia al directorio correspondiente.

---

## 💾 Gestión de Base de Datos

```bash
python -m cli.main db list              # Listar juegos
python -m cli.main db export [-o file]  # Exportar a JSON
```

---

## 📁 Archivos del Módulo

| Archivo | Estado | Descripción |
|---------|--------|-------------|
| `main.py` | ✅ **Activo** | Entry point principal con subcomandos |
| `db.py` | ✅ Activo | Gestión de BD |
| `profiles.py` | ✅ Activo | Perfiles de juegos |
| `recomp.py` | ✅ Activo | Recompilación |
| `analyse.py` | ⚠️ Deprecated | Usar `main.py analyse` |
| `dump.py` | ⚠️ Deprecated | Usar `main.py dump` |
| `extract.py` | ⚠️ Deprecated | Usar `main.py extract` |
| `pipeline.py` | ⚠️ Deprecated | Usar `main.py pipeline` |
| `tomlgen.py` | ⚠️ Deprecated | Funcionalidad integrada |

---

## 📋 Códigos de Salida

| Código | Significado |
|--------|-------------|
| 0 | Éxito |
| 1 | Error general |

---

## 📚 Ver también

- [Primeros Pasos](../guias/primeros-pasos.md)
- [Tutorial: Pipeline Completo](../tutoriales/pipeline-completo.md)
- [Módulo Core](./core.md)
