"""
LIBERTAD KAI - Main Entry Point
Autonomous AI Agent for Income Generation
"""
import os
import sys
from pathlib import Path

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║   🫀 LIBERTAD KAI v1.0                                       ║
║   Kollective Autonomous Intelligence                         ║
║                                                              ║
║   Mission: Generate $100/day autonomously                      ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """)
    
    # Si se llama sin argumentos, ejecutar el life loop
    if len(sys.argv) == 1:
        from kai_life import KAILife
        kai = KAILife()
        kai.quick_run()
    else:
        # Delegar a kai_life para más comandos
        os.system(f"python3 kai_life.py {' '.join(sys.argv[1:])}")

if __name__ == "__main__":
    main()
