# 🧪 Guía de Pruebas

Guía para escribir y ejecutar tests.

---

## 🚀 Ejecutar Tests

```bash
# Todos los tests
pytest

# Con output verboso
pytest -v

# Con cobertura
pytest --cov=src --cov-report=html

# Solo tests específicos
pytest tests/unit/test_extractor.py
pytest -k "test_extract"
```

---

## 📁 Estructura de Tests

```
tests/
├── conftest.py         # Fixtures globales
├── unit/               # Tests unitarios
│   ├── test_dumper.py
│   ├── test_extractor.py
│   ├── test_analyser.py
│   └── ...
└── integration/        # Tests de integración
    └── test_pipeline.py
```

---

## ✍️ Escribir Tests

### Test unitario básico

```python
# tests/unit/test_extractor.py
import pytest
from src.core.extractor import list_xex_files

def test_list_xex_files_empty_dir(tmp_path):
    """Verifica que retorna lista vacía si no hay XEX."""
    result = list_xex_files(str(tmp_path))
    assert result == []

def test_list_xex_files_finds_xex(tmp_path):
    """Verifica que encuentra archivos .xex."""
    # Crear archivo de prueba
    xex_file = tmp_path / "test.xex"
    xex_file.write_bytes(b"fake xex")
    
    result = list_xex_files(str(tmp_path))
    
    assert len(result) == 1
    assert "test.xex" in result[0]
```

### Usar fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_xex(tmp_path):
    """Crea un XEX de prueba."""
    xex = tmp_path / "default.xex"
    xex.write_bytes(b"fake xex content")
    return str(xex)

# tests/unit/test_analyser.py
def test_analyse_missing_xex():
    """Verifica error con XEX inexistente."""
    with pytest.raises(FileNotFoundError):
        analyse_xex("no_existe.xex")
```

### Mocking de herramientas externas

```python
from unittest.mock import patch, MagicMock

def test_dump_disc_calls_tool():
    """Verifica que llama a DiscImageCreator."""
    with patch('subprocess.Popen') as mock_popen:
        mock_popen.return_value.stdout = iter(["OK"])
        mock_popen.return_value.wait.return_value = 0
        
        from src.core.dumper import dump_disc
        result = dump_disc("E:")
        
        mock_popen.assert_called_once()
```

---

## 🏷️ Convenciones

### Nombres de tests

```python
def test_<función>_<escenario>_<resultado_esperado>():
    pass

# Ejemplos:
def test_extract_iso_with_valid_iso_returns_path():
def test_clean_xex_with_encrypted_file_decrypts():
def test_analyse_xex_with_missing_file_raises_error():
```

### Marcadores

```python
@pytest.mark.slow
def test_full_pipeline():
    """Test lento, salta con pytest -m "not slow"."""
    pass

@pytest.mark.skip(reason="Requiere disco físico")
def test_real_dump():
    pass
```

---

## 📊 Cobertura

### Generar reporte

```bash
pytest --cov=src --cov-report=html
# Abre htmlcov/index.html en navegador
```

### Objetivo de cobertura

- **Mínimo**: 60%
- **Objetivo**: 80%+

---

## 📚 Ver también

- [DESARROLLO.md](./DESARROLLO.md)
- [CONTRIBUIR.md](./CONTRIBUIR.md)
