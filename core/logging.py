"""
Frontend-specific logging utilities

Logging específico para agentes frontend siguiendo la doctrina del ecosistema:
- Se especializa solo en frontend
- No duplica funcionalidad de genesis-core
- Proporciona logging específico para operaciones frontend
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


def get_frontend_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Obtener logger específico para operaciones frontend
    
    Args:
        name: Nombre del logger (ej: 'nextjs_agent', 'react_agent')
        level: Nivel de logging
        
    Returns:
        Logger configurado para frontend
    """
    logger_name = f"genesis_frontend.{name}"
    logger = logging.getLogger(logger_name)
    
    if not logger.handlers:
        # Handler para consola
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter específico para frontend
        formatter = FrontendLogFormatter()
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.setLevel(level)
        
        # Prevenir propagación para evitar duplicados
        logger.propagate = False
    
    return logger


def setup_frontend_logging(
    output_dir: Optional[Path] = None,
    level: int = logging.INFO,
    enable_file_logging: bool = True
) -> Dict[str, Any]:
    """
    Configurar logging para todo el sistema frontend
    
    Args:
        output_dir: Directorio para logs (opcional)
        level: Nivel de logging
        enable_file_logging: Habilitar logging a archivo
        
    Returns:
        Configuración aplicada
    """
    config = {
        "level": level,
        "handlers": ["console"],
        "formatters": ["frontend"],
        "enabled": True
    }
    
    # Configurar logger raíz para frontend
    root_logger = logging.getLogger("genesis_frontend")
    root_logger.setLevel(level)
    
    # Limpiar handlers existentes
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Handler para consola
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(FrontendLogFormatter())
    root_logger.addHandler(console_handler)
    
    # Handler para archivo si está habilitado
    if enable_file_logging and output_dir:
        log_dir = Path(output_dir) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"frontend_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(FrontendLogFormatter(include_timestamp=True))
        root_logger.addHandler(file_handler)
        
        config["handlers"].append("file")
        config["log_file"] = str(log_file)
    
    # Prevenir propagación al logger raíz de Python
    root_logger.propagate = False
    
    return config


