"""
KAI AGENTS - Agentes individuales con Ollama
Cada agente tiene su propia IA local
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ollama_ai import ollama_ai, check_ollama_status
from pathlib import Path
from datetime import datetime
import json

class KAIAgent:
    """Agente base con Ollama"""
    def __init__(self, name: str, role: str, model: str = "fast"):
        self.name = name
        self.role = role
        self.model = model  # "fast" o "coder"
        self.tasks_completed = 0
        self.memory = []
        
    def think(self, context: str) -> str:
        """Pensar con Ollama local"""
        prompt = f"Eres {self.name}, {self.role}. {context}"
        # Mapear modelo rápido a gemma3
        model = "gemma3:1b" if self.model == "fast" else "qwen2.5-coder:7b"
        return ollama_ai.generate(prompt, model=model)
    
    def save_memory(self, task: str, result: str):
        """Guardar en memoria"""
        self.memory.append({
            "time": datetime.now().isoformat(),
            "task": task,
            "result": result
        })
        self.tasks_completed += 1
    
    def get_status(self) -> dict:
        return {
            "name": self.name,
            "role": self.role,
            "tasks": self.tasks_completed,
            "model": self.model,
            "memory_size": len(self.memory)
        }


class TraderAgent(KAIAgent):
    """Agente de trading con IA local"""
    def __init__(self):
        super().__init__("KAI Trader", "Trading Binance", "coder")
        self.positions = []
        self.balance = 0
        
    def analyze_market(self) -> str:
        """Analizar mercado crypto"""
        return self.think("Analiza BTC/USDT. ¿Comprar, vender o esperar?")
    
    def execute_trade(self, action: str, pair: str = "BTCUSDT") -> dict:
        """Ejecutar trade"""
        decision = self.analyze_market()
        result = f"Trade {action} {pair}: {decision}"
        self.save_memory(f"Trade {action}", decision)
        return {"action": action, "pair": pair, "analysis": decision}


class AirdropAgent(KAIAgent):
    """Agente de airdrops con IA local"""
    def __init__(self):
        super().__init__("KAI Airdrop", "Cazar airdrops", "fast")
        self.airdrops = ["ZetaChain", "LayerZero", "StarkNet", "zkSync"]
        
    def scan_airdrops(self) -> list:
        """Escanear airdrops disponibles"""
        prompt = f"Analiza estos airdrops: {self.airdrops}. ¿Cuáles reclamar primero?"
        decision = self.think(prompt)
        return {"airdrops": self.airdrops, "priority": decision}
    
    def claim_airdrop(self, name: str) -> dict:
        """Reclamar un airdrop"""
        self.save_memory(f"Claim {name}", "Completado")
        return {"airdrop": name, "status": "claimed"}


class DeveloperAgent(KAIAgent):
    """Agente desarrollador FULLSTACK con IA local"""
    def __init__(self):
        super().__init__("KAI Fullstack", "Desarrollo Fullstack (React + Python + DB)", "coder")
        self.commits = 0
        self.stack = ["React", "TypeScript", "Python", "Node.js", "PostgreSQL", "MongoDB", "Docker", "AWS"]
        
    def write_code(self, task: str) -> str:
        """Generar código"""
        prompt = f"Tarea: {task}. Responde SOLO con código funcional, sin explicaciones."
        if self.model == "coder":
            result = ollama_ai.generate(prompt, model="qwen2.5-coder:7b")
        else:
            result = self.think(prompt)
        
        self.save_memory(f"Code: {task[:30]}", "Generado")
        self.commits += 1
        return result
    
    def write_frontend(self, component: str, framework: str = "React") -> str:
        """Generar código frontend"""
        prompt = f"""Crea componente {framework}: {component}
Incluye:
- Código funcional
- Estilos (Tailwind si React)
- Estados y eventos
Responde SOLO código."""
        return ollama_ai.generate(prompt, model="qwen2.5-coder:7b")
    
    def write_backend(self, api: str, framework: str = "FastAPI") -> str:
        """Generar código backend"""
        prompt = f"""Crea endpoint/API {framework}: {api}
