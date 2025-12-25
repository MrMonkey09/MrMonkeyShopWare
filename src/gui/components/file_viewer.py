# gui/components/file_viewer.py
"""
Visor de estructura de archivos en formato árbol.
Soporta JSON y TOML.
"""
import customtkinter as ctk
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional


# Iconos por tipo de dato
TYPE_ICONS = {
    "dict": "📁",
    "list": "📋",
    "str": "🔤",
    "int": "🔢",
    "float": "🔢",
    "bool_true": "✅",
    "bool_false": "❌",
    "none": "⬜",
    "file": "📄",
}

# Colores por tipo de dato (light, dark)
TYPE_COLORS = {
    "dict": ("#1E88E5", "#64B5F6"),
    "list": ("#7B1FA2", "#BA68C8"),
    "str": ("#388E3C", "#81C784"),
    "int": ("#F57C00", "#FFB74D"),
    "float": ("#F57C00", "#FFB74D"),
    "bool": ("#0097A7", "#4DD0E1"),
    "none": ("#757575", "#BDBDBD"),
    "key": ("#1a1a2e", "#e0e0e0"),
}


class FileStructureViewer(ctk.CTkFrame):
    """
    Visor de estructura de archivos en formato árbol.
    
    Muestra JSON y TOML de forma legible con iconos por tipo.
    """
    
    def __init__(self, parent, workspace_dir: Optional[Path] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.workspace_dir = workspace_dir
        self.configure(fg_color="transparent")
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header()
        self._create_viewer()
        self._populate_files()
    
    def _create_header(self):
        """Crea el header con selector de archivo."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            header,
            text="📄 Ver archivo:",
            font=ctk.CTkFont(size=13)
        ).grid(row=0, column=0, padx=(0, 10))
        
        self.file_var = ctk.StringVar(value="Seleccionar...")
        self.file_menu = ctk.CTkOptionMenu(
            header,
            values=["Seleccionar..."],
            variable=self.file_var,
            command=self._on_file_select,
            width=250
        )
        self.file_menu.grid(row=0, column=1, sticky="w")
        
        # Botón refrescar
        refresh_btn = ctk.CTkButton(
            header,
            text="🔄",
            width=35,
            command=self._populate_files
        )
        refresh_btn.grid(row=0, column=2, padx=(10, 0))
    
    def _create_viewer(self):
        """Crea el área de visualización."""
        self.viewer = ctk.CTkScrollableFrame(
            self,
            fg_color=("gray90", "gray17"),
            corner_radius=10
        )
        self.viewer.grid(row=1, column=0, sticky="nsew")
        self.viewer.grid_columnconfigure(0, weight=1)
        
        # Mensaje inicial
        self.placeholder = ctk.CTkLabel(
            self.viewer,
            text="Selecciona un archivo para ver su estructura",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        self.placeholder.grid(row=0, column=0, pady=50)
    
    def _populate_files(self):
        """Detecta archivos disponibles en el workspace."""
        files = ["Seleccionar..."]
        
        if self.workspace_dir and self.workspace_dir.exists():
            # Archivos en raíz
            for f in ["info.json", "notes.md"]:
                path = self.workspace_dir / f
                if path.exists():
                    files.append(f)
            
            # Archivos en analysis/
            analysis_dir = self.workspace_dir / "analysis"
            if analysis_dir.exists():
                for f in analysis_dir.iterdir():
                    if f.suffix in [".json", ".toml"]:
                        files.append(f"analysis/{f.name}")
        
        self.file_menu.configure(values=files)
    
    def _on_file_select(self, filename: str):
        """Maneja selección de archivo."""
        if filename == "Seleccionar..." or not self.workspace_dir:
            return
        
        file_path = self.workspace_dir / filename
        
        if not file_path.exists():
            self._show_error(f"Archivo no encontrado: {filename}")
            return
        
        self._load_file(file_path)
    
    def _load_file(self, file_path: Path):
        """Carga y muestra un archivo."""
        # Limpiar viewer
        for widget in self.viewer.winfo_children():
            widget.destroy()
        
        try:
            suffix = file_path.suffix.lower()
            
            if suffix == ".json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self._render_tree(file_path.name, data)
                
            elif suffix == ".toml":
                try:
                    import tomllib
                except ImportError:
                    import tomli as tomllib
                
                with open(file_path, 'rb') as f:
                    data = tomllib.load(f)
                self._render_tree(file_path.name, data)
                
            elif suffix == ".md":
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._render_text(file_path.name, content)
                
            else:
                self._show_error(f"Formato no soportado: {suffix}")
                
        except Exception as e:
            self._show_error(f"Error al leer archivo: {e}")
    
    def _render_tree(self, filename: str, data: Any, parent: ctk.CTkFrame = None, depth: int = 0):
        """Renderiza datos como árbol."""
        container = parent or self.viewer
        
        # Header del archivo
        if depth == 0:
            header = ctk.CTkFrame(container, fg_color="transparent")
            header.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=10)
            
            ctk.CTkLabel(
                header,
                text=f"📄 {filename}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color=("#1a1a2e", "#ffffff")
            ).pack(side="left")
        
        # Renderizar contenido
        self._render_value(container, "", data, depth, is_root=True)
    
    def _render_value(self, parent: ctk.CTkFrame, key: str, value: Any, depth: int, is_root: bool = False):
        """Renderiza un valor con su clave."""
        row_frame = ctk.CTkFrame(parent, fg_color="transparent")
        row_frame.grid(sticky="w", padx=(10 + depth * 20, 10), pady=2)
        
        # Determinar tipo e icono
        if isinstance(value, dict):
            icon = TYPE_ICONS["dict"]
            type_color = TYPE_COLORS["dict"]
            
            # Mostrar clave si no es raíz
            if key and not is_root:
                self._add_key_value_row(row_frame, key, f"({len(value)} items)", icon, type_color, is_expandable=True)
            
            # Renderizar hijos
            for i, (k, v) in enumerate(value.items()):
                self._render_value(parent, k, v, depth + 1 if key else depth)
                
        elif isinstance(value, list):
            icon = TYPE_ICONS["list"]
            type_color = TYPE_COLORS["list"]
            
            if key:
                self._add_key_value_row(row_frame, key, f"[{len(value)} items]", icon, type_color)
            
            # Renderizar items
            for i, item in enumerate(value[:10]):  # Limitar a 10 items
                self._render_value(parent, f"[{i}]", item, depth + 1)
            
            if len(value) > 10:
                more_frame = ctk.CTkFrame(parent, fg_color="transparent")
                more_frame.grid(sticky="w", padx=(10 + (depth + 1) * 20, 10), pady=2)
                ctk.CTkLabel(
                    more_frame,
                    text=f"... y {len(value) - 10} más",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray50", "gray60")
                ).pack(side="left")
                
        elif isinstance(value, bool):
            icon = TYPE_ICONS["bool_true"] if value else TYPE_ICONS["bool_false"]
            type_color = TYPE_COLORS["bool"]
            self._add_key_value_row(row_frame, key, str(value), icon, type_color)
            
        elif isinstance(value, int):
            icon = TYPE_ICONS["int"]
            type_color = TYPE_COLORS["int"]
            self._add_key_value_row(row_frame, key, str(value), icon, type_color)
            
        elif isinstance(value, float):
            icon = TYPE_ICONS["float"]
            type_color = TYPE_COLORS["float"]
            self._add_key_value_row(row_frame, key, f"{value:.4f}", icon, type_color)
            
        elif value is None:
            icon = TYPE_ICONS["none"]
            type_color = TYPE_COLORS["none"]
            self._add_key_value_row(row_frame, key, "null", icon, type_color)
            
        else:
            # String u otro
            icon = TYPE_ICONS["str"]
            type_color = TYPE_COLORS["str"]
            display_value = str(value)
            if len(display_value) > 50:
                display_value = display_value[:47] + "..."
            self._add_key_value_row(row_frame, key, f'"{display_value}"', icon, type_color)
    
    def _add_key_value_row(self, parent: ctk.CTkFrame, key: str, value: str, icon: str, color: tuple, is_expandable: bool = False):
        """Añade una fila clave: valor."""
        # Prefijo de árbol
        prefix = "├── " if not is_expandable else "📁 "
        
        # Icono
        ctk.CTkLabel(
            parent,
            text=icon,
            font=ctk.CTkFont(size=12),
            width=20
        ).pack(side="left", padx=(0, 2))
        
        # Clave
        if key:
            ctk.CTkLabel(
                parent,
                text=f"{key}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=TYPE_COLORS["key"]
            ).pack(side="left", padx=(0, 5))
        
        # Valor
        ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(size=12),
            text_color=color
        ).pack(side="left")
    
    def _render_text(self, filename: str, content: str):
        """Renderiza texto plano o markdown."""
        # Header
        header = ctk.CTkFrame(self.viewer, fg_color="transparent")
        header.grid(row=0, column=0, sticky="w", pady=(10, 5), padx=10)
        
        ctk.CTkLabel(
            header,
            text=f"📝 {filename}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        ).pack(side="left")
        
        # Contenido
        text_frame = ctk.CTkFrame(self.viewer, fg_color=("white", "gray20"))
        text_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        text_label = ctk.CTkLabel(
            text_frame,
            text=content[:2000] if len(content) > 2000 else content,
            font=ctk.CTkFont(size=11, family="Consolas"),
            justify="left",
            anchor="nw",
            wraplength=500
        )
        text_label.pack(padx=15, pady=15, anchor="nw")
    
    def _show_error(self, message: str):
        """Muestra un mensaje de error."""
        for widget in self.viewer.winfo_children():
            widget.destroy()
        
        ctk.CTkLabel(
            self.viewer,
            text=f"❌ {message}",
            font=ctk.CTkFont(size=12),
            text_color=("#CC0000", "#FF6B6B")
        ).grid(row=0, column=0, pady=50)
