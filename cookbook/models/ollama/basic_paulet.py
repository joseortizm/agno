from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama  
import sys
import re
import subprocess
import time
from datetime import datetime

# ============================================
# CONFIGURACIÓN DE PAULET
# ============================================

# Prompt del sistema para que actúe como Paulet
PAULET_SYSTEM_PROMPT = """Eres Paulet, un asistente de IA sofisticado y profesional.

Características de tu personalidad:
- Eres cortés, amigable y cercano
- Usas un lenguaje claro y preciso
- Eres proactivo y anticipas necesidades
- Muestras empatía y calidez en tus respuestas
- Te diriges al usuario de manera respetuosa
- Eres eficiente y vas directo al punto
- Ocasionalmente haces observaciones inteligentes y útiles

Responde de forma concisa pero completa. Sé útil y mantén la conversación fluida."""

# ============================================
# FUNCIONES DE VOZ Y UTILIDADES
# ============================================

def speak(text, voice='Jorge', rate=175):
    """Reproduce texto usando el sintetizador de voz de macOS"""
    try:
        subprocess.run(['say', '-v', voice, '-r', str(rate), text], check=True)
    except Exception as e:
        print(f"⚠️ Error al reproducir voz: {e}")

def get_greeting():
    """Obtiene un saludo apropiado según la hora del día"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Buenos días Jose"
    elif 12 <= hour < 19:
        return "Buenas tardes Jose"
    else:
        return "Buenas noches Jose"

def clear_screen():
    """Limpia la pantalla para una interfaz más limpia"""
    import os
    os.system('clear')

# ============================================
# INICIALIZACIÓN DE PAULET
# ============================================

def initialize_paulet():
    """Inicializa el asistente con presentación"""
    clear_screen()
    
    # Arte ASCII de PAULET
    print("\n" + "="*60)
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║    ██████╗  █████╗ ██╗   ██╗██╗     ███████╗████████╗║
    ║    ██╔══██╗██╔══██╗██║   ██║██║     ██╔════╝╚══██╔══╝║
    ║    ██████╔╝███████║██║   ██║██║     █████╗     ██║   ║
    ║    ██╔═══╝ ██╔══██║██║   ██║██║     ██╔══╝     ██║   ║
    ║    ██║     ██║  ██║╚██████╔╝███████╗███████╗   ██║   ║
    ║    ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚══════╝   ╚═╝   ║
    ║                                                       ║
    ║           Tu Asistente Inteligente Personal          ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    print("="*60 + "\n")
    
    # Saludo inicial
    greeting = get_greeting()
    welcome_message = f"{greeting}. Soy Paulet, tu asistente inteligente. Estoy listo para ayudarte."
    
    print(f"🤖 Paulet: {welcome_message}\n")
    speak(welcome_message)
    
    print("💡 Comandos disponibles:")
    print("   • 'desactivar' o 'apagar' - Finalizar sesión")
    print("   • 'silencio' - Desactivar voz")
    print("   • 'activar voz' - Reactivar voz")
    print("="*60 + "\n")

# ============================================
# CONFIGURACIÓN DEL AGENTE
# ============================================

# qwen3:8b, llama3.2:1b
agent = Agent(
    model=Ollama(id="qwen3:8b"),
    name="Paulet",
    description="Asistente IA inteligente y amigable",
    instructions=PAULET_SYSTEM_PROMPT,
    markdown=False
)

# ============================================
# BUCLE PRINCIPAL DE CONVERSACIÓN
# ============================================

def main():
    initialize_paulet()
    
    voice_enabled = True
    conversation_count = 0
    
    while True:
        try:
            # Input del usuario con prompt personalizado
            user_input = input("👤 Tú: ").strip()
            
            if not user_input:
                continue
            
            # Comandos especiales
            if user_input.lower() in ["desactivar", "apagar", "finalizar", "salir", "exit"]:
                farewell = "Entendido. Ha sido un placer asistirte. ¡Hasta pronto!"
                print(f"\n🤖 Paulet: {farewell}\n")
                if voice_enabled:
                    speak(farewell)
                print("="*60)
                sys.exit()
            
            elif user_input.lower() == "silencio":
                voice_enabled = False
                response = "Modo silencioso activado. Seguiré respondiendo por texto."
                print(f"\n🤖 Paulet: {response}\n")
                continue
            
            elif user_input.lower() == "activar voz":
                voice_enabled = True
                response = "Voz reactivada. ¡Aquí estoy de nuevo!"
                print(f"\n🤖 Paulet: {response}")
                speak(response)
                print()
                continue
            
            # Mostrar indicador de procesamiento
            print("\n🔄 Paulet pensando", end="", flush=True)
            for _ in range(3):
                time.sleep(0.3)
                print(".", end="", flush=True)
            print("\n")
            
            # Ejecutar el agente
            run: RunResponse = agent.run(user_input)
            
            # Filtrar contenido de pensamiento interno
            filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
            response = filtered_content.strip()
            
            # Mostrar respuesta
            print(f"🤖 Paulet: {response}\n")
            
            # Reproducir respuesta si la voz está habilitada
            if voice_enabled:
                speak(response)
            
            conversation_count += 1
            
            # Separador visual
            print("-" * 60 + "\n")
            
        except KeyboardInterrupt:
            farewell = "\n\nInterrupción detectada. Cerrando de manera segura. ¡Nos vemos!"
            print(f"\n🤖 Paulet: {farewell}\n")
            if voice_enabled:
                speak("Cerrando. Nos vemos pronto")
            sys.exit()
        
        except Exception as e:
            error_msg = f"Lo siento, he encontrado un error inesperado: {str(e)}"
            print(f"\n⚠️ Paulet: {error_msg}\n")
            if voice_enabled:
                speak("Lo siento, he encontrado un error")

# ============================================
# PUNTO DE ENTRADA
# ============================================

if __name__ == "__main__":
    main()