from agno.agent import Agent, RunResponse  
from agno.tools.hackernews import HackerNewsTools
from agno.models.ollama import Ollama
import pyttsx3
import re

engine = pyttsx3.init()
agent = Agent(
    model=Ollama(id="qwen3:8b"),
    name="Hackernews Team",
    tools=[HackerNewsTools()],
    show_tool_calls=True,
    markdown=True,
)
run: RunResponse = agent.run("Escribe un resumen atractivo de los usuarios con las dos historias más importantes en HackerNews. Menciona también las historias.")
filtered_content = re.sub(r'<think>.*?</think>', '', run.content, flags=re.DOTALL)
res = filtered_content.strip()
engine.say(res)
engine.runAndWait()