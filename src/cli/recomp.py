# cli/recomp.py
"""
Comando CLI para recompilación con XenonRecomp.
"""
import argparse
import sys
import os

from core.shader_recomp import (
    run_recompilation,
    validate_recomp_output,
    check_xenon_recomp_available,
    get_recomp_version
)
from core.analyser import analyse_xex
from core.toml_generator import generate_project_toml


def log_print(msg: str):
    """Logger simple para CLI."""
    print(msg)


def cmd_recomp_toml(args):
    """Recompila desde un TOML existente."""
    toml_path = args.toml
    
    if not os.path.isfile(toml_path):
        print(f"❌ Archivo no encontrado: {toml_path}")
        sys.exit(1)
    
    print(f"🔧 Recompilando desde: {toml_path}")
    
    result = run_recompilation(
        toml_path=toml_path,
        output_dir=args.output,
        log=log_print
    )
    
    if result.success:
        print(f"\n✅ Recompilación exitosa!")
        print(f"📁 Directorio: {result.output_dir}")
        print(f"📄 Archivos C++: {len(result.cpp_files)}")
        print(f"📄 Headers: {len(result.header_files)}")
    else:
        print(f"\n❌ Recompilación fallida: {result.error}")
        sys.exit(1)


def cmd_recomp_xex(args):
    """Recompila desde un XEX (analiza, genera TOML, recompila)."""
    xex_path = args.xex
    output_dir = args.output or os.path.dirname(xex_path)
    
    if not os.path.isfile(xex_path):
        print(f"❌ Archivo no encontrado: {xex_path}")
        sys.exit(1)
    
    print(f"🔧 Pipeline de recompilación desde XEX")
    print(f"📁 XEX: {xex_path}")
    print(f"📁 Output: {output_dir}\n")
    
    # Paso 1: Analizar XEX
    print("📊 Paso 1/3: Analizando XEX...")
    analysis_result = analyse_xex(xex_path, out_dir=output_dir, log=log_print)
    
    if not analysis_result:
        print("❌ Falló el análisis del XEX")
        sys.exit(1)
    
    json_file, toml_file = analysis_result
    print(f"   ✅ Análisis completado: {json_file}")
    
    # Paso 2: Generar project.toml
    print("\n📝 Paso 2/3: Generando project.toml...")
    project_toml = generate_project_toml(xex_path, json_file, output_dir)
    print(f"   ✅ TOML generado: {project_toml}")
    
    # Paso 3: Recompilar
    print("\n🔧 Paso 3/3: Ejecutando XenonRecomp...")
    result = run_recompilation(
        toml_path=project_toml,
        output_dir=output_dir,
        log=log_print
    )
    
    if result.success:
        print(f"\n🎉 Pipeline de recompilación completado!")
        print(f"📁 Directorio: {result.output_dir}")
        print(f"📄 Archivos C++: {len(result.cpp_files)}")
        print(f"📄 Headers: {len(result.header_files)}")
    else:
        print(f"\n❌ Recompilación fallida: {result.error}")
        sys.exit(1)


def cmd_version(args):
    """Muestra la versión de XenonRecomp."""
    if not check_xenon_recomp_available():
        print("❌ XenonRecomp no está instalado o no se encuentra")
        sys.exit(1)
    
    version = get_recomp_version(log=log_print)
    print(f"XenonRecomp versión: {version}")


def cmd_validate(args):
    """Valida el output de una recompilación."""
    output_dir = args.dir
    
    if not os.path.isdir(output_dir):
        print(f"❌ Directorio no encontrado: {output_dir}")
        sys.exit(1)
    
    success, files = validate_recomp_output(output_dir, log=log_print)
    
    if success:
        print(f"\n✅ Validación exitosa: {len(files)} archivos encontrados")
    else:
        print(f"\n❌ No se encontraron archivos de recompilación")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Recompilación de Xbox 360 con XenonRecomp",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponibles")
    
    # toml - Recompilar desde TOML
    p_toml = subparsers.add_parser("toml", help="Recompilar desde project.toml")
    p_toml.add_argument("-t", "--toml", required=True, help="Ruta al project.toml")
    p_toml.add_argument("-o", "--output", help="Directorio de salida")
    p_toml.set_defaults(func=cmd_recomp_toml)
    
    # xex - Recompilar desde XEX (pipeline completo)
    p_xex = subparsers.add_parser("xex", help="Recompilar desde XEX (pipeline completo)")
    p_xex.add_argument("-x", "--xex", required=True, help="Ruta al archivo XEX")
    p_xex.add_argument("-o", "--output", help="Directorio de salida")
    p_xex.set_defaults(func=cmd_recomp_xex)
    
    # version - Mostrar versión
    p_version = subparsers.add_parser("version", help="Mostrar versión de XenonRecomp")
    p_version.set_defaults(func=cmd_version)
    
    # validate - Validar output
    p_validate = subparsers.add_parser("validate", help="Validar output de recompilación")
    p_validate.add_argument("-d", "--dir", required=True, help="Directorio a validar")
    p_validate.set_defaults(func=cmd_validate)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
