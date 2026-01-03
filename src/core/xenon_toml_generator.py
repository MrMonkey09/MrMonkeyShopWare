# core/xenon_toml_generator.py
"""
Generador de archivos TOML para XenonRecomp.
Crea configuración en el formato correcto que espera XenonRecomp.
"""
import os
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, field


@dataclass
class XenonRecompConfig:
    """Configuración para XenonRecomp."""
    
    # Rutas principales
    xex_path: str
    output_dir: str = "ppc"
    switch_table_path: Optional[str] = None
    patch_file_path: Optional[str] = None
    
    # Direcciones de funciones r14 (obligatorias para muchos juegos)
    restgprlr_14: Optional[int] = None
    savegprlr_14: Optional[int] = None
    restfpr_14: Optional[int] = None
    savefpr_14: Optional[int] = None
    restvmx_14: Optional[int] = None
    savevmx_14: Optional[int] = None
    restvmx_64: Optional[int] = None
    savevmx_64: Optional[int] = None
    
    # setjmp/longjmp (opcional)
    setjmp_address: Optional[int] = None
    longjmp_address: Optional[int] = None
    
    # Optimizaciones (habilitar después de funcionamiento básico)
    skip_lr: bool = False
    skip_msr: bool = False
    ctr_as_local: bool = False
    xer_as_local: bool = False
    reserved_as_local: bool = False
    cr_as_local: bool = False
    non_argument_as_local: bool = False
    non_volatile_as_local: bool = False
    
    # Funciones manuales
    functions: List[Dict[str, int]] = field(default_factory=list)
    
    # Instrucciones inválidas a saltar
    invalid_instructions: List[Dict[str, int]] = field(default_factory=list)
    
    # Mid-asm hooks
    midasm_hooks: List[Dict[str, Any]] = field(default_factory=list)


