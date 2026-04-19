"""Gestión de tokens y optimización de costos."""

import time
from typing import Dict, Optional
from datetime import datetime, timedelta


class TokenManager:
    """Gestiona el uso de tokens y optimiza costos."""
    
    def __init__(self):
        self.token_usage: Dict[str, list] = {}
        self.cost_limits = {
            'daily_limit': 100.0,  # $100/día
            'weekly_limit': 500.0,  # $500/semana
        }
        self.cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens (referencia)
    
    def log_usage(self, operation: str, tokens_used: int, cost: Optional[float] = None):
        """Registra el uso de tokens para una operación."""
        if operation not in self.token_usage:
            self.token_usage[operation] = []
        
        if cost is None:
            cost = (tokens_used / 1000) * self.cost_per_1k_tokens
        
        self.token_usage[operation].append({
            'timestamp': datetime.now().isoformat(),
            'tokens': tokens_used,
            'cost': cost
        })
    
    def get_total_cost(self, days: int = 1) -> float:
        """Obtiene el costo total de los últimos N días."""
        cutoff = datetime.now() - timedelta(days=days)
        total = 0.0
        
        for operation, logs in self.token_usage.items():
            for log in logs:
                if datetime.fromisoformat(log['timestamp']) >= cutoff:
                    total += log.get('cost', 0.0)
        
        return total
    
    def check_limit(self, limit_type: str = 'daily') -> bool:
        """Verifica si se ha alcanzado el límite."""
        days = 7 if limit_type == 'weekly' else 1
        current_cost = self.get_total_cost(days)
        limit = self.cost_limits.get(f'{limit_type}_limit', float('inf'))
        return current_cost < limit
    
    def get_usage_report(self) -> Dict:
        """Genera un reporte de uso de tokens."""
        report = {
            'total_operations': sum(len(logs) for logs in self.token_usage.values()),
            'operations_by_type': {op: len(logs) for op, logs in self.token_usage.items()},
            'cost_last_24h': self.get_total_cost(1),
            'cost_last_week': self.get_total_cost(7),
            'within_daily_limit': self.check_limit('daily'),
            'within_weekly_limit': self.check_limit('weekly'),
        }
        return report
    
    def optimize_batch(self, items: list, batch_size: int = 10) -> list:
        """Agrupa items para minimizar llamadas a APIs."""
        return [items[i:i + batch_size] for i in range(0, len(items), batch_size)]
