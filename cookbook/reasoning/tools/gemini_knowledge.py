# https://docs.agno.com/vectordb/lancedb#lancedb-params
# pip install lancedb 
# pip install tantivy

from pathlib import Path
from agno.agent import Agent
from agno.knowledge.text import TextKnowledgeBase
from agno.embedder.google import GeminiEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.models.google import Gemini

# Create LanceDB with Gemini embedder
vector_db = LanceDb(
    table_name="text_documents",
    uri="tmp/lancedb",
    search_type=SearchType.hybrid,  # Combines vector + keyword search
    embedder=GeminiEmbedder(dimensions=1536),
    #embedder=GeminiEmbedder(
    #    dimensions=768,  # Gemini default
    #    model="models/text-embedding-004"
    #),
    #embedder=GeminiEmbedder(
    #    "text-embedding-004",  # Nota: SIN el prefijo "models/"
    #    dimensions=768
    #),
)

# Create knowledge base from text files
knowledge_base = TextKnowledgeBase(
    path="data_examples/python.txt",  # Path to your text files directory
    vector_db=vector_db,
)

# Load the knowledge base
knowledge_base.load(recreate=True)  # Set to False after first run

# Create agent
agent = Agent(
    knowledge=knowledge_base,
    search_knowledge=True,
    show_tool_calls=True,
    markdown=True,
    model=Gemini(
        id="gemini-2.0-flash",
        instructions=["Tu eres un docente especializado en ayudar a los estudiantes con discapacidad a desarrollar habilidades digitales"],
    ),
)

#agent.print_response("De que trata el curso de HTML?", stream=True)
agent.print_response("Cual es el proyecto final del curso python?", stream=True)