# Updates to Run Objects (Enero 2026): 
from agno.agent import Agent, RunOutput
from agno.utils.pprint import pprint_run_response
from agno.models.ollama import Ollama

# mistral-nemo:12b
# phi3:3.8b
# gemma2:9b
agent = Agent(model=Ollama(id="gemma2:9b"), markdown=False)
# Run agent with input="Trending startups and products."
response: RunOutput = agent.run(input="Cual es la capital de Colombia? Se breve y amigable.")
# Print the response in markdown format
pprint_run_response(response, markdown=True)

"""
# old version
# ImportError: cannot import name 'RunResponse' from 'agno.agent'

from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama

agent = Agent(model=Ollama(id="llama3.2:latest"), markdown=False)

# Get the response in a variable
run: RunResponse = agent.run("Cual es la capital de Colombia? Se breve y amigable.")
print(run.content)

# Print the response in the terminal
#agent.print_response("Cual es la capital de Perú?")
"""

