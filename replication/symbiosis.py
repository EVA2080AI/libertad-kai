"""Sistema de simbiosis entre agentes."""

from typing import Dict, List, Optional
from datetime import datetime


class SymbiosisManager:
    """Gestiona la colaboración entre agentes."""
    
    def __init__(self):
        self.connections: Dict[str, List[str]] = {}  # agent_id -> [connected_agent_ids]
        self.shared_knowledge: Dict[str, Dict] = {}  # knowledge_id -> data
    
    def connect_agents(self, agent1_id: str, agent2_id: str) -> bool:
        """Conecta dos agentes."""
        if agent1_id not in self.connections:
            self.connections[agent1_id] = []
        if agent2_id not in self.connections:
            self.connections[agent2_id] = []
        
        if agent2_id not in self.connections[agent1_id]:
            self.connections[agent1_id].append(agent2_id)
        if agent1_id not in self.connections[agent2_id]:
            self.connections[agent2_id].append(agent1_id)
        
        return True
    
    def share_knowledge(self, agent_id: str, knowledge_id: str, data: Dict) -> bool:
        """Comparte conocimiento entre agentes conectados."""
        if agent_id in self.connections:
            self.shared_knowledge[knowledge_id] = {
                'data': data,
                'shared_by': agent_id,
                'timestamp': datetime.now().isoformat()
            }
            return True
        return False
    
    def get_shared_knowledge(self, knowledge_id: str) -> Optional[Dict]:
        """Obtiene conocimiento compartido."""
        return self.shared_knowledge.get(knowledge_id)
    
    def get_connected_agents(self, agent_id: str) -> List[str]:
        """Obtiene los agentes conectados a uno dado."""
        return self.connections.get(agent_id, [])
    
    def get_network_stats(self) -> Dict:
        """Estadísticas de la red de agentes."""
        total_connections = sum(len(agents) for agents in self.connections.values())
        return {
            'total_agents': len(self.connections),
            'total_connections': total_connections,
            'knowledge_base_size': len(self.shared_knowledge)
        }