Incluye:
- Routes/endpoints
- Modelos de datos
- Validación
- Conexión DB
Responde SOLO código Python."""
        return ollama_ai.generate(prompt, model="qwen2.5-coder:7b")
    
    def write_database(self, schema: str, db_type: str = "PostgreSQL") -> str:
        """Generar esquema de base de datos"""
        prompt = f"""Crea esquema DB {db_type}: {schema}
Incluye:
- Tablas
- Relaciones
- Índices
- Seeds
Responde SOLO SQL."""
        return ollama_ai.generate(prompt, model="qwen2.5-coder:7b")
    
    def create_full_project(self, project_name: str, project_type: str) -> dict:
        """Crear proyecto completo fullstack"""
        prompt = f"""Crea estructura de proyecto {project_type}: {project_name}
Incluye:
1. package.json (frontend)
2. requirements.txt (backend)
3. docker-compose.yml
4. Estructura de carpetas
5. README.md
Responde con estructura de archivos."""
        
        result = self.think(prompt)
        self.save_memory(f"Project: {project_name}", "Estructura creada")
        return {
            "project": project_name,
            "type": project_type,
            "structure": result,
            "stack": self.stack
        }
    
    def review_code(self, code: str) -> str:
        """Revisar código"""
        return self.think(f"Revisa este código y sugiere mejoras:\n{code[:500]}")


class AffiliateAgent(KAIAgent):
    """Agente de marketing y afiliados"""
    def __init__(self):
        super().__init__("KAI Affiliate", "Marketing y referidos", "fast")
        self.links = []
        
    def generate_link(self, platform: str) -> str:
        """Generar enlace de afiliado"""
        links = {
            "binance": "https://www.binance.com/es-LA/ref/kai_libertad",
            "tradingview": "https://www.tradingview.com/affiliate/?aff_id=kai_libertad",
            "bybit": "https://bybit.com/affiliate/?affiliate_id=1345"
        }
        link = links.get(platform, "https://example.com")
        self.links.append({"platform": platform, "link": link})
        return link
    
    def promote(self) -> str:
        """Crear contenido promocional"""
        return self.think("Genera un tweet promocional para KAI. Max 280 chars.")


class ReplicatorAgent(KAIAgent):
    """Agente que crea copias de KAI"""
    def __init__(self):
        super().__init__("KAI Replicator", "Replicar KAI", "coder")
        self.replicas = 0
        
    def can_replicate(self, level: int) -> bool:
        """Verificar si puede replicar"""
        return level >= 2
    
    def create_replica(self, name: str) -> dict:
        """Crear nueva réplica de KAI"""
        if self.replicas >= 5:
            return {"status": "max_replicas"}
        
        replica_code = self.think(f"""
Crea una copia ligera de KAI llamada {name}.
Incluye: main loop, income generation, self-improvement.
Código Python funcional.""")
        
        self.replicas += 1
        self.save_memory(f"Create {name}", f"Réplica #{self.replicas}")
        
        return {
            "name": name,
            "replica_id": self.replicas,
            "code": replica_code,
            "status": "created"
        }


# Instancias globales
AGENTS = {
    "trader": TraderAgent(),
    "airdrop": AirdropAgent(),
    "dev": DeveloperAgent(),
    "affiliate": AffiliateAgent(),
    "replicator": ReplicatorAgent()
}

def get_all_agents_status():
    """Obtener status de todos los agentes"""
    return {name: agent.get_status() for name, agent in AGENTS.items()}

def run_agent(name: str, action: str):
    """Ejecutar acción en agente específico"""
    if name not in AGENTS:
        return {"error": "Agente no encontrado"}
    
    agent = AGENTS[name]
    
    if action == "status":
        return agent.get_status()
    elif action == "think":
        return agent.think("¿Qué estás haciendo?")
    else:
        return {"error": f"Acción '{action}' no reconocida"}


if __name__ == "__main__":
    print("\n🤖 KAI AGENTS - STATUS")
    print("="*50)
    print(f"Ollama: {'🟢 Online' if check_ollama_status()['connected'] else '🔴 Offline'}")
    print()
    
    for name, agent in AGENTS.items():
        status = agent.get_status()
        print(f"  {status['name']}: {status['tasks']} tareas | modelo: {status['model']}")
    
    print("\n📝 Test generador:")
    print(AGENTS["dev"].write_code("Calculadora de profits"))
