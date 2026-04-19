#!/usr/bin/env python3
"""
PROYECTO LIBERTAD - Sistema Autónomo de Generación de Ingresos
=============================================================

Sistema multi-agente para generar ingresos de forma autónoma.
Acceso a Binance, desarrollo de proyectos, conexión con IAs.

Usage:
    python main.py                    # Iniciar sistema
    python main.py --task TASK        # Ejecutar tarea específica
    python main.py --status           # Ver estado del sistema
    python main.py --agents           # Listar agentes
"""

import argparse
import json
import sys
import os
from datetime import datetime

# Agregar el directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.config import Config
from core.storage import Storage
from core.token_manager import TokenManager
from agents.master_agent import MasterAgent
from agents.developer_agent import DeveloperAgent
from agents.connector_agent import ConnectorAgent
from replication.replicator import Replicator
from replication.symbiosis import SymbiosisManager
from monitoring.dashboard import Dashboard


def parse_args():
    """Parsea argumentos de línea de comandos."""
    parser = argparse.ArgumentParser(
        description='LIBERTAD - Sistema Autónomo de Generación de Ingresos'
    )
    parser.add_argument('--task', type=str, help='Tarea a ejecutar (JSON)')
    parser.add_argument('--status', action='store_true', help='Ver estado del sistema')
    parser.add_argument('--agents', action='store_true', help='Listar agentes activos')
    parser.add_argument('--dashboard', action='store_true', help='Iniciar dashboard')
    parser.add_argument('--income-report', action='store_true', help='Reporte de ingresos')
    parser.add_argument('--config', type=str, help='Path a config.yaml')
    return parser.parse_args()


def main():
    """Función principal."""
    args = parse_args()
    
    # Cargar configuración
    config = Config(args.config)
    storage = Storage()
    token_manager = TokenManager()
    symbiosis = SymbiosisManager()
    
    # Inicializar agentes
    agents = {
        'master': MasterAgent(config, storage, token_manager, symbiosis),
    }
    
    # Agregar agente de desarrollo si hay token de GitHub
    if config.get('GITHUB_TOKEN'):
        agents['developer'] = DeveloperAgent('developer_1', config.as_dict(), storage)
    
    # Agregar agente de conexión si hay APIs configuradas
    if config.get('OPENAI_API_KEY') or config.get('ANTHROPIC_API_KEY'):
        agents['connector'] = ConnectorAgent('connector_1', config.as_dict(), storage, token_manager)
    
    # Modo status
    if args.status:
        print("\n" + "="*50)
        print("PROYECTO LIBERTAD - Estado del Sistema")
        print("="*50 + "\n")
        
        # Dashboard
        dashboard = Dashboard(agents, storage, token_manager)
        dashboard.print_status()
        
        # Reporte de tokens
        print("\n--- Uso de Tokens ---")
        token_report = token_manager.get_usage_report()
        for key, value in token_report.items():
            print(f"  {key}: {value}")
        
        # Simbiosis
        print("\n--- Red de Agentes ---")
        symbiosis_stats = symbiosis.get_network_stats()
        for key, value in symbiosis_stats.items():
            print(f"  {key}: {value}")
        
        return
    
    # Listar agentes
    if args.agents:
        print("\n--- Agentes Activos ---")
        for name, agent in agents.items():
            status = agent.get_status()
            print(f"  {name}: {status}")
        return
    
    # Reporte de ingresos
    if args.income_report:
        print("\n--- Reporte de Ingresos ---")
        income_summary = storage.get('income_summary', {})
        if income_summary:
            for period, amount in income_summary.items():
                print(f"  {period}: ${amount:.2f}")
        else:
            print("  No hay datos de ingresos aún.")
        return
    
    # Ejecutar tarea
    if args.task:
        try:
            task = json.loads(args.task)
            master = agents['master']
            result = master.execute_task(task)
            print(json.dumps(result, indent=2))
            return
        except json.JSONDecodeError as e:
            print(f"Error al parsear tarea: {e}")
            return
    
    # Dashboard interactivo
    if args.dashboard:
        dashboard = Dashboard(agents, storage, token_manager)
        dashboard.run()
        return
    
    # Modo interactivo por defecto
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   ███████╗ ██████╗  ██████╗                                ║
║   ██╔════╝██╔════╝ ██╔═══██╗                               ║
║   █████╗  ██║  ███╗██║   ██║                               ║
║   ██╔══╝  ██║   ██║██║   ██║                               ║
║   ██║     ╚██████╔╝╚██████╔╝                               ║
║   ╚═╝      ╚═════╝  ╚═════╝                                ║
║                                                              ║
║   SISTEMA AUTÓNOMO DE GENERACIÓN DE INGRESOS                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

Opciones:
  --status          Ver estado del sistema
  --agents          Listar agentes activos
  --dashboard       Iniciar dashboard
  --income-report   Reporte de ingresos
  --task TASK       Ejecutar tarea (JSON)
  
Ejemplos:
  python main.py --status
  python main.py --task '{"type":"trade","action":"get_balance"}'
  python main.py --task '{"type":"develop","spec":{"name":"mi_proyecto"}}'
""")
    
    # Iniciar agente master en background
    print("[INFO] Iniciando Master Agent...")
    master = agents['master']
    master.start()
    print("[INFO] Sistema iniciado. Usa --status para ver el estado.")


if __name__ == '__main__':
    main()
