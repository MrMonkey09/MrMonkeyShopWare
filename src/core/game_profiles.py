# core/game_profiles.py
"""
Sistema de perfiles de configuración por juego.
"""
import os
import toml
from typing import Optional, List, Dict, Any, Callable
from dataclasses import dataclass, field
from pathlib import Path


def _get_default_profiles_dir() -> str:
    """Retorna el directorio de perfiles por defecto."""
    # Buscar en el directorio del proyecto
    module_dir = Path(__file__).parent.parent.parent  # src -> project root
    profiles_dir = module_dir / "profiles"
    
    if profiles_dir.exists():
        return str(profiles_dir)
    
    # Fallback: directorio home
    home_profiles = Path.home() / ".mrmonkeyshopware" / "profiles"
    home_profiles.mkdir(parents=True, exist_ok=True)
    return str(home_profiles)


@dataclass
class GameProfile:
    """
    Perfil de configuración para un juego.
    
    Atributos:
        title_id: Identificador Xbox del juego (8 caracteres)
        game_name: Nombre legible del juego
        description: Descripción del perfil
        recomp_settings: Configuración de recompilación
        patches: Parches conocidos a aplicar
        custom: Valores personalizados para project.toml
    """
    title_id: str
    game_name: str
    description: str = ""
    recomp_settings: Dict[str, Any] = field(default_factory=dict)
    patches: Dict[str, bool] = field(default_factory=dict)
    custom: Dict[str, Any] = field(default_factory=dict)
    
    @classmethod
    def from_toml(cls, toml_path: str) -> "GameProfile":
        """
        Carga un perfil desde un archivo TOML.
        
        :param toml_path: Ruta al archivo TOML
        :return: Instancia de GameProfile
        """
        with open(toml_path, "r", encoding="utf-8") as f:
            data = toml.load(f)
        
        profile_data = data.get("profile", {})
        
        return cls(
            title_id=profile_data.get("title_id", ""),
            game_name=profile_data.get("game_name", "Unknown"),
            description=profile_data.get("description", ""),
            recomp_settings=data.get("recomp", {}),
            patches=data.get("patches", {}),
            custom=data.get("custom", {})
        )
    
    def to_toml(self, output_path: str) -> str:
        """
        Guarda el perfil como archivo TOML.
        
        :param output_path: Ruta de salida
        :return: Ruta del archivo creado
        """
        data = {
            "profile": {
                "title_id": self.title_id,
                "game_name": self.game_name,
                "description": self.description
            }
        }
        
        if self.recomp_settings:
            data["recomp"] = self.recomp_settings
        
        if self.patches:
            data["patches"] = self.patches
        
        if self.custom:
            data["custom"] = self.custom
        
        with open(output_path, "w", encoding="utf-8") as f:
            toml.dump(data, f)
        
        return output_path


