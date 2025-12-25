# gui/components/gamedetail.py
"""
Vista de detalle de un juego para gestionar su port.
"""
import customtkinter as ctk
import json
import os
import subprocess
from typing import Callable, Optional
from core.database import GameDatabase, Game, GameStatus


class GameDetailView(ctk.CTkFrame):
    """
    Vista de detalle para gestionar un port individual.
    
    Muestra:
    - Información del juego (metadata)
    - Archivos generados (XEX, TOML, JSON)
    - Estado actual y botones para cambiar
    - Notas del usuario
    """
    
    STATUS_COLORS = {
        GameStatus.PENDING: ("#E0E0E0", "#4a4a5e"),
        GameStatus.DUMPED: ("#FFB347", "#CC8800"),
        GameStatus.EXTRACTED: ("#87CEEB", "#4682B4"),
        GameStatus.ANALYSED: ("#DDA0DD", "#9932CC"),
        GameStatus.IN_PROGRESS: ("#FFD700", "#DAA520"),
        GameStatus.COMPLETED: ("#90EE90", "#228B22"),
        GameStatus.FAILED: ("#FF6B6B", "#CC0000"),
    }
    
    def __init__(
        self, 
        parent, 
        game: Game, 
        on_back: Callable = None,
        on_update: Callable[[Game], None] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.game = game
        self.on_back = on_back
        self.on_update = on_update
        
        self.configure(fg_color="transparent")
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header()
        self._create_content()
        self._create_actions()
    
    def _create_header(self):
        """Crea el header con nombre del juego y botón volver."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header.grid_columnconfigure(1, weight=1)
        
        # Botón volver
        back_btn = ctk.CTkButton(
            header,
            text="← Volver",
            width=80,
            height=30,
            fg_color="transparent",
            hover_color=("gray70", "gray30"),
            text_color=("gray30", "gray70"),
            command=self._on_back_click
        )
        back_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Nombre del juego
        name = self.game.game_name or "Juego sin nombre"
        self.title_label = ctk.CTkLabel(
            header,
            text=f"🎮 {name}",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.grid(row=0, column=1, sticky="w")
        
        # Badge de status
        color = self.STATUS_COLORS.get(self.game.status, ("#666666", "#666666"))
        self.status_badge = ctk.CTkLabel(
            header,
            text=f" {self.game.status.value} ",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=color,
            corner_radius=8,
            padx=10
        )
        self.status_badge.grid(row=0, column=2, padx=10)
    
    def _create_content(self):
        """Crea el contenido principal con pestañas."""
        self.tabview = ctk.CTkTabview(self)
        self.tabview.grid(row=1, column=0, sticky="nsew")
        
        # Pestañas
        self.tab_info = self.tabview.add("📋 Info")
        self.tab_files = self.tabview.add("📁 Archivos")
        self.tab_structure = self.tabview.add("📊 Estructura")
        self.tab_notes = self.tabview.add("📝 Notas")
        
        self._setup_info_tab()
        self._setup_files_tab()
        self._setup_structure_tab()
        self._setup_notes_tab()
    
    def _setup_info_tab(self):
        """Configura la pestaña de información."""
        tab = self.tab_info
        tab.grid_columnconfigure(1, weight=1)
        
        # Información del juego
        info_items = [
            ("Title ID", self.game.title_id or "N/A"),
            ("Media ID", self.game.media_id or "N/A"),
            ("Versión", self.game.version or "N/A"),
            ("Disco", f"{self.game.disc_number} de {self.game.total_discs}"),
            ("Regiones", self.game.regions or "N/A"),
            ("Rating", self.game.esrb_rating or "N/A"),
            ("Entry Point", self.game.entry_point or "N/A"),
            ("PE Original", self.game.original_pe_name or "N/A"),
        ]
        
        for i, (label, value) in enumerate(info_items):
            lbl = ctk.CTkLabel(
                tab,
                text=f"{label}:",
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color=("gray30", "gray70")
            )
            lbl.grid(row=i, column=0, padx=(10, 5), pady=5, sticky="e")
            
            val = ctk.CTkLabel(
                tab,
                text=value,
                font=ctk.CTkFont(size=13),
                anchor="w"
            )
            val.grid(row=i, column=1, padx=5, pady=5, sticky="w")
        
        # Librerías estáticas (si hay)
        if self.game.xex_info_json:
            try:
                xex_info = json.loads(self.game.xex_info_json)
                libs = xex_info.get("static_libraries", [])
                if libs:
                    lbl = ctk.CTkLabel(
                        tab,
                        text="Librerías:",
                        font=ctk.CTkFont(size=13, weight="bold"),
                        text_color=("gray30", "gray70")
                    )
                    lbl.grid(row=len(info_items), column=0, padx=(10, 5), pady=5, sticky="ne")
                    
                    libs_text = "\n".join(libs[:5])
                    val = ctk.CTkLabel(
                        tab,
                        text=libs_text,
                        font=ctk.CTkFont(size=11),
                        justify="left",
                        anchor="w"
                    )
                    val.grid(row=len(info_items), column=1, padx=5, pady=5, sticky="w")
            except (json.JSONDecodeError, TypeError):
                pass
    
    def _setup_files_tab(self):
        """Configura la pestaña de archivos con checklist."""
        from pathlib import Path
        from tkinter import filedialog
        import shutil
        
        tab = self.tab_files
        
        # Limpiar tab primero
        for widget in tab.winfo_children():
            widget.destroy()
        
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(2, weight=1)
        
        # Obtener directorio workspace del juego
        workspace_dir = None
        self.workspace = None
        if self.game.extracted_dir and os.path.isdir(self.game.extracted_dir):
            workspace_dir = Path(self.game.extracted_dir)
            from core.game_workspace import GameWorkspace
            self.workspace = GameWorkspace.find_existing(self.game.title_id)
        
        # Detectar archivos externos
        external_files = []
        if self.workspace:
            external_files = self.workspace.check_external_files(self.game)
        
        # Header
        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(5, 5), padx=5)
        
        ctk.CTkLabel(
            header,
            text="📋 Checklist de Archivos",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left")
        
        if workspace_dir:
            open_folder_btn = ctk.CTkButton(
                header,
                text="📂 Abrir",
                width=80,
                height=28,
                command=lambda: self._open_path(str(workspace_dir))
            )
            open_folder_btn.pack(side="right", padx=(5, 0))
            
            # Botón sincronizar si hay externos
            if external_files:
                sync_btn = ctk.CTkButton(
                    header,
                    text="🔄 Sincronizar Todo",
                    width=130,
                    height=28,
                    fg_color=("#FF9800", "#E65100"),
                    hover_color=("#FFB74D", "#F57C00"),
                    command=self._sync_all_files
                )
                sync_btn.pack(side="right", padx=(5, 0))
        
        # Banner de advertencia si hay externos
        if external_files:
            warning_frame = ctk.CTkFrame(tab, fg_color=("#FFF3E0", "#3D2814"))
            warning_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
            
            ctk.CTkLabel(
                warning_frame,
                text=f"⚠️ {len(external_files)} archivo(s) fuera del workspace - Click 'Sincronizar' para centralizar",
                font=ctk.CTkFont(size=11),
                text_color=("#E65100", "#FFB74D")
            ).pack(padx=10, pady=8)
        
        # Scrollable frame para la lista
        scroll = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)
        scroll.grid_columnconfigure(0, weight=1)
        
        # Definir archivos esperados
        expected_files = [
            ("xex", "🎮 XEX Principal", self.game.xex_path, "default.xex", [".xex"]),
            ("toml", "📄 Analysis TOML", self.game.project_toml, "analysis/analysis.toml", [".toml"]),
            ("json", "📊 Analysis JSON", self.game.analysis_json, "analysis/analysis.json", [".json"]),
            ("iso", "📀 ISO Original", self.game.iso_path, "game.iso", [".iso"]),
            ("info", "📋 Info JSON", str(workspace_dir / "info.json") if workspace_dir else None, "info.json", [".json"]),
        ]
        
        # Extra: archivos del workspace
        if workspace_dir:
            expected_files.extend([
                ("notes", "📝 Notas", str(workspace_dir / "notes.md"), "notes.md", [".md", ".txt"]),
            ])
        
        self.file_rows = {}
        
        for i, (file_id, label, current_path, relative_dest, extensions) in enumerate(expected_files):
            exists = current_path and os.path.exists(current_path)
            
            frame = ctk.CTkFrame(scroll, fg_color=("gray88", "gray22"))
            frame.grid(row=i, column=0, sticky="ew", pady=3)
            frame.grid_columnconfigure(2, weight=1)
            
            # Icono de estado
            status_icon = "✅" if exists else "❓"
            status_color = ("#228B22", "#90EE90") if exists else ("#CC8800", "#FFB347")
            
            status_lbl = ctk.CTkLabel(
                frame,
                text=status_icon,
                font=ctk.CTkFont(size=16),
                text_color=status_color,
                width=30
            )
            status_lbl.grid(row=0, column=0, padx=(8, 5), pady=8)
            
            # Nombre del archivo
            name_lbl = ctk.CTkLabel(
                frame,
                text=label,
                font=ctk.CTkFont(size=12, weight="bold"),
                anchor="w",
                width=140
            )
            name_lbl.grid(row=0, column=1, padx=5, pady=8, sticky="w")
            
            if exists:
                # Mostrar nombre del archivo
                basename = os.path.basename(current_path)
                path_lbl = ctk.CTkLabel(
                    frame,
                    text=basename,
                    font=ctk.CTkFont(size=11),
                    text_color=("gray40", "gray60"),
                    anchor="w"
                )
                path_lbl.grid(row=0, column=2, padx=5, pady=8, sticky="w")
                
                # Botón abrir
                open_btn = ctk.CTkButton(
                    frame,
                    text="📂",
                    width=30,
                    height=26,
                    command=lambda p=current_path: self._open_path(p)
                )
                open_btn.grid(row=0, column=3, padx=(5, 8), pady=5)
            else:
                # Texto "No encontrado"
                missing_lbl = ctk.CTkLabel(
                    frame,
                    text="No encontrado",
                    font=ctk.CTkFont(size=11),
                    text_color=("gray50", "gray50"),
                    anchor="w"
                )
                missing_lbl.grid(row=0, column=2, padx=5, pady=8, sticky="w")
                
                # Botón buscar (solo si tiene destino en workspace)
                if relative_dest and workspace_dir:
                    search_btn = ctk.CTkButton(
                        frame,
                        text="❓ Buscar",
                        width=80,
                        height=26,
                        fg_color=("#FFB347", "#CC8800"),
                        hover_color=("#FFC969", "#E09900"),
                        command=lambda dest=relative_dest, exts=extensions, fid=file_id, f=frame: 
                            self._search_and_copy_file(dest, exts, fid, f)
                    )
                    search_btn.grid(row=0, column=3, padx=(5, 8), pady=5)
            
            self.file_rows[file_id] = frame
    
    def _search_and_copy_file(self, relative_dest: str, extensions: list, file_id: str, frame):
        """Busca un archivo y lo copia al workspace."""
        from tkinter import filedialog, messagebox
        from pathlib import Path
        import shutil
        
        # Construir filtro de extensiones
        ext_str = " ".join(f"*{e}" for e in extensions)
        filetypes = [(f"Archivos ({ext_str})", ext_str), ("Todos", "*.*")]
        
        file_path = filedialog.askopenfilename(
            title=f"Buscar archivo",
            filetypes=filetypes
        )
        
        if not file_path:
            return
        
        # Obtener workspace
        workspace_dir = Path(self.game.extracted_dir) if self.game.extracted_dir else None
        
        if not workspace_dir or not workspace_dir.exists():
            messagebox.showerror("Error", "No se encontró el directorio del juego")
            return
        
        # Destino
        dest_path = workspace_dir / relative_dest
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            shutil.copy2(file_path, dest_path)
            messagebox.showinfo("Copiado", f"✅ Archivo copiado a:\n{dest_path}")
            
            # Actualizar UI - refrescar pestaña
            self._setup_files_tab()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo copiar: {e}")
    
    def _sync_all_files(self):
        """Sincroniza todos los archivos externos al workspace."""
        from tkinter import messagebox
        
        if not self.workspace:
            messagebox.showerror("Error", "No se encontró el workspace")
            return
        
        # Confirmar
        external = self.workspace.check_external_files(self.game)
        if not external:
            messagebox.showinfo("Sincronización", "✅ Todos los archivos ya están en el workspace")
            return
        
        total_size = sum(ef.size for ef in external) / (1024 * 1024)  # MB
        
        if not messagebox.askyesno(
            "Confirmar Sincronización",
            f"Se copiarán {len(external)} archivo(s) ({total_size:.1f} MB) al workspace.\n\n"
            f"Destino: {self.workspace.root}\n\n"
            "¿Continuar?"
        ):
            return
        
        # Ejecutar sincronización
        messages = []
        def log(msg):
            messages.append(msg)
        
        new_paths = self.workspace.sync_all_files(self.game, log=log)
        
        # Actualizar rutas en BD si hay cambios
        if new_paths:
            try:
                for field, path in new_paths.items():
                    setattr(self.game, field, path)
                
                with GameDatabase() as db:
                    db.update_game(self.game)
                
                messages.append("\n💾 Rutas actualizadas en base de datos")
            except Exception as e:
                messages.append(f"\n⚠️ Error actualizando BD: {e}")
        
        # Mostrar resultado
        messagebox.showinfo("Sincronización", "\n".join(messages))
        
        # Refrescar pestaña
        self._setup_files_tab()
    
    def _setup_structure_tab(self):
        """Configura la pestaña de estructura de archivos."""
        from pathlib import Path
        from gui.components.file_viewer import FileStructureViewer
        
        tab = self.tab_structure
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        # Obtener workspace
        workspace_dir = None
        if self.game.extracted_dir and os.path.isdir(self.game.extracted_dir):
            workspace_dir = Path(self.game.extracted_dir)
        
        if workspace_dir:
            # Crear visor
            self.file_viewer = FileStructureViewer(
                tab,
                workspace_dir=workspace_dir
            )
            self.file_viewer.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        else:
            # Mensaje si no hay workspace
            ctk.CTkLabel(
                tab,
                text="📁 No se encontró directorio del juego\n\nAnaliza el XEX primero para crear el workspace",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60"),
                justify="center"
            ).grid(row=0, column=0, pady=50)
    
    def _setup_notes_tab(self):
        """Configura la pestaña de notas."""
        tab = self.tab_notes
        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)
        
        # Área de texto para notas
        self.notes_text = ctk.CTkTextbox(
            tab,
            font=ctk.CTkFont(size=12),
            wrap="word"
        )
        self.notes_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Cargar notas existentes
        if self.game.notes:
            self.notes_text.insert("1.0", self.game.notes)
        
        # Botón guardar notas
        save_btn = ctk.CTkButton(
            tab,
            text="💾 Guardar Notas",
            command=self._save_notes
        )
        save_btn.grid(row=1, column=0, pady=10)
    
    def _create_actions(self):
        """Crea los botones de acción."""
        actions = ctk.CTkFrame(self, fg_color="transparent")
        actions.grid(row=2, column=0, pady=15)
        
        # Cambiar status
        ctk.CTkLabel(
            actions,
            text="Cambiar estado:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.status_var = ctk.StringVar(value=self.game.status.value)
        status_menu = ctk.CTkOptionMenu(
            actions,
            values=[s.value for s in GameStatus],
            variable=self.status_var,
            command=self._on_status_change,
            width=120
        )
        status_menu.pack(side="left", padx=5)
        
        # Separador
        ctk.CTkLabel(actions, text="  |  ").pack(side="left", padx=5)
        
        # Botón eliminar
        delete_btn = ctk.CTkButton(
            actions,
            text="🗑️ Eliminar",
            fg_color="transparent",
            border_width=1,
            text_color=("#CC0000", "#FF6B6B"),
            border_color=("#CC0000", "#FF6B6B"),
            hover_color=("#ffeeee", "#3a2020"),
            command=self._delete_game
        )
        delete_btn.pack(side="left", padx=10)
    
    def _on_back_click(self):
        """Maneja clic en volver."""
        if self.on_back:
            self.on_back()
    
    def _open_path(self, path: str):
        """Abre un archivo o carpeta en el explorador."""
        if os.path.isfile(path):
            # Abrir carpeta contenedora y seleccionar archivo
            subprocess.run(['explorer', '/select,', path])
        elif os.path.isdir(path):
            subprocess.run(['explorer', path])
    
    def _save_notes(self):
        """Guarda las notas del juego."""
        from tkinter import messagebox
        
        notes = self.notes_text.get("1.0", "end-1c")
        self.game.notes = notes
        
        try:
            with GameDatabase() as db:
                db.update_game(self.game)
            messagebox.showinfo("Notas", "✅ Notas guardadas")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las notas: {e}")
    
    def _on_status_change(self, new_status: str):
        """Maneja cambio de status."""
        from tkinter import messagebox
        
        try:
            self.game.status = GameStatus(new_status)
            with GameDatabase() as db:
                db.update_game(self.game)
            
            # Actualizar badge
            color = self.STATUS_COLORS.get(self.game.status, ("#666666", "#666666"))
            self.status_badge.configure(text=f" {new_status} ", fg_color=color)
            
            if self.on_update:
                self.on_update(self.game)
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar el estado: {e}")
    
    def _delete_game(self):
        """Elimina el juego de la base de datos."""
        from tkinter import messagebox
        
        if not messagebox.askyesno(
            "Confirmar", 
            f"¿Eliminar '{self.game.game_name}' del historial?\n\n"
            "Esto no eliminará los archivos, solo el registro en la base de datos."
        ):
            return
        
        try:
            with GameDatabase() as db:
                db.delete_game(self.game.id)
            
            messagebox.showinfo("Eliminado", "Juego eliminado del historial")
            
            if self.on_back:
                self.on_back()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar: {e}")
