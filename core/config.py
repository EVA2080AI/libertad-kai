"""Configuración del sistema."""

import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv


class Config:
    """Gestión de configuración del sistema."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path
        self.data = {}
        
        # Cargar .env si existe
        if config_path and os.path.exists(config_path):
            load_dotenv(config_path)
        
        self._load_env()
    
    def _load_env(self):
        """Carga variables de entorno."""
        env_mapping = {
            'BINANCE_API_KEY': 'binance_api_key',
            'BINANCE_API_SECRET': 'binance_api_secret',
            'OPENAI_API_KEY': 'openai_api_key',
            'ANTHROPIC_API_KEY': 'anthropic_api_key',
            'GITHUB_TOKEN': 'github_token',
            'ETHERSCAN_API_KEY': 'etherscan_api_key',
            'LOG_LEVEL': 'log_level',
        }
        
        for env_var, config_key in env_mapping.items():
            value = os.getenv(env_var)
            if value:
                self.data[config_key] = value
        
        if 'log_level' not in self.data:
            self.data['log_level'] = 'INFO'
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor de configuración."""
        return self.data.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor de configuración."""
        self.data[key] = value
    
    def as_dict(self) -> Dict:
        """Retorna toda la configuración como diccionario."""
        return self.data.copy()
