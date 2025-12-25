import os
import subprocess


from core.config import EXTRACT_XISO_PATH


def _sanitize_path(path: str) -> str:
    """Normaliza rutas para Windows."""
    return os.path.abspath(os.path.normpath(path))


def extract_iso(iso_path: str, output_dir: str = None, log=None) -> str | None:
    """
    Extrae un ISO de Xbox 360 usando extract-xiso.
    - iso_path: ruta del archivo ISO
    - output_dir: carpeta destino (si no se pasa, se crea junto al ISO)
    - log: función de logging opcional
    """
    iso_path = _sanitize_path(iso_path)

    # Carpeta destino base
    if output_dir:
        final_output = _sanitize_path(output_dir)
    else:
        base, _ = os.path.splitext(iso_path)
        final_output = base

    # Si ya existe, generamos nombre incremental
    original_output = final_output
    i = 1
    while os.path.exists(final_output):
        final_output = f"{original_output}_{i}"
        i += 1

    os.makedirs(final_output, exist_ok=True)

    if log:
        log(f"📂 Carpeta de destino (workaround sin -d): {final_output}")

    # Ejecutamos extract-xiso desde final_output como cwd
    cmd = [EXTRACT_XISO_PATH, "-x", iso_path]

    if log:
        log(f"Ejecutando en cwd={final_output}: {' '.join(cmd)}")
    else:
        print("[DEBUG]", " ".join(cmd), f"(cwd={final_output})")

    try:
        subprocess.run(cmd, cwd=final_output, check=True)
        return final_output
    except subprocess.CalledProcessError as e:
        if log:
            log("❌ Error al extraer ISO")
            log(str(e))
        else:
            print("❌ Error al extraer ISO:", e)
        return None


def list_xex_files(output_dir: str) -> list[str]:
    """
    Busca todos los archivos .xex dentro del directorio extraído.
    """
    output_dir = _sanitize_path(output_dir)
    xex_files = []

    for root, _, files in os.walk(output_dir):
        for f in files:
            if f.lower().endswith(".xex"):
                xex_files.append(os.path.join(root, f))

    return xex_files
