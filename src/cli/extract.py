# cli/extract.py
"""
⚠️ DEPRECATED: Este módulo está obsoleto.
Usar en su lugar: python -m cli.main extract <iso>

Este archivo se mantiene por compatibilidad pero será eliminado en futuras versiones.
"""
import argparse
import sys
import os

from core.extractor import extract_iso, list_xex_files


def main():
    parser = argparse.ArgumentParser(description="Extractor de ISOs de Xbox360")
    parser.add_argument("iso_path", help="Ruta al archivo ISO")
    parser.add_argument(
        "-o", "--output", help="Directorio de salida (opcional, por defecto junto al ISO)"
    )
    args = parser.parse_args()

    iso_path = os.path.abspath(args.iso_path)
    output_dir = os.path.abspath(args.output) if args.output else None

    print(f"🔄 Extrayendo ISO: {iso_path}")

    result = extract_iso(iso_path, output_dir)

    if not result:
        print("❌ Error en la extracción")
        sys.exit(1)

    print(f"✅ Extracción completada en: {result}")

    # Listar archivos .xex
    xex_files = list_xex_files(result)
    if xex_files:
        print("📄 Archivos XEX encontrados:")
        for xf in xex_files:
            print(f" - {xf}")
    else:
        print("⚠️ No se encontraron archivos .xex")


if __name__ == "__main__":
    main()
