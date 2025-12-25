import subprocess
import os
import tempfile
from core.config import DISC_IMAGE_CREATOR_PATH


def dump_disc(drive_letter, gui_ref=None, out_path=None):
    """
    Hace dump de un disco de Xbox 360 con DiscImageCreator.

    :param drive_letter: unidad óptica (ej: 'D:\\')
    :param gui_ref: referencia a GUI para loggear (opcional)
    :param out_path: ruta de salida para el ISO. Si no se pasa, se usa %TEMP%/x360dump/game.iso
    :return: True si éxito, False si error
    """
    log = gui_ref.log if gui_ref else print

    if not os.path.isfile(DISC_IMAGE_CREATOR_PATH):
        log(f"❌ No se encontró DiscImageCreator en {DISC_IMAGE_CREATOR_PATH}")
        return False

    # Definir salida
    if out_path is None:
        base_tmp = tempfile.gettempdir()
        tmp_dir = os.path.join(base_tmp, "x360dump")
        os.makedirs(tmp_dir, exist_ok=True)
        out_path = os.path.join(tmp_dir, "game.iso")

    out_path = os.path.abspath(out_path)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Comando DiscImageCreator
    cmd = [DISC_IMAGE_CREATOR_PATH, "dvd", drive_letter, out_path, "4"]
    log(f"Ejecutando: {' '.join(cmd)}")

    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )
        for line in proc.stdout:
            log(line.strip())
        rc = proc.wait()
    except Exception as e:
        log(f"❌ Error ejecutando DiscImageCreator: {e}")
        return False

    if rc == 0:
        return True
    else:
        log(f"❌ Error en dump (rc={rc})")
        # Limpieza si falla
        if os.path.exists(out_path):
            try:
                os.remove(out_path)
            except Exception:
                pass
        return False
