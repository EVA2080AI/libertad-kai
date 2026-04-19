"""Agente de venta de proyectos."""

import os
import sys
from typing import Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent
from core.storage import Storage


class ProjectSeller:
    """Gestiona la venta de proyectos."""
    
    def __init__(self, storage: Storage, repo_manager=None):
        self.storage = storage
        self.repo_manager = repo_manager
        self.active_projects_key = 'active_projects'
    
    def list_projects(self) -> List[Dict]:
        """Lista proyectos activos."""
        return self.storage.get(self.active_projects_key, [])
    
    def add_project(self, project: Dict) -> bool:
        """Agrega un nuevo proyecto."""
        projects = self.list_projects()
        projects.append({
            **project,
            'created_at': self.storage.get_timestamp()
        })
        self.storage.set(self.active_projects_key, projects)
        return True
    
    def get_marketplace_value(self, project: Dict) -> float:
        """Estima el valor de un proyecto en el mercado."""
        base_value = 50.0
        complexity_multiplier = project.get('complexity', 1.0)
        return base_value * complexity_multiplier


class DeveloperAgent(BaseAgent):
    """Agente que desarrolla proyectos vendibles."""
    
    def __init__(self, agent_id: str, config: Dict, storage: Storage):
        super().__init__(agent_id, 'developer', config, storage)
        self.github_token = config.get('GITHUB_TOKEN')
        self.project_seller = ProjectSeller(storage, None)
    
    def execute_task(self, task: Dict) -> Dict:
        """Ejecuta una tarea de desarrollo."""
        task_type = task.get('type')
        
        if task_type == 'create_project':
            return self._create_project(task)
        elif task_type == 'list_projects':
            return {'projects': self.project_seller.list_projects()}
        else:
            return {'status': 'error', 'message': f'Unknown task type: {task_type}'}
    
    def _create_project(self, task: Dict) -> Dict:
        """Crea un nuevo proyecto."""
        project_spec = task.get('spec', {})
        name = project_spec.get('name', f'project_{self.storage.get_timestamp()}')
        
        project = {
            'name': name,
            'description': project_spec.get('description', ''),
            'stack': project_spec.get('stack', ['python']),
            'complexity': project_spec.get('complexity', 1.0),
            'estimated_value': self.project_seller.get_marketplace_value(project_spec),
            'status': 'created'
        }
        
        self.project_seller.add_project(project)
        
        return {
            'status': 'success',
            'project': project,
            'estimated_value': project['estimated_value']
        }
    
    def generate_project_structure(self, name: str, stack: List[str]) -> Dict:
        """Genera la estructura de un nuevo proyecto."""
        return {
            'name': name,
            'files': ['main.py', 'README.md', 'requirements.txt', '.gitignore'],
            'stack': stack
        }
