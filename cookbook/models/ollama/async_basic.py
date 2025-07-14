import asyncio

from agno.agent import Agent
from agno.models.ollama import Ollama

agent = Agent(
    model=Ollama(id="llama3.2:latest"),
    description="Tu eres un especialista en empleabilidad y contratación de personas con discapacidad",
    instructions=["Las recomendaciones debes de explicarlas de forma sencillay máximo 3"],
)
# -*- Print a response to the cli
asyncio.run(agent.aprint_response("Si voy a tener mi entrevista de trabajo, necesito recomendaciones", markdown=True))
