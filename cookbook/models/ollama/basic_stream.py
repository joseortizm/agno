from typing import Iterator  # noqa
from agno.agent import Agent, RunResponseEvent  # noqa
from agno.models.ollama import Ollama

agent = Agent(model=Ollama(id="qwen3:4b"), markdown=True)

# Get the response in a variable
run_response: Iterator[RunResponseEvent] = agent.run("De que trata el algoritmo Dijkstra", stream=True)
for chunk in run_response:
    print(chunk.content)
    ## \<think>
    ## Okay
    ## ,
    ##  the
    ##  user
    ##  is
    ##  asking
    ##  about
    ##  the
    ##  D
    ## ijkstra
    ##  algorithm
    ## .

# Print the response in the terminal
#agent.print_response("De que trata el algoritmo Dijkstra?", stream=True)
