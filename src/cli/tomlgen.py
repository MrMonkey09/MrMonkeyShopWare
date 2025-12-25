# cli/tomlgen.py
"""
⚠️ DEPRECATED: Este módulo está obsoleto.
La funcionalidad de generación de TOML está integrada en el pipeline principal.

Este archivo se mantiene por compatibilidad pero será eliminado en futuras versiones.
"""
import argparse
import os
import shutil
from core.config import XENON_RECOMP_PATH
from core.toml_generator import validate_project_toml

def get_analysis_dir():
    """Devuelve la ruta fija donde XenonAnalyse genera sus salidas"""
    return os.path.join(os.environ.get("TEMP", "/tmp"), "x360dump", "analysis")

def main():
    parser = argparse.ArgumentParser(description="Generar project.toml desde XenonAnalyse")
    parser.add_argument(
        "--out",
        default="output",
        help="Carpeta donde guardar project.toml (default: ./output)"
    )
    args = parser.parse_args()

    analysis_dir = get_analysis_dir()
    analysis_toml = os.path.join(analysis_dir, "analysis.toml")

    if not os.path.exists(analysis_toml):
        print(f"❌ No se encontró analysis.toml en {analysis_dir}")
        return

    # Asegurar carpeta de salida
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    project_toml = os.path.join(out_dir, "project.toml")

    # Copiar archivo
    shutil.copyfile(analysis_toml, project_toml)
    print(f"📂 Usando carpeta de análisis: {analysis_dir}")
    print(f"✅ Copiado analysis.toml → {project_toml}")

    # Validar
    print("🔎 Validando con XenonRecomp...")
    if validate_project_toml(project_toml):
        print("✅ project.toml válido")
    else:
        print("❌ project.toml inválido o XenonRecomp crasheó")

if __name__ == "__main__":
    main()
