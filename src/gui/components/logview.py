# gui/components/logview.py
"""
Vista de logs con scroll y timestamps.
"""
import customtkinter as ctk
from datetime import datetime
from typing import Optional


class LogView(ctk.CTkFrame):
    """
    Área de logs con scroll automático y timestamps.
    """
    
    def __init__(self, parent, max_lines: int = 500, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.max_lines = max_lines
        self.line_count = 0
        
        # Configurar grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header = ctk.CTkLabel(
            self,
            text="📋 Log",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.header.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Botón limpiar
        self.clear_btn = ctk.CTkButton(
            self,
            text="🗑️",
            width=30,
            height=25,
            command=self.clear,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        self.clear_btn.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="e")
        
        # Área de texto
        self.textbox = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family="Consolas", size=12),
            state="disabled",
            wrap="word"
        )
        self.textbox.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        
        # Configurar tags de colores
        self._setup_tags()
    
    def _setup_tags(self):
        """Configura tags para diferentes tipos de mensajes."""
        # Los tags se aplican al texto interno
        pass
    
    def log(self, message: str, level: str = "info"):
        """
        Añade un mensaje al log.
        
        :param message: Mensaje a mostrar
        :param level: Nivel (info, success, warning, error)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Iconos por nivel
        icons = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
            "debug": "🔍"
        }
        icon = icons.get(level, "")
        
        formatted = f"[{timestamp}] {icon} {message}\n"
        
        self.textbox.configure(state="normal")
        self.textbox.insert("end", formatted)
        self.textbox.see("end")
        self.textbox.configure(state="disabled")
        
        self.line_count += 1
        
        # Limpiar si hay demasiadas líneas
        if self.line_count > self.max_lines:
            self._trim_lines()
    
    def _trim_lines(self):
        """Elimina las líneas más antiguas."""
        self.textbox.configure(state="normal")
        # Eliminar primeras 100 líneas
        self.textbox.delete("1.0", "100.0")
        self.textbox.configure(state="disabled")
        self.line_count -= 100
    
    def clear(self):
        """Limpia todo el log."""
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.configure(state="disabled")
        self.line_count = 0
    
    def info(self, message: str):
        """Log de información."""
        self.log(message, "info")
    
    def success(self, message: str):
        """Log de éxito."""
        self.log(message, "success")
    
    def warning(self, message: str):
        """Log de advertencia."""
        self.log(message, "warning")
    
    def error(self, message: str):
        """Log de error."""
        self.log(message, "error")
    
    def debug(self, message: str):
        """Log de debug."""
        self.log(message, "debug")
