# cli/profiles.py
"""
Comando CLI para gestionar perfiles de juegos.
"""
import argparse
import sys
from core.game_profiles import ProfileManager, GameProfile


def cmd_list(args):
    """Lista todos los perfiles disponibles."""
    manager = ProfileManager()
    profiles = manager.list_profiles()
    
    if not profiles:
        print("No hay perfiles disponibles.")
        print(f"📁 Directorio de perfiles: {manager.profiles_dir}")
        return
    
    print(f"\n{'═'*60}")
    print(f"📋 PERFILES DISPONIBLES ({len(profiles)})")
    print(f"{'═'*60}\n")
    
    for profile in profiles:
        print(f"🎮 [{profile.title_id}] {profile.game_name}")
        if profile.description:
            print(f"   {profile.description}")
        patches_count = len([p for p, v in profile.patches.items() if v])
        if patches_count:
            print(f"   📦 {patches_count} parches activos")
        print()
    
    print(f"📁 Directorio: {manager.profiles_dir}")


def cmd_show(args):
    """Muestra detalles de un perfil."""
    manager = ProfileManager()
    profile = manager.load_profile(args.title_id)
    
    if not profile:
        print(f"❌ No existe perfil para: {args.title_id}")
        sys.exit(1)
    
    print(f"\n{'═'*60}")
    print(f"🎮 {profile.game_name}")
    print(f"{'═'*60}\n")
    
    print(f"Title ID:    {profile.title_id}")
    print(f"Descripción: {profile.description or 'N/A'}")
    
    if profile.recomp_settings:
        print(f"\n📊 Configuración de Recompilación:")
        for key, value in profile.recomp_settings.items():
            print(f"   {key}: {value}")
    
    if profile.patches:
        print(f"\n📦 Parches:")
        for patch, enabled in profile.patches.items():
            status = "✅" if enabled else "❌"
            print(f"   {status} {patch}")
    
    if profile.custom:
        print(f"\n⚙️ Configuración Personalizada:")
        for key, value in profile.custom.items():
            print(f"   {key}: {value}")


def cmd_create(args):
    """Crea un nuevo perfil."""
    manager = ProfileManager()
    
    # Verificar si ya existe
    existing = manager.load_profile(args.title_id)
    if existing and not args.force:
        print(f"⚠️ Ya existe perfil para {args.title_id}: {existing.game_name}")
        print("   Usa --force para sobrescribir")
        sys.exit(1)
    
    profile = manager.create_profile(
        title_id=args.title_id,
        game_name=args.name,
        description=args.description or "",
        log=print
    )
    
    print(f"\n✅ Perfil creado exitosamente")
    print(f"   Title ID: {profile.title_id}")
    print(f"   Nombre:   {profile.game_name}")


def cmd_default(args):
    """Muestra el perfil por defecto."""
    manager = ProfileManager()
    profile = manager.get_default_profile()
    
    print(f"\n📋 Perfil por Defecto")
    print(f"{'─'*40}")
    print(f"Title ID: {profile.title_id}")
    print(f"Nombre:   {profile.game_name}")
    
    if profile.recomp_settings:
        print(f"\n📊 Configuración:")
        for key, value in profile.recomp_settings.items():
            print(f"   {key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="Gestión de perfiles de juegos",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # list
    p_list = subparsers.add_parser("list", help="Listar perfiles")
    p_list.set_defaults(func=cmd_list)
    
    # show
    p_show = subparsers.add_parser("show", help="Mostrar perfil")
    p_show.add_argument("title_id", help="Title ID del juego")
    p_show.set_defaults(func=cmd_show)
    
    # create
    p_create = subparsers.add_parser("create", help="Crear perfil")
    p_create.add_argument("-t", "--title-id", required=True, help="Title ID")
    p_create.add_argument("-n", "--name", required=True, help="Nombre del juego")
    p_create.add_argument("-d", "--description", help="Descripción")
    p_create.add_argument("-f", "--force", action="store_true", help="Sobrescribir")
    p_create.set_defaults(func=cmd_create)
    
    # default
    p_default = subparsers.add_parser("default", help="Mostrar perfil por defecto")
    p_default.set_defaults(func=cmd_default)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
