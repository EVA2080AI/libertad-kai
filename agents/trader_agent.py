"""Agente de trading."""

from .base_agent import BaseAgent
from ..core.storage import Storage
from ..core.token_manager import TokenManager
from ..income.trading import TradingManager


class TraderAgent(BaseAgent):
    """Agente especializado en trading."""
    
    def __init__(self, agent_id: str, config, storage: Storage, token_manager: TokenManager):
        agent_config = {'name': 'Trader', 'type': 'trader', 'log_level': 'INFO'}
        super().__init__(agent_id, 'trader', agent_config, storage)
        self.token_manager = token_manager
        self.trading_manager = TradingManager(config)
        self.strategies = []
    
    def execute_task(self, task):
        """Ejecuta tarea de trading."""
        action = task.get('action')
        
        if action == 'get_balance':
            return self.trading_manager.get_account_balance()
        elif action == 'get_prices':
            return self.trading_manager.get_prices(task.get('symbols', []))
        elif action == 'execute_trade':
            return self.trading_manager.execute_trade(
                task.get('symbol'),
                task.get('side'),
                task.get('amount')
            )
        elif action == 'get_strategy':
            return {'strategies': self.strategies}
        
        return {'status': 'error', 'message': f'Unknown action: {action}'}
    
    def add_strategy(self, strategy):
        """Agrega una estrategia de trading."""
        self.strategies.append(strategy)
        return {'status': 'added', 'strategy': strategy}
