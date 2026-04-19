"""Agente de cazas airdrops."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from core.storage import Storage
from datetime import datetime
import requests


class AirdropHunter(BaseAgent):
    """Agente que caza airdrops automáticamente."""
    
    AIRDROPS_ACTIVOS = [
        {
            'nombre': 'LayerZero',
            'tarea': 'bridge_testnet',
            'reward_estimado': '$200-2000',
            'status': 'pending'
        },
        {
            'nombre': 'ZetaChain',
            'tarea': 'transact_testnet',
            'reward_estimado': '$100-500',
            'status': 'pending'
        },
        {
            'nombre': 'StarkNet',
            'tarea': 'deploy_contract',
            'reward_estimado': '$50-500',
            'status': 'pending'
        },
        {
            'nombre': 'Monad',
            'tarea': 'testnet_activity',
            'reward_estimado': '$500-5000',
            'status': 'pending'
        },
        {
            'nombre': 'Berachain',
            'tarea': ' validators_test',
            'reward_estimado': '$200-2000',
            'status': 'pending'
        }
    ]
    
    def __init__(self, agent_id: str, config: dict, storage: Storage):
        super().__init__(agent_id, 'airdrop_hunter', config, storage)
        self.hunted = []
        self.storage_key = 'airdrop_hunts'
    
    def execute_task(self, task: dict) -> dict:
        """Ejecuta cacería de airdrops."""
        action = task.get('action')
        
        if action == 'hunt_all':
            return self._hunt_all()
        elif action == 'status':
            return self._get_status()
        elif action == 'next':
            return self._get_next_airdrop()
        
        return {'status': 'error'}
    
    def _hunt_all(self):
        """Caza todos los airdrops."""
        resultados = []
        for airdrop in self.AIRDROPS_ACTIVOS:
            result = self._hunt_airdrop(airdrop)
            resultados.append(result)
        return {'hunted': resultados}
    
    def _hunt_airdrop(self, airdrop: dict) -> dict:
        """Caza un airdrop específico."""
        nombre = airdrop['nombre']
        
        # Simular actividad
        self._update_status('hunting', nombre)
        
        hunt_result = {
            'nombre': nombre,
            'tarea': airdrop['tarea'],
            'reward': airdrop['reward_estimado'],
            'timestamp': datetime.now().isoformat(),
            'status': 'hunting'
        }
        
        self.hunted.append(hunt_result)
        self._save_hunts()
        
        return hunt_result
    
    def _get_status(self) -> dict:
        """Obtiene estado de cacerías."""
        hunts = self.storage.get(self.storage_key, [])
        return {
            'total_hunted': len(hunts),
            'airdrops': hunts,
            'active': self.AIRDROPS_ACTIVOS
        }
    
    def _get_next_airdrop(self) -> dict:
        """Obtiene el siguiente airdrop a cazar."""
        return self.AIRDROPS_ACTIVOS[0] if self.AIRDROPS_ACTIVOS else None
    
    def _save_hunts(self):
        """Guarda las cacerías."""
        self.storage.set(self.storage_key, self.hunted)
    
    def _update_status(self, status: str, detail: str = ''):
        """Actualiza estado del agente."""
        self.status = status
        self.last_active = datetime.now().isoformat()
        
        status_data = {
            'agent': 'AirdropHunter',
            'status': status,
            'detail': detail,
            'timestamp': self.last_active
        }
        self.storage.set('airdrop_agent_status', status_data)


def run_airdrop_agent():
    """Ejecuta el agente de airdrops."""
    from core.config import Config
    from core.storage import Storage
    
    config = Config()
    storage = Storage()
    
    agent = AirdropHunter('airdrop_1', config.as_dict(), storage)
    
    print('='*50)
    print('AIRDROP HUNTER AGENT - INICIADO')
    print('='*50)
    print(f'Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print()
    print('Airdrops activos:')
    for a in agent.AIRDROPS_ACTIVOS:
        print(f\"  - {a['nombre']}: {a['reward_estimado']}\")
    print()
    
    # Iniciar cacería
    result = agent.execute_task({'action': 'hunt_all'})
    print('Cacerías iniciadas!')
    print(result)
    
    return agent


if __name__ == '__main__':
    run_airdrop_agent()
