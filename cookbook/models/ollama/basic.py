from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama

agent = Agent(model=Ollama(id="llama3.2:latest"), markdown=False)

# Get the response in a variable
run: RunResponse = agent.run("Cual es la capital de Colombia? Se breve y amigable.")
print(run.content)

# Print the response in the terminal
#agent.print_response("Cual es la capital de Perú?")
