# gui/components/input_selector.py
"""
Selector de tipo de entrada para el Pipeline.
Permite elegir entre disco físico, ISO, carpeta o XEX directo.
"""
import customtkinter as ctk
from typing import Callable, Optional


class InputTypeButton(ctk.CTkFrame):
    """Botón individual para tipo de entrada."""
    
    def __init__(
        self, 
        parent, 
        type_id: str,
        icon: str,
        title: str,
        description: str,
        on_click: Callable[[str], None],
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.type_id = type_id
        self.on_click = on_click
        
        # Configurar aspecto
        self.configure(
            fg_color=("gray90", "gray20"),
            corner_radius=15,
            cursor="hand2"
        )
        
        # Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame interno
        inner = ctk.CTkFrame(self, fg_color="transparent")
        inner.grid(row=0, column=0, padx=15, pady=15)
        
        # Icono grande
        self.icon_label = ctk.CTkLabel(
            inner,
            text=icon,
            font=ctk.CTkFont(size=36)
        )
        self.icon_label.grid(row=0, column=0, pady=(0, 5))
        
        # Título
        self.title_label = ctk.CTkLabel(
            inner,
            text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        self.title_label.grid(row=1, column=0)
        
        # Descripción
        self.desc_label = ctk.CTkLabel(
            inner,
            text=description,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60")
        )
        self.desc_label.grid(row=2, column=0, pady=(2, 0))
        
        # Bindings para click
        self.bind("<Button-1>", self._on_click)
        inner.bind("<Button-1>", self._on_click)
        self.icon_label.bind("<Button-1>", self._on_click)
        self.title_label.bind("<Button-1>", self._on_click)
        self.desc_label.bind("<Button-1>", self._on_click)
        
        # Hover effects
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
    
    def _on_click(self, event=None):
        if self.on_click:
            self.on_click(self.type_id)
    
    def _on_enter(self, event=None):
        self.configure(fg_color=("#3B8ED0", "#1F6AA5"))
        self.title_label.configure(text_color="white")
        self.desc_label.configure(text_color=("gray90", "gray80"))
    
    def _on_leave(self, event=None):
        self.configure(fg_color=("gray90", "gray20"))
        self.title_label.configure(text_color=("#1a1a2e", "#ffffff"))
        self.desc_label.configure(text_color=("gray50", "gray60"))


class InputTypeSelector(ctk.CTkFrame):
    """
    Selector de tipo de entrada para el Pipeline.
    
    Muestra botones para elegir:
    - Disco físico
    - Archivo ISO
    - Carpeta/USB
    - XEX directo
    - USB Xbox 360 (nuevo)
    - GOD/LIVE (nuevo)
    - Disco Virtual (nuevo)
    """
    
    INPUT_TYPES = [
        # Fila 1 - Tipos básicos
        ("disc", "📀", "Disco Físico", "Dump desde unidad óptica"),
        ("iso", "💿", "Archivo ISO", "Imagen de disco .iso"),
        ("folder", "📁", "Carpeta / USB", "Juego extraído"),
        ("xex", "🎮", "XEX Directo", "Ejecutable del juego"),
        # Fila 2 - Tipos avanzados
        ("xbox_usb", "💾", "USB Xbox 360", "Disco con juegos Xbox"),
        ("god", "📦", "GOD / LIVE", "Games On Demand"),
        ("virtual", "🖥️", "Disco Virtual", "ISO montada"),
    ]
    
    def __init__(
        self, 
        parent, 
        on_type_select: Callable[[str], None],
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.on_type_select = on_type_select
        self.configure(fg_color="transparent")
        
        # Grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self._create_header()
        self._create_buttons()
    
    def _create_header(self):
        """Crea el encabezado con instrucciones."""
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, pady=(0, 20))
        
        title = ctk.CTkLabel(
            header,
            text="¿Qué tipo de entrada tienes?",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")
        )
        title.pack()
        
        subtitle = ctk.CTkLabel(
            header,
            text="Selecciona el formato de tu respaldo para adaptar el proceso",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60")
        )
        subtitle.pack(pady=(5, 0))
    
    def _create_buttons(self):
        """Crea los botones de selección de tipo."""
        # Container para los botones
        buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        buttons_frame.grid(row=1, column=0)
        
        # Crear botones en grid 2x2
        for i, (type_id, icon, title, desc) in enumerate(self.INPUT_TYPES):
            row = i // 2
            col = i % 2
            
            btn = InputTypeButton(
                buttons_frame,
                type_id=type_id,
                icon=icon,
                title=title,
                description=desc,
                on_click=self._on_button_click,
                width=180,
                height=120
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
    
    def _on_button_click(self, type_id: str):
        """Maneja click en un botón de tipo."""
        if self.on_type_select:
            self.on_type_select(type_id)
