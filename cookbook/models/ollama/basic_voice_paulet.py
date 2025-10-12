from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama  
import sys
import re
import subprocess
import time
from datetime import datetime
import pyaudio
import threading
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

import random

# ============================================
# CONFIGURACIÓN GLOBAL
# ============================================

DEEPGRAM_API_KEY = "7cc7ed130e6393062db37fd0a8618a902485f6f4"  # ⚠️ Reemplaza con tu API Key

# ============================================
# CONFIGURACIÓN DE PAULET
# ============================================

PAULET_SYSTEM_PROMPT = """Eres Paulet y eres el asistente de Jose.

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
# FUNCIONES DE VOZ (SALIDA)
# ============================================

def speak(text, voice='Jorge', rate=175):
    """Reproduce texto usando el sintetizador de voz de macOS"""
    try:
        subprocess.run(['say', '-v', voice, '-r', str(rate), text], check=True)
    except Exception as e:
        print(f"⚠️ Error al reproducir voz: {e}")

# ============================================
# FUNCIONES DE RECONOCIMIENTO DE VOZ (ENTRADA)
# ============================================

class VoiceRecognizer:
    """Clase para manejar el reconocimiento de voz con Deepgram"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.transcribed_text = ""
        self.is_listening = False
        self.lock = threading.Lock()
        self.exit_flag = False
        
    def listen(self):
        """Escucha el micrófono y retorna el texto transcrito"""
        
        if self.api_key == "TU_API_KEY_AQUI":
            print("❌ Necesitas configurar tu API Key de Deepgram")
            return None
        
        try:
            # Crear cliente Deepgram
            deepgram = DeepgramClient(self.api_key)
            dg_connection = deepgram.listen.websocket.v("1")
            
            # Resetear variables
            self.transcribed_text = ""
            self.is_listening = True
            self.exit_flag = False
            
            # Guardar referencia a self para usar en los callbacks
            recognizer = self
            
            # Callback para transcripciones
            def on_message(self, result, **kwargs):
                sentence = result.channel.alternatives[0].transcript
                if len(sentence) == 0:
                    return
                if result.is_final:
                    # Agregar al texto transcrito usando la referencia correcta
                    with recognizer.lock:
                        if recognizer.transcribed_text:
                            recognizer.transcribed_text += " " + sentence
                        else:
                            recognizer.transcribed_text = sentence
                    print(f"✅ {sentence}")
                else:
                    print(f"🔄 {sentence}", end='\r')
            
            def on_open(self, open, **kwargs):
                print("🎤 Conectado. Habla ahora (presiona Enter cuando termines)...")
            
            def on_error(self, error, **kwargs):
                print(f"❌ Error de Deepgram: {error}")
            
            # Registrar eventos
            dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
            dg_connection.on(LiveTranscriptionEvents.Open, on_open)
            dg_connection.on(LiveTranscriptionEvents.Error, on_error)
            
            # Opciones de transcripción
            options = LiveOptions(
                model="nova-2",
                language="es",
                smart_format=True,
                interim_results=True,
                encoding="linear16",
                sample_rate=16000,
                channels=1
            )
            
            # Iniciar conexión
            if dg_connection.start(options) is False:
                print("❌ Falló la conexión a Deepgram")
                return None
            
            # Configuración del micrófono
            CHUNK = 1024 * 4
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            
            # Función del hilo del micrófono
            def microphone_thread():
                p = pyaudio.PyAudio()
                stream = p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK
                )
                
                try:
                    while True:
                        with recognizer.lock:
                            should_exit = recognizer.exit_flag
                        
                        if should_exit:
                            break
                        
                        try:
                            data = stream.read(CHUNK, exception_on_overflow=False)
                            dg_connection.send(data)
                        except Exception as e:
                            print(f"Error leyendo micrófono: {e}")
                            break
                            
                finally:
                    stream.stop_stream()
                    stream.close()
                    p.terminate()
            
            # Iniciar hilo del micrófono
            mic_thread = threading.Thread(target=microphone_thread)
            mic_thread.start()
            
            # Esperar a que el usuario presione Enter
            input()
            
            # Señalar salida usando la referencia correcta
            with recognizer.lock:
                recognizer.exit_flag = True
            
            # Esperar al hilo
            mic_thread.join()
            
            # Cerrar conexión
            dg_connection.finish()
            
            # Pequeña pausa para asegurar que se procese todo
            time.sleep(0.5)
            
            return self.transcribed_text.strip()
            
        except Exception as e:
            print(f"❌ Error en reconocimiento de voz: {e}")
            return None

# ============================================
# FUNCIONES DE UTILIDADES
# ============================================

def get_greeting():
    """Obtiene un saludo apropiado según la hora del día"""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Buenos días"
    elif 12 <= hour < 19:
        return "Buenas tardes"
    else:
        return "Buenas noches"

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
    ║                  🎤 Con Reconocimiento de Voz        ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    print("="*60 + "\n")
    
    # Saludo inicial
    greeting = get_greeting()
    welcome_message = f"{greeting}. Estoy listo para ayudarte."
    
    print(f"🤖 Paulet: {welcome_message}\n")
    speak(welcome_message)
    
    print("💡 Comandos disponibles:")
    print("   • Escribe tu mensaje o presiona SOLO Enter para hablar 🎤")
    print("   • 'desactivar' o 'apagar' - Finalizar sesión")
    print("   • 'silencio' - Desactivar voz de respuesta")
    print("   • 'activar voz' - Reactivar voz de respuesta")
    print("="*60 + "\n")

# ============================================
# CONFIGURACIÓN DEL AGENTE
# ============================================

agent = Agent(
    model=Ollama(id="llama3.2:1b"),
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
    voice_recognizer = VoiceRecognizer(DEEPGRAM_API_KEY)
    conversation_count = 0
    
    while True:
        try:
            # Input del usuario (texto o voz)
            user_input = input("👤 Tú (Enter=🎤 o escribe): ").strip()
            
            # Si presiona Enter sin escribir, activar reconocimiento de voz
            if not user_input:
                print("\n🎤 Modo voz activado...")
                user_input = voice_recognizer.listen()
                
                if not user_input:
                    print("⚠️ No se detectó ningún texto. Intenta de nuevo.\n")
                    continue
                
                print(f"\n📝 Transcripción completa: {user_input}\n")
            
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