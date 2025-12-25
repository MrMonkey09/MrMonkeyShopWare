# tests/unit/test_logger.py
"""
Tests unitarios para el módulo logger.
"""
import pytest
import logging

from core.logger import (
    get_logger,
    GUILogHandler,
    ColoredFormatter,
    LOGGER_NAME
)


class TestGetLogger:
    """Tests para get_logger."""
    
    def test_get_main_logger(self):
        """Verifica obtención del logger principal."""
        logger = get_logger()
        assert logger.name == LOGGER_NAME
    
    def test_get_module_logger(self):
        """Verifica obtención de logger de módulo."""
        logger = get_logger("test_module")
        assert logger.name == f"{LOGGER_NAME}.test_module"


class TestGUILogHandler:
    """Tests para GUILogHandler."""
    
    def test_callback_called(self):
        """Verifica que el callback se llama."""
        messages = []
        handler = GUILogHandler(lambda m: messages.append(m))
        
        unique_logger = logging.getLogger("test_callback")
        unique_logger.handlers.clear()
        unique_logger.addHandler(handler)
        unique_logger.setLevel(logging.INFO)
        
        unique_logger.info("Test")
        
        assert len(messages) == 1
        assert "Test" in messages[0]
    
    def test_emoji_error(self):
        """Verifica emoji de error."""
        messages = []
        handler = GUILogHandler(lambda m: messages.append(m))
        
        unique_logger = logging.getLogger("test_emoji")
        unique_logger.handlers.clear()
        unique_logger.addHandler(handler)
        unique_logger.setLevel(logging.DEBUG)
        
        unique_logger.error("Fail")
        
        assert "❌" in messages[-1]
    
    def test_emoji_warning(self):
        """Verifica emoji de warning."""
        messages = []
        handler = GUILogHandler(lambda m: messages.append(m))
        
        unique_logger = logging.getLogger("test_warn")
        unique_logger.handlers.clear()
        unique_logger.addHandler(handler)
        unique_logger.setLevel(logging.DEBUG)
        
        unique_logger.warning("Warn")
        
        assert "⚠️" in messages[-1]


class TestColoredFormatter:
    """Tests para ColoredFormatter."""
    
    def test_format_message(self):
        """Verifica formato de mensaje."""
        formatter = ColoredFormatter(use_colors=False)
        
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Test",
            args=(),
            exc_info=None
        )
        
        formatted = formatter.format(record)
        assert "INFO" in formatted
        assert "Test" in formatted
    
    def test_format_error(self):
        """Verifica formato de error."""
        formatter = ColoredFormatter(use_colors=False)
        
        record = logging.LogRecord(
            name="test",
            level=logging.ERROR,
            pathname="",
            lineno=0,
            msg="Error msg",
            args=(),
            exc_info=None
        )
        
        formatted = formatter.format(record)
        assert "ERROR" in formatted