def generate_xenon_toml(
    config: XenonRecompConfig,
    output_path: str,
    log=None
) -> str:
    """
    Genera un archivo TOML en el formato correcto para XenonRecomp.
    
    :param config: Configuración del recompilador
    :param output_path: Ruta donde guardar el TOML
    :param log: Función de logging
    :return: Ruta al archivo generado
    """
    
    # Usar rutas relativas con / (Unix style como espera XenonRecomp)
    def to_relative(path: str, base: str) -> str:
        try:
            rel = os.path.relpath(path, base)
            return rel.replace("\\", "/")
        except ValueError:
            return path.replace("\\", "/")
    
    base_dir = os.path.dirname(output_path)
    os.makedirs(base_dir, exist_ok=True)
    
    lines = [
        "# XenonRecomp Configuration",
        "# Generado por MrMonkeyShopWare",
        "",
        "[main]"
    ]
    
    # Rutas principales
    lines.append(f'file_path = "{to_relative(config.xex_path, base_dir)}"')
    
    if config.patch_file_path:
        lines.append(f'patch_file_path = "{to_relative(config.patch_file_path, base_dir)}"')
    
    lines.append(f'out_directory_path = "{config.output_dir}"')
    
    if config.switch_table_path:
        lines.append(f'switch_table_file_path = "{to_relative(config.switch_table_path, base_dir)}"')
    
    # Optimizaciones
    lines.extend([
        "",
        "# ═══════════════════════════════════════════════════════",
        "# OPTIMIZACIONES",
        "# NOTA: Habilitar solo después de que funcione básico",
        "# ═══════════════════════════════════════════════════════"
    ])
    
    lines.append(f"skip_lr = {str(config.skip_lr).lower()}")
    lines.append(f"skip_msr = {str(config.skip_msr).lower()}")
    lines.append(f"ctr_as_local = {str(config.ctr_as_local).lower()}")
    lines.append(f"xer_as_local = {str(config.xer_as_local).lower()}")
    lines.append(f"reserved_as_local = {str(config.reserved_as_local).lower()}")
    lines.append(f"cr_as_local = {str(config.cr_as_local).lower()}")
    lines.append(f"non_argument_as_local = {str(config.non_argument_as_local).lower()}")
    lines.append(f"non_volatile_as_local = {str(config.non_volatile_as_local).lower()}")
    
    # Direcciones de funciones r14
    lines.extend([
        "",
        "# ═══════════════════════════════════════════════════════",
        "# DIRECCIONES DE FUNCIONES DE REGISTRO (r14)",
        "# Buscar con Binary Ninja/IDA/Ghidra si no se detectan",
        "# ═══════════════════════════════════════════════════════"
    ])
    
    if config.restgprlr_14:
        lines.append(f"restgprlr_14_address = 0x{config.restgprlr_14:08X}")
    else:
        lines.append("# restgprlr_14_address = 0x00000000")
    
    if config.savegprlr_14:
        lines.append(f"savegprlr_14_address = 0x{config.savegprlr_14:08X}")
    else:
        lines.append("# savegprlr_14_address = 0x00000000")
    
    if config.restfpr_14:
        lines.append(f"restfpr_14_address = 0x{config.restfpr_14:08X}")
    else:
        lines.append("# restfpr_14_address = 0x00000000")
    
    if config.savefpr_14:
        lines.append(f"savefpr_14_address = 0x{config.savefpr_14:08X}")
    else:
        lines.append("# savefpr_14_address = 0x00000000")
    
    if config.restvmx_14:
        lines.append(f"restvmx_14_address = 0x{config.restvmx_14:08X}")
    else:
        lines.append("# restvmx_14_address = 0x00000000")
    
    if config.savevmx_14:
        lines.append(f"savevmx_14_address = 0x{config.savevmx_14:08X}")
    else:
        lines.append("# savevmx_14_address = 0x00000000")
    
    if config.restvmx_64:
        lines.append(f"restvmx_64_address = 0x{config.restvmx_64:08X}")
    else:
        lines.append("# restvmx_64_address = 0x00000000")
    
    if config.savevmx_64:
        lines.append(f"savevmx_64_address = 0x{config.savevmx_64:08X}")
    else:
        lines.append("# savevmx_64_address = 0x00000000")
    
    # setjmp/longjmp
    lines.extend([
        "",
        "# ═══════════════════════════════════════════════════════",
        "# SETJMP/LONGJMP (solo si el juego los usa)",
        "# ═══════════════════════════════════════════════════════"
    ])
    
    if config.longjmp_address:
        lines.append(f"longjmp_address = 0x{config.longjmp_address:08X}")
    else:
        lines.append("# longjmp_address = 0x00000000")
    
    if config.setjmp_address:
        lines.append(f"setjmp_address = 0x{config.setjmp_address:08X}")
    else:
        lines.append("# setjmp_address = 0x00000000")
    
    # Funciones manuales
    if config.functions:
        lines.extend([
            "",
            "# ═══════════════════════════════════════════════════════",
            "# FUNCIONES MANUALES (para jump tables no detectadas)",
            "# ═══════════════════════════════════════════════════════",
            "functions = ["
        ])
        for func in config.functions:
            lines.append(f'    {{ address = 0x{func["address"]:08X}, size = 0x{func["size"]:X} }},')
        lines.append("]")
    else:
        lines.extend([
            "",
            "# functions = [",
            "#     { address = 0x00000000, size = 0x00 },",
            "# ]"
        ])
    
    # Instrucciones inválidas
    if config.invalid_instructions:
        lines.extend([
            "",
            "# ═══════════════════════════════════════════════════════",
            "# INSTRUCCIONES INVÁLIDAS A IGNORAR",
            "# ═══════════════════════════════════════════════════════",
            "invalid_instructions = ["
        ])
        for instr in config.invalid_instructions:
            lines.append(f'    {{ data = 0x{instr["data"]:08X}, size = {instr["size"]} }},')
        lines.append("]")
    else:
        lines.extend([
            "",
            "# invalid_instructions = [",
            "#     { data = 0x00000000, size = 4 },  # Padding",
            "# ]"
        ])
    
    # Mid-asm hooks
    if config.midasm_hooks:
        lines.extend([
            "",
            "# ═══════════════════════════════════════════════════════",
            "# MID-ASM HOOKS",
            "# ═══════════════════════════════════════════════════════"
        ])
        for hook in config.midasm_hooks:
            lines.append("")
            lines.append("[[midasm_hook]]")
            lines.append(f'name = "{hook["name"]}"')
            lines.append(f'address = 0x{hook["address"]:08X}')
            if "registers" in hook:
                regs = ', '.join(f'"{r}"' for r in hook["registers"])
                lines.append(f"registers = [{regs}]")
    else:
        lines.extend([
            "",
            "# ═══════════════════════════════════════════════════════",
            "# MID-ASM HOOKS (para insertar código custom)",
            "# ═══════════════════════════════════════════════════════",
            "# [[midasm_hook]]",
            '# name = "MyHook"',
            "# address = 0x00000000",
            '# registers = ["r3"]'
        ])
    
    # Escribir archivo
    content = "\n".join(lines)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    if log:
        log(f"✅ TOML generado: {output_path}")
    
    return output_path


