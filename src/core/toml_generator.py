import os
import toml
import subprocess
from core.config import PPC_CONTEXT_PATH, XENON_RECOMP_PATH

def generate_project_toml(xex_path: str, analysis_json: str, output_dir: str) -> str:
    """
    Genera un project.toml con una estructura mínima válida.
    """
    os.makedirs(output_dir, exist_ok=True)
    toml_path = os.path.join(output_dir, "project.toml")

    content = {
        "project": {
            "title_id": "00000000",  # Placeholder por ahora
            "game_name": os.path.splitext(os.path.basename(xex_path))[0]
        },
        "input": {
            "xex_path": xex_path.replace("\\", "/"),
            "analysis_json": analysis_json.replace("\\", "/")
        },
        "output": {
            "target_dir": "build/"
        }
    }

    with open(toml_path, "w", encoding="utf-8") as f:
        toml.dump(content, f)

    return toml_path


def validate_project_toml(toml_path: str, log=None) -> bool:
    cmd = [
    XENON_RECOMP_PATH,
    toml_path,
    PPC_CONTEXT_PATH
]
    if log:
        log("Ejecutando validación: " + " ".join(cmd))

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=os.path.dirname(toml_path),  # ⚡ aseguramos que cwd sea la carpeta del TOML
            shell=False
        )
        print(result)
        if result.returncode == 0:
            if log: log("✅ project.toml válido (sin errores reportados)")
            return True
        else:
            if result.returncode == 3221226505:
                if log: log("⚠️ XenonRecomp se cerró inesperadamente (posible problema de cwd o TOML)")
            else:
                if log: log(f"❌ Código de error: {result.returncode}")
            if log and result.stdout: log("STDOUT:\n" + result.stdout)
            if log and result.stderr: log("STDERR:\n" + result.stderr)
            return False
    except Exception as e:
        if log: log(f"⚠️ Error al ejecutar XenonRecomp: {e}")
        return False

