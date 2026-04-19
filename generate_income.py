#!/usr/bin/env python3
"""Generador automático de proyectos vendibles."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.storage import Storage
from agents.developer_agent import DeveloperAgent
from datetime import datetime


class IncomeGenerator:
    """Genera proyectos vendibles para obtener capital inicial."""
    
    PROYECTOS = [
        {
            'name': 'trading-bot-binance',
            'description': 'Bot de trading automatizado para Binance con estrategias SMA y RSI',
            'stack': ['python', 'binance-connector', 'pandas'],
            'complexity': 2.0
        },
        {
            'name': 'portfolio-tracker',
            'description': 'Dashboard para rastrear portfolio de criptomonedas en tiempo real',
            'stack': ['python', 'streamlit', 'binance-api'],
            'complexity': 1.5
        },
        {
            'name': 'arbitrage-scanner',
            'description': 'Scanner de arbitraje entre exchanges de criptomonedas',
            'stack': ['python', 'requests', 'asyncio'],
            'complexity': 2.5
        },
        {
            'name': 'trading-signals-bot',
            'description': 'Bot de Telegram que envía señales de trading basadas en análisis técnico',
            'stack': ['python', 'telegram-bot', 'ta-lib'],
            'complexity': 1.8
        },
        {
            'name': 'nft-marketplace-bot',
            'description': 'Bot para monitorear y automatizar compras/ventas de NFTs',
            'stack': ['python', 'web3', 'opensea-api'],
            'complexity': 3.0
        },
        {
            'name': 'crypto-tax-calculator',
            'description': 'Calculadora de impuestos para operaciones de criptomonedas',
            'stack': ['python', 'flask', 'sqlite'],
            'complexity': 2.2
        },
        {
            'name': 'trading-view-webhook',
            'description': 'Sistema de alertas TradingView con webhooks para Binance',
            'stack': ['python', 'fastapi', 'tradingview-webhook'],
            'complexity': 1.5
        },
        {
            'name': 'dea-bot-autonomo',
            'description': 'Bot de IA autónomo que genera contenido y marketing crypto',
            'stack': ['python', 'openai-api', 'telegram-bot'],
            'complexity': 3.5
        }
    ]
    
    def __init__(self):
        self.storage = Storage()
        config = {'GITHUB_TOKEN': None}
        self.dev = DeveloperAgent('income_gen', config, self.storage)
    
    def generar_proyectos(self, cantidad=5):
        """Genera proyectos vendibles."""
        proyectos_creados = []
        
        for i, spec in enumerate(self.PROYECTOS[:cantidad]):
            task = {'type': 'create_project', 'spec': spec}
            result = self.dev.execute_task(task)
            proyectos_creados.append(result['project'])
            print(f"  [{i+1}] {result['project']['name']} - ${result['estimated_value']}")
        
        return proyectos_creados
    
    def calcular_valor_total(self):
        """Calcula el valor total de todos los proyectos."""
        projects = self.storage.get('active_projects', [])
        return sum(p.get('estimated_value', 0) for p in projects)
    
    def generar_reporte(self):
        """Genera reporte de ingresos potenciales."""
        projects = self.storage.get('active_projects', [])
        total = sum(p.get('estimated_value', 0) for p in projects)
        
        print('\\n' + '='*50)
        print('REPORTE DE INGRESOS POTENCIALES')
        print('='*50)
        print(f'Proyectos creados: {len(projects)}')
        print(f'Valor total potencial: ${total:.2f}')
        print(f'\\nMeta diaria: $100')
        print(f'Progreso: {min(total/100*100, 100):.1f}%')
        print('='*50)
        
        if projects:
            print('\\nProyectos:')
            for p in projects:
                print(f\"  - {p['name']}: ${p.get('estimated_value', 0)}\")


if __name__ == '__main__':
    print('\\n=== GENERADOR DE INGRESOS - LIBERTAD ===')
    gen = IncomeGenerator()
    proyectos = gen.generar_proyectos(8)
    gen.generar_reporte()
