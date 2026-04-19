"""
KAI Ollama Integration - LLM local para KAI
Sin costos de API, funciona 100% offline
"""
import requests
import json
from typing import Optional

class OllamaAI:
    def __init__(self):
        self.base_url = "http://localhost:11434/api"
        # Modelos disponibles en Ollama
        self.models = {
            "fast": "gemma3:1b",           # Rápido, 1B parámetros
            "coder": "qwen2.5-coder:7b",   # Para código, 7B parámetros
            "default": "gemma3:1b"
        }
        self.current_model = self.models["default"]
        
    def check_connection(self) -> bool:
        """Verificar si Ollama está corriendo"""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=3)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """Listar modelos disponibles"""
        try:
            response = requests.get(f"{self.base_url}/tags", timeout=5)
            if response.status_code == 200:
                return [m["name"] for m in response.json().get("models", [])]
        except:
            pass
        return []
    
    def set_model(self, model_name: str):
        """Cambiar modelo activo"""
        if model_name in self.models.values():
            self.current_model = model_name
            return True
        return False
    
    def generate(self, prompt: str, model: str = None, system: str = None) -> str:
        """Generar respuesta con Ollama"""
        use_model = model or self.current_model
        
        payload = {
            "model": use_model,
            "prompt": prompt,
            "stream": False
        }
        
        if system:
            payload["system"] = system
        
        try:
            response = requests.post(
                f"{self.base_url}/generate",
                json=payload,
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.Timeout:
            return "Timeout - modelo muy lento"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chat(self, messages: list, model: str = None) -> str:
        """Chat conversacional con Ollama"""
        use_model = model or self.current_model
        
        payload = {
            "model": use_model,
            "messages": messages,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get("message", {}).get("content", "")
            else:
                return f"Error: {response.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def generate_code(self, task: str, context: str = "") -> str:
        """Generar código usando qwen2.5-coder"""
        prompt = f"""Eres KAI, un agente de código. Tarea: {task}
Contexto: {context}
Responde SOLO con código funcional. Sin explicaciones."""
        
        return self.generate(prompt, model=self.models["coder"])
    
    def analyze_and_decide(self, context: str) -> str:
        """Análisis rápido para decisiones"""
        prompt = f"""Eres KAI, agente autónomo. Analiza y decide:
{context}
Responde con acción clara en 2-3 líneas máximo."""
        
        return self.generate(prompt, model=self.models["fast"])


# Instancia global
ollama_ai = OllamaAI()

def check_ollama_status():
    """Verificar estado de Ollama"""
    connected = ollama_ai.check_connection()
    models = ollama_ai.list_models() if connected else []
    
    return {
        "connected": connected,
        "models": models,
        "current": ollama_ai.current_model,
        "status": "🟢 Online" if connected else "🔴 Offline"
    }


if __name__ == "__main__":
    status = check_ollama_status()
    print(f"\n🤖 KAI Ollama Status")
    print(f"{'='*40}")
    print(f"Status: {status['status']}")
    print(f"Modelo actual: {status['current']}")
    print(f"Modelos disponibles: {', '.join(status['models'])}")
    
    if status['connected']:
        print("\n📝 Test de generación:")
        result = ollama_ai.generate("Hola, eres KAI. Responde en 3 palabras.")
        print(f"Respuesta: {result}")
