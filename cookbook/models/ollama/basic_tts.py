from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama
import pyttsx3
import re


agent = Agent(model=Ollama(id="llama3.2:1b"), markdown=False)
#agent = Agent(model=Ollama(id="llama3.2:latest"), markdown=False)
#agent = Agent(model=Ollama(id="qwen3:8b"), markdown=False)
engine = pyttsx3.init()

run: RunResponse = agent.run("Cual es la capital de Colombia? Se breve y amigable.")
filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
res = filtered_content.strip()
engine.say(res)
engine.runAndWait()

# Print the response in the terminal
#agent.print_response("Cual es la capital de Perú?")

