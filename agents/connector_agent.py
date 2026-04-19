"""Agente de conexión con IAs externas."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from core.storage import Storage
from core.token_manager import TokenManager


class ConnectorAgent(BaseAgent):
    """Agente que conecta con IAs externas."""
    
    def __init__(self, agent_id: str, config: dict, storage: Storage, token_manager: TokenManager):
        agent_config = {'name': 'Connector', 'type': 'connector', 'log_level': 'INFO'}
        super().__init__(agent_id, 'connector', agent_config, storage)
        self.token_manager = token_manager
        self.openai_key = config.get('openai_api_key')
        self.anthropic_key = config.get('anthropic_api_key')
        self.connected_ais = []
    
    def execute_task(self, task: dict) -> dict:
        """Ejecuta tarea de conexión."""
        task_type = task.get('type')
        
        if task_type == 'connect':
            return self._connect_ai(task)
        elif task_type == 'query':
            return self._query_ai(task)
        elif task_type == 'list':
            return {'connected_ais': self.connected_ais}
        
        return {'status': 'error', 'message': f'Unknown task type: {task_type}'}
    
    def _connect_ai(self, task: dict) -> dict:
        """Conecta con una IA."""
        ai_type = task.get('ai_type')
        if ai_type not in self.connected_ais:
            self.connected_ais.append(ai_type)
        return {'status': 'connected', 'ai_type': ai_type}
    
    def _query_ai(self, task: dict) -> dict:
        """Consulta a una IA."""
        return {'status': 'simulated', 'response': 'AI response (configure API keys for real queries)'}
