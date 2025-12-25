# tests/unit/test_pipeline.py
"""
Tests unitarios para el módulo pipeline.
"""
import os
import pytest
from unittest.mock import Mock, patch, MagicMock
from core.pipeline import (
    PipelineResult,
    find_main_xex,
    full_pipeline
)


class TestPipelineResult:
    """Tests para la dataclass PipelineResult."""
    
    def test_default_values(self):
        """Verifica valores por defecto de PipelineResult."""
        result = PipelineResult(success=False)
        
        assert result.success is False
        assert result.iso_path is None
        assert result.extracted_dir is None
        assert result.main_xex is None
        assert result.analysis_json is None
        assert result.analysis_toml is None
        assert result.project_toml is None
        assert result.error is None
        assert result.steps_completed == []
    
    def test_with_values(self):
        """Verifica PipelineResult con valores."""
        result = PipelineResult(
            success=True,
            iso_path="/path/to/game.iso",
            main_xex="/path/to/default.xex",
            steps_completed=["dump", "extract"]
        )
        
        assert result.success is True
        assert result.iso_path == "/path/to/game.iso"
        assert result.main_xex == "/path/to/default.xex"
        assert "dump" in result.steps_completed


class TestFindMainXex:
    """Tests para find_main_xex."""
    
    def test_finds_default_xex(self, tmp_path):
        """Verifica que encuentra default.xex."""
        # Crear estructura de archivos
        xex_dir = tmp_path / "extracted"
        xex_dir.mkdir()
        (xex_dir / "default.xex").touch()
        (xex_dir / "other.xex").touch()
        
        result = find_main_xex(str(xex_dir))
        
        assert result is not None
        assert os.path.basename(result).lower() == "default.xex"
    
    def test_fallback_to_first_xex(self, tmp_path):
        """Verifica fallback al primer XEX cuando no hay default.xex."""
        xex_dir = tmp_path / "extracted"
        xex_dir.mkdir()
        (xex_dir / "game.xex").touch()
        
        result = find_main_xex(str(xex_dir))
        
        assert result is not None
        assert result.endswith(".xex")
    
    def test_returns_none_when_no_xex(self, tmp_path):
        """Verifica que retorna None si no hay archivos XEX."""
        xex_dir = tmp_path / "extracted"
        xex_dir.mkdir()
        (xex_dir / "readme.txt").touch()
        
        result = find_main_xex(str(xex_dir))
        
        assert result is None


class TestFullPipeline:
    """Tests para full_pipeline."""
    
    def test_no_params_returns_error(self):
        """Verifica error cuando no se pasan parámetros."""
        result = full_pipeline()
        
        assert result.success is False
        assert result.error is not None
        assert "Debe proporcionar" in result.error
    
    @patch('core.pipeline.dump_disc')
    def test_dump_failure_stops_pipeline(self, mock_dump):
        """Verifica que el pipeline se detiene si dump falla."""
        mock_dump.return_value = False
        
        result = full_pipeline(drive_letter="E:")
        
        assert result.success is False
        assert "dump" not in result.steps_completed
        mock_dump.assert_called_once()
    
    @patch('core.pipeline.extract_iso')
    def test_extract_failure_stops_pipeline(self, mock_extract):
        """Verifica que el pipeline se detiene si extract falla."""
        mock_extract.return_value = None
        
        result = full_pipeline(iso_path="/fake/game.iso")
        
        assert result.success is False
        assert "extract" not in result.steps_completed
    
    @patch('core.pipeline.generate_project_toml')
    @patch('core.pipeline.analyse_xex')
    def test_xex_mode_success(self, mock_analyse, mock_toml, tmp_path):
        """Verifica pipeline exitoso desde XEX."""
        # Crear archivo XEX fake
        xex_file = tmp_path / "default.xex"
        xex_file.touch()
        
        json_file = str(tmp_path / "analysis.json")
        toml_file = str(tmp_path / "analysis.toml")
        project_toml = str(tmp_path / "project.toml")
        
        mock_analyse.return_value = (json_file, toml_file)
        mock_toml.return_value = project_toml
        
        result = full_pipeline(
            xex_path=str(xex_file),
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is True
        assert "analyse" in result.steps_completed
        assert "toml" in result.steps_completed
    
    @patch('core.pipeline.list_xex_files')
    @patch('core.pipeline.generate_project_toml')
    @patch('core.pipeline.analyse_xex')
    @patch('core.pipeline.extract_iso')
    def test_iso_mode_success(
        self, mock_extract, mock_analyse, mock_toml, mock_list_xex, tmp_path
    ):
        """Verifica pipeline exitoso desde ISO."""
        # Setup mocks
        extracted_dir = str(tmp_path / "extracted")
        os.makedirs(extracted_dir)
        xex_file = os.path.join(extracted_dir, "default.xex")
        with open(xex_file, "w") as f:
            f.write("")
        
        mock_extract.return_value = extracted_dir
        mock_list_xex.return_value = [xex_file]
        mock_analyse.return_value = ("analysis.json", "analysis.toml")
        mock_toml.return_value = "project.toml"
        
        result = full_pipeline(
            iso_path="/fake/game.iso",
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is True
        assert "extract" in result.steps_completed


class TestPipelineLogging:
    """Tests para verificar que logging funciona."""
    
    def test_custom_log_function(self):
        """Verifica que se usa la función de log personalizada."""
        log_messages = []
        custom_log = lambda msg: log_messages.append(msg)
        
        result = full_pipeline(log=custom_log)
        
        # Debe haber mensajes de log aunque falle
        assert len(log_messages) > 0
