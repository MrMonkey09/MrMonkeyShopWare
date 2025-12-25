# cli/pipeline.py
"""
⚠️ DEPRECATED: Este módulo está obsoleto.
Usar en su lugar: python -m cli.main pipeline <drive>

Este archivo se mantiene por compatibilidad pero será eliminado en futuras versiones.
"""
import argparse
import sys
from core.pipeline import full_pipeline


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline completo Xbox 360: dump → extract → analyse → toml",
        epilog="Ejemplos:\n"
               "  pipeline -d E:              # Desde disco\n"
               "  pipeline -i game.iso        # Desde ISO\n"
               "  pipeline -x default.xex     # Desde XEX",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Grupo mutuamente excluyente para el origen
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument(
        "-d", "--drive",
        metavar="LETRA",
        help="Letra de unidad óptica (ej: E:)"
    )
    source.add_argument(
        "-i", "--iso",
        metavar="RUTA",
        help="Ruta a archivo ISO existente"
    )
    source.add_argument(
        "-x", "--xex",
        metavar="RUTA",
        help="Ruta a archivo XEX existente"
    )
    
    parser.add_argument(
        "-o", "--output",
        metavar="DIR",
        help="Directorio de salida (por defecto: temporal)"
    )
    
    args = parser.parse_args()
    
    # Ejecutar pipeline
    result = full_pipeline(
        drive_letter=args.drive,
        iso_path=args.iso,
        xex_path=args.xex,
        output_dir=args.output
    )
    
    # Imprimir resumen final
    if result.success:
        print("\n" + "=" * 50)
        print("📊 RESUMEN DE RESULTADOS")
        print("=" * 50)
        if result.iso_path:
            print(f"  ISO:          {result.iso_path}")
        if result.extracted_dir:
            print(f"  Extraído:     {result.extracted_dir}")
        if result.main_xex:
            print(f"  XEX:          {result.main_xex}")
        if result.analysis_json:
            print(f"  Análisis:     {result.analysis_json}")
        if result.project_toml:
            print(f"  Project TOML: {result.project_toml}")
        sys.exit(0)
    else:
        print(f"\n❌ Pipeline fallido: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
