import win32file

def get_drives_with_types():
    """
    Devuelve un diccionario con las unidades disponibles y su tipo.
    Ejemplo:
        {
            'C:\\': DRIVE_FIXED,
            'D:\\': DRIVE_CDROM,
            'E:\\': DRIVE_REMOVABLE
        }
    """

    drives = {}
    bitmask = win32file.GetLogicalDrives()

    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        if bitmask & 1:
            drive = f"{letter}:\\"
            try:
                dtype = win32file.GetDriveType(drive)
                drives[drive] = dtype
            except Exception:
                # ignorar errores en unidades inaccesibles
                pass
        bitmask >>= 1

    return drives
