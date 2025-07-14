from typing import List

from agno.agent import Agent, RunResponse  # noqa
from agno.models.ollama import Ollama
from pydantic import BaseModel, Field
from rich.pretty import pprint  # noqa

class LessonPlan(BaseModel):
    name: str = Field(..., description="Dale un nombre a esta lección o tema")
    subject: str = Field(..., description="Tema principal de la lección (Ej. Matemáticas, Historia, etc.)")
    grade_level: str = Field(..., description="Nivel educativo para esta lección (Ej. Primaria, Secundaria, Universidad)")
    objectives: List[str] = Field(..., description="Objetivos principales de la lección (en formato de lista).")
    materials: List[str] = Field(..., description="Materiales necesarios para la lección (Ej. libros, videos, etc.)")
    activities: List[str] = Field(..., description="Actividades que se realizarán durante la lección.")
    duration: str = Field(..., description="Duración estimada de la lección (Ej. 30 minutos, 1 hora)")
    conclusion: str = Field(..., description="Resumen o cierre de la lección. ¿Qué deberían aprender los estudiantes al finalizar?")


# Agent that returns a structured output
structured_output_agent = Agent(
    model=Ollama(id="llama3.2:latest"),
    description="Tu creas contenido educativo para estudiantes con discapacidad.",
    response_model=LessonPlan,
)

structured_output_response: RunResponse = structured_output_agent.run("Genera un curso sobre HTML")
pprint(structured_output_response.content)

# Run the agent
# structured_output_agent.print_response("back to the future")





