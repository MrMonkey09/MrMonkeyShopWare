# core/game_workspace.py
"""
Gestión de directorios de trabajo para cada juego/port.
Centraliza todos los archivos generados en una estructura organizada.
"""
import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

from core.xex_parser import XexInfo


def get_base_ports_dir() -> Path:
    """Obtiene el directorio base para todos los ports."""
    # Usar directorio de usuario
    base = Path.home() / "MrMonkeyShopWare" / "ports"
    base.mkdir(parents=True, exist_ok=True)
    return base


def sanitize_folder_name(name: str) -> str:
    """Sanitiza un nombre para usarlo como carpeta."""
    # Caracteres no permitidos en Windows
    invalid_chars = '<>:"/\\|?*'
    result = name
    for char in invalid_chars:
        result = result.replace(char, '_')
    # Limitar longitud
    return result[:50].strip()


@dataclass
class GameInfo:
    """Información completa de un juego guardada en info.json."""
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
    source_type: str = ""  # "iso", "xex", "usb", "god", etc.
    source_path: str = ""
    created_at: str = ""
    updated_at: str = ""
    status: str = "pending"
    notes: str = ""
    
    @classmethod
    def from_xex_info(cls, xex_info: XexInfo, source_type: str = "", source_path: str = "") -> "GameInfo":
        """Crea GameInfo desde XexInfo."""
        now = datetime.now().isoformat()
        return cls(
            title_id=xex_info.title_id,
            game_name=xex_info.display_name or xex_info.original_pe_name,
            version=xex_info.version,
            media_id=xex_info.media_id,
            regions=xex_info.regions,
            esrb_rating=xex_info.esrb_rating,
            disc_number=xex_info.disc_number,
            total_discs=xex_info.total_discs,
            entry_point=xex_info.entry_point,
            original_pe_name=xex_info.original_pe_name,
            source_type=source_type,
            source_path=source_path,
            created_at=now,
            updated_at=now,
            status="analysed"
        )


@dataclass
class ExternalFile:
    """Representa un archivo que está fuera del workspace."""
    file_type: str      # "xex", "iso", "toml", "json"
    label: str          # Etiqueta para mostrar
    current_path: str   # Ruta actual (externa)
    target_path: str    # Ruta destino en workspace
    size: int = 0       # Tamaño en bytes


