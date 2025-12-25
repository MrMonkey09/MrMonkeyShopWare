# ⚙️ API de Perfiles de Juegos

## Visión General

El módulo `game_profiles` proporciona un sistema de perfiles TOML personalizados por Title ID.

---

## Importación

```python
from core.game_profiles import GameProfile, ProfileManager
```

---

## 📊 GameProfile (Dataclass)

```python
@dataclass
class GameProfile:
    title_id: str           # "4D5307E6"
    game_name: str          # "Halo 3"
    description: str        # Descripción opcional
    recomp_settings: dict   # Configuración de recompilación
    patches: dict           # Parches conocidos
    custom: dict            # Valores custom para TOML
```

---

## 🔧 ProfileManager

### Carga de Perfiles

```python
manager = ProfileManager()

# Cargar perfil específico
profile = manager.load_profile("4D5307E6")

# Cargar perfil o default
profile = manager.get_profile_or_default("UNKNOWN")
```

### Listado

```python
profiles = manager.list_profiles()
for p in profiles:
    print(f"{p.title_id}: {p.game_name}")
```

### Crear Perfil

```python
profile = manager.create_profile(
    title_id="12345678",
    game_name="Mi Juego"
)
```

### Aplicar a TOML

```python
toml_content = {"project": {}}
result = manager.apply_to_toml(profile, toml_content)
```

---

## 🖥️ CLI

```bash
# Listar perfiles
python -m cli.profiles list

# Ver perfil
python -m cli.profiles show 4D5307E6

# Crear perfil
python -m cli.profiles create -t "4D5307E6" -n "Halo 3"
```

---

## 📁 Estructura de Perfiles

```
profiles/
├── _default.toml     # Perfil por defecto
├── 4D5307E6.toml     # Halo 3
└── 4D5307D1.toml     # Gears of War
```

---

## Formato TOML

```toml
[profile]
title_id = "4D5307E6"
game_name = "Halo 3"

[recomp]
optimize_level = 2

[patches]
apply_vsync_fix = true

[custom]
output_dir = "build/halo3"
```
