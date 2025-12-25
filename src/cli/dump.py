# cli/dump.py
"""
⚠️ DEPRECATED: Este módulo está obsoleto.
Usar en su lugar: python -m cli.main dump <drive>

Este archivo se mantiene por compatibilidad pero será eliminado en futuras versiones.
"""
import argparse
import os
import tempfile
from core.dumper import dump_disc

def main():
    parser = argparse.ArgumentParser(description="Dump de discos Xbox 360")
    parser.add_argument("drive", help="Unidad óptica (ej: D:\\)")
    parser.add_argument(
        "--out",
        default=None,
        help="Ruta de salida para el ISO. Si no se especifica, se usa %TEMP%/x360dump/game.iso"
    )
    args = parser.parse_args()

    # Si no se pasó --out, usar ruta temporal por defecto
    if args.out is None:
        base_tmp = tempfile.gettempdir()
        args.out = os.path.join(base_tmp, "x360dump", "game.iso")
        print(f"📂 Usando ruta temporal por defecto: {args.out}")

    success = dump_disc(args.drive, out_path=args.out)
    if success:
        print(f"✅ Dump completado → {args.out}")
    else:
        print("❌ Error en dump")

if __name__ == "__main__":
    main()
