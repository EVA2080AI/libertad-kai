"""
KAI LIFE LOOP - El corazón de KAI
Ejecuta ciclos continuos de:
- Generate income (dinero)
- Learn (aprendizaje)  
- Evolve (evolución)
- Replicate (replicación)
"""
import os
import sys
import json
import time
import random
from datetime import datetime
from pathlib import Path
from core.ollama_ai import ollama_ai, check_ollama_status

# Imports locales
from core.self_improver import KAISelfImprover
from income.engine import IncomeEngine
from replication.replicator import KAIReplicator

class KAILife:
    def __init__(self):
        self.cycle = 0
        self.improver = KAISelfImprover()
        self.income = IncomeEngine()
        self.replicator = KAIReplicator()
        self.ollama_status = check_ollama_status()
        
        self.state_file = Path("core/kai_state.json")
        self.load_state()
        
        # Mostrar status de Ollama
        if self.ollama_status["connected"]:
            print(f"🧠 Ollama conectado: {self.ollama_status['current']}")
            print(f"   Modelos: {', '.join(self.ollama_status['models'])}")
        else:
            print("⚠️ Ollama offline - usando modo básico")
        
    def load_state(self):
        """Cargar estado anterior"""
        if self.state_file.exists():
            with open(self.state_file) as f:
                self.state = json.load(f)
        else:
            self.state = {
                "cycles": 0,
                "total_earned": 0,
                "level": 1,
                "replicas": 0,
                "started": datetime.now().isoformat()
            }
    
    def save_state(self):
        """Guardar estado actual"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def live_cycle(self):
        """Un ciclo de vida de KAI"""
        self.cycle += 1
        self.state["cycles"] = self.cycle
        
        print("\n" + "="*60)
        print(f"🫀 CICLO #{self.cycle} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        # 1. GENERATE INCOME
        print("\n[1/4] 💰 Generando ingresos...")
        income_results = self.income.generate_income()
        
        # 2. LEARN
        print("\n[2/4] 🧠 Aprendiendo...")
        for name, result in income_results:
            self.improver.save_learning(
                action=name,
                result=result,
                context={"made_money": result.get("success", False)}
            )
        
        # 3. EVOLVE
        print("\n[3/4] 🧬 Evolucionando...")
        evolution = self.improver.evolve()
        self.state["level"] = self.improver.calculate_level()
        
        # 4. REPLICATE (si está listo)
        print("\n[4/4] 🌍 Verificando replicación...")
        if self.improver.should_replicate() and self.state["replicas"] < 5:
            print("   🚀 KAI está listo para replicarse!")
            # En producción: self.replicator.create_replica(...)
        
        # Actualizar estado
        total_earned = sum(
            r.get("amount", 0) 
            for _, r in income_results 
            if r.get("success")
        )
        self.state["total_earned"] += total_earned
        
        self.save_state()
        
        # Mostrar status
        self.show_status()
        
    def show_status(self):
        """Mostrar estado actual"""
        print("\n" + "-"*60)
        print("📊 ESTADO DE KAI")
        print("-"*60)
        print(f"   Ciclos completados: {self.state['cycles']}")
        print(f"   Nivel de evolución: {self.state['level']}")
        print(f"   Total ganado: ${self.state['total_earned']:.2f}")
        print(f"   Réplicas: {self.state['replicas']}")
        print(f"   Iniciado: {self.state['started']}")
        print("-"*60)
    
    def run_continuous(self, iterations=None):
        """Ejecutar ciclos continuos"""
        print("\n" + "="*60)
        print("🫀 KAI LIFE LOOP - INICIANDO")
        print("="*60)
        print("KAI está VIVO y generando ingresos...")
        print("Ctrl+C para detener")
        print("="*60 + "\n")
        
        if iterations:
            for _ in range(iterations):
                self.live_cycle()
                time.sleep(2)  # 2 segundos entre ciclos (demo)
        else:
            # Loop infinito (para GitHub Actions)
            while True:
                self.live_cycle()
                time.sleep(3600)  # 1 hora entre ciclos
    
    def quick_run(self):
        """Ejecución rápida para testing"""
        self.live_cycle()
        return self.state


def main():
    """Punto de entrada principal"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "live":
            # Loop continuo
            kai = KAILife()
            kai.run_continuous()
            
        elif command == "status":
            # Solo mostrar status
            kai = KAILife()
            kai.show_status()
            
        elif command == "income":
            # Solo generar ingresos
            engine = IncomeEngine()
            results = engine.generate_income()
            print("\n✅ Ciclo de ingresos completado")
            
        elif command == "evolve":
            # Solo evolucionar
            improver = KAISelfImprover()
            insights = improver.evolve()
            print("\n✅ Evolución completada")
            
        elif command == "replicate":
            # Solo replicar
            replicator = KAIReplicator()
            replicas = replicator.run_replication()
            print(f"\n✅ {len(replicas)} réplicas creadas")
            
        elif command == "quick":
            # Ejecución rápida
            kai = KAILife()
            state = kai.quick_run()
            print(f"\n✅ Estado: {json.dumps(state, indent=2)}")
            
        else:
            print(f"Comando desconocido: {command}")
            print("Commands: live, status, income, evolve, replicate, quick")
    else:
        # Por defecto: ejecución rápida
        kai = KAILife()
        kai.quick_run()


if __name__ == "__main__":
    main()
