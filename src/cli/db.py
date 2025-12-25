# cli/db.py
"""
Comando CLI para gestionar la base de datos de juegos.
"""
import argparse
import sys
from core.database import GameDatabase, Game, GameStatus


def format_game(game: Game, verbose: bool = False) -> str:
    """Formatea un juego para mostrar en consola."""
    status_icons = {
        GameStatus.PENDING: "⏳",
        GameStatus.DUMPED: "💿",
        GameStatus.EXTRACTED: "📂",
        GameStatus.ANALYSED: "🔬",
        GameStatus.COMPLETED: "✅",
        GameStatus.FAILED: "❌"
    }
    icon = status_icons.get(game.status, "❓")
    
    if verbose:
        lines = [
            f"{icon} [{game.id}] {game.game_name}",
            f"   Title ID: {game.title_id or 'N/A'}",
            f"   Status:   {game.status.value}",
        ]
        if game.iso_path:
            lines.append(f"   ISO:      {game.iso_path}")
        if game.xex_path:
            lines.append(f"   XEX:      {game.xex_path}")
        if game.project_toml:
            lines.append(f"   TOML:     {game.project_toml}")
        if game.notes:
            lines.append(f"   Notes:    {game.notes}")
        if game.updated_at:
            lines.append(f"   Updated:  {game.updated_at}")
        return "\n".join(lines)
    else:
        return f"{icon} [{game.id:3d}] {game.game_name[:30]:30s} | {game.status.value:10s} | {game.title_id or 'N/A'}"


def cmd_list(args):
    """Lista juegos."""
    with GameDatabase() as db:
        status = GameStatus(args.status) if args.status else None
        games = db.list_games(status=status, limit=args.limit)
        
        if not games:
            print("No hay juegos registrados.")
            return
        
        print(f"\n{'═'*60}")
        print(f"📋 LISTA DE JUEGOS ({len(games)} resultados)")
        print(f"{'═'*60}\n")
        
        for game in games:
            print(format_game(game, verbose=args.verbose))
            if args.verbose:
                print()
        
        # Estadísticas
        if not args.verbose:
            print(f"\n{'─'*60}")
            total = db.count()
            completed = db.count(GameStatus.COMPLETED)
            failed = db.count(GameStatus.FAILED)
            print(f"Total: {total} | ✅ Completados: {completed} | ❌ Fallidos: {failed}")


def cmd_show(args):
    """Muestra detalles de un juego."""
    with GameDatabase() as db:
        game = db.get_game(args.id)
        if not game:
            print(f"❌ No se encontró juego con ID {args.id}")
            sys.exit(1)
        
        print(format_game(game, verbose=True))


def cmd_search(args):
    """Busca juegos."""
    with GameDatabase() as db:
        games = db.search(args.query)
        
        if not games:
            print(f"No se encontraron juegos para '{args.query}'")
            return
        
        print(f"\n🔍 Resultados para '{args.query}': {len(games)}\n")
        for game in games:
            print(format_game(game))


def cmd_add(args):
    """Añade un juego manualmente."""
    game = Game(
        title_id=args.title_id,
        game_name=args.name,
        notes=args.notes
    )
    
    with GameDatabase() as db:
        try:
            game_id = db.add_game(game)
            print(f"✅ Juego añadido con ID: {game_id}")
        except Exception as e:
            print(f"❌ Error al añadir juego: {e}")
            sys.exit(1)


def cmd_delete(args):
    """Elimina un juego."""
    with GameDatabase() as db:
        game = db.get_game(args.id)
        if not game:
            print(f"❌ No se encontró juego con ID {args.id}")
            sys.exit(1)
        
        if not args.force:
            confirm = input(f"¿Eliminar '{game.game_name}'? (s/N): ")
            if confirm.lower() != 's':
                print("Cancelado.")
                return
        
        db.delete_game(args.id)
        print(f"✅ Juego '{game.game_name}' eliminado.")


def cmd_status(args):
    """Actualiza el status de un juego."""
    with GameDatabase() as db:
        game = db.get_game(args.id)
        if not game:
            print(f"❌ No se encontró juego con ID {args.id}")
            sys.exit(1)
        
        try:
            new_status = GameStatus(args.status)
        except ValueError:
            print(f"❌ Status inválido: {args.status}")
            print(f"   Válidos: {', '.join(s.value for s in GameStatus)}")
            sys.exit(1)
        
        db.update_status(args.id, new_status)
        print(f"✅ Status actualizado: {game.game_name} → {new_status.value}")


def main():
    parser = argparse.ArgumentParser(
        description="Gestión de base de datos de juegos",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # list
    p_list = subparsers.add_parser("list", help="Listar juegos")
    p_list.add_argument("-s", "--status", choices=[s.value for s in GameStatus],
                        help="Filtrar por status")
    p_list.add_argument("-l", "--limit", type=int, default=50,
                        help="Límite de resultados (default: 50)")
    p_list.add_argument("-v", "--verbose", action="store_true",
                        help="Mostrar detalles")
    p_list.set_defaults(func=cmd_list)
    
    # show
    p_show = subparsers.add_parser("show", help="Mostrar detalles de un juego")
    p_show.add_argument("id", type=int, help="ID del juego")
    p_show.set_defaults(func=cmd_show)
    
    # search
    p_search = subparsers.add_parser("search", help="Buscar juegos")
    p_search.add_argument("query", help="Término de búsqueda")
    p_search.set_defaults(func=cmd_search)
    
    # add
    p_add = subparsers.add_parser("add", help="Añadir juego manualmente")
    p_add.add_argument("-t", "--title-id", default="", help="Title ID")
    p_add.add_argument("-n", "--name", required=True, help="Nombre del juego")
    p_add.add_argument("--notes", help="Notas adicionales")
    p_add.set_defaults(func=cmd_add)
    
    # delete
    p_del = subparsers.add_parser("delete", help="Eliminar juego")
    p_del.add_argument("id", type=int, help="ID del juego")
    p_del.add_argument("-f", "--force", action="store_true",
                       help="No pedir confirmación")
    p_del.set_defaults(func=cmd_delete)
    
    # status
    p_status = subparsers.add_parser("status", help="Cambiar status de un juego")
    p_status.add_argument("id", type=int, help="ID del juego")
    p_status.add_argument("status", help="Nuevo status")
    p_status.set_defaults(func=cmd_status)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
