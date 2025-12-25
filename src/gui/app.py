# gui/app.py
"""
GUI moderna de MrMonkeyShopWare con CustomTkinter.
"""
import customtkinter as ctk
import threading
import os
from typing import Optional

# Intentar importar tkinterdnd2 para drag & drop
try:
    from tkinterdnd2 import TkinterDnD
    HAS_DND = True
except ImportError:
    HAS_DND = False
    print("⚠️ tkinterdnd2 no disponible, drag & drop deshabilitado")

from gui.components.sidebar import Sidebar
from gui.components.dropzone import DropZone
from gui.components.logview import LogView
from gui.components.gamelist import GameList
from gui.components.settings import SettingsView
from gui.components.gamedetail import GameDetailView
from gui.components.input_selector import InputTypeSelector

from core.pipeline import full_pipeline, PipelineResult
from core.database import GameDatabase, Game, GameStatus
from core.dumper import dump_disc
from core.extractor import extract_iso
from core.analyser import analyse_xex


class ModernApp(ctk.CTk if not HAS_DND else TkinterDnD.Tk):
    """
    Aplicación principal de MrMonkeyShopWare.
    """
    
    def __init__(self):
        super().__init__()
        
        # Configuración de ventana
        self.title("🎮 MrMonkeyShopWare")
        self.geometry("1100x750")
        self.minsize(900, 600)
        
        # Tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Cargar y aplicar configuración guardada
        from core.settings import load_settings, apply_tool_settings
        self.settings = load_settings()
        apply_tool_settings()
        
        # Aplicar tema guardado
        theme = self.settings.get("appearance", {}).get("theme", "Dark")
        ctk.set_appearance_mode(theme.lower())
        
        # Estado
        self.current_view = "pipeline"
        self.is_processing = False
        
        # Base de datos
        self.db = GameDatabase()
        
        # Crear UI
        self._create_layout()
        self._create_sidebar()
        self._create_main_area()
        self._create_status_bar()
        
        # Configurar drag & drop si está disponible
        if HAS_DND:
            self._setup_dnd()
    
    def _create_layout(self):
        """Configura el grid principal."""
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
    
    def _create_sidebar(self):
        """Crea la barra lateral."""
        self.sidebar = Sidebar(
            self,
            on_navigate=self._on_navigate,
            width=180,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
    
    def _create_main_area(self):
        """Crea el área principal."""
        # Container principal - fondo que contrasta correctamente
        self.main_container = ctk.CTkFrame(self, fg_color=("#f5f5f5", "gray15"))  # Light gray / Dark blue
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_container.grid_rowconfigure(1, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Header con toggle de tema
        self.header_frame = ctk.CTkFrame(self.main_container, fg_color=("#f5f5f5", "#1a1a2e"))
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.view_title = ctk.CTkLabel(
            self.header_frame,
            text="🚀 Pipeline Completo",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")  # Dark text for light, white for dark
        )
        self.view_title.grid(row=0, column=0, sticky="w")
        
        # Toggle de tema
        self.theme_btn = ctk.CTkButton(
            self.header_frame,
            text="🌙",
            width=40,
            height=40,
            font=ctk.CTkFont(size=18),
            command=self._toggle_theme,
            fg_color=("#e0e0e0", "#3d3d5c"),  # Light gray for light, purple-gray for dark
            hover_color=("#c0c0c0", "#4a4a6a"),
            text_color=("#1a1a2e", "#ffffff"),
            corner_radius=10
        )
        self.theme_btn.grid(row=0, column=1)
        
        # Frame de contenido (cambia según la vista)
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # LogView persistente (siempre visible)
        self.logview = LogView(self.main_container, max_lines=200)
        self.logview.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        self.logview.configure(height=150)
        
        # Ajustar row weights
        self.main_container.grid_rowconfigure(1, weight=1)  # content crece
        self.main_container.grid_rowconfigure(2, weight=0)  # logview fijo
        
        # Mostrar vista inicial
        self._on_navigate("pipeline")
    
    def _create_status_bar(self):
        """Crea la barra de estado inferior."""
        self.status_bar = ctk.CTkFrame(self, height=30, corner_radius=0)
        self.status_bar.grid(row=1, column=1, sticky="ew")
        self.status_bar.grid_columnconfigure(0, weight=1)
        
        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Listo",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        self.status_label.grid(row=0, column=0, padx=10, sticky="w")
        
        self.version_label = ctk.CTkLabel(
            self.status_bar,
            text="v0.1.0",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        )
        self.version_label.grid(row=0, column=1, padx=10)
    
    def _setup_dnd(self):
        """Configura drag & drop."""
        if hasattr(self, 'dropzone'):
            self.dropzone.setup_dnd(self)
    
    def _toggle_theme(self):
        """Alterna entre tema oscuro y claro."""
        current = ctk.get_appearance_mode()
        if current == "Dark":
            ctk.set_appearance_mode("light")
            self.theme_btn.configure(text="☀️")
        else:
            ctk.set_appearance_mode("dark")
            self.theme_btn.configure(text="🌙")
    
    def _on_navigate(self, view_id: str):
        """Maneja navegación del sidebar."""
        self.current_view = view_id
        
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Mostrar vista correspondiente
        view_handlers = {
            "pipeline": self._show_pipeline_view,
            "dump": self._show_dump_view,
            "extract": self._show_extract_view,
            "analyse": self._show_analyse_view,
            "toml": self._show_toml_view,
            "history": self._show_history_view,
            "config": self._show_config_view,
        }
        
        titles = {
            "pipeline": "🚀 Pipeline Completo",
            "dump": "📀 Dump de Disco",
            "extract": "📂 Extraer ISO",
            "analyse": "🔬 Analizar XEX",
            "toml": "📝 Generar TOML",
            "history": "📚 Historial",
            "config": "⚙️ Configuración",
        }
        
        self.view_title.configure(text=titles.get(view_id, ""))
        
        handler = view_handlers.get(view_id, self._show_pipeline_view)
        handler()
    
    def _show_pipeline_view(self):
        """Muestra la vista de pipeline con selector de tipo."""
        # Configurar grid del content_frame
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Estado para saber si estamos en selector o en flujo específico
        self.pipeline_state = "selector"
        
        # Mostrar selector de tipo de entrada
        self.input_selector = InputTypeSelector(
            self.content_frame,
            on_type_select=self._on_input_type_selected
        )
        self.input_selector.grid(row=0, column=0, sticky="nsew")
    
    def _on_input_type_selected(self, type_id: str):
        """Maneja la selección de tipo de entrada."""
        self.pipeline_state = type_id
        
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Configurar grid
        self.content_frame.grid_rowconfigure(0, weight=0)  # header
        self.content_frame.grid_rowconfigure(1, weight=1)  # contenido
        self.content_frame.grid_rowconfigure(2, weight=0)  # progress
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Crear header con botón volver
        self._create_pipeline_header(type_id)
        
        # Mostrar UI específica según tipo
        if type_id == "disc":
            self._show_disc_input()
        elif type_id == "iso":
            self._show_iso_input()
        elif type_id == "folder":
            self._show_folder_input()
        elif type_id == "xex":
            self._show_xex_input()
        elif type_id == "xbox_usb":
            self._show_xbox_usb_input()
        elif type_id == "god":
            self._show_god_input()
        elif type_id == "virtual":
            self._show_virtual_input()
        
        # Crear barra de progreso
        self._create_progress_bar()
    
    def _create_pipeline_header(self, type_id: str):
        """Crea header con título y botón volver."""
        titles = {
            "disc": ("📀", "Disco Físico"),
            "iso": ("💿", "Archivo ISO"),
            "folder": ("📁", "Carpeta / USB"),
            "xex": ("🎮", "XEX Directo"),
            "xbox_usb": ("💾", "USB Xbox 360"),
            "god": ("📦", "GOD / LIVE"),
            "virtual": ("🖥️", "Disco Virtual"),
        }
        icon, title = titles.get(type_id, ("🚀", "Pipeline"))
        
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 10), padx=10)
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
            command=self._back_to_selector
        )
        back_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Título
        title_lbl = ctk.CTkLabel(
            header,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title_lbl.grid(row=0, column=1, sticky="w")
    
    def _create_progress_bar(self):
        """Crea la barra de progreso."""
        self.progress_frame = ctk.CTkFrame(self.content_frame)
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(10, 0), padx=10)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Progreso",
            font=ctk.CTkFont(size=12)
        )
        self.progress_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.progress_bar.set(0)
    
    def _back_to_selector(self):
        """Vuelve al selector de tipo."""
        self._on_navigate("pipeline")
    
    def _show_disc_input(self):
        """Muestra UI para disco físico."""
        from core.folder_scanner import get_optical_drives
        
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Container centrado
        center = ctk.CTkFrame(frame, fg_color="transparent")
        center.grid(row=0, column=0)
        
        # Icono
        ctk.CTkLabel(center, text="📀", font=ctk.CTkFont(size=48)).pack(pady=(0, 10))
        
        # Instrucción
        ctk.CTkLabel(
            center,
            text="Selecciona la unidad óptica con el disco Xbox 360",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 15))
        
        # Selector de unidad
        drives = get_optical_drives()
        self.drive_var = ctk.StringVar(value=drives[0] if drives else "D:")
        
        drive_menu = ctk.CTkOptionMenu(
            center,
            values=drives if drives else ["D:", "E:", "F:"],
            variable=self.drive_var,
            width=150
        )
        drive_menu.pack(pady=10)
        
        # Botón iniciar
        ctk.CTkButton(
            center,
            text="💿 Iniciar Dump",
            font=ctk.CTkFont(size=14),
            height=40,
            command=lambda: self._start_dump_from_selector()
        ).pack(pady=20)
    
    def _show_iso_input(self):
        """Muestra UI para archivo ISO."""
        self.dropzone = DropZone(
            self.content_frame,
            on_file_drop=self._on_file_selected,
            accepted_extensions=(".iso",)
        )
        self.dropzone.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.dropzone.main_label.configure(text="Arrastra tu archivo .iso aquí")
        
        if HAS_DND:
            self.dropzone.setup_dnd(self)
    
    def _show_folder_input(self):
        """Muestra UI para carpeta/USB."""
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Container centrado
        center = ctk.CTkFrame(frame, fg_color="transparent")
        center.grid(row=0, column=0)
        
        # Icono
        ctk.CTkLabel(center, text="📁", font=ctk.CTkFont(size=48)).pack(pady=(0, 10))
        
        # Instrucción
        ctk.CTkLabel(
            center,
            text="Selecciona la carpeta que contiene el juego",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            center,
            text="Se buscará automáticamente el archivo default.xex",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        ).pack(pady=(0, 15))
        
        # Botón seleccionar
        ctk.CTkButton(
            center,
            text="📂 Seleccionar Carpeta",
            font=ctk.CTkFont(size=14),
            height=40,
            command=self._select_game_folder
        ).pack(pady=20)
    
    def _show_xex_input(self):
        """Muestra UI para XEX directo."""
        self.dropzone = DropZone(
            self.content_frame,
            on_file_drop=self._start_analyse,
            accepted_extensions=(".xex",)
        )
        self.dropzone.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.dropzone.main_label.configure(text="Arrastra tu archivo .xex aquí")
        
        if HAS_DND:
            self.dropzone.setup_dnd(self)
    
    def _start_dump_from_selector(self):
        """Inicia dump desde el selector."""
        drive = self.drive_var.get()
        self._log(f"📀 Iniciando dump desde {drive}")
        self._start_dump(drive)
    
    def _select_game_folder(self):
        """Abre selector de carpeta y busca XEX."""
        from tkinter import filedialog
        from core.folder_scanner import find_xex_in_folder
        
        folder = filedialog.askdirectory(title="Seleccionar carpeta del juego")
        
        if folder:
            self._log(f"📁 Buscando XEX en {folder}...")
            xex_path = find_xex_in_folder(folder)
            
            if xex_path:
                self._log(f"✅ Encontrado: {os.path.basename(xex_path)}")
                self._start_analyse(xex_path)
            else:
                self._log("❌ No se encontró ningún archivo XEX en la carpeta")
    
    def _show_xbox_usb_input(self):
        """Muestra UI para USB Xbox 360."""
        from core.folder_scanner import get_drive_letters
        
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Container centrado
        center = ctk.CTkFrame(frame, fg_color="transparent")
        center.grid(row=0, column=0)
        
        # Icono
        ctk.CTkLabel(center, text="💾", font=ctk.CTkFont(size=48)).pack(pady=(0, 10))
        
        # Instrucción
        ctk.CTkLabel(
            center,
            text="Selecciona el disco USB con juegos Xbox 360",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(0, 15))
        
        # Selector de unidad
        drives = get_drive_letters()
        self.xbox_drive_var = ctk.StringVar(value=drives[-1] if drives else "E:")
        
        drive_menu = ctk.CTkOptionMenu(
            center,
            values=drives if drives else ["D:", "E:", "F:"],
            variable=self.xbox_drive_var,
            width=150
        )
        drive_menu.pack(pady=10)
        
        # Botón escanear
        ctk.CTkButton(
            center,
            text="🔍 Escanear Juegos",
            font=ctk.CTkFont(size=14),
            height=40,
            command=self._scan_xbox_usb
        ).pack(pady=20)
    
    def _scan_xbox_usb(self):
        """Escanea USB Xbox 360 y muestra juegos."""
        from core.xbox_drive_scanner import is_xbox_usb, list_games_on_drive
        
        drive = self.xbox_drive_var.get()
        self._log(f"💾 Escaneando {drive} ...")
        
        if not is_xbox_usb(drive):
            self._log("❌ No se detectó estructura Xbox 360 en este disco")
            return
        
        games = list_games_on_drive(drive)
        
        if not games:
            self._log("❌ No se encontraron juegos en el disco")
            return
        
        self._log(f"✅ Encontrados {len(games)} juego(s)")
        
        # Mostrar lista de juegos
        for widget in self.content_frame.winfo_children():
            if hasattr(widget, 'grid_info') and widget.grid_info().get('row') == 1:
                widget.destroy()
        
        # Frame scrollable para lista de juegos
        games_frame = ctk.CTkScrollableFrame(
            self.content_frame, 
            fg_color="transparent",
            height=300
        )
        games_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        games_frame.grid_columnconfigure(0, weight=1)
        
        for i, game in enumerate(games):
            game_btn = ctk.CTkButton(
                games_frame,
                text=f"🎮 {game.display_name or game.title_id}",
                font=ctk.CTkFont(size=13),
                anchor="w",
                fg_color=("gray85", "gray25"),
                hover_color=("gray75", "gray35"),
                text_color=("#1a1a2e", "#ffffff"),
                height=40,
                command=lambda g=game: self._select_xbox_game(g)
            )
            game_btn.grid(row=i, column=0, sticky="ew", pady=2)
    
    def _select_xbox_game(self, game):
        """Selecciona un juego del USB Xbox 360."""
        if game.xex_path:
            self._log(f"🎮 Seleccionado: {game.display_name}")
            self._start_analyse(game.xex_path)
        else:
            self._log(f"❌ No se encontró XEX para {game.display_name}")
    
    def _show_god_input(self):
        """Muestra UI para GOD/LIVE (por implementar)."""
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        center = ctk.CTkFrame(frame, fg_color="transparent")
        center.grid(row=0, column=0)
        
        ctk.CTkLabel(center, text="📦", font=ctk.CTkFont(size=48)).pack(pady=(0, 10))
        ctk.CTkLabel(
            center,
            text="Soporte GOD/LIVE",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack()
        ctk.CTkLabel(
            center,
            text="Requiere god2iso.exe\nConfigúralo en ⚙️ Configuración",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
            justify="center"
        ).pack(pady=10)
        
        ctk.CTkLabel(
            center,
            text="🚧 Próximamente",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("orange", "orange")
        ).pack(pady=20)
    
    def _show_virtual_input(self):
        """Muestra UI para disco virtual - detecta ISOs montadas."""
        from core.virtual_disc import detect_virtual_drives, get_all_drives_with_type
        
        frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        frame.grid(row=1, column=0, sticky="nsew", padx=10)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        # Header
        header = ctk.CTkFrame(frame, fg_color="transparent")
        header.grid(row=0, column=0, pady=(0, 15))
        
        ctk.CTkLabel(header, text="🖥️", font=ctk.CTkFont(size=36)).pack()
        ctk.CTkLabel(
            header,
            text="Detectar Disco Virtual",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack()
        ctk.CTkLabel(
            header,
            text="Unidades que parecen contener juegos Xbox 360",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        ).pack(pady=(5, 0))
        
        # Detectar unidades
        virtual_drives = detect_virtual_drives()
        all_drives = get_all_drives_with_type()
        
        # Frame para lista de unidades
        list_frame = ctk.CTkScrollableFrame(
            frame,
            fg_color="transparent",
            height=250
        )
        list_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        list_frame.grid_columnconfigure(0, weight=1)
        
        if virtual_drives:
            self._log(f"🖥️ Encontradas {len(virtual_drives)} unidad(es) con contenido Xbox")
            
            for i, drive in enumerate(virtual_drives):
                label = f"{drive.letter} - {drive.label or 'Sin etiqueta'} ({drive.drive_type})"
                btn = ctk.CTkButton(
                    list_frame,
                    text=f"🎮 {label}",
                    font=ctk.CTkFont(size=13),
                    anchor="w",
                    fg_color=("gray85", "gray25"),
                    hover_color=("#3B8ED0", "#1F6AA5"),
                    text_color=("#1a1a2e", "#ffffff"),
                    height=45,
                    command=lambda d=drive: self._use_virtual_drive(d)
                )
                btn.grid(row=i, column=0, sticky="ew", pady=3)
        else:
            # Mostrar todas las unidades CD-ROM
            cdrom_drives = [d for d in all_drives if d.drive_type == "CD-ROM"]
            
            if cdrom_drives:
                ctk.CTkLabel(
                    list_frame,
                    text="📀 Unidades CD-ROM detectadas:",
                    font=ctk.CTkFont(size=12, weight="bold")
                ).grid(row=0, column=0, pady=(0, 10), sticky="w")
                
                for i, drive in enumerate(cdrom_drives):
                    label = f"{drive.letter} - {drive.label or 'Vacía'}"
                    btn = ctk.CTkButton(
                        list_frame,
                        text=f"💿 {label}",
                        font=ctk.CTkFont(size=13),
                        anchor="w",
                        fg_color=("gray85", "gray25"),
                        hover_color=("gray75", "gray35"),
                        text_color=("#1a1a2e", "#ffffff"),
                        height=40,
                        command=lambda d=drive: self._use_virtual_drive(d)
                    )
                    btn.grid(row=i+1, column=0, sticky="ew", pady=2)
            else:
                ctk.CTkLabel(
                    list_frame,
                    text="No se detectaron unidades virtuales.\n\nMonta una ISO con tu software preferido\n(Daemon Tools, Windows, etc.)",
                    font=ctk.CTkFont(size=12),
                    text_color=("gray50", "gray60"),
                    justify="center"
                ).grid(row=0, column=0, pady=30)
        
        # Botón refrescar
        ctk.CTkButton(
            frame,
            text="🔄 Refrescar",
            width=120,
            command=lambda: self._on_input_type_selected("virtual")
        ).grid(row=2, column=0, pady=10)
    
    def _use_virtual_drive(self, drive):
        """Usa un juego desde disco virtual."""
        from core.virtual_disc import find_xex_on_drive
        
        self._log(f"🖥️ Buscando juego en {drive.letter}...")
        
        xex_path = find_xex_on_drive(drive.letter)
        
        if xex_path:
            self._log(f"✅ Encontrado: {os.path.basename(xex_path)}")
            self._start_analyse(xex_path)
        else:
            self._log(f"❌ No se encontró XEX en {drive.letter}")
            self._log("💡 Tip: Asegúrate de que la ISO esté montada correctamente")
    
    def _show_history_view(self):
        """Muestra la vista de historial."""
        self.gamelist = GameList(
            self.content_frame,
            on_game_select=self._on_game_select
        )
        self.gamelist.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def _show_dump_view(self):
        """Muestra la vista de dump."""
        self._show_simple_action_view(
            "Inserta un disco Xbox 360 y haz clic en Iniciar Dump",
            "💿 Iniciar Dump",
            self._start_dump
        )
    
    def _show_extract_view(self):
        """Muestra la vista de extracción."""
        self.dropzone = DropZone(
            self.content_frame,
            on_file_drop=self._start_extract,
            accepted_extensions=(".iso",)
        )
        self.dropzone.grid(row=0, column=0, sticky="nsew", pady=20, padx=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def _show_analyse_view(self):
        """Muestra la vista de análisis."""
        self.dropzone = DropZone(
            self.content_frame,
            on_file_drop=self._start_analyse,
            accepted_extensions=(".xex",)
        )
        self.dropzone.grid(row=0, column=0, sticky="nsew", pady=20, padx=10)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def _show_toml_view(self):
        """Muestra la vista de generación TOML."""
        info = ctk.CTkLabel(
            self.content_frame,
            text="La generación de TOML está integrada en el Pipeline.\n\nUsa la vista Pipeline o Analyse para generar automáticamente.",
            font=ctk.CTkFont(size=14),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        info.grid(row=0, column=0, pady=50, sticky="n")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def _show_config_view(self):
        """Muestra la vista de configuración con pestañas."""
        self.settings_view = SettingsView(
            self.content_frame,
            on_save=lambda: self.set_status("✅ Configuración guardada")
        )
        self.settings_view.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def _show_simple_action_view(self, description: str, button_text: str, action):
        """Muestra una vista simple con descripción y botón."""
        # Configurar grid
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Container centrado
        center_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        center_frame.grid(row=0, column=0)
        
        desc_label = ctk.CTkLabel(
            center_frame,
            text=description,
            font=ctk.CTkFont(size=14),
            text_color=("#1a1a2e", "#e0e0e0")
        )
        desc_label.grid(row=0, column=0, pady=30)
        
        action_btn = ctk.CTkButton(
            center_frame,
            text=button_text,
            font=ctk.CTkFont(size=16),
            height=50,
            width=200,
            command=action
        )
        action_btn.grid(row=1, column=0, pady=20)
    
    def _on_file_selected(self, file_path: str):
        """Maneja archivo seleccionado para pipeline."""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.dropzone.show_processing(os.path.basename(file_path))
        self.set_status(f"Procesando: {os.path.basename(file_path)}")
        
        def job():
            try:
                if file_path.lower().endswith(".iso"):
                    result = full_pipeline(iso_path=file_path, log=self._log)
                elif file_path.lower().endswith(".xex"):
                    result = full_pipeline(xex_path=file_path, log=self._log)
                else:
                    self._log("❌ Tipo de archivo no soportado")
                    return
                
                self._on_pipeline_complete(result)
            except Exception as e:
                self._log(f"❌ Error: {e}")
            finally:
                self.is_processing = False
                self.after(0, self.dropzone.reset)
                self.after(0, lambda: self.set_status("Listo"))
        
        threading.Thread(target=job, daemon=True).start()
    
    def _on_pipeline_complete(self, result: PipelineResult):
        """Maneja finalización del pipeline."""
        if result.success:
            self._log("🎉 Pipeline completado exitosamente")
            self.after(0, lambda: self.progress_bar.set(1.0))
            
            # Guardar en base de datos
            try:
                game_name = os.path.basename(result.main_xex or "Unknown")
                game = Game(
                    game_name=game_name.replace(".xex", ""),
                    status=GameStatus.COMPLETED,
                    iso_path=result.iso_path,
                    extracted_dir=result.extracted_dir,
                    xex_path=result.main_xex,
                    analysis_json=result.analysis_json,
                    project_toml=result.project_toml
                )
                self.db.add_game(game)
                self._log("💾 Juego guardado en historial")
            except Exception as e:
                self._log(f"⚠️ No se pudo guardar en historial: {e}")
        else:
            self._log(f"❌ Pipeline fallido: {result.error}")
    
    def _start_dump(self):
        """Inicia dump de disco."""
        from tkinter.simpledialog import askstring
        drive = askstring("Unidad", "Ingresa la letra de la unidad (ej: E:)")
        if not drive:
            return
        
        self.set_status(f"Dumpeando desde {drive}...")
        self._log(f"💿 Iniciando dump desde {drive}")
        
        def job():
            try:
                result = dump_disc(drive, out_path=None)
                if result:
                    self._log(f"✅ Dump completado")
                else:
                    self._log("❌ Error en dump")
            except FileNotFoundError as e:
                self._log(f"❌ Error: {e}")
            except Exception as e:
                self._log(f"❌ Error inesperado: {e}")
            finally:
                self.after(0, lambda: self.set_status("Listo"))
        
        threading.Thread(target=job, daemon=True).start()
    
    def _start_extract(self, file_path: str):
        """Inicia extracción de ISO."""
        self.set_status(f"Extrayendo {os.path.basename(file_path)}...")
        self._log(f"📦 Iniciando extracción de {os.path.basename(file_path)}")
        
        def job():
            try:
                result = extract_iso(file_path, log=self._log)
                if result:
                    self._log(f"✅ Extracción completada: {result}")
                else:
                    self._log("❌ Error en extracción")
            except FileNotFoundError as e:
                self._log(f"❌ Error: {e}")
            except Exception as e:
                self._log(f"❌ Error inesperado: {e}")
            finally:
                self.after(0, lambda: self.set_status("Listo"))
        
        threading.Thread(target=job, daemon=True).start()
    
    def _start_analyse(self, file_path: str):
        """Inicia análisis de XEX con workspace organizado."""
        self.set_status(f"Analizando {os.path.basename(file_path)}...")
        self._log(f"🔬 Iniciando análisis de {os.path.basename(file_path)}")
        
        def job():
            try:
                import json
                from core.game_workspace import GameWorkspace, GameInfo, get_or_create_workspace
                
                result = analyse_xex(file_path, log=self._log)
                
                if result and result.success:
                    # Mostrar resumen del juego detectado
                    self._log(f"\n{'═'*50}")
                    self._log("📋 RESUMEN DEL ANÁLISIS")
                    self._log(f"{'═'*50}")
                    
                    if result.xex_info and result.xex_info.title_id:
                        xex_info = result.xex_info
                        self._log(f"🎮 Juego: {xex_info.display_name}")
                        self._log(f"   Title ID: {xex_info.title_id}")
                        if xex_info.version:
                            self._log(f"   Versión: {xex_info.version}")
                        if xex_info.regions:
                            self._log(f"   Regiones: {xex_info.regions}")
                        if xex_info.esrb_rating:
                            self._log(f"   Rating: {xex_info.esrb_rating}")
                        
                        # Verificar si existe en BD
                        with GameDatabase() as db:
                            existing = db.get_by_title_id(xex_info.title_id)
                            
                            if existing:
                                self._log(f"\n⚠️ Juego ya existe en BD (ID: {existing.id})")
                                self._log(f"   Actualizando información...")
                        
                        # Crear/obtener workspace organizado
                        game_name = xex_info.display_name or os.path.basename(file_path).replace(".xex", "")
                        workspace, is_new = get_or_create_workspace(xex_info.title_id, game_name)
                        
                        if is_new:
                            self._log(f"\n📁 Creado directorio del juego:")
                        else:
                            self._log(f"\n📁 Usando directorio existente:")
                        self._log(f"   {workspace.root}")
                        
                        # Guardar info.json en el workspace
                        game_info = GameInfo.from_xex_info(
                            xex_info, 
                            source_type="xex", 
                            source_path=file_path
                        )
                        workspace.save_info(game_info)
                        self._log(f"   ✅ info.json guardado")
                        
                        # Mover/copiar archivos de análisis al workspace
                        import shutil
                        if result.json_file and os.path.exists(result.json_file):
                            dest = workspace.analysis_dir / os.path.basename(result.json_file)
                            shutil.copy2(result.json_file, dest)
                            result.json_file = str(dest)
                        
                        if result.toml_file and os.path.exists(result.toml_file):
                            dest = workspace.analysis_dir / os.path.basename(result.toml_file)
                            shutil.copy2(result.toml_file, dest)
                            result.toml_file = str(dest)
                        
                        # Guardar en base de datos
                        try:
                            game = Game(
                                title_id=xex_info.title_id,
                                game_name=game_name,
                                status=GameStatus.ANALYSED,
                                xex_path=file_path,
                                extracted_dir=str(workspace.root),  # Directorio del workspace
                                analysis_json=result.json_file,
                                project_toml=result.toml_file,
                                media_id=xex_info.media_id,
                                version=xex_info.version,
                                disc_number=xex_info.disc_number,
                                total_discs=xex_info.total_discs,
                                regions=xex_info.regions,
                                esrb_rating=xex_info.esrb_rating,
                                entry_point=xex_info.entry_point,
                                original_pe_name=xex_info.original_pe_name,
                                xex_info_json=json.dumps({
                                    "static_libraries": xex_info.static_libraries[:10],
                                    "is_retail": xex_info.is_retail,
                                    "workspace": str(workspace.root)
                                })
                            )
                            
                            with GameDatabase() as db:
                                game_id = db.add_or_update_game(game)
                            
                            self._log(f"\n💾 Juego guardado en base de datos (ID: {game_id})")
                            self._log(f"📚 Ve a 'Historial' para ver el juego")
                        except Exception as e:
                            self._log(f"⚠️ No se pudo guardar en BD: {e}")
                    else:
                        self._log("⚠️ No se pudo detectar información del juego")
                    
                    self._log(f"\n📄 Archivos generados:")
                    self._log(f"   TOML: {result.toml_file}")
                    self._log(f"   JSON: {result.json_file}")
                    self._log(f"{'═'*50}")
                    self._log("🎉 ¡Análisis completado exitosamente!")
                else:
                    self._log("❌ Error en análisis")
            except FileNotFoundError as e:
                self._log(f"❌ Error: {e}")
            except Exception as e:
                self._log(f"❌ Error inesperado: {e}")
            finally:
                self.after(0, lambda: self.set_status("Listo"))
        
        threading.Thread(target=job, daemon=True).start()
    
    def _on_game_select(self, game: Game):
        """Maneja selección de juego en historial - muestra vista de detalle."""
        self._log(f"Abriendo detalle de: {game.game_name}")
        self._show_game_detail(game)
    
    def _show_game_detail(self, game: Game):
        """Muestra la vista de detalle de un juego."""
        # Limpiar contenido actual
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Actualizar título
        self.view_title.configure(text=f"🎮 {game.game_name}")
        
        # Mostrar vista de detalle
        self.game_detail = GameDetailView(
            self.content_frame,
            game=game,
            on_back=self._back_to_history,
            on_update=lambda g: self._log(f"Juego actualizado: {g.game_name}")
        )
        self.game_detail.grid(row=0, column=0, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def _back_to_history(self):
        """Vuelve a la vista de historial desde el detalle."""
        self._on_navigate("history")
    
    def _log(self, message: str):
        """Log thread-safe."""
        if hasattr(self, 'logview'):
            self.after(0, lambda: self.logview.info(message))
    
    def set_status(self, text: str):
        """Actualiza la barra de estado."""
        self.status_label.configure(text=text)
    
    def on_closing(self):
        """Limpieza al cerrar."""
        self.db.close()
        self.destroy()


def main():
    """Punto de entrada de la GUI moderna."""
    app = ModernApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()


if __name__ == "__main__":
    main()
