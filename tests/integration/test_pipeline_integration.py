# tests/integration/test_pipeline_integration.py
"""
Tests de integración para el pipeline.
Usa mocks de herramientas externas para portabilidad.
"""
import os
import pytest
from unittest.mock import patch, MagicMock
from core.pipeline import full_pipeline


@pytest.fixture
def mock_external_tools(tmp_path):
    """
    Fixture que mockea todas las herramientas externas.
    Simula un flujo exitoso completo.
    """
    extracted_dir = tmp_path / "extracted"
    extracted_dir.mkdir()
    
    # Crear XEX fake
    xex_file = extracted_dir / "default.xex"
    xex_file.touch()
    
    # Crear archivos de análisis
    analysis_dir = tmp_path / "analysis"
    analysis_dir.mkdir()
    json_file = analysis_dir / "analysis.json"
    json_file.write_text("{}")
    toml_file = analysis_dir / "analysis.toml"
    toml_file.write_text("")
    
    # Crear project.toml
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    project_toml = project_dir / "project.toml"
    project_toml.write_text("[project]\ntitle_id = '00000000'")
    
    return {
        "tmp_path": tmp_path,
        "extracted_dir": str(extracted_dir),
        "xex_file": str(xex_file),
        "json_file": str(json_file),
        "toml_file": str(toml_file),
        "project_toml": str(project_toml),
    }


class TestPipelineFromDrive:
    """Tests de pipeline desde disco físico (con mocks)."""
    
    @patch('core.pipeline.generate_project_toml')
    @patch('core.pipeline.analyse_xex')
    @patch('core.pipeline.list_xex_files')
    @patch('core.pipeline.extract_iso')
    @patch('core.pipeline.dump_disc')
    def test_full_pipeline_from_drive(
        self,
        mock_dump,
        mock_extract,
        mock_list_xex,
        mock_analyse,
        mock_toml,
        mock_external_tools,
        tmp_path
    ):
        """Test completo desde disco."""
        # Setup mocks
        iso_path = str(tmp_path / "game.iso")
        with open(iso_path, "w") as f:
            f.write("")
        
        mock_dump.return_value = True
        mock_extract.return_value = mock_external_tools["extracted_dir"]
        mock_list_xex.return_value = [mock_external_tools["xex_file"]]
        mock_analyse.return_value = (
            mock_external_tools["json_file"],
            mock_external_tools["toml_file"]
        )
        mock_toml.return_value = mock_external_tools["project_toml"]
        
        # Ejecutar pipeline
        result = full_pipeline(
            drive_letter="E:",
            output_dir=str(tmp_path / "output")
        )
        
        # Verificar
        assert result.success is True
        assert "dump" in result.steps_completed
        assert "extract" in result.steps_completed
        assert "analyse" in result.steps_completed
        assert "toml" in result.steps_completed
        
        mock_dump.assert_called_once()
        mock_extract.assert_called_once()
        mock_analyse.assert_called_once()
        mock_toml.assert_called_once()


class TestPipelineFromISO:
    """Tests de pipeline desde ISO."""
    
    @patch('core.pipeline.generate_project_toml')
    @patch('core.pipeline.analyse_xex')
    @patch('core.pipeline.list_xex_files')
    @patch('core.pipeline.extract_iso')
    def test_full_pipeline_from_iso(
        self,
        mock_extract,
        mock_list_xex,
        mock_analyse,
        mock_toml,
        mock_external_tools,
        tmp_path
    ):
        """Test pipeline desde ISO existente."""
        mock_extract.return_value = mock_external_tools["extracted_dir"]
        mock_list_xex.return_value = [mock_external_tools["xex_file"]]
        mock_analyse.return_value = (
            mock_external_tools["json_file"],
            mock_external_tools["toml_file"]
        )
        mock_toml.return_value = mock_external_tools["project_toml"]
        
        result = full_pipeline(
            iso_path="/fake/game.iso",
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is True
        assert "dump" not in result.steps_completed
        assert "extract" in result.steps_completed
        assert "analyse" in result.steps_completed
        assert "toml" in result.steps_completed


class TestPipelineFromXEX:
    """Tests de pipeline desde XEX."""
    
    @patch('core.pipeline.generate_project_toml')
    @patch('core.pipeline.analyse_xex')
    def test_full_pipeline_from_xex(
        self,
        mock_analyse,
        mock_toml,
        mock_external_tools,
        tmp_path
    ):
        """Test pipeline desde XEX existente."""
        mock_analyse.return_value = (
            mock_external_tools["json_file"],
            mock_external_tools["toml_file"]
        )
        mock_toml.return_value = mock_external_tools["project_toml"]
        
        result = full_pipeline(
            xex_path=mock_external_tools["xex_file"],
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is True
        assert "dump" not in result.steps_completed
        assert "extract" not in result.steps_completed
        assert "analyse" in result.steps_completed
        assert "toml" in result.steps_completed
        assert result.main_xex == mock_external_tools["xex_file"]


class TestPipelineErrorHandling:
    """Tests de manejo de errores."""
    
    @patch('core.pipeline.extract_iso')
    def test_handles_no_xex_found(self, mock_extract, tmp_path):
        """Verifica manejo cuando no se encuentra XEX."""
        # Crear directorio vacío (sin XEX)
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        mock_extract.return_value = str(empty_dir)
        
        result = full_pipeline(
            iso_path="/fake/game.iso",
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is False
        assert "xex" in result.error.lower()
    
    @patch('core.pipeline.analyse_xex')
    def test_handles_analysis_failure(self, mock_analyse, tmp_path):
        """Verifica manejo cuando análisis falla."""
        # Crear XEX fake
        xex_file = tmp_path / "test.xex"
        xex_file.touch()
        
        mock_analyse.return_value = None
        
        result = full_pipeline(
            xex_path=str(xex_file),
            output_dir=str(tmp_path / "output")
        )
        
        assert result.success is False
        assert result.error is not None
