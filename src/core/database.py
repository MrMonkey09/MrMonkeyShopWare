# core/database.py
"""
Base de datos SQLite para gestión de juegos procesados.
"""
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum
from pathlib import Path
import os


class GameStatus(Enum):
    """Estados posibles de un juego en el pipeline."""
    PENDING = "pending"
    DUMPED = "dumped"
    EXTRACTED = "extracted"
    ANALYSED = "analysed"
    IN_PROGRESS = "in_progress"  # Port en desarrollo activo
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Game:
    """Representa un juego en la base de datos."""
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
    # Campos de metadata de XexTool
    media_id: Optional[str] = None
    version: Optional[str] = None
    disc_number: int = 1
    total_discs: int = 1
    regions: Optional[str] = None
    esrb_rating: Optional[str] = None
    entry_point: Optional[str] = None
    original_pe_name: Optional[str] = None
    xex_info_json: Optional[str] = None  # JSON completo de XexInfo


def _get_default_db_path() -> str:
    """Retorna la ruta por defecto de la base de datos."""
    home = Path.home()
    db_dir = home / ".mrmonkeyshopware"
    db_dir.mkdir(parents=True, exist_ok=True)
    return str(db_dir / "games.db")


class GameDatabase:
    """
    Gestor de base de datos de juegos.
    
    Uso:
        db = GameDatabase()  # Usa ruta por defecto
        db = GameDatabase(":memory:")  # BD en memoria (para tests)
        
        game = Game(title_id="12345678", game_name="My Game")
        game_id = db.add_game(game)
        
        db.update_status(game_id, GameStatus.COMPLETED)
        games = db.list_games(status=GameStatus.COMPLETED)
    """
    
    def __init__(self, db_path: str = None):
        """
        Inicializa la conexión a la base de datos.
        
        :param db_path: Ruta a la BD. Si es None, usa ~/.mrmonkeyshopware/games.db
                        Usa ":memory:" para BD en memoria (tests)
        """
        self.db_path = db_path or _get_default_db_path()
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_schema()
    
    def _init_schema(self):
        """Crea las tablas si no existen."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_id TEXT UNIQUE,
                game_name TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                iso_path TEXT,
                extracted_dir TEXT,
                xex_path TEXT,
                analysis_json TEXT,
                project_toml TEXT,
                notes TEXT,
                media_id TEXT,
                version TEXT,
                disc_number INTEGER DEFAULT 1,
                total_discs INTEGER DEFAULT 1,
                regions TEXT,
                esrb_rating TEXT,
                entry_point TEXT,
                original_pe_name TEXT,
                xex_info_json TEXT
            )
        """)
        
        # Migración: añadir columnas nuevas si no existen
        self._migrate_schema(cursor)
        
        # Crear índices para búsquedas rápidas
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_games_status ON games(status)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_games_title_id ON games(title_id)
        """)
        
        self.conn.commit()
    
    def _migrate_schema(self, cursor):
        """Añade columnas nuevas para usuarios existentes."""
        new_columns = [
            ("media_id", "TEXT"),
            ("version", "TEXT"),
            ("disc_number", "INTEGER DEFAULT 1"),
            ("total_discs", "INTEGER DEFAULT 1"),
            ("regions", "TEXT"),
            ("esrb_rating", "TEXT"),
            ("entry_point", "TEXT"),
            ("original_pe_name", "TEXT"),
            ("xex_info_json", "TEXT"),
        ]
        
        for column_name, column_type in new_columns:
            try:
                cursor.execute(f"ALTER TABLE games ADD COLUMN {column_name} {column_type}")
            except Exception:
                pass  # Columna ya existe
    
    def _row_to_game(self, row: sqlite3.Row) -> Game:
        """Convierte una fila de SQLite a un objeto Game."""
        # Helper para obtener campos que pueden no existir en BD antiguas
        def get_field(name, default=None):
            try:
                return row[name]
            except (IndexError, KeyError):
                return default
        
        return Game(
            id=row["id"],
            title_id=row["title_id"] or "",
            game_name=row["game_name"],
            status=GameStatus(row["status"]),
            created_at=datetime.fromisoformat(row["created_at"]) if row["created_at"] else None,
            updated_at=datetime.fromisoformat(row["updated_at"]) if row["updated_at"] else None,
            iso_path=row["iso_path"],
            extracted_dir=row["extracted_dir"],
            xex_path=row["xex_path"],
            analysis_json=row["analysis_json"],
            project_toml=row["project_toml"],
            notes=row["notes"],
            # Nuevos campos de metadata
            media_id=get_field("media_id"),
            version=get_field("version"),
            disc_number=get_field("disc_number", 1) or 1,
            total_discs=get_field("total_discs", 1) or 1,
            regions=get_field("regions"),
            esrb_rating=get_field("esrb_rating"),
            entry_point=get_field("entry_point"),
            original_pe_name=get_field("original_pe_name"),
            xex_info_json=get_field("xex_info_json"),
        )
    
    def add_game(self, game: Game) -> int:
        """
        Añade un juego a la base de datos.
        
        :param game: Objeto Game a insertar
        :return: ID del juego insertado
        :raises sqlite3.IntegrityError: Si el title_id ya existe
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO games (
                title_id, game_name, status, iso_path, extracted_dir,
                xex_path, analysis_json, project_toml, notes,
                media_id, version, disc_number, total_discs,
                regions, esrb_rating, entry_point, original_pe_name, xex_info_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            game.title_id or None,
            game.game_name,
            game.status.value,
            game.iso_path,
            game.extracted_dir,
            game.xex_path,
            game.analysis_json,
            game.project_toml,
            game.notes,
            game.media_id,
            game.version,
            game.disc_number,
            game.total_discs,
            game.regions,
            game.esrb_rating,
            game.entry_point,
            game.original_pe_name,
            game.xex_info_json,
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_or_update_game(self, game: Game) -> int:
        """
        Añade un juego o actualiza si ya existe (por title_id).
        
        :param game: Objeto Game a insertar/actualizar
        :return: ID del juego
        """
        # Buscar si existe por title_id
        if game.title_id:
            existing = self.get_by_title_id(game.title_id)
            if existing:
                # Actualizar juego existente
                game.id = existing.id
                # Mantener campos que no queremos sobrescribir
                if not game.notes and existing.notes:
                    game.notes = existing.notes
                if not game.iso_path and existing.iso_path:
                    game.iso_path = existing.iso_path
                self.update_game(game)
                return existing.id
        
        # Insertar nuevo
        return self.add_game(game)
    
    def get_game(self, game_id: int) -> Optional[Game]:
        """
        Obtiene un juego por ID.
        
        :param game_id: ID del juego
        :return: Objeto Game o None si no existe
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM games WHERE id = ?", (game_id,))
        row = cursor.fetchone()
        return self._row_to_game(row) if row else None
    
    def get_by_title_id(self, title_id: str) -> Optional[Game]:
        """
        Obtiene un juego por Title ID.
        
        :param title_id: Title ID del juego (ej: "12345678")
        :return: Objeto Game o None si no existe
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM games WHERE title_id = ?", (title_id,))
        row = cursor.fetchone()
        return self._row_to_game(row) if row else None
    
    def update_game(self, game: Game) -> bool:
        """
        Actualiza un juego existente.
        
        :param game: Objeto Game con ID válido
        :return: True si se actualizó, False si no existe
        """
        if game.id is None:
            return False
        
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE games SET
                title_id = ?,
                game_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP,
                iso_path = ?,
                extracted_dir = ?,
                xex_path = ?,
                analysis_json = ?,
                project_toml = ?,
                notes = ?,
                media_id = ?,
                version = ?,
                disc_number = ?,
                total_discs = ?,
                regions = ?,
                esrb_rating = ?,
                entry_point = ?,
                original_pe_name = ?,
                xex_info_json = ?
            WHERE id = ?
        """, (
            game.title_id or None,
            game.game_name,
            game.status.value,
            game.iso_path,
            game.extracted_dir,
            game.xex_path,
            game.analysis_json,
            game.project_toml,
            game.notes,
            game.media_id,
            game.version,
            game.disc_number,
            game.total_discs,
            game.regions,
            game.esrb_rating,
            game.entry_point,
            game.original_pe_name,
            game.xex_info_json,
            game.id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def update_status(self, game_id: int, status: GameStatus, **kwargs) -> bool:
        """
        Actualiza el status de un juego y opcionalmente otros campos.
        
        :param game_id: ID del juego
        :param status: Nuevo status
        :param kwargs: Campos adicionales a actualizar (iso_path, xex_path, etc.)
        :return: True si se actualizó
        """
        # Construir query dinámicamente
        set_clauses = ["status = ?", "updated_at = CURRENT_TIMESTAMP"]
        values = [status.value]
        
        valid_fields = ["iso_path", "extracted_dir", "xex_path", 
                       "analysis_json", "project_toml", "notes"]
        
        for field_name in valid_fields:
            if field_name in kwargs:
                set_clauses.append(f"{field_name} = ?")
                values.append(kwargs[field_name])
        
        values.append(game_id)
        
        cursor = self.conn.cursor()
        cursor.execute(
            f"UPDATE games SET {', '.join(set_clauses)} WHERE id = ?",
            values
        )
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_game(self, game_id: int) -> bool:
        """
        Elimina un juego.
        
        :param game_id: ID del juego a eliminar
        :return: True si se eliminó
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM games WHERE id = ?", (game_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def list_games(self, status: GameStatus = None, limit: int = 100) -> List[Game]:
        """
        Lista juegos, opcionalmente filtrados por status.
        
        :param status: Filtrar por status (opcional)
        :param limit: Límite de resultados (default: 100)
        :return: Lista de objetos Game
        """
        cursor = self.conn.cursor()
        
        if status:
            cursor.execute(
                "SELECT * FROM games WHERE status = ? ORDER BY updated_at DESC LIMIT ?",
                (status.value, limit)
            )
        else:
            cursor.execute(
                "SELECT * FROM games ORDER BY updated_at DESC LIMIT ?",
                (limit,)
            )
        
        return [self._row_to_game(row) for row in cursor.fetchall()]
    
    def search(self, query: str) -> List[Game]:
        """
        Busca juegos por nombre o title_id.
        
        :param query: Término de búsqueda
        :return: Lista de juegos que coinciden
        """
        cursor = self.conn.cursor()
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM games 
            WHERE game_name LIKE ? OR title_id LIKE ?
            ORDER BY updated_at DESC
        """, (search_term, search_term))
        
        return [self._row_to_game(row) for row in cursor.fetchall()]
    
    def count(self, status: GameStatus = None) -> int:
        """
        Cuenta el número de juegos.
        
        :param status: Filtrar por status (opcional)
        :return: Número de juegos
        """
        cursor = self.conn.cursor()
        
        if status:
            cursor.execute(
                "SELECT COUNT(*) FROM games WHERE status = ?",
                (status.value,)
            )
        else:
            cursor.execute("SELECT COUNT(*) FROM games")
        
        return cursor.fetchone()[0]
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        self.conn.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
