#!/usr/bin/env python3
"""
Script portable para generar un config.toml de XenonRecomp
a partir de un switch_tables.toml generado por XenonAnalyse.

Uso:
    python generate_config.py --switch switch_tables.toml --xex default.xex --out output_cpp --config config.toml \
        --rest 0x822CB4B0 0x822CB460 0x822CBE8C 0x822CBE40 0x822CDAE8 0x822CD850 0x822CDB7C 0x822CD8E4
"""

import argparse
import toml
import os

def main():
    parser = argparse.ArgumentParser(description="Generador de config.toml para XenonRecomp")
    parser.add_argument("--switch", required=True, help="Ruta al switch_tables.toml generado por XenonAnalyse")
    parser.add_argument("--xex", required=True, help="Ruta al archivo .xex")
    parser.add_argument("--out", required=True, help="Carpeta de salida para código C++ recompilado")
    parser.add_argument("--config", default="config.toml", help="Ruta donde guardar el config.toml resultante")
    parser.add_argument("--rest", nargs=8, metavar=("RESTGPR", "SAVEGPR", "RESTFPR", "SAVEFPR",
                                                   "RESTVMX14", "SAVEVMX14", "RESTVMX64", "SAVEVMX64"),
                        help="Direcciones hexadecimales de funciones rest/save detectadas por XenonAnalyse")
    args = parser.parse_args()

    # Cargar el TOML de switch tables (aunque solo lo referenciamos en config)
    if not os.path.exists(args.switch):
        raise FileNotFoundError(f"No se encontró {args.switch}")
    switch_file_name = os.path.basename(args.switch)

    # Construcción de config.toml
    config = {
        "main": {
            "file_path": args.xex,
            "out_directory_path": args.out,
            "switch_table_file_path": switch_file_name,
        },
        "functions": [],
        "invalid_instructions": [],
        "optimizations": {
            "skip_lr": False,
            "skip_msr": False,
            "ctr_as_local": False,
            "xer_as_local": False,
            "reserved_as_local": False,
            "cr_as_local": False,
            "non_argument_as_local": False,
            "non_volatile_as_local": False,
        }
    }

    # Incluir rest/save addresses si se entregaron
    if args.rest:
        keys = [
            "restgprlr_14_address", "savegprlr_14_address",
            "restfpr_14_address", "savefpr_14_address",
            "restvmx_14_address", "savevmx_14_address",
            "restvmx_64_address", "savevmx_64_address"
        ]
        for key, value in zip(keys, args.rest):
            config["main"][key] = value

    # Guardar config.toml
    os.makedirs(os.path.dirname(args.config), exist_ok=True)
    with open(args.config, "w") as f:
        toml.dump(config, f)

    print(f"✅ Config.toml generado en {args.config}")
    print("📂 Referencia a switch tables:", args.switch)
    print("📦 Archivo .xex:", args.xex)
    print("📤 Out directory:", args.out)

if __name__ == "__main__":
    main()
