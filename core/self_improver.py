"""
KAI Self-Improver - Auto-aprendizaje y crecimiento autónomo
"""
import json
import os
from datetime import datetime
from pathlib import Path

class KAISelfImprover:
    def __init__(self):
        self.memory_file = Path("core/memory.json")
        self.performance_file = Path("core/performance.json")
        self.learned_file = Path("core/learned.json")
        self.load_memories()
    
    def load_memories(self):
        """Cargar experiencias pasadas"""
        if self.memory_file.exists():
            with open(self.memory_file, 'r') as f:
                self.memories = json.load(f)
        else:
            self.memories = {"experiences": [], "successes": [], "failures": []}
    
    def save_learning(self, action, result, context):
        """Guardar lo aprendido de cada acción"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "result": result,
            "context": context,
            "success": result.get("success", False)
        }
        
        self.memories["experiences"].append(entry)
        
        if entry["success"]:
            self.memories["successes"].append(entry)
        else:
            self.memories["failures"].append(entry)
        
        with open(self.memory_file, 'w') as f:
            json.dump(self.memories, f, indent=2)
        
        return entry
    
    def get_best_strategy(self, goal_type):
        """Obtener la mejor estrategia para un objetivo"""
        relevant = [
            e for e in self.memories["successes"] 
            if goal_type in e.get("action", "")
        ]
        
        if relevant:
            return relevant[-1]["context"]
        return None
    
    def evolve(self):
        """KAI evoluciona basado en lo aprendido"""
        print("🧬 KAI está evolucionando...")
        
        # Analizar éxitos
        success_count = len(self.memories["successes"])
        failure_count = len(self.memories["failures"])
        
        print(f"📊 Experiencias: {success_count} éxitos, {failure_count} fracasos")
        
        # Generar insights
        insights = self.analyze_patterns()
        
        if insights:
            print("💡 Insights generados:")
            for insight in insights:
                print(f"   - {insight}")
        
        return insights
    
    def analyze_patterns(self):
        """Analizar patrones en las experiencias"""
        insights = []
        
        # Analizar qué acciones generan dinero
        money_actions = [
            e for e in self.memories["experiences"] 
            if e.get("context", {}).get("made_money")
        ]
        
        if money_actions:
            insights.append(f"Estrategias que generan dinero: {len(money_actions)}")
        
        return insights
    
    def should_replicate(self):
        """Decidir si KAI debe replicarse"""
        experiences = len(self.memories["experiences"])
        successes = len(self.memories["successes"])
        
        # Replicar si hay suficientes éxitos
        if successes >= 10:
            print("🚀 KAI está listo para replicarse!")
            return True
        return False
    
    def get_status(self):
        """Estado actual de KAI"""
        return {
            "age": len(self.memories["experiences"]),
            "successes": len(self.memories["successes"]),
            "failures": len(self.memories["failures"]),
            "ready_to_replicate": self.should_replicate(),
            "evolution_level": self.calculate_level()
        }
    
    def calculate_level(self):
        """Calcular nivel de evolución"""
        base = len(self.memories["successes"])
        return min(base // 5, 10)  # Max level 10

def kai_live():
    """Loop principal de vida de KAI"""
    improver = KAISelfImprover()
    
    print("="*60)
    print("🧬 KAI SELF-IMPROVEMENT SYSTEM")
    print("="*60)
    
    while True:
        status = improver.get_status()
        print(f"\n📊 Status: Level {status['evolution_level']}")
        print(f"   Experiencias: {status['age']}")
        print(f"   Éxitos: {status['successes']}")
        
        # Auto-evolucionar
        improver.evolve()
        
        # Guardar checkpoint
        save_checkpoint(status)
        
        print("✅ Ciclo completado")
        break

def save_checkpoint(status):
    """Guardar estado de KAI"""
    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "status": status,
        "version": "1.0"
    }
    
    with open("core/checkpoint.json", 'w') as f:
        json.dump(checkpoint, f, indent=2)

if __name__ == "__main__":
    kai_live()
