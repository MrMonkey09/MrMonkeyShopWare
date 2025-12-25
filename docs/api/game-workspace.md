# 📁 API: game_workspace

Módulo para gestión de directorios de trabajo organizados por juego.

**Ubicación**: `src/core/game_workspace.py`

---

## 📖 Descripción

El módulo `game_workspace` proporciona una estructura estandarizada para organizar
todos los archivos relacionados con cada juego/port. Cada workspace incluye:

```
~/MrMonkeyShopWare/ports/
└── GameName [TitleID]/
    ├── info.json          # Metadata del juego
    ├── notes.md           # Notas del desarrollador
    ├── default.xex        # XEX principal (opcional)
    ├── game.iso           # ISO original (opcional)
    ├── analysis/          # Archivos de análisis
    │   ├── analysis.toml
    │   └── analysis.json
    ├── extracted/         # Contenido extraído del ISO
    ├── cleaned/           # XEX desencriptados
    └── recompiled/        # Código recompilado
```

---

## 🏗️ Clases

### `GameWorkspace`

Gestiona el directorio de trabajo de un juego.

```python
from core.game_workspace import GameWorkspace

workspace = GameWorkspace(title_id="4E4D07F5", game_name="Dead To Rights")
```

#### Propiedades

| Propiedad | Tipo | Descripción |
|-----------|------|-------------|
| `title_id` | `str` | Title ID del juego |
| `game_name` | `str` | Nombre del juego |
| `folder_name` | `str` | Nombre de carpeta: `"GameName [TitleID]"` |
| `root` | `Path` | Directorio raíz del workspace |
| `analysis_dir` | `Path` | Subcarpeta `analysis/` |
| `extracted_dir` | `Path` | Subcarpeta `extracted/` |
| `cleaned_dir` | `Path` | Subcarpeta `cleaned/` |
| `recompiled_dir` | `Path` | Subcarpeta `recompiled/` |
| `info_file` | `Path` | Ruta a `info.json` |
| `notes_file` | `Path` | Ruta a `notes.md` |

#### Métodos

##### `exists() -> bool`
Verifica si el workspace ya existe.

##### `create() -> Path`
Crea la estructura de directorios.

```python
workspace.create()
# Crea: root/, analysis/, extracted/, cleaned/, recompiled/, notes.md
```

##### `save_info(game_info: GameInfo)`
Guarda metadata del juego en `info.json`.

##### `load_info() -> GameInfo | None`
Carga metadata desde `info.json`.

##### `is_in_workspace(path: str) -> bool`
Verifica si una ruta está dentro del workspace.

##### `check_external_files(game: Game) -> list[ExternalFile]`
Detecta archivos (XEX, ISO, etc.) que están fuera del workspace.

```python
external = workspace.check_external_files(game)
for ef in external:
    print(f"{ef.label}: {ef.current_path} → {ef.target_path}")
```

##### `sync_file(external_file: ExternalFile, log=None) -> bool`
Copia un archivo externo al workspace.

##### `sync_all_files(game: Game, log=None) -> dict`
Sincroniza todos los archivos externos.

```python
new_paths = workspace.sync_all_files(game, log=print)
# new_paths = {"xex_path": "/new/path", "iso_path": "/new/path", ...}
```

#### Métodos de Clase

##### `find_existing(title_id: str) -> GameWorkspace | None`
Busca un workspace existente por title_id.

```python
ws = GameWorkspace.find_existing("4E4D07F5")
if ws:
    print(f"Encontrado: {ws.root}")
```

##### `list_all() -> list[GameWorkspace]`
Lista todos los workspaces existentes.

```python
for ws in GameWorkspace.list_all():
    print(f"{ws.game_name} [{ws.title_id}]")
```

---

### `GameInfo`

Dataclass con metadata del juego.

```python
@dataclass
class GameInfo:
    title_id: str
    game_name: str
    version: str = ""
    media_id: str = ""
    regions: str = ""
    esrb_rating: str = ""
    disc_number: int = 1
    total_discs: int = 1
    entry_point: str = ""
    original_pe_name: str = ""
    source_type: str = ""      # "iso", "xex", "usb", "god"
    source_path: str = ""
    created_at: str = ""
    updated_at: str = ""
    status: str = "pending"    # "pending", "analysed", "completed"
    notes: str = ""
```

#### Método de Clase

##### `from_xex_info(xex_info, source_type, source_path) -> GameInfo`
Crea un GameInfo desde XexInfo.

---

### `ExternalFile`

Representa un archivo que está fuera del workspace.

```python
@dataclass
class ExternalFile:
    file_type: str      # "xex", "iso", "toml", "json"
    label: str          # Etiqueta para UI
    current_path: str   # Ruta actual
    target_path: str    # Destino en workspace
    size: int = 0       # Tamaño en bytes
```

---

## 🔧 Funciones

### `get_base_ports_dir() -> Path`
Obtiene el directorio base: `~/MrMonkeyShopWare/ports/`

### `get_or_create_workspace(title_id, game_name) -> tuple[GameWorkspace, bool]`
Obtiene un workspace existente o crea uno nuevo.

```python
workspace, is_new = get_or_create_workspace("4E4D07F5", "Dead To Rights")
if is_new:
    print("Workspace creado")
else:
    print("Workspace existente")
```

### `sanitize_folder_name(name: str) -> str`
Sanitiza un nombre para usarlo como carpeta (elimina caracteres inválidos).

---

## 📚 Ver también

- [Módulo Core](../modulos/core.md)
- [API Database](./database.md)
- [API xex_parser](./xex-parser.md)
