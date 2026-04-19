"""Sistema de logging."""

import os
from datetime import datetime
from typing import Optional


class Logger:
    """Sistema de logging simple."""
    
    def __init__(self, name: str, log_dir: str = 'logs'):
        self.name = name
        self.log_dir = log_dir
        self._ensure_log_dir()
    
    def _ensure_log_dir(self):
        """Crea directorio de logs si no existe."""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _get_log_file(self) -> str:
        """Obtiene el archivo de log del día."""
        date = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(self.log_dir, f'{date}.log')
    
    def _write(self, level: str, message: str):
        """Escribe un mensaje de log."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f'[{timestamp}] [{level}] [{self.name}] {message}\n'
        
        try:
            with open(self._get_log_file(), 'a') as f:
                f.write(log_line)
        except IOError:
            pass
    
    def info(self, message: str):
        """Log nivel info."""
        self._write('INFO', message)
    
    def warning(self, message: str):
        """Log nivel warning."""
        self._write('WARNING', message)
    
    def error(self, message: str):
        """Log nivel error."""
        self._write('ERROR', message)
    
    def debug(self, message: str):
        """Log nivel debug."""
        self._write('DEBUG', message)
