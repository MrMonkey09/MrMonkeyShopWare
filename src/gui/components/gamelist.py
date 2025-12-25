# gui/components/gamelist.py
"""
Lista de juegos del historial.
"""
import customtkinter as ctk
from typing import Callable, List, Optional
from core.database import GameDatabase, Game, GameStatus


class GameCard(ctk.CTkFrame):
    """
    Tarjeta individual de un juego.
    """
    
    STATUS_COLORS = {
        GameStatus.PENDING: ("gray70", "gray40"),
        GameStatus.DUMPED: ("#FFB347", "#CC8800"),
        GameStatus.EXTRACTED: ("#87CEEB", "#4682B4"),
        GameStatus.ANALYSED: ("#DDA0DD", "#9932CC"),
        GameStatus.IN_PROGRESS: ("#FFD700", "#DAA520"),
        GameStatus.COMPLETED: ("#90EE90", "#228B22"),
        GameStatus.FAILED: ("#FF6B6B", "#CC0000"),
    }
    
    STATUS_ICONS = {
        GameStatus.PENDING: "⏳",
        GameStatus.DUMPED: "💿",
        GameStatus.EXTRACTED: "📂",
        GameStatus.ANALYSED: "🔬",
        GameStatus.IN_PROGRESS: "🔧",
        GameStatus.COMPLETED: "✅",
        GameStatus.FAILED: "❌",
    }
    
    def __init__(self, parent, game: Game, on_click: Callable[[Game], None] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.game = game
        self.on_click = on_click
        
        # Configurar aspecto
        self.configure(
            corner_radius=10,
            border_width=1,
            border_color=("gray70", "gray30")
        )
        
        # Grid
        self.grid_columnconfigure(1, weight=1)
        
        # Icono de status
        icon = self.STATUS_ICONS.get(game.status, "❓")
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=ctk.CTkFont(size=24),
            width=40
        )
        self.icon_label.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10)
        
        # Nombre del juego
        self.name_label = ctk.CTkLabel(
            self,
            text=game.game_name or "Sin nombre",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        self.name_label.grid(row=0, column=1, padx=5, pady=(10, 0), sticky="w")
        
        # Info secundaria
        info_text = f"ID: {game.title_id or 'N/A'} | {game.status.value}"
        self.info_label = ctk.CTkLabel(
            self,
            text=info_text,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w"
        )
        self.info_label.grid(row=1, column=1, padx=5, pady=(0, 10), sticky="w")
        
        # Badge de status
        color = self.STATUS_COLORS.get(game.status, ("gray50", "gray50"))
        self.status_badge = ctk.CTkLabel(
            self,
            text=game.status.value,
            font=ctk.CTkFont(size=10),
            fg_color=color,
            corner_radius=5,
            padx=8,
            pady=2
        )
        self.status_badge.grid(row=0, column=2, rowspan=2, padx=10, pady=10)
        
        # Hacer clickeable
        self.bind("<Button-1>", self._on_click)
        for child in self.winfo_children():
            child.bind("<Button-1>", self._on_click)
    
    def _on_click(self, event=None):
        if self.on_click:
            self.on_click(self.game)


class GameList(ctk.CTkScrollableFrame):
    """
    Lista scrolleable de juegos.
    """
    
    def __init__(
        self, 
        parent, 
        on_game_select: Callable[[Game], None] = None,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        
        self.on_game_select = on_game_select
        self.game_cards: List[GameCard] = []
        
        # Configurar
        self.grid_columnconfigure(0, weight=1)
        
        # Header
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.header_frame.grid_columnconfigure(1, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame,
            text="📚 Historial de Juegos",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.header_label.grid(row=0, column=0, sticky="w")
        
        # Filtro de status
        self.filter_var = ctk.StringVar(value="all")
        self.filter_menu = ctk.CTkOptionMenu(
            self.header_frame,
            values=["all", "pending", "analysed", "in_progress", "completed", "failed"],
            variable=self.filter_var,
            command=self._on_filter_change,
            width=120
        )
        self.filter_menu.grid(row=0, column=2, padx=5)
        
        # Botón refresh
        self.refresh_btn = ctk.CTkButton(
            self.header_frame,
            text="🔄",
            width=30,
            command=self.refresh,
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        self.refresh_btn.grid(row=0, column=3)
        
        # Placeholder para lista vacía
        self.empty_label = ctk.CTkLabel(
            self,
            text="No hay juegos en el historial",
            text_color=("gray50", "gray60")
        )
        
        # Cargar juegos
        self.refresh()
    
    def _on_filter_change(self, value: str):
        """Maneja cambio de filtro."""
        self.refresh()
    
    def refresh(self):
        """Recarga la lista de juegos."""
        # Limpiar cards existentes
        for card in self.game_cards:
            card.destroy()
        self.game_cards.clear()
        
        # Obtener juegos
        try:
            with GameDatabase() as db:
                filter_value = self.filter_var.get()
                
                if filter_value == "all":
                    games = db.list_games(limit=50)
                else:
                    status = GameStatus(filter_value)
                    games = db.list_games(status=status, limit=50)
        except Exception as e:
            games = []
            print(f"Error cargando juegos: {e}")
        
        # Mostrar vacío o lista
        if not games:
            self.empty_label.grid(row=1, column=0, pady=50)
        else:
            self.empty_label.grid_forget()
            
            for i, game in enumerate(games):
                card = GameCard(
                    self,
                    game=game,
                    on_click=self.on_game_select
                )
                card.grid(row=i+1, column=0, sticky="ew", pady=5, padx=5)
                self.game_cards.append(card)
    
    def add_game(self, game: Game):
        """Añade un juego a la lista (sin recargar todo)."""
        card = GameCard(
            self,
            game=game,
            on_click=self.on_game_select
        )
        # Insertar al principio
        card.grid(row=1, column=0, sticky="ew", pady=5, padx=5)
        self.game_cards.insert(0, card)
        
        # Re-grid las demás
        for i, existing_card in enumerate(self.game_cards[1:], start=2):
            existing_card.grid(row=i, column=0, sticky="ew", pady=5, padx=5)
