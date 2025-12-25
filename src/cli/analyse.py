# cli/analyse.py
"""
⚠️ DEPRECATED: Este módulo está obsoleto.
Usar en su lugar: python -m cli.main analyse <xex>

Este archivo se mantiene por compatibilidad pero será eliminado en futuras versiones.
"""
import argparse
import os
import sys
import json
from core.analyser import analyse_xex


def main():
    parser = argparse.ArgumentParser(description="Analizar un default.xex con XenonAnalyse")
    parser.add_argument("xex", help="Ruta al archivo XEX a analizar")
    args = parser.parse_args()

    xex_path = args.xex
    if not os.path.exists(xex_path):
        print(f"❌ No se encontró el archivo {xex_path}")
        sys.exit(1)

    result = analyse_xex(xex_path)
    if not result:
        print("❌ Error durante el análisis")
        sys.exit(1)

    json_file, toml_file = result
    print("✅ Análisis completado.")
    print(f"- TOML en: {toml_file}")
    print(f"- JSON en: {json_file}")

    # Leer JSON para generar un pequeño resumen
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"⚠️ No se pudo leer el JSON: {e}")
        sys.exit(1)

    print("\n📊 Resumen del análisis")
    if not data:
        print("⚠️ El archivo de salida está vacío o no contiene secciones.")
    else:
        for key, value in data.items():
            if isinstance(value, dict):
                print(f"- {key}: {len(value)} elementos (dict)")
            elif isinstance(value, list):
                print(f"- {key}: {len(value)} entradas (list)")
            else:
                print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
