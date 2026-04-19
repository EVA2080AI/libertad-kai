"""Almacenamiento y persistencia de datos."""

import json
import os
from datetime import datetime
from typing import Any, Dict, Optional


class Storage:
    """Sistema de almacenamiento simple basado en archivos JSON."""
    
    def __init__(self, storage_dir: str = '.libertad_data'):
        self.storage_dir = storage_dir
        self._ensure_storage_dir()
        self.memory: Dict[str, Any] = {}
        self._load_from_disk()
    
    def _ensure_storage_dir(self):
        """Crea el directorio de almacenamiento si no existe."""
        if not os.path.exists(self.storage_dir):
            os.makedirs(self.storage_dir)
    
    def _get_file_path(self, key: str) -> str:
        """Obtiene la ruta del archivo para una clave."""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.storage_dir, f'{safe_key}.json')
    
    def _load_from_disk(self):
        """Carga datos desde el disco."""
        if os.path.exists(self.storage_dir):
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.storage_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            key = filename[:-5]
                            self.memory[key] = json.load(f)
                    except (json.JSONDecodeError, IOError):
                        pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Obtiene un valor del almacenamiento."""
        return self.memory.get(key, default)
    
    def set(self, key: str, value: Any):
        """Establece un valor en el almacenamiento."""
        self.memory[key] = value
        self._save_to_disk(key, value)
    
    def _save_to_disk(self, key: str, value: Any):
        """Guarda un valor al disco."""
        filepath = self._get_file_path(key)
        try:
            with open(filepath, 'w') as f:
                json.dump(value, f, indent=2, default=str)
        except IOError as e:
            print(f"Error guardando {key}: {e}")
    
    def delete(self, key: str):
        """Elimina un valor del almacenamiento."""
        if key in self.memory:
            del self.memory[key]
            filepath = self._get_file_path(key)
            if os.path.exists(filepath):
                os.remove(filepath)
    
    def list_keys(self) -> list:
        """Lista todas las claves en el almacenamiento."""
        return list(self.memory.keys())
    
    def get_timestamp(self) -> str:
        """Obtiene timestamp actual."""
        return datetime.now().isoformat()
    
    def append(self, key: str, value: Any):
        """Agrega un valor a una lista."""
        if key not in self.memory:
            self.memory[key] = []
        if isinstance(self.memory[key], list):
            self.memory[key].append(value)
            self._save_to_disk(key, self.memory[key])
    
    def get_stats(self) -> Dict:
        """Obtiene estadísticas del almacenamiento."""
        return {
            'total_keys': len(self.memory),
            'keys': list(self.memory.keys()),
            'storage_dir': self.storage_dir
        }
