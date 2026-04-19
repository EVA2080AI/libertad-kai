"""Módulo de trading e inversiones."""

import requests
from typing import Dict, List, Optional


class TradingManager:
    """Gestiona operaciones de trading e inversiones."""
    
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('binance_api_key')
        self.api_secret = config.get('binance_api_secret')
        self.base_url = 'https://api.binance.com'
        self.active = False
        self.wallets = {}
    
    def is_active(self) -> bool:
        """Verifica si el trading está activo."""
        return self.active
    
    def get_account_balance(self) -> Dict:
        """Obtiene el balance de la cuenta."""
        if not self.api_key or not self.api_secret:
            return {'status': 'not_configured', 'message': 'API keys not configured'}
        
        return {
            'status': 'success',
            'balances': self.wallets,
            'total_usd': 0.0
        }
    
    def get_prices(self, symbols: List[str]) -> Dict:
        """Obtiene precios de símbolos."""
        if not symbols:
            symbols = ['BTCUSDT', 'ETHUSDT']
        
        prices = {}
        for symbol in symbols:
            try:
                response = requests.get(
                    f'{self.base_url}/api/v3/ticker/price',
                    params={'symbol': symbol},
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    prices[symbol] = float(data.get('price', 0))
            except Exception:
                prices[symbol] = 0.0
        
        return {'status': 'success', 'prices': prices}
    
    def execute_trade(self, symbol: str, side: str, amount: float) -> Dict:
        """Ejecuta una operación de trading."""
        if not self.api_key or not self.api_secret:
            return {'status': 'error', 'message': 'API not configured'}
        
        return {
            'status': 'simulated',
            'symbol': symbol,
            'side': side,
            'amount': amount,
            'message': 'Trade simulated (API keys required for real trading)'
        }
    
    def get_total_balance(self) -> float:
        """Obtiene el balance total en USD."""
        return sum(self.wallets.values())


class WalletManager:
    """Gestiona múltiples wallets."""
    
    def __init__(self):
        self.wallets: Dict[str, float] = {}
    
    def add_wallet(self, currency: str, amount: float):
        """Agrega una wallet."""
        self.wallets[currency] = amount
    
    def get_balance(self, currency: str) -> float:
        """Obtiene balance de una currency."""
        return self.wallets.get(currency, 0.0)
    
    def get_total_usd(self, prices: Dict[str, float]) -> float:
        """Calcula el total en USD."""
        total = 0.0
        for currency, amount in self.wallets.items():
            price = prices.get(f'{currency}USDT', 1.0)
            total += amount * price
        return total
