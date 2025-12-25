# gui/components/settings.py
"""
Componente de configuración con pestañas.
"""
import customtkinter as ctk
import os
from typing import Callable, Optional
from pathlib import Path

# Importar sistema de persistencia
from core.settings import load_settings, save_settings, apply_tool_settings


class SettingsView(ctk.CTkFrame):
    """
    Vista de configuración con pestañas organizadas por responsabilidad.
    
    Pestañas:
    - 🔧 Herramientas: Rutas a herramientas externas
    - 🎨 Apariencia: Tema, colores
    - 💾 Base de Datos: Configuración de almacenamiento
    - 📜 Logs: Configuración de logging
    """
    
    def __init__(self, parent, on_save: Callable = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_save = on_save
        self.configure(fg_color="transparent")
        
        # Grid config
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Cargar configuración existente
        self.current_settings = load_settings()
        
        # Crear pestañas
        self._create_tabview()
        
        # Botón guardar
        self._create_save_button()
        
        # Cargar valores guardados en los widgets
        self._load_saved_values()
    
    def _create_tabview(self):
        """Crea el contenedor de pestañas."""
        self.tabview = ctk.CTkTabview(
            self,
            fg_color=("white", "#2a2a3e"),
            segmented_button_fg_color=("#e0e0e0", "#3a3a4e"),
            segmented_button_selected_color=("#3B8ED0", "#1F6AA5"),
            segmented_button_unselected_color=("#d0d0d0", "#4a4a5e"),
            text_color=("#1a1a2e", "#ffffff")
        )
        self.tabview.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        
        # Añadir pestañas
        self.tab_tools = self.tabview.add("🔧 Herramientas")
        self.tab_appearance = self.tabview.add("🎨 Apariencia")
        self.tab_database = self.tabview.add("💾 Base de Datos")
        self.tab_logs = self.tabview.add("📜 Logs")
        
        # Configurar cada pestaña para que sea scrollable
        for tab in [self.tab_tools, self.tab_appearance, self.tab_database, self.tab_logs]:
            tab.grid_rowconfigure(0, weight=1)
            tab.grid_columnconfigure(0, weight=1)
        
        # Configurar cada pestaña
        self._setup_tools_tab()
        self._setup_appearance_tab()
        self._setup_database_tab()
        self._setup_logs_tab()
    
    def _setup_tools_tab(self):
        """Configura la pestaña de herramientas con scroll."""
        tab = self.tab_tools
        
        # Usar scrollable frame dentro de la pestaña
        scroll_frame = ctk.CTkScrollableFrame(
            tab,
            fg_color="transparent",
            scrollbar_button_color=("gray70", "gray30")
        )
        scroll_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        scroll_frame.grid_columnconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            scroll_frame,
            text="Rutas de Herramientas Externas",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title.grid(row=0, column=0, columnspan=3, pady=(10, 20), sticky="w")
        
        # Herramientas
        tools = [
            ("XenonAnalyse", "XENON_ANALYSE_PATH"),
            ("XenonRecomp", "XENON_RECOMP_PATH"),
            ("XexTool", "XEXTOOL_PATH"),
            ("Extract-XISO", "EXTRACT_XISO_PATH"),
            ("DiscImageCreator", "DISC_IMAGE_CREATOR_PATH"),
            ("PPC Context", "PPC_CONTEXT_PATH"),
            ("God2ISO", "GOD2ISO_PATH"),  # Para convertir GOD/LIVE
        ]
        
        self.tool_entries = {}
        
        for i, (name, env_var) in enumerate(tools):
            row = i + 1
            
            # Label
            lbl = ctk.CTkLabel(
                scroll_frame,
                text=f"{name}:",
                font=ctk.CTkFont(size=13),
                text_color=("#1a1a2e", "#e0e0e0")
            )
            lbl.grid(row=row, column=0, padx=(10, 5), pady=8, sticky="e")
            
            # Entry
            entry = ctk.CTkEntry(
                scroll_frame,
                placeholder_text=f"Ruta a {name}"
            )
            entry.grid(row=row, column=1, padx=5, pady=8, sticky="ew")
            
            # Cargar valor actual
            current_value = os.environ.get(env_var, "")
            if current_value:
                entry.insert(0, current_value)
            
            self.tool_entries[env_var] = entry
            
            # Botón buscar
            btn = ctk.CTkButton(
                scroll_frame,
                text="📁",
                width=35,
                command=lambda e=entry: self._browse_file(e)
            )
            btn.grid(row=row, column=2, padx=(5, 10), pady=8)
    
    def _setup_appearance_tab(self):
        """Configura la pestaña de apariencia."""
        tab = self.tab_appearance
        tab.grid_columnconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            tab,
            text="Configuración de Apariencia",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")
        
        # Tema
        lbl_theme = ctk.CTkLabel(
            tab,
            text="Tema:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_theme.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.theme_var = ctk.StringVar(value=ctk.get_appearance_mode())
        self.theme_menu = ctk.CTkOptionMenu(
            tab,
            values=["Dark", "Light", "System"],
            variable=self.theme_var,
            command=self._on_theme_change,
            width=200
        )
        self.theme_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Tamaño de ventana
        lbl_size = ctk.CTkLabel(
            tab,
            text="Tamaño de Ventana:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_size.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        self.size_var = ctk.StringVar(value="1100x750")
        self.size_menu = ctk.CTkOptionMenu(
            tab,
            values=["900x600", "1100x750", "1280x800", "1400x900"],
            variable=self.size_var,
            width=200
        )
        self.size_menu.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Escala UI
        lbl_scale = ctk.CTkLabel(
            tab,
            text="Escala UI:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_scale.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        self.scale_slider = ctk.CTkSlider(
            tab,
            from_=0.8,
            to=1.5,
            number_of_steps=7,
            width=200
        )
        self.scale_slider.set(1.0)
        self.scale_slider.grid(row=3, column=1, padx=10, pady=10, sticky="w")
    
    def _setup_database_tab(self):
        """Configura la pestaña de base de datos."""
        tab = self.tab_database
        tab.grid_columnconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            tab,
            text="Configuración de Base de Datos",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")
        
        # Ruta de BD
        lbl_db = ctk.CTkLabel(
            tab,
            text="Ruta de Base de Datos:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_db.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        default_db = Path.home() / ".mrmonkeyshopware" / "games.db"
        self.db_entry = ctk.CTkEntry(tab, width=400)
        self.db_entry.insert(0, str(default_db))
        self.db_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Estadísticas
        lbl_stats = ctk.CTkLabel(
            tab,
            text="Estadísticas:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_stats.grid(row=2, column=0, padx=10, pady=10, sticky="ne")
        
        self.stats_label = ctk.CTkLabel(
            tab,
            text="Cargando...",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#aaaaaa"),
            justify="left"
        )
        self.stats_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Actualizar estadísticas
        self._update_db_stats()
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        btn_backup = ctk.CTkButton(
            btn_frame,
            text="📦 Backup",
            width=120,
            command=self._backup_database
        )
        btn_backup.pack(side="left", padx=5)
        
        btn_clear = ctk.CTkButton(
            btn_frame,
            text="🗑️ Limpiar",
            width=120,
            fg_color="transparent",
            border_width=1,
            text_color=("#1a1a2e", "#e0e0e0"),
            command=self._clear_database
        )
        btn_clear.pack(side="left", padx=5)
    
    def _setup_logs_tab(self):
        """Configura la pestaña de logs."""
        tab = self.tab_logs
        tab.grid_columnconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            tab,
            text="Configuración de Logging",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="w")
        
        # Nivel de log
        lbl_level = ctk.CTkLabel(
            tab,
            text="Nivel de Log:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_level.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        
        self.log_level_var = ctk.StringVar(value="INFO")
        self.log_level_menu = ctk.CTkOptionMenu(
            tab,
            values=["DEBUG", "INFO", "WARNING", "ERROR"],
            variable=self.log_level_var,
            width=200
        )
        self.log_level_menu.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        
        # Directorio de logs
        lbl_logdir = ctk.CTkLabel(
            tab,
            text="Directorio de Logs:",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_logdir.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        
        default_logdir = Path.home() / ".mrmonkeyshopware" / "logs"
        self.logdir_entry = ctk.CTkEntry(tab, width=400)
        self.logdir_entry.insert(0, str(default_logdir))
        self.logdir_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")
        
        # Tamaño máximo
        lbl_maxsize = ctk.CTkLabel(
            tab,
            text="Tamaño Máximo (MB):",
            font=ctk.CTkFont(size=13),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        lbl_maxsize.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        
        self.maxsize_entry = ctk.CTkEntry(tab, width=100)
        self.maxsize_entry.insert(0, "5")
        self.maxsize_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")
        
        # Botón abrir logs
        btn_open = ctk.CTkButton(
            tab,
            text="📂 Abrir Carpeta de Logs",
            command=self._open_logs_folder
        )
        btn_open.grid(row=4, column=0, columnspan=2, pady=20)
    
    def _create_save_button(self):
        """Crea el botón de guardar."""
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, pady=10)
        
        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="💾 Guardar Configuración",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40,
            width=200,
            command=self._save_settings
        )
        self.save_btn.pack()
    
    def _browse_file(self, entry: ctk.CTkEntry):
        """Abre diálogo para seleccionar archivo."""
        from tkinter import filedialog
        
        filepath = filedialog.askopenfilename(
            title="Seleccionar ejecutable",
            filetypes=[("Ejecutables", "*.exe"), ("Todos", "*.*")]
        )
        
        if filepath:
            entry.delete(0, "end")
            entry.insert(0, filepath)
    
    def _on_theme_change(self, value: str):
        """Cambia el tema de la aplicación."""
        ctk.set_appearance_mode(value.lower())
    
    def _update_db_stats(self):
        """Actualiza estadísticas de la base de datos."""
        try:
            from core.database import GameDatabase
            db = GameDatabase()
            games = db.list_games()
            
            stats = f"📊 Total de juegos: {len(games)}\n"
            
            from core.database import GameStatus
            status_counts = {}
            for g in games:
                s = g.status.value
                status_counts[s] = status_counts.get(s, 0) + 1
            
            for status, count in status_counts.items():
                stats += f"   • {status}: {count}\n"
            
            db.close()
            self.stats_label.configure(text=stats)
        except Exception as e:
            self.stats_label.configure(text=f"Error: {e}")
    
    def _backup_database(self):
        """Crea backup de la base de datos."""
        from tkinter import filedialog, messagebox
        import shutil
        
        src = Path.home() / ".mrmonkeyshopware" / "games.db"
        if not src.exists():
            messagebox.showwarning("Backup", "No existe base de datos para respaldar")
            return
        
        dst = filedialog.asksaveasfilename(
            title="Guardar Backup",
            defaultextension=".db",
            filetypes=[("SQLite DB", "*.db")]
        )
        
        if dst:
            shutil.copy(src, dst)
            messagebox.showinfo("Backup", f"Backup guardado en:\n{dst}")
    
    def _clear_database(self):
        """Limpia la base de datos."""
        from tkinter import messagebox
        
        if messagebox.askyesno("Limpiar BD", "¿Estás seguro de eliminar todos los registros?"):
            try:
                from core.database import GameDatabase
                db = GameDatabase()
                for game in db.list_games():
                    db.delete_game(game.id)
                db.close()
                self._update_db_stats()
                messagebox.showinfo("Limpiar", "Base de datos limpiada")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def _open_logs_folder(self):
        """Abre la carpeta de logs."""
        import subprocess
        
        log_dir = Path.home() / ".mrmonkeyshopware" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        subprocess.Popen(f'explorer "{log_dir}"')
    
    def _save_settings(self):
        """Guarda la configuración."""
        from tkinter import messagebox
        
        # Recopilar valores de los widgets
        settings = {
            "tools": {},
            "appearance": {},
            "database": {},
            "logging": {}
        }
        
        # Herramientas
        for key, entry in self.tool_entries.items():
            settings["tools"][key] = entry.get()
        
        # Apariencia
        settings["appearance"]["theme"] = self.theme_var.get()
        settings["appearance"]["window_size"] = self.size_var.get()
        settings["appearance"]["ui_scale"] = self.scale_slider.get()
        
        # Base de datos
        settings["database"]["path"] = self.db_entry.get()
        
        # Logging
        settings["logging"]["level"] = self.log_level_var.get()
        settings["logging"]["log_dir"] = self.logdir_entry.get()
        try:
            settings["logging"]["max_size_mb"] = int(self.maxsize_entry.get())
        except ValueError:
            settings["logging"]["max_size_mb"] = 5
        
        # Guardar
        if save_settings(settings):
            # Aplicar rutas de herramientas a variables de entorno
            apply_tool_settings()
            
            # Recargar config.py para que use los nuevos valores
            from core.config import reload_config
            reload_config()
            
            messagebox.showinfo(
                "Configuración",
                "✅ Configuración guardada correctamente"
            )
            
            if self.on_save:
                self.on_save()
        else:
            messagebox.showerror(
                "Error",
                "❌ No se pudo guardar la configuración"
            )
    
    def _load_saved_values(self):
        """Carga los valores guardados en los widgets."""
        settings = self.current_settings
        
        # Herramientas
        tools = settings.get("tools", {})
        for key, entry in self.tool_entries.items():
            value = tools.get(key, "")
            if value:
                entry.delete(0, "end")
                entry.insert(0, value)
        
        # Apariencia
        appearance = settings.get("appearance", {})
        if "theme" in appearance:
            self.theme_var.set(appearance["theme"])
        if "window_size" in appearance:
            self.size_var.set(appearance["window_size"])
        if "ui_scale" in appearance:
            self.scale_slider.set(appearance["ui_scale"])
        
        # Base de datos
        database = settings.get("database", {})
        if "path" in database:
            self.db_entry.delete(0, "end")
            self.db_entry.insert(0, database["path"])
        
        # Logging
        logging = settings.get("logging", {})
        if "level" in logging:
            self.log_level_var.set(logging["level"])
        if "log_dir" in logging:
            self.logdir_entry.delete(0, "end")
            self.logdir_entry.insert(0, logging["log_dir"])
        if "max_size_mb" in logging:
            self.maxsize_entry.delete(0, "end")
            self.maxsize_entry.insert(0, str(logging["max_size_mb"]))
