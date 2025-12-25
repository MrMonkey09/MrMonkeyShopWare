# gui/components/sidebar.py
"""
Barra lateral de navegación.
"""
import customtkinter as ctk
from typing import Callable, Dict


class Sidebar(ctk.CTkFrame):
    """
    Barra lateral con botones de navegación.
    """
    
    def __init__(self, parent, on_navigate: Callable[[str], None] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.on_navigate = on_navigate
        self.buttons: Dict[str, ctk.CTkButton] = {}
        self.active_button: str = None
        
        # Configurar grid - permitir expansión horizontal y vertical
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(10, weight=1)  # Espacio flexible
        
        # Logo / Título
        self.logo_label = ctk.CTkLabel(
            self,
            text="🎮 MrMonkey\nShopWare",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botones de navegación
        self._create_nav_buttons()
        
        # Separador visual (espacio)
        self.separator = ctk.CTkFrame(self, height=2, fg_color="gray40")
        self.separator.grid(row=10, column=0, sticky="ew", padx=20, pady=10)
        
        # Botones inferiores
        self._create_bottom_buttons()
    
    def _create_nav_buttons(self):
        """Crea los botones de navegación principales."""
        buttons_config = [
            ("pipeline", "🚀 Pipeline", 1),
            ("dump", "📀 Dump Disc", 2),
            ("extract", "📂 Extraer ISO", 3),
            ("analyse", "🔬 Analizar XEX", 4),
            ("toml", "📝 Generar TOML", 5),
        ]
        
        for btn_id, text, row in buttons_config:
            btn = ctk.CTkButton(
                self,
                text=text,
                font=ctk.CTkFont(size=14),
                height=40,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda b=btn_id: self._on_button_click(b)
            )
            btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            self.buttons[btn_id] = btn
        
        # Activar pipeline por defecto
        self.set_active("pipeline")
    
    def _create_bottom_buttons(self):
        """Crea los botones de la parte inferior."""
        # Historial
        self.history_btn = ctk.CTkButton(
            self,
            text="📚 Historial",
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self._on_button_click("history")
        )
        self.history_btn.grid(row=11, column=0, padx=10, pady=5, sticky="ew")
        self.buttons["history"] = self.history_btn
        
        # Configuración
        self.config_btn = ctk.CTkButton(
            self,
            text="⚙️ Configuración",
            font=ctk.CTkFont(size=14),
            height=40,
            anchor="w",
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=lambda: self._on_button_click("config")
        )
        self.config_btn.grid(row=12, column=0, padx=10, pady=(5, 20), sticky="ew")
        self.buttons["config"] = self.config_btn
    
    def _on_button_click(self, btn_id: str):
        """Maneja click en botón."""
        self.set_active(btn_id)
        if self.on_navigate:
            self.on_navigate(btn_id)
    
    def set_active(self, btn_id: str):
        """Establece el botón activo."""
        # Desactivar anterior
        if self.active_button and self.active_button in self.buttons:
            self.buttons[self.active_button].configure(
                fg_color="transparent"
            )
        
        # Activar nuevo
        if btn_id in self.buttons:
            self.buttons[btn_id].configure(
                fg_color=("gray75", "gray25")
            )
            self.active_button = btn_id
