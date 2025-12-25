# core/cleaner_xex.py
import os
import subprocess
from core.config import XEXTOOL_PATH

def _ensure_tool_exists(path, tool_name="xextool"):
    # Si path es un nombre (p.ej. en PATH) dejamos que Windows lo resuelva.
    if os.path.basename(path).lower() == f"{tool_name}.exe":
        return True
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No se encontró {tool_name} en '{path}'. "
            f"Ajusta core/config.py o define la variable de entorno {tool_name.upper()}_PATH."
        )
    return True

def check_xex_info(xex_path, log=None):
    _ensure_tool_exists(XEXTOOL_PATH, "xextool")
    cmd = [XEXTOOL_PATH, "-l", xex_path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    if log:
        log(out.strip())
    return out

def clean_xex(xex_path, output_dir, log=None):
    """
    Usa xextool para desencriptar (-e d) y descomprimir (-c u) si hace falta.
    Devuelve la ruta al XEX limpio (o el original si no fue necesario o falló).
    """
    info = check_xex_info(xex_path, log=log).lower()
    needs_decrypt = "encrypted" in info
    needs_uncompress = "compressed" in info

    if not needs_decrypt and not needs_uncompress:
        if log:
            log("✅ XEX no requiere limpieza")
        return xex_path

    os.makedirs(output_dir, exist_ok=True)
    clean_path = os.path.join(
        output_dir,
        os.path.basename(xex_path).replace(".xex", "_clean.xex")
    )

    args = [XEXTOOL_PATH]
    if needs_decrypt:
        args += ["-e", "d"]
    if needs_uncompress:
        args += ["-c", "u"]
    args += ["-o", clean_path, xex_path]

    if log:
        log(f"Ejecutando limpieza con: {' '.join(args)}")

    proc = subprocess.run(args, capture_output=True, text=True)
    if log:
        log((proc.stdout or "") + (proc.stderr or ""))

    if proc.returncode == 0 and os.path.exists(clean_path):
        if log:
            log(f"✅ XEX limpio en {clean_path}")
        return clean_path

    if log:
        log("⚠️ No se pudo limpiar el XEX, se usará el original")
    return xex_path
