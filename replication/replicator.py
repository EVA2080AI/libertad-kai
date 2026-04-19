"""Sistema de replicación de agentes."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from core.storage import Storage


class Replicator:
    """Gestiona la replicación de agentes."""
    
    def __init__(self, storage: Storage):
        self.storage = storage
        self.agents_registry_key = 'replicated_agents'
    
    def create_agent(self, agent_type: str, config: dict) -> dict:
        """Crea un nuevo agente replicado."""
        agents = self.storage.get(self.agents_registry_key, [])
        agent_id = f'{agent_type}_{len(agents) + 1}'
        
        new_agent = {
            'id': agent_id,
            'type': agent_type,
            'config': config,
            'created_at': self.storage.get_timestamp()
        }
        
        agents.append(new_agent)
        self.storage.set(self.agents_registry_key, agents)
        
        return {'status': 'created', 'agent': new_agent}
    
    def list_agents(self) -> list:
        """Lista agentes replicados."""
        return self.storage.get(self.agents_registry_key, [])
    
    def get_agent(self, agent_id: str) -> dict:
        """Obtiene un agente por ID."""
        agents = self.list_agents()
        for agent in agents:
            if agent.get('id') == agent_id:
                return agent
        return None
