#!/usr/bin/env python3
# cli/main.py
"""
MrMonkeyShopWare CLI - Entry point principal con subcomandos.
"""
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="mrmonkey",
        description="🐵 MrMonkeyShopWare - Gestión de ports Xbox 360 a PC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  mrmonkey analyse path/to/default.xex   Analizar un XEX
  mrmonkey scan-usb E:                   Escanear USB Xbox 360
  mrmonkey list                          Listar juegos/workspaces
  mrmonkey info 4E4D07F5                 Ver info de un juego
        """
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="MrMonkeyShopWare v0.1.0"
    )
    
    subparsers = parser.add_subparsers(
        dest="command",
        title="Comandos disponibles",
        metavar="<comando>"
    )
    
    # Registrar todos los subcomandos
    _register_subcommands(subparsers)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Ejecutar el comando
    if hasattr(args, 'func'):
        try:
            args.func(args)
        except KeyboardInterrupt:
            print("\n\n⚠️ Operación cancelada por el usuario")
            sys.exit(1)
        except Exception as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        parser.print_help()


def _register_subcommands(subparsers):
    """Registra todos los subcomandos disponibles."""
    
    # === Comandos de procesamiento ===
    
    # analyse
    analyse_parser = subparsers.add_parser(
        "analyse",
        help="Analizar un archivo XEX",
        description="Analiza un XEX y crea un workspace organizado"
    )
    analyse_parser.add_argument("xex", help="Ruta al archivo XEX")
    analyse_parser.add_argument("-o", "--output", help="Directorio de salida (opcional)")
    analyse_parser.set_defaults(func=_cmd_analyse)
    
    # extract
    extract_parser = subparsers.add_parser(
        "extract",
        help="Extraer contenido de un ISO",
        description="Extrae el contenido de una imagen ISO de Xbox 360"
    )
    extract_parser.add_argument("iso", help="Ruta al archivo ISO")
    extract_parser.add_argument("-o", "--output", help="Directorio de salida")
    extract_parser.set_defaults(func=_cmd_extract)
    
    # dump
    dump_parser = subparsers.add_parser(
        "dump",
        help="Hacer dump de un disco físico",
        description="Crea una imagen ISO desde un disco Xbox 360 en la unidad óptica"
    )
    dump_parser.add_argument("drive", help="Letra de la unidad (ej: E:)")
    dump_parser.add_argument("-o", "--output", help="Directorio de salida")
    dump_parser.set_defaults(func=_cmd_dump)
    
    # pipeline
    pipeline_parser = subparsers.add_parser(
        "pipeline",
        help="Pipeline completo (dump → extract → analyse)",
        description="Ejecuta el pipeline completo de procesamiento"
    )
    pipeline_parser.add_argument("drive", help="Letra de la unidad (ej: E:)")
    pipeline_parser.add_argument("-o", "--output", help="Directorio de salida")
    pipeline_parser.set_defaults(func=_cmd_pipeline)
    
    # === Comandos de gestión ===
    
    # scan-usb
    scan_parser = subparsers.add_parser(
        "scan-usb",
        help="Escanear USB Xbox 360",
        description="Detecta y lista juegos en un USB con formato Xbox 360"
    )
    scan_parser.add_argument("drive", help="Letra de la unidad USB (ej: E:)")
    scan_parser.add_argument("-a", "--analyse", action="store_true", help="Analizar juego seleccionado")
    scan_parser.set_defaults(func=_cmd_scan_usb)
    
    # list
    list_parser = subparsers.add_parser(
        "list",
        help="Listar juegos/workspaces",
        description="Muestra todos los workspaces de juegos creados"
    )
    list_parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar más detalles")
    list_parser.set_defaults(func=_cmd_list)
    
    # info
    info_parser = subparsers.add_parser(
        "info",
        help="Ver información de un juego",
        description="Muestra información detallada de un juego por Title ID"
    )
    info_parser.add_argument("title_id", help="Title ID del juego (ej: 4E4D07F5)")
    info_parser.set_defaults(func=_cmd_info)
    
    # sync
    sync_parser = subparsers.add_parser(
        "sync",
        help="Sincronizar archivos al workspace",
        description="Copia archivos externos al workspace del juego"
    )
    sync_parser.add_argument("title_id", help="Title ID del juego (ej: 4E4D07F5)")
    sync_parser.add_argument("-y", "--yes", action="store_true", help="No pedir confirmación")
    sync_parser.set_defaults(func=_cmd_sync)
    
    # === Comandos de utilidad ===
    
    # db
    db_parser = subparsers.add_parser(
        "db",
        help="Gestionar base de datos",
        description="Operaciones sobre la base de datos de juegos"
    )
    db_sub = db_parser.add_subparsers(dest="db_command")
    
    db_list = db_sub.add_parser("list", help="Listar juegos en BD")
    db_list.set_defaults(func=_cmd_db_list)
    
    db_export = db_sub.add_parser("export", help="Exportar BD a JSON")
    db_export.add_argument("-o", "--output", default="games_export.json")
    db_export.set_defaults(func=_cmd_db_export)


# === Implementación de comandos ===

def _cmd_analyse(args):
    """Comando: analyse"""
    import os
    from core.analyser import analyse_xex
    from core.game_workspace import get_or_create_workspace, GameInfo
    from core.database import GameDatabase, Game, GameStatus
    
    xex_path = args.xex
    if not os.path.exists(xex_path):
        print(f"❌ No se encontró el archivo: {xex_path}")
        sys.exit(1)
    
    print(f"🔬 Analizando {os.path.basename(xex_path)}...")
    
    result = analyse_xex(xex_path)
    
    if not result or not result.success:
        print("❌ Error durante el análisis")
        sys.exit(1)
    
    xex_info = result.xex_info
    
    if xex_info and xex_info.title_id:
        print(f"\n📋 Juego detectado: {xex_info.display_name}")
        print(f"   Title ID: {xex_info.title_id}")
        
        # Crear workspace
        game_name = xex_info.display_name or os.path.basename(xex_path).replace(".xex", "")
        workspace, is_new = get_or_create_workspace(xex_info.title_id, game_name)
        
        if is_new:
            print(f"\n📁 Creado workspace: {workspace.root}")
        else:
            print(f"\n📁 Usando workspace existente: {workspace.root}")
        
        # Guardar info
        game_info = GameInfo.from_xex_info(xex_info, source_type="xex", source_path=xex_path)
        workspace.save_info(game_info)
        print("   ✅ info.json guardado")
        
        # Copiar archivos de análisis
        import shutil
        if result.json_file and os.path.exists(result.json_file):
            dest = workspace.analysis_dir / os.path.basename(result.json_file)
            shutil.copy2(result.json_file, dest)
            print(f"   📊 {os.path.basename(result.json_file)} copiado")
        
        if result.toml_file and os.path.exists(result.toml_file):
            dest = workspace.analysis_dir / os.path.basename(result.toml_file)
            shutil.copy2(result.toml_file, dest)
            print(f"   📄 {os.path.basename(result.toml_file)} copiado")
        
        # Guardar en BD
        try:
            import json
            game = Game(
                title_id=xex_info.title_id,
                game_name=game_name,
                status=GameStatus.ANALYSED,
                xex_path=xex_path,
                extracted_dir=str(workspace.root),
                analysis_json=result.json_file,
                project_toml=result.toml_file,
                media_id=xex_info.media_id,
                version=xex_info.version,
                regions=xex_info.regions,
                esrb_rating=xex_info.esrb_rating
            )
            
            with GameDatabase() as db:
                game_id = db.add_or_update_game(game)
            
            print(f"\n💾 Guardado en base de datos (ID: {game_id})")
        except Exception as e:
            print(f"⚠️ No se pudo guardar en BD: {e}")
    
    print("\n🎉 ¡Análisis completado!")


def _cmd_extract(args):
    """Comando: extract"""
    from core.extractor import extract_iso
    
    print(f"📦 Extrayendo {args.iso}...")
    result = extract_iso(args.iso, args.output)
    
    if result:
        print(f"✅ Extraído en: {result}")
    else:
        print("❌ Error durante la extracción")
        sys.exit(1)


def _cmd_dump(args):
    """Comando: dump"""
    from core.dumper import dump_disc
    
    print(f"📀 Iniciando dump desde {args.drive}...")
    success = dump_disc(args.drive, args.output if hasattr(args, 'output') else None)
    
    if success:
        print("✅ Dump completado con éxito")
    else:
        print("❌ Error en el dump")
        sys.exit(1)


def _cmd_pipeline(args):
    """Comando: pipeline"""
    from core.pipeline import full_pipeline
    
    print(f"🚀 Iniciando pipeline completo desde {args.drive}...")
    result = full_pipeline(args.drive)
    
    if result and result.success:
        print("\n🎉 ¡Pipeline completado!")
        if result.xex_info:
            print(f"   Juego: {result.xex_info.display_name}")
    else:
        print("❌ Error en el pipeline")
        sys.exit(1)


def _cmd_scan_usb(args):
    """Comando: scan-usb"""
    from core.xbox_drive_scanner import is_xbox_usb, list_games_on_drive
    
    drive = args.drive
    print(f"💾 Escaneando {drive}...")
    
    if not is_xbox_usb(drive):
        print("❌ No se detectó estructura Xbox 360 en este disco")
        sys.exit(1)
    
    games = list_games_on_drive(drive)
    
    if not games:
        print("❌ No se encontraron juegos")
        sys.exit(1)
    
    print(f"\n✅ Encontrados {len(games)} juego(s):\n")
    
    for i, game in enumerate(games, 1):
        print(f"  [{i}] {game.display_name or game.title_id}")
        print(f"      Title ID: {game.title_id}")
        if game.xex_path:
            print(f"      XEX: {game.xex_path}")
        print()
    
    if args.analyse:
        try:
            choice = input("Selecciona un juego (1-{}) o 'q' para salir: ".format(len(games)))
            if choice.lower() == 'q':
                return
            
            idx = int(choice) - 1
            if 0 <= idx < len(games):
                selected = games[idx]
                if selected.xex_path:
                    print(f"\n🔬 Analizando {selected.display_name}...")
                    # Simular args para analyse
                    class AnalyseArgs:
                        xex = selected.xex_path
                        output = None
                    _cmd_analyse(AnalyseArgs())
                else:
                    print("❌ No se encontró XEX para este juego")
        except (ValueError, IndexError):
            print("❌ Selección inválida")


def _cmd_list(args):
    """Comando: list"""
    from core.game_workspace import GameWorkspace
    import os
    
    workspaces = GameWorkspace.list_all()
    
    if not workspaces:
        print("📂 No hay workspaces creados aún")
        print("\n💡 Usa 'mrmonkey analyse <xex>' para crear uno")
        return
    
    print(f"📂 Workspaces ({len(workspaces)}):\n")
    
    for ws in workspaces:
        info = ws.load_info()
        print(f"  📁 {ws.game_name} [{ws.title_id}]")
        
        if info:
            print(f"     Estado: {info.status}")
        
        if args.verbose:
            print(f"     Ruta: {ws.root}")
            # Verificar archivos
            files = []
            if ws.info_file.exists():
                files.append("✅ info.json")
            if (ws.analysis_dir / "analysis.toml").exists():
                files.append("✅ TOML")
            if (ws.analysis_dir / "analysis.json").exists():
                files.append("✅ JSON")
            print(f"     Archivos: {' '.join(files) if files else '❓ ninguno'}")
        
        print()
    
    print(f"Total: {len(workspaces)} workspace(s)")


def _cmd_info(args):
    """Comando: info"""
    from core.game_workspace import GameWorkspace
    from core.database import GameDatabase
    
    title_id = args.title_id.upper()
    
    # Buscar en workspace
    workspace = GameWorkspace.find_existing(title_id)
    
    if workspace:
        info = workspace.load_info()
        
        print(f"\n📋 {info.game_name if info else workspace.game_name}\n")
        print(f"  Title ID:    {title_id}")
        
        if info:
            print(f"  Media ID:    {info.media_id or 'N/A'}")
            print(f"  Versión:     {info.version or 'N/A'}")
            print(f"  Regiones:    {info.regions or 'N/A'}")
            print(f"  Rating:      {info.esrb_rating or 'N/A'}")
            print(f"\n  Estado:      {info.status}")
            print(f"  Creado:      {info.created_at[:10] if info.created_at else 'N/A'}")
        
        print(f"\n📁 Workspace: {workspace.root}")
    else:
        # Buscar en BD
        with GameDatabase() as db:
            game = db.get_by_title_id(title_id)
        
        if game:
            print(f"\n📋 {game.game_name}\n")
            print(f"  Title ID:    {game.title_id}")
            print(f"  Estado:      {game.status.value}")
            print(f"  XEX:         {game.xex_path or 'N/A'}")
        else:
            print(f"❌ No se encontró juego con Title ID: {title_id}")


def _cmd_sync(args):
    """Comando: sync"""
    from core.game_workspace import GameWorkspace
    from core.database import GameDatabase
    
    title_id = args.title_id.upper()
    
    # Buscar workspace
    workspace = GameWorkspace.find_existing(title_id)
    
    if not workspace:
        print(f"❌ No se encontró workspace para Title ID: {title_id}")
        sys.exit(1)
    
    # Buscar juego en BD
    with GameDatabase() as db:
        game = db.get_by_title_id(title_id)
    
    if not game:
        print(f"❌ No se encontró juego en BD con Title ID: {title_id}")
        sys.exit(1)
    
    print(f"🔄 Verificando archivos de {game.game_name}...")
    
    # Detectar externos
    external = workspace.check_external_files(game)
    
    if not external:
        print("\n✅ Todos los archivos ya están en el workspace")
        print(f"📁 {workspace.root}")
        return
    
    print(f"\n⚠️ Encontrados {len(external)} archivo(s) fuera del workspace:\n")
    
    for ef in external:
        size_mb = ef.size / (1024 * 1024)
        print(f"  {ef.label}")
        print(f"     Actual:  {ef.current_path}")
        print(f"     Destino: {ef.target_path}")
        print(f"     Tamaño:  {size_mb:.1f} MB\n")
    
    # Confirmar
    if not args.yes:
        response = input("¿Sincronizar ahora? (s/n): ")
        if response.lower() != 's':
            print("Cancelado")
            return
    
    # Ejecutar sync
    print("\n📥 Sincronizando...")
    new_paths = workspace.sync_all_files(game, log=print)
    
    # Actualizar BD
    if new_paths:
        try:
            for field, path in new_paths.items():
                setattr(game, field, path)
            
            with GameDatabase() as db:
                db.update_game(game)
            
            print("\n💾 Rutas actualizadas en base de datos")
        except Exception as e:
            print(f"\n⚠️ Error actualizando BD: {e}")
    
    print("\n🎉 ¡Sincronización completada!")
    print(f"📁 Workspace: {workspace.root}")


def _cmd_db_list(args):
    """Comando: db list"""
    from core.database import GameDatabase
    
    with GameDatabase() as db:
        games = db.list_games()
    
    if not games:
        print("📚 Base de datos vacía")
        return
    
    print(f"📚 Juegos en base de datos ({len(games)}):\n")
    
    for game in games:
        status_icon = "✅" if game.status.value == "completed" else "🔄"
        print(f"  {status_icon} [{game.id}] {game.game_name}")
        print(f"     Title ID: {game.title_id or 'N/A'} | Estado: {game.status.value}")
    
    print(f"\nTotal: {len(games)} juego(s)")


def _cmd_db_export(args):
    """Comando: db export"""
    import json
    from core.database import GameDatabase
    
    with GameDatabase() as db:
        games = db.list_games()
    
    export_data = []
    for game in games:
        export_data.append({
            "id": game.id,
            "title_id": game.title_id,
            "game_name": game.game_name,
            "status": game.status.value,
            "xex_path": game.xex_path,
            "iso_path": game.iso_path,
        })
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Exportados {len(games)} juegos a {args.output}")


if __name__ == "__main__":
    main()
