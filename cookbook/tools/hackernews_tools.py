from agno.agent import Agent
from agno.tools.hackernews import HackerNewsTools
from agno.models.ollama import Ollama
# Por defecto deberia de funcionar con la api de open ai configurada en .env
# Para mi caso de uso lo utilice con ollama y funciono
# solo se agrego: model=Ollama(id="qwen3:8b")
agent = Agent(
    model=Ollama(id="qwen3:8b"),
    name="Hackernews Team",
    tools=[HackerNewsTools()],
    show_tool_calls=True,
    markdown=True,
)
agent.print_response(
    "Write an engaging summary of the users with the top 2 stories on hackernews. Please mention the stories as well.",
)
