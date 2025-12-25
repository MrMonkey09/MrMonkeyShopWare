# tests/conftest.py
"""
Configuración de pytest para MrMonkeyShopWare.
"""
import pytest
import sys
from pathlib import Path

# Añadir src al path para imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture que proporciona un directorio temporal."""
    return tmp_path


@pytest.fixture
def sample_xex_path():
    """Fixture que proporciona una ruta de ejemplo para XEX (mock)."""
    return "C:\\test\\default.xex"


@pytest.fixture
def sample_iso_path():
    """Fixture que proporciona una ruta de ejemplo para ISO (mock)."""
    return "C:\\test\\game.iso"
