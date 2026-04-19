"""Agente principal que coordina el sistema."""

import time
import sys
import os
from datetime import datetime
from typing import Dict, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from core.storage import Storage
from core.token_manager import TokenManager
from replication.symbiosis import SymbiosisManager
from income.trading import TradingManager
from monitoring.logger import Logger


class MasterAgent(BaseAgent):
    """Agente coordinador principal del sistema."""
    
    def __init__(self, config, storage: Storage, token_manager: TokenManager, symbiosis: SymbiosisManager):
        agent_config = {
            'name': 'Master',
            'type': 'master',
            'log_level': 'INFO'
        }
        super().__init__('master', 'master', agent_config, storage)
        self.token_manager = token_manager
        self.symbiosis = symbiosis
        self.trading_manager = TradingManager(config)
        self.logger = Logger('MasterAgent')
        self.active_agents: Dict = {}
        self.running = False
    
    def start(self):
        """Inicia el agente master."""
        self.running = True
        self.logger.info('Master Agent iniciado')
        self._update_status('running')
        
        # Conectar agentes básicos
        self.symbiosis.connect_agents('master', 'trader')
        self.symbiosis.connect_agents('master', 'developer')
        
        self._run_main_loop()
    
    def _run_main_loop(self):
        """Loop principal del agente."""
        while self.running:
            try:
                # Monitorear agentes activos
                self._check_agents()
                
                # Procesar tareas pendientes
                self._process_pending_tasks()
                
                # Actualizar dashboard de ingresos
                self._update_income_tracking()
                
                time.sleep(60)  # Esperar 1 minuto entre iteraciones
                
            except Exception as e:
                self.logger.error(f'Error en main loop: {e}')
                time.sleep(60)
    
    def _check_agents(self):
        """Verifica el estado de los agentes."""
        for agent_id, agent in self.active_agents.items():
            if hasattr(agent, 'get_status'):
                status = agent.get_status()
                self.logger.debug(f'Agente {agent_id}: {status}')
    
    def _process_pending_tasks(self):
        """Procesa tareas pendientes."""
        pending_tasks = self.storage.get('pending_tasks', [])
        if pending_tasks:
            task = pending_tasks[0]
            result = self.execute_task(task)
            self.storage.set(f'task_result_{task.get("id")}', result)
            pending_tasks.pop(0)
            self.storage.set('pending_tasks', pending_tasks)
    
    def _update_income_tracking(self):
        """Actualiza el tracking de ingresos."""
        income_summary = self.storage.get('income_summary', {})
        income_summary['last_updated'] = datetime.now().isoformat()
        
        # Agregar ingresos del trading si está activo
        if self.trading_manager.is_active():
            balance = self.trading_manager.get_total_balance()
            income_summary['current_balance_usd'] = balance
        
        self.storage.set('income_summary', income_summary)
    
    def execute_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea específica."""
        task_type = task.get('type')
        self.logger.info(f'Ejecutando tarea: {task_type}')
        
        if task_type == 'trade':
            return self._handle_trade(task)
        elif task_type == 'develop':
            return self._handle_develop(task)
        elif task_type == 'connect':
            return self._handle_connect(task)
        elif task_type == 'status':
            return self._get_system_status()
        else:
            return {'status': 'error', 'message': f'Tipo de tarea desconocido: {task_type}'}
    
    def _handle_trade(self, task: Dict) -> Dict:
        """Maneja tareas de trading."""
        action = task.get('action')
        
        if action == 'get_balance':
            return self.trading_manager.get_account_balance()
        elif action == 'get_prices':
            return self.trading_manager.get_prices(task.get('symbols', []))
        elif action == 'execute':
            return self.trading_manager.execute_trade(
                task.get('symbol'),
                task.get('side'),
                task.get('amount')
            )
        else:
            return {'status': 'error', 'message': f'Acción desconocida: {action}'}
    
    def _handle_develop(self, task: Dict) -> Dict:
        """Maneja tareas de desarrollo."""
        return {
            'status': 'delegate',
            'to': 'developer',
            'task': task
        }
    
    def _handle_connect(self, task: Dict) -> Dict:
        """Maneja tareas de conexión con IAs."""
        return {
            'status': 'delegate',
            'to': 'connector',
            'task': task
        }
    
    def _get_system_status(self) -> Dict:
        """Obtiene el estado del sistema."""
        return {
            'status': 'running',
            'active_agents': list(self.active_agents.keys()),
            'master': self.get_status(),
            'symbiosis': self.symbiosis.get_network_stats(),
            'token_usage': self.token_manager.get_usage_report()
        }
    
    def stop(self):
        """Detiene el agente master."""
        self.running = False
        self._update_status('stopped')
        self.logger.info('Master Agent detenido')
    
    def register_agent(self, agent_id: str, agent):
        """Registra un agente activo."""
        self.active_agents[agent_id] = agent
        self.symbiosis.connect_agents('master', agent_id)