class FrontendLogFormatter(logging.Formatter):
    """
    Formatter personalizado para logs de frontend
    
    Formatea logs con información específica de frontend:
    - Framework siendo procesado
    - Agente específico
    - Indicadores visuales para diferentes tipos de operaciones
    """
    
    def __init__(self, include_timestamp: bool = False):
        self.include_timestamp = include_timestamp
        
        # Colores ANSI para diferentes niveles
        self.colors = {
            'DEBUG': '\033[36m',    # Cyan
            'INFO': '\033[32m',     # Green
            'WARNING': '\033[33m',  # Yellow
            'ERROR': '\033[31m',    # Red
            'CRITICAL': '\033[35m', # Magenta
            'RESET': '\033[0m'      # Reset
        }
        
        # Prefijos específicos para frontend
        self.prefixes = {
            'nextjs': '⚛️ ',
            'react': '⚛️ ',
            'vue': '💚',
            'ui': '🎨',
            'component': '🧩',
            'template': '📄',
            'optimization': '⚡',
            'validation': '✅',
            'error': '❌',
            'warning': '⚠️ ',
            'success': '✅',
            'generation': '🏗️ ',
            'build': '🔨',
            'test': '🧪'
        }
        
        super().__init__()
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formatear registro de log
        """
        # Determinar color basado en nivel
        color = self.colors.get(record.levelname, '')
        reset = self.colors['RESET']
        
        # Determinar prefijo basado en el contexto
        prefix = self._get_context_prefix(record)
        
        # Construir timestamp si está habilitado
        timestamp = ""
        if self.include_timestamp:
            timestamp = f"[{datetime.now().strftime('%H:%M:%S')}] "
        
        # Extraer nombre del agente del logger
        agent_name = self._extract_agent_name(record.name)
        
        # Formatear mensaje principal
        message = record.getMessage()
        
        # Construir log final
        if agent_name:
            formatted_log = f"{timestamp}{color}{prefix}[{agent_name}]{reset} {message}"
        else:
            formatted_log = f"{timestamp}{color}{prefix}{message}{reset}"
        
        # Agregar información de excepción si existe
        if record.exc_info:
            formatted_log += f"\n{self.formatException(record.exc_info)}"
        
        return formatted_log
    
    def _get_context_prefix(self, record: logging.LogRecord) -> str:
        """
        Obtener prefijo basado en el contexto del log
        """
        message = record.getMessage().lower()
        
        # Buscar palabras clave en el mensaje
        for keyword, prefix in self.prefixes.items():
            if keyword in message:
                return prefix
        
        # Prefijo por defecto basado en nivel
        level_prefixes = {
            'DEBUG': '🔍',
            'INFO': 'ℹ️ ',
            'WARNING': '⚠️ ',
            'ERROR': '❌',
            'CRITICAL': '🚨'
        }
        
        return level_prefixes.get(record.levelname, '')
    
    def _extract_agent_name(self, logger_name: str) -> str:
        """
        Extraer nombre del agente del nombre del logger
        """
        if "genesis_frontend." in logger_name:
            parts = logger_name.split(".")
            if len(parts) >= 2:
                agent_name = parts[-1]
                # Limpiar nombre del agente
                if agent_name.endswith("_agent"):
                    agent_name = agent_name[:-6]  # Remover "_agent"
                return agent_name.upper()
        
        return ""


class FrontendLogContext:
    """
    Context manager para logging con información adicional de frontend
    """
    
    def __init__(self, logger: logging.Logger, framework: str, operation: str):
        self.logger = logger
        self.framework = framework
        self.operation = operation
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Iniciando {self.operation} para {self.framework}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = datetime.now() - self.start_time
        
        if exc_type is None:
            self.logger.info(
                f"Completado {self.operation} para {self.framework} "
                f"en {duration.total_seconds():.2f}s"
            )
        else:
            self.logger.error(
                f"Error en {self.operation} para {self.framework} "
                f"después de {duration.total_seconds():.2f}s: {exc_val}"
            )
    
    def log_progress(self, message: str, step: int = None, total: int = None):
        """
        Log de progreso durante la operación
        """
        if step is not None and total is not None:
            progress_msg = f"[{step}/{total}] {message}"
        else:
            progress_msg = message
        
        self.logger.info(f"{self.framework} - {progress_msg}")


def log_frontend_operation(
    logger: logging.Logger, 
    framework: str, 
    operation: str
) -> FrontendLogContext:
    """
    Crear context manager para operación frontend
    
    Args:
        logger: Logger a usar
        framework: Framework siendo procesado
        operation: Tipo de operación
        
    Returns:
        Context manager para logging
        
    Example:
        >>> logger = get_frontend_logger("nextjs_agent")
        >>> with log_frontend_operation(logger, "nextjs", "component_generation"):
        ...     # Operación aquí
        ...     pass
    """
    return FrontendLogContext(logger, framework, operation)


def setup_agent_logger(agent_id: str, output_dir: Optional[Path] = None) -> logging.Logger:
    """
    Configurar logger específico para un agente
    
    Args:
        agent_id: ID del agente (ej: 'nextjs_agent')
        output_dir: Directorio para logs
        
    Returns:
        Logger configurado para el agente
    """
    logger = get_frontend_logger(agent_id)
    
    # Configurar logging de archivos si se proporciona directorio
    if output_dir:
        log_dir = Path(output_dir) / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Archivo específico del agente
        log_file = log_dir / f"{agent_id}_{datetime.now().strftime('%Y%m%d')}.log"
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(FrontendLogFormatter(include_timestamp=True))
        
        logger.addHandler(file_handler)
    
    return logger


# Configuración por defecto para el módulo
_default_config = {
    "level": logging.INFO,
    "console_enabled": True,
    "file_enabled": False,
    "format": "frontend"
}


def get_logging_config() -> Dict[str, Any]:
    """
    Obtener configuración actual de logging
    """
    return _default_config.copy()


def update_logging_config(**kwargs) -> None:
    """
    Actualizar configuración de logging
    """
    _default_config.update(kwargs)
