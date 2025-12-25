# tests/unit/test_game_profiles.py
"""
Tests unitarios para el módulo game_profiles.
"""
import pytest
import tempfile
import os
import toml

from core.game_profiles import GameProfile, ProfileManager


class TestGameProfile:
    """Tests para la dataclass GameProfile."""
    
    def test_create_basic(self):
        """Verifica creación básica."""
        profile = GameProfile(
            title_id="4D5307E6",
            game_name="Halo 3"
        )
        
        assert profile.title_id == "4D5307E6"
        assert profile.game_name == "Halo 3"
        assert profile.description == ""
        assert profile.recomp_settings == {}
        assert profile.patches == {}
    
    def test_create_full(self):
        """Verifica creación con todos los campos."""
        profile = GameProfile(
            title_id="4D5307E6",
            game_name="Halo 3",
            description="Test profile",
            recomp_settings={"optimize": 2},
            patches={"vsync": True},
            custom={"output": "build"}
        )
        
        assert profile.description == "Test profile"
        assert profile.recomp_settings["optimize"] == 2
        assert profile.patches["vsync"] is True
    
    def test_from_toml(self):
        """Verifica carga desde TOML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = os.path.join(tmpdir, "test.toml")
            
            content = {
                "profile": {
                    "title_id": "12345678",
                    "game_name": "Test Game",
                    "description": "A test"
                },
                "recomp": {"level": 1},
                "patches": {"fix_a": True}
            }
            
            with open(toml_path, "w") as f:
                toml.dump(content, f)
            
            profile = GameProfile.from_toml(toml_path)
            
            assert profile.title_id == "12345678"
            assert profile.game_name == "Test Game"
            assert profile.recomp_settings["level"] == 1
    
    def test_to_toml(self):
        """Verifica guardado a TOML."""
        profile = GameProfile(
            title_id="ABCD1234",
            game_name="Save Test",
            patches={"test": True}
        )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "output.toml")
            result_path = profile.to_toml(output_path)
            
            assert os.path.isfile(result_path)
            
            with open(result_path, "r") as f:
                data = toml.load(f)
            
            assert data["profile"]["title_id"] == "ABCD1234"
            assert data["patches"]["test"] is True


class TestProfileManager:
    """Tests para ProfileManager."""
    
    def test_init_default_dir(self):
        """Verifica inicialización con directorio por defecto."""
        manager = ProfileManager()
        assert manager.profiles_dir is not None
    
    def test_init_custom_dir(self):
        """Verifica inicialización con directorio custom."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ProfileManager(profiles_dir=tmpdir)
            assert manager.profiles_dir == tmpdir
    
    def test_load_nonexistent_profile(self):
        """Verifica carga de perfil inexistente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ProfileManager(profiles_dir=tmpdir)
            profile = manager.load_profile("NONEXIST")
            
            assert profile is None
    
    def test_load_existing_profile(self):
        """Verifica carga de perfil existente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear perfil de prueba
            toml_path = os.path.join(tmpdir, "12345678.toml")
            content = {
                "profile": {
                    "title_id": "12345678",
                    "game_name": "Load Test"
                }
            }
            with open(toml_path, "w") as f:
                toml.dump(content, f)
            
            manager = ProfileManager(profiles_dir=tmpdir)
            profile = manager.load_profile("12345678")
            
            assert profile is not None
            assert profile.game_name == "Load Test"
    
    def test_get_default_profile(self):
        """Verifica perfil por defecto."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ProfileManager(profiles_dir=tmpdir)
            default = manager.get_default_profile()
            
            assert default is not None
            assert default.title_id == "00000000"
    
    def test_get_profile_or_default_existing(self):
        """Verifica get_profile_or_default con perfil existente."""
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = os.path.join(tmpdir, "AAAAAAAA.toml")
            content = {"profile": {"title_id": "AAAAAAAA", "game_name": "Exists"}}
            with open(toml_path, "w") as f:
                toml.dump(content, f)
            
            manager = ProfileManager(profiles_dir=tmpdir)
            profile = manager.get_profile_or_default("AAAAAAAA")
            
            assert profile.game_name == "Exists"
    
    def test_get_profile_or_default_fallback(self):
        """Verifica fallback a default."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ProfileManager(profiles_dir=tmpdir)
            profile = manager.get_profile_or_default("NONEXIST")
            
            assert profile.title_id == "00000000"  # Default
    
    def test_list_profiles(self):
        """Verifica listado de perfiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear dos perfiles
            for tid, name in [("11111111", "Game A"), ("22222222", "Game B")]:
                toml_path = os.path.join(tmpdir, f"{tid}.toml")
                content = {"profile": {"title_id": tid, "game_name": name}}
                with open(toml_path, "w") as f:
                    toml.dump(content, f)
            
            manager = ProfileManager(profiles_dir=tmpdir)
            profiles = manager.list_profiles()
            
            assert len(profiles) == 2
    
    def test_create_profile(self):
        """Verifica creación de perfil."""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ProfileManager(profiles_dir=tmpdir)
            profile = manager.create_profile(
                title_id="NEWGAME1",
                game_name="New Game"
            )
            
            assert profile.title_id == "NEWGAME1"
            assert os.path.isfile(os.path.join(tmpdir, "NEWGAME1.toml"))
    
    def test_apply_to_toml(self):
        """Verifica aplicación de perfil a TOML."""
        profile = GameProfile(
            title_id="TESTTEST",
            game_name="Applied",
            recomp_settings={"optimize": 3},
            custom={"extra": "value"}
        )
        
        manager = ProfileManager()
        base_toml = {"project": {"name": "original"}}
        
        result = manager.apply_to_toml(profile, base_toml)
        
        assert result["project"]["title_id"] == "TESTTEST"
        assert result["project"]["game_name"] == "Applied"
        assert result["recomp"]["optimize"] == 3
        assert result["extra"] == "value"
    
    def test_cache(self):
        """Verifica cache de perfiles."""
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = os.path.join(tmpdir, "CACHED00.toml")
            content = {"profile": {"title_id": "CACHED00", "game_name": "Cached"}}
            with open(toml_path, "w") as f:
                toml.dump(content, f)
            
            manager = ProfileManager(profiles_dir=tmpdir)
            
            # Primera carga
            profile1 = manager.load_profile("CACHED00")
            # Segunda carga (debe venir del cache)
            profile2 = manager.load_profile("CACHED00")
            
            assert profile1 is profile2  # Misma instancia