class GameWorkspace:
    """
    Gestiona el directorio de trabajo de un juego.
    
    Estructura:
        ~/MrMonkeyShopWare/ports/GameName [TitleID]/
        ├── info.json
        ├── analysis/
        ├── extracted/
        ├── cleaned/
        ├── recompiled/
        └── notes.md
    """
    
    def __init__(self, title_id: str, game_name: str = ""):
        self.title_id = title_id
        self.game_name = game_name or title_id
        self._root: Optional[Path] = None
    
    @property
    def folder_name(self) -> str:
        """Nombre de la carpeta del juego."""
        clean_name = sanitize_folder_name(self.game_name)
        return f"{clean_name} [{self.title_id}]"
    
    @property
    def root(self) -> Path:
        """Directorio raíz del workspace."""
        if self._root is None:
            self._root = get_base_ports_dir() / self.folder_name
        return self._root
    
    @property
    def analysis_dir(self) -> Path:
        """Directorio para archivos de análisis."""
        return self.root / "analysis"
    
    @property
    def extracted_dir(self) -> Path:
        """Directorio para contenido extraído del ISO."""
        return self.root / "extracted"
    
    @property
    def cleaned_dir(self) -> Path:
        """Directorio para XEX limpios."""
        return self.root / "cleaned"
    
    @property
    def recompiled_dir(self) -> Path:
        """Directorio para código recompilado."""
        return self.root / "recompiled"
    
    @property
    def info_file(self) -> Path:
        """Archivo info.json."""
        return self.root / "info.json"
    
    @property
    def notes_file(self) -> Path:
        """Archivo de notas."""
        return self.root / "notes.md"
    
    def exists(self) -> bool:
        """Verifica si el workspace ya existe."""
        return self.root.exists()
    
    def create(self) -> Path:
        """Crea la estructura de directorios."""
        self.root.mkdir(parents=True, exist_ok=True)
        self.analysis_dir.mkdir(exist_ok=True)
        self.extracted_dir.mkdir(exist_ok=True)
        self.cleaned_dir.mkdir(exist_ok=True)
        self.recompiled_dir.mkdir(exist_ok=True)
        
        # Crear notes.md si no existe
        if not self.notes_file.exists():
            self.notes_file.write_text(f"# {self.game_name}\n\nNotas del port:\n\n")
        
        return self.root
    
    def save_info(self, game_info: GameInfo):
        """Guarda la información del juego en info.json."""
        game_info.updated_at = datetime.now().isoformat()
        
        with open(self.info_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(game_info), f, indent=2, ensure_ascii=False)
    
    def load_info(self) -> Optional[GameInfo]:
        """Carga la información del juego desde info.json."""
        if not self.info_file.exists():
            return None
        
        try:
            with open(self.info_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return GameInfo(**data)
        except Exception:
            return None
    
    def get_notes(self) -> str:
        """Lee las notas del juego."""
        if self.notes_file.exists():
            return self.notes_file.read_text(encoding='utf-8')
        return ""
    
    def save_notes(self, notes: str):
        """Guarda las notas del juego."""
        self.notes_file.write_text(notes, encoding='utf-8')
    
    def is_in_workspace(self, path: str) -> bool:
        """Verifica si una ruta está dentro del workspace."""
        if not path:
            return True  # Sin ruta = no hay problema
        
        try:
            path_resolved = Path(path).resolve()
            workspace_resolved = self.root.resolve()
            return str(path_resolved).startswith(str(workspace_resolved))
        except Exception:
            return False
    
    def check_external_files(self, game) -> list["ExternalFile"]:
        """
        Detecta archivos que están fuera del workspace.
        
        :param game: Objeto Game de la BD
        :return: Lista de archivos externos
        """
        external = []
        
        # Verificar XEX
        if game.xex_path and not self.is_in_workspace(game.xex_path):
            if os.path.exists(game.xex_path):
                external.append(ExternalFile(
                    file_type="xex",
                    label="🎮 XEX Principal",
                    current_path=game.xex_path,
                    target_path=str(self.root / "default.xex"),
                    size=os.path.getsize(game.xex_path)
                ))
        
        # Verificar ISO
        if game.iso_path and not self.is_in_workspace(game.iso_path):
            if os.path.exists(game.iso_path):
                external.append(ExternalFile(
                    file_type="iso",
                    label="📀 ISO Original",
                    current_path=game.iso_path,
                    target_path=str(self.root / "game.iso"),
                    size=os.path.getsize(game.iso_path)
                ))
        
        # Verificar TOML
        if game.project_toml and not self.is_in_workspace(game.project_toml):
            if os.path.exists(game.project_toml):
                external.append(ExternalFile(
                    file_type="toml",
                    label="📄 Analysis TOML",
                    current_path=game.project_toml,
                    target_path=str(self.analysis_dir / os.path.basename(game.project_toml)),
                    size=os.path.getsize(game.project_toml)
                ))
        
        # Verificar JSON
        if game.analysis_json and not self.is_in_workspace(game.analysis_json):
            if os.path.exists(game.analysis_json):
                external.append(ExternalFile(
                    file_type="json",
                    label="📊 Analysis JSON",
                    current_path=game.analysis_json,
                    target_path=str(self.analysis_dir / os.path.basename(game.analysis_json)),
                    size=os.path.getsize(game.analysis_json)
                ))
        
        return external
    
    def sync_file(self, external_file: "ExternalFile", log=None) -> bool:
        """
        Copia un archivo externo al workspace.
        
        :param external_file: Archivo a sincronizar
        :param log: Función de logging opcional
        :return: True si se copió correctamente
        """
        import shutil
        
        try:
            target = Path(external_file.target_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            
            if log:
                size_mb = external_file.size / (1024 * 1024)
                log(f"📥 Copiando {external_file.label} ({size_mb:.1f} MB)...")
            
            shutil.copy2(external_file.current_path, target)
            
            if log:
                log(f"   ✅ {os.path.basename(external_file.current_path)} → {target.name}")
            
            return True
        except Exception as e:
            if log:
                log(f"   ❌ Error: {e}")
            return False
    
    def sync_all_files(self, game, log=None) -> dict:
        """
        Sincroniza todos los archivos externos al workspace.
        
        :param game: Objeto Game de la BD
        :param log: Función de logging
        :return: Dict con nuevas rutas para actualizar en BD
        """
        external = self.check_external_files(game)
        new_paths = {}
        
        if not external:
            if log:
                log("✅ Todos los archivos ya están en el workspace")
            return new_paths
        
        if log:
            log(f"🔄 Sincronizando {len(external)} archivo(s)...\n")
        
        for ef in external:
            if self.sync_file(ef, log):
                # Mapear tipo a campo de BD
                field_map = {
                    "xex": "xex_path",
                    "iso": "iso_path",
                    "toml": "project_toml",
                    "json": "analysis_json"
                }
                if ef.file_type in field_map:
                    new_paths[field_map[ef.file_type]] = ef.target_path
        
        if log:
            log(f"\n✅ Sincronización completada ({len(new_paths)} archivos)")
        
        return new_paths
    
    @classmethod
    def find_existing(cls, title_id: str) -> Optional["GameWorkspace"]:
        """Busca un workspace existente por title_id."""
        base = get_base_ports_dir()
        
        if not base.exists():
            return None
        
        # Buscar carpetas que contengan el title_id
        # No usamos glob porque [] son caracteres especiales
        suffix = f"[{title_id}]"
        for folder in base.iterdir():
            if folder.is_dir() and folder.name.endswith(suffix):
                # Extraer nombre del juego
                name = folder.name.rsplit(' [', 1)[0]
                ws = cls(title_id, name)
                ws._root = folder
                return ws
        
        return None
    
    @classmethod
    def list_all(cls) -> list["GameWorkspace"]:
        """Lista todos los workspaces existentes."""
        base = get_base_ports_dir()
        workspaces = []
        
        if not base.exists():
            return workspaces
        
        for folder in base.iterdir():
            if folder.is_dir() and '[' in folder.name and ']' in folder.name:
                try:
                    # Extraer nombre y title_id
                    name, tid = folder.name.rsplit(' [', 1)
                    tid = tid.rstrip(']')
                    ws = cls(tid, name)
                    ws._root = folder
                    workspaces.append(ws)
                except ValueError:
                    continue
        
        return workspaces


def get_or_create_workspace(title_id: str, game_name: str) -> tuple[GameWorkspace, bool]:
    """
    Obtiene un workspace existente o crea uno nuevo.
    
    Returns:
        (workspace, is_new): Tupla con el workspace y si es nuevo
    """
    existing = GameWorkspace.find_existing(title_id)
    
    if existing:
        return existing, False
    
    new_ws = GameWorkspace(title_id, game_name)
    new_ws.create()
    return new_ws, True
