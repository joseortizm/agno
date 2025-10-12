from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama  
import sys
import re
import subprocess

def speak_say(text):
    """Usar el comando 'say' nativo de macOS"""
    try:
        # El comando 'say' de macOS es muy confiable
        subprocess.run(['say', text], check=True)
    except Exception as e:
        print(f"⚠️ Error al hablar: {e}")

agent = Agent(model=Ollama(id="llama3.2:1b"), name="Asistente", markdown=False)
print("🤖 Asistente iniciado. Escribe tu mensaje (o 'finalizar' para salir).")

while True:
    user_input = input("\nTú: ")
    
    if user_input.lower().strip() in ["finalizar", "salir", "exit"]:
        print("👋 Conversación finalizada.")
        sys.exit()
    
    # Ejecutar el agente
    run: RunResponse = agent.run(user_input)
    filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
    res = filtered_content.strip()
    
    print("\n🧠 Agente:", res)
    
    # Hablar usando el comando nativo de macOS
    speak_say(res)

# Solo daba verbalizacion en primera respuesta, se modifico para usar el nativo
"""
import pyttsx3
from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama  
import sys
import re
import time



# Función para iniciar el motor de voz
def init_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Ajustar la velocidad (opcional)
    return engine

engine = init_engine() 

agent = Agent(model=Ollama(id="llama3.2:1b"), name="Asistente", markdown=False)
print("🤖 Asistente iniciado. Escribe tu mensaje (o 'finalizar' para salir).")

while True:
    user_input = input("\nTú: ")

    if user_input.lower().strip() in ["finalizar", "salir", "exit"]:
        print("👋 Conversación finalizada.")
        engine.stop()
        sys.exit()

    # Ejecutar el agente
    run: RunResponse = agent.run(user_input)
    filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
    res = filtered_content.strip()

    # Imprimir y leer la respuesta
    print("\n🧠 Agente:", res)

    # Leer la respuesta en voz alta usando pyttsx3
    engine.say(res)
    engine.runAndWait()  # Espera a que termine de hablar
    #engine.stop()



"""