# use langgraph to create a report agent

import os
from typing import Optional, Any, Dict
from pathlib import Path

# Import Jinja2 for template rendering
try:
    from jinja2 import Environment, FileSystemLoader
    JINJA2_AVAILABLE = True
except ImportError:
    print("Warning: jinja2 not available. Template rendering disabled.")
    JINJA2_AVAILABLE = False

# Import langgraph components
try:
    from langgraph.graph import StateGraph, START, END
    LANGGRAPH_AVAILABLE = True
except ImportError:
    print("Warning: langgraph not available. AI features disabled.")
    LANGGRAPH_AVAILABLE = False

# use gemini api to generate a report
try:
    from langchain_google_genai import GoogleGenerativeAI
    LANGCHAIN_AVAILABLE = True
except ImportError:
    print("Warning: langchain-google-genai not available. AI features disabled.")
    LANGCHAIN_AVAILABLE = False

# Try to import Ollama as fallback
try:
    from langchain_ollama import OllamaLLM
    OLLAMA_AVAILABLE = True
except ImportError:
    print("Warning: langchain-ollama not available. Ollama fallback disabled.")
    OLLAMA_AVAILABLE = False

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize LLM with fallback to Ollama
llm: Optional[Any] = None
if GEMINI_API_KEY and LANGCHAIN_AVAILABLE:
    try:
        llm = GoogleGenerativeAI(model="gemini-2.0-flash-001")
        print("Using Google Generative AI (Gemini)")
    except Exception as e:
        print(f"Warning: Could not initialize Google Generative AI: {e}")
        llm = None

# Fallback to Ollama if Gemini is not available
if llm is None and OLLAMA_AVAILABLE:
    try:
        llm = OllamaLLM(model="llama3.2")
        print("Using Ollama with llama3.2 model")
    except Exception as e:
        print(f"Warning: Could not initialize Ollama: {e}")
        llm = None

if llm is None:
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set.")
    if not LANGCHAIN_AVAILABLE:
        print("Warning: langchain-google-genai not available.")
    if not OLLAMA_AVAILABLE:
        print("Warning: langchain-community not available for Ollama.")
    print("AI-powered features will be disabled.")


# create a state graph
if LANGGRAPH_AVAILABLE and llm and not isinstance(llm, OllamaLLM):
    # Only use StateGraph with non-Ollama LLMs
    graph: Optional[StateGraph] = StateGraph(llm)  # create a state graph

    # create a state
    state: dict = {
        "messages": [],
        "report": None
    }
else:
    graph = None
    state = None

# create a function to generate a report
def generate_report(state):
    return {"report": "This is a report"}


# create a function to save a report
def save_report(state):
    return {"report": "This is a report"}


# create a function to display a report
def display_report(state):
    return {"report": "This is a report"}


# create a state transition
if graph is not None and state is not None:
    graph.add_node("generate_report", generate_report)
    graph.add_node("save_report", save_report)
    graph.add_node("display_report", display_report)

    graph.add_edge(START, "generate_report")
    graph.add_edge("generate_report", "save_report")
    graph.add_edge("save_report", "display_report")
    graph.add_edge("display_report", END)
    graph.compile()

    # run the graph
    result = graph.invoke(state)

    # print the report
    if result and "report" in result:
        print(result["report"])
    else:
        print("No report generated")
elif llm is not None and isinstance(llm, OllamaLLM):
    # Use Ollama directly without StateGraph
    print("Using Ollama for report generation...")
    try:
        # Simple prompt for report generation
        prompt = "Generate a brief project report summary."
        response = llm.invoke(prompt)
        print(f"Ollama Report: {response}")
    except Exception as e:
        print(f"Error generating report with Ollama: {e}")
        print("Fallback report - AI features disabled")
else:
    print("AI features not available - using fallback report generation")
    fallback_report = {"report": "Fallback report - AI features disabled"}
    print(fallback_report["report"])


# Template loading functions
def load_templates(language: str = "en") -> Dict[str, Any]:
    """Load templates for the specified language"""
    if not JINJA2_AVAILABLE:
        print("Warning: Jinja2 not available. Using default templates.")
        return {}
    
    try:
        template_dir = Path(f"templates_{language}")
        if not template_dir.exists():
            print(f"Warning: Template directory {template_dir} not found. Using English.")
            template_dir = Path("templates_en")
        
        env = Environment(loader=FileSystemLoader(template_dir))
        
        templates = {}
        for template_name in ["system_prompt", "user_prompt", "user_form"]:
            try:
                template = env.get_template(f"{template_name}.jinja")
                templates[template_name] = template
            except Exception as e:
                print(f"Warning: Could not load {template_name} template: {e}")
        
        return templates
    except Exception as e:
        print(f"Warning: Could not load templates: {e}")
        return {}


def generate_report_with_templates(
    llm, 
    project_data: Dict[str, Any], 
    language: str = "en"
) -> str:
    """Generate a report using templates and the specified language"""
    templates = load_templates(language)
    
    if not templates:
        return "Template rendering not available."
    
    try:
        # Render the user form with project data
        if "user_form" in templates:
            user_form = templates["user_form"].render(**project_data)
        else:
            user_form = str(project_data)
        
        # Create the system prompt
        if "system_prompt" in templates:
            system_prompt = templates["system_prompt"].render()
        else:
            system_prompt = "You are an expert report writer."
        
        # Create the user prompt
        if "user_prompt" in templates:
            user_prompt = templates["user_prompt"].render(
                input_data=user_form,
                project_name=project_data.get("field1", "Project"),
                **project_data
            )
        else:
            user_prompt = f"Generate a report for: {user_form}"
        
        # Combine prompts
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        
        # Generate report using LLM
        if llm:
            response = llm.invoke(full_prompt)
            return response
        else:
            return "LLM not available for report generation."
            
    except Exception as e:
        print(f"Error generating report with templates: {e}")
        return f"Error generating report: {e}"


# Example usage function
def generate_language_report(project_data: Dict[str, Any], language: str = "en") -> str:
    """Generate a report in the specified language using templates"""
    return generate_report_with_templates(llm, project_data, language)      