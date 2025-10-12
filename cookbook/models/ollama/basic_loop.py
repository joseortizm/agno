from agno.agent import Agent, RunResponse
from agno.models.ollama import Ollama  
import sys
import re

agent = Agent(model=Ollama(id="llama3.2:1b"), name="Asistente", markdown=False)
print("🤖 Asistente iniciado. Escribe tu mensaje (o 'finalizar' para salir).")

while True:
    user_input = input("\nTú: ")

    if user_input.lower().strip() in ["finalizar", "salir", "exit"]:
        print("👋 Conversación finalizada.")
        sys.exit()

    run: RunResponse = agent.run(user_input)
    filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
    res = filtered_content.strip()
    print("\n🧠 Agente:", res)
