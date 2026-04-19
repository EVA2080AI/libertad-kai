"""Dashboard de monitoreo."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.token_manager import TokenManager
from datetime import datetime


class Dashboard:
    """Dashboard para visualizar el estado del sistema."""
    
    INCOME_GOAL_DAILY = 100.0  # Meta diaria en USD
    
    def __init__(self, agents: dict, storage, token_manager: TokenManager):
        self.agents = agents
        self.storage = storage
        self.token_manager = token_manager
    
    def print_status(self):
        """Imprime el estado del sistema."""
        print("=" * 50)
        print("PROYECTO LIBERTAD - Dashboard")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Ingresos
        income_summary = self.storage.get('income_summary', {})
        current = income_summary.get('current_balance_usd', 0.0)
        progress = min(current / self.INCOME_GOAL_DAILY * 100, 100)
        
        print(f"META DIARIA: ${self.INCOME_GOAL_DAILY}")
        print(f"ACTUAL: ${current:.2f} ({progress:.1f}%)")
        print(f"[{'#' * int(progress/5)}{'.' * (20 - int(progress/5))}]")
        print()
        
        # Agentes
        print("AGENTES:")
        for name, agent in self.agents.items():
            if hasattr(agent, 'get_status'):
                status = agent.get_status()
                print(f"  - {name}: {status.get('status', 'unknown')}")
        print()
        
        # Tokens
        token_report = self.token_manager.get_usage_report()
        print(f"TOKENS - Costo 24h: ${token_report.get('cost_last_24h', 0):.2f}")
    
    def run(self):
        """Ejecuta el dashboard interactivo."""
        self.print_status()
