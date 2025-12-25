# core/pipeline.py
"""
Pipeline automatizado para Xbox 360.
Encadena: dump → extracción → análisis → generación TOML
Ahora con auto-guardado en base de datos.
"""
import os
import json
from dataclasses import dataclass, field
from typing import Callable, Optional

from core.dumper import dump_disc
from core.extractor import extract_iso, list_xex_files
from core.analyser import analyse_xex, AnalysisResult
from core.toml_generator import generate_project_toml
from core.config import TEMP_BASE
from core.database import GameDatabase, Game, GameStatus
from core.xex_parser import XexInfo


@dataclass
class PipelineResult:
    """Resultado estructurado del pipeline."""
    success: bool
    iso_path: Optional[str] = None
    extracted_dir: Optional[str] = None
    main_xex: Optional[str] = None
    analysis_json: Optional[str] = None
    analysis_toml: Optional[str] = None
    project_toml: Optional[str] = None
    error: Optional[str] = None
    steps_completed: list = field(default_factory=list)
    xex_info: Optional[XexInfo] = None  # Metadata del juego detectado
    game_id: Optional[int] = None  # ID del juego en BD


def find_main_xex(extracted_dir: str) -> Optional[str]:
    """
    Encuentra el XEX principal en un directorio extraído.
    
    Prioridad:
    1. default.xex (ejecutable principal típico)
    2. Primer .xex encontrado
    
    :param extracted_dir: Directorio con contenido extraído del ISO
    :return: Ruta absoluta al XEX o None si no hay ninguno
    """
    xex_files = list_xex_files(extracted_dir)
    
    if not xex_files:
        return None
    
    # Buscar default.xex primero
    for xex in xex_files:
        if os.path.basename(xex).lower() == "default.xex":
            return xex
    
    # Fallback: primer XEX encontrado
    return xex_files[0]


