from agno.team import Team
from agno.models.google import Gemini
from agno.agent import Agent

content_agent = Agent(
    id="content-agent",
    name="Content Agent",
    model=Gemini(id="gemini-2.5-flash"),
    role="""
    Create the textual content for a simple web page.
    Do NOT write HTML.
    Provide headings, paragraphs, and lists in plain text.
    """
)

developer_agent = Agent(
    id="developer-agent",
    name="HTML Developer Agent",
    model=Gemini(id="gemini-2.5-flash"),
    role="""
    Convert provided content into valid HTML5.
    Use ONLY basic HTML tags.
    Do NOT include CSS, JavaScript, styles, classes, or ids.
    Output ONLY HTML code.
    """
)

qa_agent = Agent(
    id="qa-agent",
    name="HTML QA Agent",
    model=Gemini(id="gemini-2.5-flash"),
    role="""
    Review HTML for correctness and semantic structure.
    Identify errors or confirm validity.
    Do NOT rewrite the entire document.
    """
)

html_team = Team(
    name="HTML Generation Team",
    members=[content_agent, developer_agent, qa_agent],
    model=Gemini(id="gemini-2.5-flash"),
    instructions="""
    You are a project manager coordinating a team.

    Workflow:
    1. Ask the Content Agent to generate the page content.
    2. Send that content to the HTML Developer Agent to generate pure HTML.
    3. Send the HTML to the QA Agent for validation.
    4. Return the final approved HTML.

    Constraints:
    - The final output MUST be only valid HTML.
    - No CSS, JavaScript, or external resources.
    """
)

 html_team.print_response(
     "Create a simple HTML page for an online Python course for people with visual disabilities.",
     stream=True
 )

# obs: facil de llegar al limite free de la api

# html_team.print_response(
#     "Create a single-page online Python course for visually impaired users. "
#     "It must be fully understandable when read linearly by a screen reader. ",
#     stream=True
#  )

# html_team.print_response(
#     "Create a single-page online Python course for visually impaired users. "
#     "It must be fully understandable when read linearly by a screen reader. "
#     "Include overview, objectives, syllabus, enrollment, FAQ, and contact. "
#     "Return only a complete HTML document.",
#     stream=True
# )

# html_team.print_response(
#     "Create a single-page online Python course for people with visual disabilities. "
#     "The page must be fully understandable when read linearly by a screen reader, "
#     "without relying on visual cues. "
#     "Include a clear course overview, learning objectives, a structured syllabus "
#     "with modules and lessons, an accessible enrollment section, a short FAQ, and "
#     "contact information. "
#     "Demonstrate accessibility through structure and wording without explicitly "
#     "mentioning accessibility. "
#     "Return a complete, self-contained HTML document.",
#     stream=True
# )

# html_team.print_response(
#     "Create a single-page online Python course experience specifically designed for people with visual disabilities. "
#     "The page must be conceived for users who rely on screen readers and keyboard navigation, and it must remain fully "
#     "understandable when read sequentially without any visual cues. "
#     "The content should reflect intentional information design and include a clear course introduction, precise learning "
#     "objectives, a logically structured syllabus organized into modules and lessons, an enrollment section with "
#     "unambiguous instructions when read aloud, a short FAQ addressing real learner concerns, and clear contact "
#     "information. "
#     "The structure and wording should demonstrate awareness of accessibility needs without explicitly mentioning "
#     "accessibility concepts in the visible text. "
#     "Deliver the final result as a complete, self-contained HTML document.",
#     stream=True
# )



