from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama

# qwen3:8b 
# codeqwen:7b
# qwen2.5-coder:14b
agent = Agent(model=Ollama(id="qwen2.5-coder:14b"), markdown=False)

# Get the response in a variable
#run: RunResponse = agent.run("give me code to make a snake game")
run: RunResponse = agent.run("build a recommendation system using collaborative filtering with pandas and numpy")

print(run.content)

# Print the response in the terminal
#agent.print_response("Cual es la capital de Perú?")
