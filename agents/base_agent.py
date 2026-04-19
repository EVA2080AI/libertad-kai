"""Agente base para el sistema."""

from datetime import datetime
from typing import Dict, Optional


class BaseAgent:
    """Clase base para todos los agentes."""
    
    def __init__(self, agent_id: str, agent_type: str, config: Dict, storage):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.config = config
        self.storage = storage
        self.status = 'initialized'
        self.created_at = datetime.now().isoformat()
        self.last_active = self.created_at
    
    def get_status(self) -> Dict:
        """Obtiene el estado del agente."""
        return {
            'id': self.agent_id,
            'type': self.agent_type,
            'status': self.status,
            'created_at': self.created_at,
            'last_active': self.last_active
        }
    
    def _update_status(self, status: str):
        """Actualiza el estado del agente."""
        self.status = status
        self.last_active = datetime.now().isoformat()
    
    def execute_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea. Override en subclases."""
        return {'status': 'error', 'message': 'execute_task not implemented'}
    
    def get_id(self) -> str:
        """Retorna el ID del agente."""
        return self.agent_id
    
    def get_type(self) -> str:
        """Retorna el tipo del agente."""
        return self.agent_type
