# gui/components/dropzone.py
"""
Zona para arrastrar y soltar archivos.
"""
import customtkinter as ctk
from typing import Callable, Optional
import os


class DropZone(ctk.CTkFrame):
    """
    Zona de drop para archivos ISO/XEX.
    Soporta drag & drop y click para seleccionar.
    """
    
    def __init__(
        self, 
        parent, 
        on_file_drop: Callable[[str], None] = None,
        accepted_extensions: tuple = (".iso", ".xex"),
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.on_file_drop = on_file_drop
        self.accepted_extensions = accepted_extensions
        self.is_dragging = False
        
        # Configurar aspecto
        self.configure(
            corner_radius=15,
            border_width=3,
            border_color=("gray70", "gray30"),
            fg_color=("gray95", "gray17")
        )
        
        # Contenido centrado
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Frame interno
        self.inner_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.inner_frame.grid(row=0, column=0)
        
        # Icono
        self.icon_label = ctk.CTkLabel(
            self.inner_frame,
            text="📁",
            font=ctk.CTkFont(size=48)
        )
        self.icon_label.grid(row=0, column=0, pady=(0, 10))
        
        # Texto principal
        self.main_label = ctk.CTkLabel(
            self.inner_frame,
            text="Arrastra un archivo ISO o XEX aquí",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#1a1a2e", "#ffffff")  # Dark for light mode, white for dark mode
        )
        self.main_label.grid(row=1, column=0)
        
        # Texto secundario
        self.sub_label = ctk.CTkLabel(
            self.inner_frame,
            text="o haz clic para seleccionar",
            font=ctk.CTkFont(size=12),
            text_color=("#666666", "#aaaaaa")  # Better contrast
        )
        self.sub_label.grid(row=2, column=0, pady=(5, 0))
        
        # Hacer clickeable
        self.bind("<Button-1>", self._on_click)
        self.inner_frame.bind("<Button-1>", self._on_click)
        self.icon_label.bind("<Button-1>", self._on_click)
        self.main_label.bind("<Button-1>", self._on_click)
        self.sub_label.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event=None):
        """Abre diálogo de selección de archivo."""
        from tkinter import filedialog
        
        filetypes = []
        if ".iso" in self.accepted_extensions:
            filetypes.append(("Xbox360 ISO", "*.iso"))
        if ".xex" in self.accepted_extensions:
            filetypes.append(("Xbox360 XEX", "*.xex"))
        filetypes.append(("Todos los archivos", "*.*"))
        
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=filetypes
        )
        
        if file_path:
            self._handle_file(file_path)
    
    def _handle_file(self, file_path: str):
        """Procesa un archivo seleccionado o arrastrado."""
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext in self.accepted_extensions:
            if self.on_file_drop:
                self.on_file_drop(file_path)
        else:
            # Mostrar error visual
            self.show_error(f"Tipo de archivo no soportado: {ext}")
    
    def setup_dnd(self, root):
        """Configura drag & drop usando tkinterdnd2."""
        try:
            self.drop_target_register("DND_Files")
            self.dnd_bind("<<Drop>>", self._on_dnd_drop)
            self.dnd_bind("<<DragEnter>>", self._on_drag_enter)
            self.dnd_bind("<<DragLeave>>", self._on_drag_leave)
        except Exception as e:
            print(f"Drag & drop no disponible: {e}")
    
    def _on_dnd_drop(self, event):
        """Maneja drop de archivo."""
        file_path = event.data
        # Limpiar path (puede venir con llaves en Windows)
        if file_path.startswith("{") and file_path.endswith("}"):
            file_path = file_path[1:-1]
        
        self._on_drag_leave(None)
        self._handle_file(file_path)
    
    def _on_drag_enter(self, event):
        """Visual feedback al arrastrar sobre la zona."""
        self.is_dragging = True
        self.configure(
            border_color=("#3B8ED0", "#1F6AA5"),
            fg_color=("gray90", "gray20")
        )
        self.icon_label.configure(text="📥")
    
    def _on_drag_leave(self, event):
        """Restaura visual al salir."""
        self.is_dragging = False
        self.configure(
            border_color=("gray70", "gray30"),
            fg_color=("gray95", "gray17")
        )
        self.icon_label.configure(text="📁")
    
    def show_error(self, message: str):
        """Muestra un error temporal."""
        original_text = self.main_label.cget("text")
        self.main_label.configure(text=f"❌ {message}", text_color="red")
        self.after(3000, lambda: self.main_label.configure(
            text=original_text, 
            text_color=("gray10", "gray90")
        ))
    
    def show_processing(self, filename: str):
        """Muestra estado de procesamiento."""
        self.icon_label.configure(text="⏳")
        self.main_label.configure(text=f"Procesando: {filename}")
        self.sub_label.configure(text="Por favor espera...")
    
    def reset(self):
        """Restaura estado inicial."""
        self.icon_label.configure(text="📁")
        self.main_label.configure(text="Arrastra un archivo ISO o XEX aquí")
        self.sub_label.configure(text="o haz clic para seleccionar")
