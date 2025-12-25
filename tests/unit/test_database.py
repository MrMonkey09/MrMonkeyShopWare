# tests/unit/test_database.py
"""
Tests unitarios para el módulo database.
"""
import pytest
from datetime import datetime
from core.database import GameDatabase, Game, GameStatus


@pytest.fixture
def db():
    """Fixture que proporciona una BD en memoria."""
    database = GameDatabase(":memory:")
    yield database
    database.close()


@pytest.fixture
def sample_game():
    """Fixture que proporciona un juego de ejemplo."""
    return Game(
        title_id="12345678",
        game_name="Test Game",
        status=GameStatus.PENDING
    )


class TestGameDataclass:
    """Tests para la dataclass Game."""
    
    def test_default_values(self):
        """Verifica valores por defecto."""
        game = Game()
        
        assert game.id is None
        assert game.title_id == ""
        assert game.game_name == ""
        assert game.status == GameStatus.PENDING
        assert game.iso_path is None
    
    def test_with_values(self):
        """Verifica Game con valores."""
        game = Game(
            title_id="ABCD1234",
            game_name="My Game",
            status=GameStatus.COMPLETED,
            iso_path="/path/to/game.iso"
        )
        
        assert game.title_id == "ABCD1234"
        assert game.game_name == "My Game"
        assert game.status == GameStatus.COMPLETED
        assert game.iso_path == "/path/to/game.iso"


class TestGameStatus:
    """Tests para el enum GameStatus."""
    
    def test_all_statuses_exist(self):
        """Verifica que existen todos los estados."""
        statuses = [s.value for s in GameStatus]
        
        assert "pending" in statuses
        assert "dumped" in statuses
        assert "extracted" in statuses
        assert "analysed" in statuses
        assert "completed" in statuses
        assert "failed" in statuses
    
    def test_status_from_string(self):
        """Verifica conversión desde string."""
        assert GameStatus("pending") == GameStatus.PENDING
        assert GameStatus("completed") == GameStatus.COMPLETED


class TestGameDatabaseInit:
    """Tests para inicialización de GameDatabase."""
    
    def test_create_in_memory(self):
        """Verifica creación de BD en memoria."""
        db = GameDatabase(":memory:")
        assert db.conn is not None
        db.close()
    
    def test_schema_created(self, db):
        """Verifica que el esquema se crea correctamente."""
        cursor = db.conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='games'"
        )
        assert cursor.fetchone() is not None


class TestAddGame:
    """Tests para añadir juegos."""
    
    def test_add_game_returns_id(self, db, sample_game):
        """Verifica que add_game retorna un ID."""
        game_id = db.add_game(sample_game)
        
        assert game_id is not None
        assert game_id > 0
    
    def test_add_game_persists(self, db, sample_game):
        """Verifica que el juego se guarda en la BD."""
        game_id = db.add_game(sample_game)
        
        retrieved = db.get_game(game_id)
        
        assert retrieved is not None
        assert retrieved.title_id == sample_game.title_id
        assert retrieved.game_name == sample_game.game_name
    
    def test_add_game_without_title_id(self, db):
        """Verifica que se puede añadir juego sin title_id."""
        game = Game(game_name="No Title ID Game")
        game_id = db.add_game(game)
        
        assert game_id > 0


class TestGetGame:
    """Tests para obtener juegos."""
    
    def test_get_existing_game(self, db, sample_game):
        """Verifica obtención de juego existente."""
        game_id = db.add_game(sample_game)
        
        retrieved = db.get_game(game_id)
        
        assert retrieved is not None
        assert retrieved.id == game_id
    
    def test_get_nonexistent_game(self, db):
        """Verifica que retorna None para ID inexistente."""
        retrieved = db.get_game(999)
        
        assert retrieved is None
    
    def test_get_by_title_id(self, db, sample_game):
        """Verifica búsqueda por title_id."""
        db.add_game(sample_game)
        
        retrieved = db.get_by_title_id(sample_game.title_id)
        
        assert retrieved is not None
        assert retrieved.title_id == sample_game.title_id


