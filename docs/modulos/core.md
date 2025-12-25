# 🧠 Módulo Core

El módulo `core` contiene toda la lógica de negocio del proyecto MrMonkeyShopWare.

---

## 📁 Archivos

| Archivo | Tamaño | Descripción |
|---------|--------|-------------|
| `game_workspace.py` | 13 KB | 🆕 Gestión de directorios por juego |
| `database.py` | 15 KB | Base de datos SQLite |
| `pipeline.py` | 12 KB | Pipeline de procesamiento |
| `game_profiles.py` | 9 KB | Perfiles de juegos |
| `xbox_drive_scanner.py` | 7 KB | 🆕 Escáner USB Xbox 360 |
| `shader_recomp.py` | 8 KB | Recompilación de shaders |
| `xex_parser.py` | 7 KB | 🆕 Parser de metadata XexTool |
| `logger.py` | 6 KB | Sistema de logging |
| `virtual_disc.py` | 5 KB | 🆕 Detección de disco virtual |
| `analyser.py` | 5 KB | Análisis de XEX |
| `folder_scanner.py` | 4 KB | Escáner de carpetas |
| `settings.py` | 4 KB | Configuración persistente |
| `config.py` | 3 KB | Rutas de herramientas |
| `cleaner_xex.py` | 2 KB | Limpieza de XEX |
| `toml_generator.py` | 2 KB | Generador TOML |
| `extractor.py` | 2 KB | Extractor de ISO |
| `dumper.py` | 2 KB | Dumper de discos |

---

## 📁 game_workspace.py (🆕 Nuevo)

Gestiona directorios organizados por juego.

### Clases

#### `GameWorkspace`

```python
workspace = GameWorkspace(title_id="4E4D07F5", game_name="Dead To Rights")

# Propiedades
workspace.root         # Directorio raíz
workspace.analysis_dir # Carpeta analysis/
workspace.extracted_dir # Carpeta extracted/
workspace.info_file    # info.json

# Métodos
workspace.create()              # Crear estructura
workspace.save_info(game_info)  # Guardar metadata
workspace.load_info()           # Cargar metadata
workspace.check_external_files(game)  # Detectar archivos externos
workspace.sync_all_files(game, log)   # Sincronizar al workspace
```

#### `GameInfo`

```python
@dataclass
class GameInfo:
    title_id: str
    game_name: str
    version: str
    media_id: str
    regions: str
    status: str  # "pending", "analysed", "completed"
```

#### `ExternalFile`

```python
@dataclass
class ExternalFile:
    file_type: str   # "xex", "iso", "toml", "json"
    label: str       # Etiqueta para mostrar
    current_path: str
    target_path: str
    size: int
```

### Funciones

```python
get_or_create_workspace(title_id, game_name) -> (GameWorkspace, is_new)
```

---

## 💾 xbox_drive_scanner.py (🆕 Nuevo)

Detecta juegos en USB con formato Xbox 360.

```python
from core.xbox_drive_scanner import is_xbox_usb, list_games_on_drive

# Verificar si es USB Xbox
if is_xbox_usb("E:"):
    games = list_games_on_drive("E:")
    for game in games:
        print(f"{game.display_name} - {game.title_id}")
```

---

## 🔬 xex_parser.py (🆕 Nuevo)

Parser de metadata desde salida de XexTool.

```python
from core.xex_parser import XexInfo, parse_xex_info

# Parsear información
xex_info = parse_xex_info(xex_path)

# Propiedades
xex_info.title_id      # "4E4D07F5"
xex_info.media_id      # "50B46754"
xex_info.display_name  # "Dead To Rights Retribution"
xex_info.version       # "v0.0.0.1"
xex_info.regions       # "All Regions"
xex_info.esrb_rating   # "Mature 17+"
xex_info.entry_point   # "0x82000000"
```

---

## 💿 virtual_disc.py (🆕 Nuevo)

Detecta ISOs montadas como disco virtual.

```python
from core.virtual_disc import is_virtual_disc, detect_mounted_iso

if is_virtual_disc("E:"):
    iso_info = detect_mounted_iso("E:")
```

---

## 🔧 config.py

Rutas de herramientas externas.

```python
XENON_ANALYSE_PATH = ...
XEXTOOL_PATH = ...
EXTRACT_XISO_PATH = ...
DISC_IMAGE_CREATOR_PATH = ...
XENON_RECOMP_PATH = ...
```

---

## 📀 dumper.py

```python
dump_disc(drive_letter, gui_ref=None, out_path=None) -> bool
```

---

## 📦 extractor.py

```python
extract_iso(iso_path, output_dir=None, log=None) -> str | None
list_xex_files(output_dir) -> list[str]
```

---

## 🔍 analyser.py

```python
analyse_xex(xex_path, out_dir=None, log=None) -> AnalysisResult | None
```

---

## 🧹 cleaner_xex.py

```python
clean_xex(xex_path, output_dir, log=None) -> str
check_xex_info(xex_path, log=None) -> str
```

---

## 📝 toml_generator.py

```python
generate_project_toml(xex_path, analysis_json, output_dir) -> str
validate_project_toml(toml_path, log=None) -> bool
```

---

## 💾 database.py

Sistema de persistencia con SQLite.

```python
from core.database import GameDatabase, Game, GameStatus

with GameDatabase() as db:
    # Añadir/actualizar juego
    game_id = db.add_or_update_game(game)
    
    # Consultar
    games = db.list_games()
    game = db.get_by_title_id("4E4D07F5")
```

---

## 📚 Ver también

- [API game_workspace](../api/game-workspace.md)
- [API xex_parser](../api/xex-parser.md)
- [Módulo CLI](./cli.md)
- [Módulo GUI](./gui.md)
