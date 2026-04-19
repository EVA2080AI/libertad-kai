"""
KAI UX/UI Agent - Diseño de interfaces y experiencia de usuario
Usa Ollama para generar diseños y componentes
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.ollama_ai import ollama_ai
from pathlib import Path

class UXUIAgent:
    """Agente de diseño UX/UI"""
    def __init__(self):
        self.name = "KAI UX/UI"
        self.role = "Diseño de interfaces y experiencia"
        self.model = "gemma3:1b"  # Rápido para diseño
        self.designs = []
        
    def think(self, context: str) -> str:
        """Pensar con Ollama"""
        prompt = f"Eres KAI UX/UI Designer. {context}"
        return ollama_ai.generate(prompt, model=self.model)
    
    def create_design_system(self, project: str) -> str:
        """Crear sistema de diseño"""
        prompt = f"""Proyecto: {project}
Crea un sistema de diseño completo:
1. Paleta de colores (hex codes)
2. Tipografía (Google Fonts)
3. Espaciado y grid
4. Componentes básicos (botones, inputs, cards)
Responde en formato estructurado."""
        return ollama_ai.generate(prompt, model=self.model)
    
    def design_component(self, component: str, style: str = "modern") -> str:
        """Diseñar componente específico"""
        prompt = f"""Diseña un componente: {component}
Estilo: {style}
Incluye:
- Estados (default, hover, active, disabled)
- Dimensiones
- Código Tailwind/CSS
Responde en código funcional."""
        return ollama_ai.generate(prompt, model=self.model)
    
    def create_prototype(self, page: str, features: list) -> str:
        """Crear prototipo de página"""
        prompt = f"""Página: {page}
Features: {', '.join(features)}
Crea un prototipo HTML/CSS/Tailwind funcional.
Incluye layout, componentes y micro-interacciones."""
        return ollama_ai.generate(prompt, model=self.model)
    
    def analyze_ux(self, description: str) -> str:
        """Analizar UX de una interfaz"""
        prompt = f"""Analiza la UX de: {description}
Da sugerencias de:
1. Mejoras de usabilidad
2. Accesibilidad
3. Journey del usuario
4. Pain points
Responde en bullet points."""
        return ollama_ai.generate(prompt, model=self.model)
    
    def create_color_palette(self, mood: str) -> dict:
        """Crear paleta de colores"""
        result = self.think(f"Crea paleta de colores para: {mood}")
        return {
            "mood": mood,
            "analysis": result,
            "colors": {
                "primary": "#00ff88",
                "secondary": "#00d4ff",
                "background": "#0a0a0f",
                "surface": "#1a1a2e",
                "text": "#ffffff"
            }
        }
    
    def get_status(self) -> dict:
        return {
            "name": self.name,
            "role": self.role,
            "designs": len(self.designs),
            "model": self.model
        }


if __name__ == "__main__":
    agent = UXUIAgent()
    print("\n🎨 KAI UX/UI AGENT")
    print("="*50)
    status = agent.get_status()
    print(f"Name: {status['name']}")
    print(f"Role: {status['role']}")
    print(f"Model: {status['model']}")
    print()
    
    # Test
    print("📝 Test: Diseño de botón...")
    btn = agent.design_component("Botón principal")
    print(btn[:300])