class TestUpdateGame:
    """Tests para actualizar juegos."""
    
    def test_update_game(self, db, sample_game):
        """Verifica actualización completa."""
        game_id = db.add_game(sample_game)
        
        sample_game.id = game_id
        sample_game.game_name = "Updated Name"
        sample_game.status = GameStatus.COMPLETED
        
        result = db.update_game(sample_game)
        
        assert result is True
        
        retrieved = db.get_game(game_id)
        assert retrieved.game_name == "Updated Name"
        assert retrieved.status == GameStatus.COMPLETED
    
    def test_update_status(self, db, sample_game):
        """Verifica actualización solo de status."""
        game_id = db.add_game(sample_game)
        
        result = db.update_status(game_id, GameStatus.EXTRACTED)
        
        assert result is True
        
        retrieved = db.get_game(game_id)
        assert retrieved.status == GameStatus.EXTRACTED
    
    def test_update_status_with_fields(self, db, sample_game):
        """Verifica actualización de status con campos adicionales."""
        game_id = db.add_game(sample_game)
        
        db.update_status(
            game_id, 
            GameStatus.DUMPED,
            iso_path="/path/to/game.iso"
        )
        
        retrieved = db.get_game(game_id)
        assert retrieved.status == GameStatus.DUMPED
        assert retrieved.iso_path == "/path/to/game.iso"


class TestDeleteGame:
    """Tests para eliminar juegos."""
    
    def test_delete_existing_game(self, db, sample_game):
        """Verifica eliminación de juego existente."""
        game_id = db.add_game(sample_game)
        
        result = db.delete_game(game_id)
        
        assert result is True
        assert db.get_game(game_id) is None
    
    def test_delete_nonexistent_game(self, db):
        """Verifica que delete retorna False para ID inexistente."""
        result = db.delete_game(999)
        
        assert result is False


class TestListGames:
    """Tests para listar juegos."""
    
    def test_list_empty(self, db):
        """Verifica lista vacía."""
        games = db.list_games()
        
        assert games == []
    
    def test_list_all_games(self, db):
        """Verifica listado de todos los juegos."""
        db.add_game(Game(game_name="Game 1"))
        db.add_game(Game(game_name="Game 2"))
        db.add_game(Game(game_name="Game 3"))
        
        games = db.list_games()
        
        assert len(games) == 3
    
    def test_list_by_status(self, db):
        """Verifica filtrado por status."""
        db.add_game(Game(game_name="Pending", status=GameStatus.PENDING))
        db.add_game(Game(game_name="Completed", status=GameStatus.COMPLETED))
        db.add_game(Game(game_name="Failed", status=GameStatus.FAILED))
        
        completed = db.list_games(status=GameStatus.COMPLETED)
        
        assert len(completed) == 1
        assert completed[0].game_name == "Completed"


class TestSearch:
    """Tests para búsqueda."""
    
    def test_search_by_name(self, db):
        """Verifica búsqueda por nombre."""
        db.add_game(Game(game_name="Halo 3"))
        db.add_game(Game(game_name="Gears of War"))
        db.add_game(Game(game_name="Halo Reach"))
        
        results = db.search("Halo")
        
        assert len(results) == 2
    
    def test_search_by_title_id(self, db):
        """Verifica búsqueda por title_id."""
        db.add_game(Game(title_id="ABC123", game_name="Game 1"))
        db.add_game(Game(title_id="XYZ789", game_name="Game 2"))
        
        results = db.search("ABC")
        
        assert len(results) == 1
        assert results[0].game_name == "Game 1"
    
    def test_search_no_results(self, db):
        """Verifica búsqueda sin resultados."""
        db.add_game(Game(game_name="Test Game"))
        
        results = db.search("nonexistent")
        
        assert results == []


class TestCount:
    """Tests para conteo."""
    
    def test_count_empty(self, db):
        """Verifica conteo vacío."""
        assert db.count() == 0
    
    def test_count_all(self, db):
        """Verifica conteo total."""
        db.add_game(Game(game_name="Game 1"))
        db.add_game(Game(game_name="Game 2"))
        
        assert db.count() == 2
    
    def test_count_by_status(self, db):
        """Verifica conteo por status."""
        db.add_game(Game(game_name="G1", status=GameStatus.PENDING))
        db.add_game(Game(game_name="G2", status=GameStatus.COMPLETED))
        db.add_game(Game(game_name="G3", status=GameStatus.COMPLETED))
        
        assert db.count(GameStatus.COMPLETED) == 2
        assert db.count(GameStatus.PENDING) == 1


class TestContextManager:
    """Tests para context manager."""
    
    def test_with_statement(self):
        """Verifica uso con 'with'."""
        with GameDatabase(":memory:") as db:
            game_id = db.add_game(Game(game_name="Test"))
            assert game_id > 0
