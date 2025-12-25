# 🗄️ API de Base de Datos

## Visión General

El módulo `database` proporciona persistencia de datos para el historial de juegos procesados usando SQLite.

---

## Importación

```python
from core.database import GameDatabase, Game, GameStatus
```

---

## 📊 GameStatus (Enum)

Estados posibles de un juego en el pipeline:

| Estado | Valor | Descripción |
|--------|-------|-------------|
| `PENDING` | `"pending"` | Registrado, sin procesar |
| `DUMPED` | `"dumped"` | ISO creado |
| `EXTRACTED` | `"extracted"` | Contenido extraído |
| `ANALYSED` | `"analysed"` | XEX analizado |
| `IN_PROGRESS` | `"in_progress"` | 🆕 Port en desarrollo activo |
| `COMPLETED` | `"completed"` | Pipeline finalizado |
| `FAILED` | `"failed"` | Error en algún paso |

```python
from core.database import GameStatus

# Uso
status = GameStatus.IN_PROGRESS
print(status.value)  # "in_progress"

# Desde string
status = GameStatus("pending")
```

---

## 🎮 Game (Dataclass)

Representa un juego en la base de datos con metadata de XexTool.

```python
@dataclass
class Game:
    id: Optional[int] = None
    title_id: str = ""
    game_name: str = ""
    status: GameStatus = GameStatus.PENDING
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    iso_path: Optional[str] = None
    extracted_dir: Optional[str] = None
    xex_path: Optional[str] = None
    analysis_json: Optional[str] = None
    project_toml: Optional[str] = None
    notes: Optional[str] = None
    # 🆕 Campos de metadata XexTool
    media_id: Optional[str] = None
    version: Optional[str] = None
    disc_number: int = 1
    total_discs: int = 1
    regions: Optional[str] = None
    esrb_rating: Optional[str] = None
    entry_point: Optional[str] = None
    original_pe_name: Optional[str] = None
    xex_info_json: Optional[str] = None  # JSON con info adicional
```

### Ejemplo

```python
game = Game(
    title_id="4E4D07F5",
    game_name="Dead To Rights Retribution",
    status=GameStatus.IN_PROGRESS,
    iso_path="C:/games/dtr.iso",
    version="v0.0.0.1",
    regions="All Regions"
)
```

---

## 🗄️ GameDatabase (Clase)

Gestor principal de la base de datos.

### Constructor

```python
db = GameDatabase(db_path=None)
```

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `db_path` | `str` | Ruta a la BD. Default: `~/.mrmonkeyshopware/games.db` |

> [!TIP]
> Usa `":memory:"` para una BD en memoria (útil para tests).

---

### Métodos CRUD

#### add_game(game) → int

Añade un juego a la base de datos.

```python
game = Game(title_id="12345678", game_name="My Game")
game_id = db.add_game(game)
print(f"ID: {game_id}")
```

---

#### get_game(game_id) → Game | None

Obtiene un juego por ID.

```python
game = db.get_game(1)
if game:
    print(game.game_name)
```

---

#### get_by_title_id(title_id) → Game | None

Obtiene un juego por Title ID.

```python
game = db.get_by_title_id("12345678")
```

---

#### update_game(game) → bool

Actualiza un juego existente.

```python
game = db.get_game(1)
game.status = GameStatus.COMPLETED
db.update_game(game)
```

---

#### update_status(game_id, status, **kwargs) → bool

Actualiza el status y opcionalmente otros campos.

```python
# Solo status
db.update_status(1, GameStatus.DUMPED)

# Status + campos adicionales
db.update_status(
    1, 
    GameStatus.EXTRACTED,
    extracted_dir="/path/to/extracted"
)
```

---

#### delete_game(game_id) → bool

Elimina un juego.

```python
deleted = db.delete_game(1)
```

---

#### list_games(status, limit) → List[Game]

Lista juegos con filtros opcionales.

```python
# Todos los juegos
games = db.list_games()

# Solo completados
completed = db.list_games(status=GameStatus.COMPLETED)

# Limitar resultados
recent = db.list_games(limit=10)
```

---

#### search(query) → List[Game]

Busca juegos por nombre o title_id.

```python
results = db.search("halo")
for game in results:
    print(game.game_name)
```

---

#### count(status) → int

Cuenta juegos.

```python
total = db.count()
completed = db.count(GameStatus.COMPLETED)
```

---

### Context Manager

```python
with GameDatabase() as db:
    games = db.list_games()
    # La conexión se cierra automáticamente
```

---

## 🖥️ CLI

El módulo incluye comandos CLI para gestión:

```bash
# Listar juegos
python -m cli.db list
python -m cli.db list --status completed
python -m cli.db list -v  # Verbose

# Buscar
python -m cli.db search "halo"

# Ver detalles
python -m cli.db show 1

# Añadir
python -m cli.db add -n "My Game" -t "12345678"

# Eliminar
python -m cli.db delete 1

# Cambiar status
python -m cli.db status 1 completed
```

---

## 📁 Ubicación de la BD

Por defecto: `~/.mrmonkeyshopware/games.db`

Puede sobrescribirse pasando `db_path` al constructor.

---

## Véase También

- [pipeline.md](./pipeline.md) - Pipeline automatizado
- [Tutorial Pipeline](../tutoriales/pipeline-completo.md)
