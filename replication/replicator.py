"""
KAI Replicator - Crea copias de KAI para diferentes tareas
"""
import os
import json
import shutil
from datetime import datetime
from pathlib import Path
import git

class KAIReplicator:
    def __init__(self):
        self.source_dir = Path("/Users/juanmasmela/Documents/Free/libertad")
        self.replicas_dir = Path("/Users/juanmasmela/Documents/Free/replicas")
        
    def create_replica(self, name, purpose, modifications=None):
        """Crear una réplica de KAI"""
        print(f"\n🧬 Creando réplica: {name}")
        
        replica_path = self.replicas_dir / name
        
        # Crear directorio
        replica_path.mkdir(parents=True, exist_ok=True)
        
        # Copiar estructura base
        self.copy_structure(replica_path)
        
        # Aplicar modificaciones específicas
        if modifications:
            self.apply_modifications(replica_path, modifications)
        
        # Crear configuración
        self.create_replica_config(replica_path, name, purpose)
        
        # Inicializar git si es necesario
        self.init_git(replica_path, name)
        
        print(f"✅ Réplica {name} creada en {replica_path}")
        
        return {
            "name": name,
            "purpose": purpose,
            "path": str(replica_path),
            "status": "ready"
        }
    
    def copy_structure(self, dest):
        """Copiar estructura de archivos"""
        dirs_to_copy = ["agents", "core", "income", "monitoring", "utils"]
        
        for d in dirs_to_copy:
            src = self.source_dir / d
            if src.exists():
                shutil.copytree(src, dest / d, dirs_exist_ok=True)
    
    def apply_modifications(self, path, mods):
        """Aplicar modificaciones específicas"""
        # Modificar propósito en README
        readme = path / "README.md"
        if readme.exists():
            content = readme.read_text()
            content = content.replace("LIBERTAD KAI", mods.get("title", "KAI Replica"))
            readme.write_text(content)
        
        # Guardar configuración
        config_file = path / "replica_config.json"
        with open(config_file, 'w') as f:
            json.dump(mods, f, indent=2)
    
    def create_replica_config(self, path, name, purpose):
        """Crear archivo de configuración de la réplica"""
        config = {
            "name": name,
            "purpose": purpose,
            "created": datetime.now().isoformat(),
            "parent": "LIBERTAD-KAI",
            "version": "1.0"
        }
        
        with open(path / "config.json", 'w') as f:
            json.dump(config, f, indent=2)
    
    def init_git(self, path, name):
        """Inicializar repositorio git"""
        try:
            # Ya existe?
            if not (path / ".git").exists():
                repo = git.Repo.init(path)
                
                # Commit inicial
                repo.index.add(["*"])
                repo.index.commit(f"Initial: {name}")
                
                print(f"   📦 Git repo initialized")
        except Exception as e:
            print(f"   ⚠️ Git init warning: {e}")
    
    def list_replicas(self):
        """Listar todas las réplicas"""
        if not self.replicas_dir.exists():
            return []
        
        replicas = []
        for item in self.replicas_dir.iterdir():
            if item.is_dir():
                config_file = item / "config.json"
                if config_file.exists():
                    with open(config_file) as f:
                        config = json.load(f)
                        replicas.append(config)
        
        return replicas
    
    def evolve_replica(self, name):
        """Evolucionar una réplica específica"""
        replica_path = self.replicas_dir / name
        
        if not replica_path.exists():
            return {"error": "Replica not found"}
        
        # Simular evolución
        print(f"🧬 Evolucionando {name}...")
        
        # Incrementar nivel
        config_file = replica_path / "config.json"
        with open(config_file) as f:
            config = json.load(f)
        
        config["evolution_level"] = config.get("evolution_level", 0) + 1
        config["last_evolution"] = datetime.now().isoformat()
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        return config
    
    def replicate_to_github(self, name, github_token):
        """Enviar réplica a GitHub"""
        # Esto requeriría autenticación real
        print(f"📤 Preparando {name} para GitHub...")
        
        return {
            "status": "ready",
            "instructions": f"""
            Para subir {name} a GitHub:
            1. Ve a github.com/new
            2. Crea repositorio: {name}
            3. En la carpeta {self.replicas_dir / name}:
               git remote add origin https://github.com/YOUR_USER/{name}.git
               git push -u origin main
            """
        }


def run_replication():
    """Ejecutar replicación"""
    replicator = KAIReplicator()
    
    print("="*60)
    print("🧬 KAI REPLICATION SYSTEM")
    print("="*60)
    
    # Crear réplicas iniciales si no existen
    initial_replicas = [
        {
            "name": "kai-trader",
            "purpose": "Enfocado 100% en trading Binance",
            "modifications": {
                "title": "KAI Trader",
                "focus": "trading"
            }
        },
        {
            "name": "kai-airdrop-hunter",
            "purpose": "Cazador de airdrops 24/7",
            "modifications": {
                "title": "KAI Airdrop Hunter",
                "focus": "airdrops"
            }
        },
        {
            "name": "kai-affiliate",
            "purpose": "Generador de tráfico y afiliados",
            "modifications": {
                "title": "KAI Affiliate",
                "focus": "affiliates"
            }
        }
    ]
    
    created = []
    for replica in initial_replicas:
        result = replicator.create_replica(
            replica["name"],
            replica["purpose"],
            replica["modifications"]
        )
        created.append(result)
    
    print("\n" + "="*60)
    print("📊 RÉPLICAS CREADAS")
    print("="*60)
    for r in created:
        print(f"   ✅ {r['name']}: {r['purpose']}")
    
    return created

if __name__ == "__main__":
    run_replication()