def full_pipeline(
    drive_letter: Optional[str] = None,
    iso_path: Optional[str] = None,
    xex_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    log: Optional[Callable[[str], None]] = None
) -> PipelineResult:
    """
    Pipeline completo que encadena dump → extract → analyse → toml.
    
    Modos de uso (mutuamente excluyentes, en orden de prioridad):
    - drive_letter: Inicia desde disco físico (dump + extract + analyse + toml)
    - iso_path: Inicia desde ISO existente (extract + analyse + toml)
    - xex_path: Inicia desde XEX existente (analyse + toml)
    
    :param drive_letter: Letra de unidad óptica (ej: "E:")
    :param iso_path: Ruta a archivo ISO existente
    :param xex_path: Ruta a archivo XEX existente
    :param output_dir: Directorio de salida (si no se especifica, usa temp)
    :param log: Función de logging opcional
    :return: PipelineResult con resultados y estado
    """
    _log = log if log else print
    result = PipelineResult(success=False)
    
    # Validar que al menos un parámetro fue proporcionado
    if not any([drive_letter, iso_path, xex_path]):
        result.error = "Debe proporcionar drive_letter, iso_path o xex_path"
        _log(f"❌ {result.error}")
        return result
    
    # Configurar directorio de salida
    if output_dir is None:
        output_dir = os.path.join(TEMP_BASE, "pipeline_output")
    os.makedirs(output_dir, exist_ok=True)
    
    _log(f"📁 Directorio de salida: {output_dir}")
    
    # ══════════════════════════════════════════════════════════════
    # PASO 1: Dump (solo si se proporciona drive_letter)
    # ══════════════════════════════════════════════════════════════
    if drive_letter:
        _log(f"\n{'═'*50}")
        _log(f"📀 PASO 1: Dump desde unidad {drive_letter}")
        _log(f"{'═'*50}")
        
        iso_out = os.path.join(output_dir, "game.iso")
        dump_result = dump_disc(drive_letter, out_path=iso_out)
        
        if not dump_result:
            result.error = f"Error en dump desde {drive_letter}"
            _log(f"❌ {result.error}")
            return result
        
        result.iso_path = iso_out
        result.steps_completed.append("dump")
        _log(f"✅ Dump completado: {iso_out}")
        
        # Ahora usamos el ISO generado
        iso_path = iso_out
    
    # ══════════════════════════════════════════════════════════════
    # PASO 2: Extracción (si tenemos ISO)
    # ══════════════════════════════════════════════════════════════
    if iso_path:
        _log(f"\n{'═'*50}")
        _log(f"📂 PASO 2: Extracción de {os.path.basename(iso_path)}")
        _log(f"{'═'*50}")
        
        extract_out = os.path.join(output_dir, "extracted")
        extracted_dir = extract_iso(iso_path, output_dir=extract_out, log=_log)
        
        if not extracted_dir:
            result.error = f"Error extrayendo {iso_path}"
            _log(f"❌ {result.error}")
            return result
        
        result.extracted_dir = extracted_dir
        result.steps_completed.append("extract")
        _log(f"✅ Extracción completada: {extracted_dir}")
        
        # Buscar XEX principal
        main_xex = find_main_xex(extracted_dir)
        if not main_xex:
            result.error = "No se encontró ningún archivo .xex"
            _log(f"❌ {result.error}")
            return result
        
        result.main_xex = main_xex
        _log(f"🎮 XEX principal: {os.path.basename(main_xex)}")
        
        # Ahora usamos el XEX encontrado
        xex_path = main_xex
    
    # ══════════════════════════════════════════════════════════════
    # PASO 3: Análisis XEX
    # ══════════════════════════════════════════════════════════════
    if xex_path:
        _log(f"\n{'═'*50}")
        _log(f"🔬 PASO 3: Análisis de {os.path.basename(xex_path)}")
        _log(f"{'═'*50}")
        
        # Si no tenemos main_xex guardado, guardamos este
        if not result.main_xex:
            result.main_xex = xex_path
        
        analysis_dir = os.path.join(output_dir, "analysis")
        analysis_result = analyse_xex(xex_path, out_dir=analysis_dir, log=_log)
        
        if not analysis_result or not analysis_result.success:
            result.error = f"Error analizando {xex_path}"
            _log(f"❌ {result.error}")
            return result
        
        # Extraer resultados del AnalysisResult
        result.analysis_json = analysis_result.json_file
        result.analysis_toml = analysis_result.toml_file
        result.xex_info = analysis_result.xex_info
        result.steps_completed.append("analyse")
        
        _log(f"   📄 JSON: {analysis_result.json_file}")
        _log(f"   📄 TOML: {analysis_result.toml_file}")
        
        # ══════════════════════════════════════════════════════════
        # PASO 4: Generar project.toml
        # ══════════════════════════════════════════════════════════
        _log(f"\n{'═'*50}")
        _log(f"📝 PASO 4: Generando project.toml")
        _log(f"{'═'*50}")
        
        project_dir = os.path.join(output_dir, "project")
        project_toml = generate_project_toml(xex_path, analysis_result.json_file, project_dir)
        
        result.project_toml = project_toml
        result.steps_completed.append("toml")
        _log(f"✅ project.toml generado: {project_toml}")
        
        # ══════════════════════════════════════════════════════════
        # PASO 5: Auto-guardar en Base de Datos
        # ══════════════════════════════════════════════════════════
        if result.xex_info and result.xex_info.title_id:
            _log(f"\n{'═'*50}")
            _log(f"💾 PASO 5: Guardando en Base de Datos")
            _log(f"{'═'*50}")
            
            try:
                xex_info = result.xex_info
                
                # Crear objeto Game con la metadata extraída
                game = Game(
                    title_id=xex_info.title_id,
                    game_name=xex_info.display_name or os.path.basename(xex_path).replace(".xex", ""),
                    status=GameStatus.ANALYSED,
                    iso_path=result.iso_path,
                    extracted_dir=result.extracted_dir,
                    xex_path=result.main_xex,
                    analysis_json=result.analysis_json,
                    project_toml=result.project_toml,
                    media_id=xex_info.media_id,
                    version=xex_info.version,
                    disc_number=xex_info.disc_number,
                    total_discs=xex_info.total_discs,
                    regions=xex_info.regions,
                    esrb_rating=xex_info.esrb_rating,
                    entry_point=xex_info.entry_point,
                    original_pe_name=xex_info.original_pe_name,
                    xex_info_json=json.dumps({
                        "static_libraries": xex_info.static_libraries[:10],
                        "is_retail": xex_info.is_retail,
                        "is_encrypted": xex_info.is_encrypted,
                        "load_address": xex_info.load_address,
                    })
                )
                
                # Guardar o actualizar en BD
                with GameDatabase() as db:
                    game_id = db.add_or_update_game(game)
                    result.game_id = game_id
                
                _log(f"✅ Juego guardado en BD con ID: {game_id}")
                _log(f"   🎮 {game.game_name} ({game.title_id})")
                
            except Exception as e:
                _log(f"⚠️ No se pudo guardar en BD: {e}")
    
    # ══════════════════════════════════════════════════════════════
    # FINALIZACIÓN
    # ══════════════════════════════════════════════════════════════
    result.success = True
    _log(f"\n{'═'*50}")
    _log(f"🎉 PIPELINE COMPLETADO EXITOSAMENTE")
    _log(f"{'═'*50}")
    _log(f"Pasos completados: {' → '.join(result.steps_completed)}")
    
    if result.game_id:
        _log(f"📚 Juego disponible en Historial (ID: {result.game_id})")
    
    return result