def generate_default_config(
    xex_path: str,
    output_dir: str,
    analysis_toml: Optional[str] = None,
    patch_path: Optional[str] = None,
    log=None
) -> str:
    """
    Genera un TOML con configuración por defecto para un juego.
    
    :param xex_path: Ruta al XEX del juego
    :param output_dir: Directorio de salida
    :param analysis_toml: Ruta al TOML de análisis (jump tables)
    :param patch_path: Ruta al parche .xexp (opcional)
    :param log: Función de logging
    :return: Ruta al TOML generado
    """
    config = XenonRecompConfig(
        xex_path=xex_path,
        output_dir="ppc",
        switch_table_path=analysis_toml,
        patch_file_path=patch_path,
        # Instrucciones inválidas por defecto
        invalid_instructions=[
            {"data": 0x00000000, "size": 4},  # Padding
        ]
    )
    
    toml_path = os.path.join(output_dir, "config.toml")
    
    return generate_xenon_toml(config, toml_path, log)


def update_toml_with_r14_addresses(
    toml_path: str,
    r14_addresses: Dict[str, int],
    log=None
) -> bool:
    """
    Actualiza un TOML existente con direcciones r14 detectadas.
    
    :param toml_path: Ruta al TOML
    :param r14_addresses: Diccionario con direcciones
    :param log: Función de logging
    :return: True si se actualizó correctamente
    """
    import re
    
    if not os.path.isfile(toml_path):
        if log:
            log(f"❌ TOML no encontrado: {toml_path}")
        return False
    
    with open(toml_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Mapeo de nombres
    address_map = {
        "restgprlr_14": "restgprlr_14_address",
        "savegprlr_14": "savegprlr_14_address",
        "restfpr_14": "restfpr_14_address",
        "savefpr_14": "savefpr_14_address",
        "restvmx_14": "restvmx_14_address",
        "savevmx_14": "savevmx_14_address",
        "restvmx_64": "restvmx_64_address",
        "savevmx_64": "savevmx_64_address",
        "longjmp": "longjmp_address",
        "setjmp": "setjmp_address",
    }
    
    updated = False
    for key, addr in r14_addresses.items():
        toml_key = address_map.get(key, f"{key}_address")
        
        # Buscar línea comentada y descomentarla
        pattern = rf"#\s*{toml_key}\s*=\s*0x[0-9A-Fa-f]+"
        replacement = f"{toml_key} = 0x{addr:08X}"
        
        new_content, count = re.subn(pattern, replacement, content)
        if count > 0:
            content = new_content
            updated = True
            if log:
                log(f"📝 Actualizado {toml_key} = 0x{addr:08X}")
        else:
            # Buscar línea existente y actualizarla
            pattern = rf"{toml_key}\s*=\s*0x[0-9A-Fa-f]+"
            new_content, count = re.subn(pattern, replacement, content)
            if count > 0:
                content = new_content
                updated = True
    
    if updated:
        with open(toml_path, "w", encoding="utf-8") as f:
            f.write(content)
        if log:
            log(f"✅ TOML actualizado: {toml_path}")
    
    return updated
