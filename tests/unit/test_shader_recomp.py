# tests/unit/test_shader_recomp.py
"""
Tests unitarios para el módulo shader_recomp.
"""
import pytest
from unittest.mock import patch, MagicMock
import os
import tempfile

from core.shader_recomp import (
    RecompResult,
    run_recompilation,
    validate_recomp_output,
    check_xenon_recomp_available,
    get_recomp_version,
    _find_generated_files
)


class TestRecompResult:
    """Tests para la dataclass RecompResult."""
    
    def test_default_values(self):
        """Verifica valores por defecto."""
        result = RecompResult(success=True)
        
        assert result.success is True
        assert result.output_dir is None
        assert result.cpp_files == []
        assert result.header_files == []
        assert result.error is None
        assert result.return_code == 0
    
    def test_with_values(self):
        """Verifica RecompResult con valores."""
        result = RecompResult(
            success=True,
            output_dir="/path/to/output",
            cpp_files=["file1.cpp", "file2.cpp"],
            header_files=["header.h"],
            return_code=0
        )
        
        assert result.success is True
        assert result.output_dir == "/path/to/output"
        assert len(result.cpp_files) == 2
        assert len(result.header_files) == 1
    
    def test_failed_result(self):
        """Verifica resultado de fallo."""
        result = RecompResult(
            success=False,
            error="XenonRecomp not found",
            return_code=1
        )
        
        assert result.success is False
        assert result.error == "XenonRecomp not found"


class TestCheckXenonRecompAvailable:
    """Tests para check_xenon_recomp_available."""
    
    @patch('core.shader_recomp.os.path.isfile')
    def test_available(self, mock_isfile):
        """Verifica detección cuando está disponible."""
        mock_isfile.return_value = True
        
        assert check_xenon_recomp_available() is True
    
    @patch('core.shader_recomp.os.path.isfile')
    def test_not_available(self, mock_isfile):
        """Verifica detección cuando no está disponible."""
        mock_isfile.return_value = False
        
        assert check_xenon_recomp_available() is False


class TestRunRecompilation:
    """Tests para run_recompilation."""
    
    @patch('core.shader_recomp.check_xenon_recomp_available')
    def test_xenon_not_available(self, mock_check):
        """Verifica error cuando XenonRecomp no está disponible."""
        mock_check.return_value = False
        
        result = run_recompilation("/path/to/project.toml")
        
        assert result.success is False
        assert "no encontrado" in result.error
    
    @patch('core.shader_recomp.check_xenon_recomp_available')
    def test_toml_not_found(self, mock_check):
        """Verifica error cuando TOML no existe."""
        mock_check.return_value = True
        
        result = run_recompilation("/nonexistent/project.toml")
        
        assert result.success is False
        assert "TOML no encontrado" in result.error
    
    @patch('core.shader_recomp.subprocess.run')
    @patch('core.shader_recomp.os.path.isfile')
    @patch('core.shader_recomp.check_xenon_recomp_available')
    def test_successful_recompilation(self, mock_check, mock_isfile, mock_run):
        """Verifica recompilación exitosa."""
        mock_check.return_value = True
        mock_isfile.return_value = True
        
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "Success"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = os.path.join(tmpdir, "project.toml")
            with open(toml_path, "w") as f:
                f.write("[project]\n")
            
            result = run_recompilation(toml_path, output_dir=tmpdir)
            
            assert result.success is True
            assert result.return_code == 0
    
    @patch('core.shader_recomp.subprocess.run')
    @patch('core.shader_recomp.os.path.isfile')
    @patch('core.shader_recomp.check_xenon_recomp_available')
    def test_failed_recompilation(self, mock_check, mock_isfile, mock_run):
        """Verifica manejo de fallo en recompilación."""
        mock_check.return_value = True
        mock_isfile.return_value = True
        
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Error"
        mock_run.return_value = mock_result
        
        with tempfile.TemporaryDirectory() as tmpdir:
            toml_path = os.path.join(tmpdir, "project.toml")
            with open(toml_path, "w") as f:
                f.write("[project]\n")
            
            result = run_recompilation(toml_path, output_dir=tmpdir)
            
            assert result.success is False
            assert result.return_code == 1
    
    def test_with_logging(self):
        """Verifica que la función de log se llama."""
        log_messages = []
        
        def mock_log(msg):
            log_messages.append(msg)
        
        with patch('core.shader_recomp.check_xenon_recomp_available', return_value=False):
            run_recompilation("/fake/path.toml", log=mock_log)
        
        assert len(log_messages) > 0
        assert any("XenonRecomp" in msg for msg in log_messages)


class TestFindGeneratedFiles:
    """Tests para _find_generated_files."""
    
    def test_find_cpp_files(self):
        """Verifica búsqueda de archivos .cpp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Crear archivos de prueba
            open(os.path.join(tmpdir, "main.cpp"), "w").close()
            open(os.path.join(tmpdir, "utils.cpp"), "w").close()
            open(os.path.join(tmpdir, "header.h"), "w").close()
            
            cpp_files, header_files = _find_generated_files(tmpdir)
            
            assert len(cpp_files) == 2
            assert len(header_files) == 1
    
    def test_empty_directory(self):
        """Verifica directorio vacío."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cpp_files, header_files = _find_generated_files(tmpdir)
            
            assert cpp_files == []
            assert header_files == []


class TestValidateRecompOutput:
    """Tests para validate_recomp_output."""
    
    def test_valid_output(self):
        """Verifica validación con archivos .cpp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "main.cpp"), "w").close()
            
            success, files = validate_recomp_output(tmpdir)
            
            assert success is True
            assert len(files) == 1
    
    def test_invalid_output_no_cpp(self):
        """Verifica validación sin archivos .cpp."""
        with tempfile.TemporaryDirectory() as tmpdir:
            open(os.path.join(tmpdir, "readme.txt"), "w").close()
            
            success, files = validate_recomp_output(tmpdir)
            
            assert success is False
    
    def test_nonexistent_directory(self):
        """Verifica manejo de directorio inexistente."""
        success, files = validate_recomp_output("/nonexistent/path")
        
        assert success is False
        assert files == []
