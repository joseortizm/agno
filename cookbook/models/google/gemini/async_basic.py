import asyncio

from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini

agent = Agent(
    model=Gemini(
        id="gemini-2.0-flash",
        instructions=["Tu eres un docente especializado en ayudar a los estudiantes con discapacidad a desarrollar habilidades digitales"],
    ),
    markdown=True,
)

# Get the response in a variable
run: RunResponse = agent.run("Que recomendación puedes dar a un estudiante que tiene dificultad para concentrase? Genera máximo 3 parrafos con recomendaciones.")
print(run.content)

# Print the response in the terminal
# asyncio.run(agent.aprint_response("Share a 2 sentence horror story"))
