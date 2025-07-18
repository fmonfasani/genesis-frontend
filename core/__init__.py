"""
Genesis Frontend Core Module

Módulo core específico para funcionalidades frontend.
Siguiendo la doctrina del ecosistema genesis-frontend:
- Se especializa solo en frontend
- No coordina workflows generales
- Colabora con genesis-templates
"""

from .logging import get_frontend_logger, setup_frontend_logging
from .validation import FrontendValidator
from .optimization import FrontendOptimizer

__all__ = [
    "get_frontend_logger",
    "setup_frontend_logging", 
    "FrontendValidator",
    "FrontendOptimizer",
]
