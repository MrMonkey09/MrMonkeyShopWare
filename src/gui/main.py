import tkinter as tk
from tkinter import filedialog
import threading
import tempfile
import os

from core.dumper import dump_disc
from core.extractor import extract_iso, list_xex_files
from core.analyser import analyse_xex


class LauncherGUI:
    def __init__(self, root):
        self.root = root
        root.title("Launcher Xbox360")

        self.status_label = tk.Label(
            root, text="Esperando acción", font=("Arial", 14)
        )
        self.status_label.pack(pady=12)

        # Botón: Dump Disc
        self.dump_button = tk.Button(
            root, text="Dump Disc", width=20, command=self.on_dump
        )
        self.dump_button.pack(pady=6)

        # Botón: Extract ISO
        self.extract_button = tk.Button(
            root, text="Extract ISO", width=20, command=self.on_extract
        )
        self.extract_button.pack(pady=6)

        # Botón: Analyse XEX
        self.analyse_button = tk.Button(
            root, text="Analyse XEX", width=20, command=self.on_analyse
        )
        self.analyse_button.pack(pady=6)

        # Caja de logs
        self.log_box = tk.Text(root, height=12, width=80, state=tk.DISABLED)
        self.log_box.pack(padx=10, pady=12)

    def log(self, msg):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, f"{msg}\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def set_status(self, msg):
        self.status_label.config(text=msg)

    # -------------------
    # Dump Disc
    # -------------------
    def on_dump(self):
        from tkinter.simpledialog import askstring
        drive = askstring(
            "Unidad óptica", "Ingresa la letra de la unidad (ej: E:)")
        if not drive:
            return

        self.set_status("Dumpeando disco…")
        self.log(f"Iniciando dump desde {drive}")

        def job():
            result = dump_disc(drive, gui_ref=self)
            if result:
                self.log(f"✅ Dump completado → {result}")
            else:
                self.log("❌ Error en dump")
            self.set_status("Esperando acción")

        threading.Thread(target=job, daemon=True).start()

        # -------------------
    # Extract ISO
    # -------------------
    def on_extract(self):
        iso_path = filedialog.askopenfilename(
            title="Seleccionar archivo ISO",
            filetypes=[("Xbox360 ISO", "*.iso"), ("Todos los archivos", "*.*")]
        )
        if not iso_path:
            return

        self.set_status("Extrayendo ISO…")
        self.log(f"Iniciando extracción de {iso_path}")

        def job():
            from core.extractor import extract_iso, list_xex_files
            result = extract_iso(iso_path, log=self.log)
            if result:
                # Mostrar carpeta final
                self.log(f"✅ Extracción completada en: {result}")

                # Listar .xex encontrados
                xex_files = list_xex_files(result)
                if xex_files:
                    self.log("📄 Archivos XEX encontrados:")
                    for xf in xex_files:
                        self.log(f" - {xf}")
                else:
                    self.log("⚠️ No se encontraron archivos .xex")
            else:
                self.log("❌ Error en extracción")

            self.set_status("Esperando acción")

        threading.Thread(target=job, daemon=True).start()

    # -------------------
    # Analyse XEX
    # -------------------
    def on_analyse(self):
        xex_path = filedialog.askopenfilename(
            title="Seleccionar archivo XEX",
            filetypes=[("Xbox360 XEX", "*.xex"), ("Todos los archivos", "*.*")]
        )
        if not xex_path:
            return

        self.set_status("Analizando XEX…")
        self.log(f"Iniciando análisis de {xex_path}")

        def job():
            base_tmp = tempfile.gettempdir()
            output_dir = os.path.join(base_tmp, "x360dump", "gamefiles")

            result = analyse_xex(xex_path, out_dir=output_dir)
            if result:
                self.log(f"✅ Análisis completado → {result}")
            else:
                self.log("❌ Error en análisis")
            self.set_status("Esperando acción")

        threading.Thread(target=job, daemon=True).start()


def main():
    root = tk.Tk()
    app = LauncherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