class ProfileManager:
    """
    Gestor de perfiles de juegos.
    
    Uso:
        manager = ProfileManager()
        profile = manager.load_profile("4D5307E6")
        if profile:
            print(f"Perfil: {profile.game_name}")
    """
    
    def __init__(self, profiles_dir: str = None):
        """
        Inicializa el gestor de perfiles.
        
        :param profiles_dir: Directorio de perfiles (usa default si None)
        """
        self.profiles_dir = profiles_dir or _get_default_profiles_dir()
        self._cache: Dict[str, GameProfile] = {}
    
    def load_profile(self, title_id: str, log: Callable[[str], None] = None) -> Optional[GameProfile]:
        """
        Carga un perfil por Title ID.
        
        :param title_id: ID del juego (ej: "4D5307E6")
        :param log: Función de logging opcional
        :return: GameProfile o None si no existe
        """
        # Normalizar title_id
        title_id = title_id.upper().strip()
        
        # Verificar cache
        if title_id in self._cache:
            if log:
                log(f"📋 Perfil {title_id} (cache)")
            return self._cache[title_id]
        
        # Buscar archivo
        profile_path = os.path.join(self.profiles_dir, f"{title_id}.toml")
        
        if not os.path.isfile(profile_path):
            if log:
                log(f"⚠️ No existe perfil para {title_id}")
            return None
        
        try:
            profile = GameProfile.from_toml(profile_path)
            self._cache[title_id] = profile
            
            if log:
                log(f"✅ Perfil cargado: {profile.game_name}")
            
            return profile
        except Exception as e:
            if log:
                log(f"❌ Error cargando perfil {title_id}: {e}")
            return None
    
    def get_default_profile(self) -> GameProfile:
        """
        Retorna el perfil por defecto.
        
        :return: GameProfile default
        """
        default_path = os.path.join(self.profiles_dir, "_default.toml")
        
        if os.path.isfile(default_path):
            try:
                return GameProfile.from_toml(default_path)
            except:
                pass
        
        # Retornar perfil vacío por defecto
        return GameProfile(
            title_id="00000000",
            game_name="Default",
            description="Perfil por defecto"
        )
    
    def get_profile_or_default(self, title_id: str, log: Callable[[str], None] = None) -> GameProfile:
        """
        Obtiene perfil específico o el default.
        
        :param title_id: ID del juego
        :param log: Función de logging
        :return: GameProfile (nunca None)
        """
        profile = self.load_profile(title_id, log)
        if profile:
            return profile
        
        if log:
            log("📋 Usando perfil por defecto")
        return self.get_default_profile()
    
    def list_profiles(self) -> List[GameProfile]:
        """
        Lista todos los perfiles disponibles.
        
        :return: Lista de GameProfile
        """
        profiles = []
        
        if not os.path.isdir(self.profiles_dir):
            return profiles
        
        for filename in os.listdir(self.profiles_dir):
            if filename.endswith(".toml") and not filename.startswith("_"):
                filepath = os.path.join(self.profiles_dir, filename)
                try:
                    profile = GameProfile.from_toml(filepath)
                    profiles.append(profile)
                except:
                    continue
        
        return sorted(profiles, key=lambda p: p.game_name)
    
    def create_profile(
        self, 
        title_id: str, 
        game_name: str, 
        description: str = "",
        log: Callable[[str], None] = None
    ) -> GameProfile:
        """
        Crea un nuevo perfil.
        
        :param title_id: ID del juego
        :param game_name: Nombre del juego
        :param description: Descripción opcional
        :param log: Función de logging
        :return: GameProfile creado
        """
        title_id = title_id.upper().strip()
        
        profile = GameProfile(
            title_id=title_id,
            game_name=game_name,
            description=description
        )
        
        os.makedirs(self.profiles_dir, exist_ok=True)
        output_path = os.path.join(self.profiles_dir, f"{title_id}.toml")
        profile.to_toml(output_path)
        
        self._cache[title_id] = profile
        
        if log:
            log(f"✅ Perfil creado: {output_path}")
        
        return profile
    
    def apply_to_toml(self, profile: GameProfile, toml_content: dict) -> dict:
        """
        Aplica un perfil a un contenido TOML.
        
        :param profile: Perfil a aplicar
        :param toml_content: Contenido TOML base
        :return: Contenido TOML modificado
        """
        result = toml_content.copy()
        
        # Aplicar datos del proyecto
        if "project" not in result:
            result["project"] = {}
        
        result["project"]["title_id"] = profile.title_id
        result["project"]["game_name"] = profile.game_name
        
        # Aplicar configuración de recompilación
        if profile.recomp_settings:
            if "recomp" not in result:
                result["recomp"] = {}
            result["recomp"].update(profile.recomp_settings)
        
        # Aplicar valores custom
        if profile.custom:
            for key, value in profile.custom.items():
                if isinstance(value, dict) and key in result:
                    result[key].update(value)
                else:
                    result[key] = value
        
        return result
