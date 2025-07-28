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

# Agent state definition
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    project_data: Dict[str, Any]
    language: str
    templates: Dict[str, Any]
    report: Optional[str]
    status: str


# create a function to load templates
def load_templates_agent(state: AgentState) -> AgentState:
    """Load templates for the specified language"""
    language = state.get("language", "en")
    
    if not JINJA2_AVAILABLE:
        state["status"] = "Template rendering not available"
        return state
    
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
        
        state["templates"] = templates
        state["status"] = "Templates loaded successfully"
        return state
        
    except Exception as e:
        print(f"Warning: Could not load templates: {e}")
        state["templates"] = {}
        state["status"] = f"Template loading failed: {e}"
        return state


# create a function to generate a report
def generate_report_agent(state: AgentState) -> AgentState:
    """Generate a report using templates and AI"""
    templates = state.get("templates", {})
    project_data = state.get("project_data", {})
    
    if not templates:
        state["report"] = "Template rendering not available."
        state["status"] = "No templates available"
        return state
    
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
            state["report"] = response
            state["status"] = "Report generated successfully"
        else:
            state["report"] = "LLM not available for report generation."
            state["status"] = "No LLM available"
            
    except Exception as e:
        print(f"Error generating report with templates: {e}")
        state["report"] = f"Error generating report: {e}"
        state["status"] = f"Report generation failed: {e}"
    
    return state


# create a function to save a report
def save_report_agent(state: AgentState) -> AgentState:
    """Save the generated report (placeholder for future implementation)"""
    report = state.get("report", "")
    if report and report != "Template rendering not available.":
        # Here you could save to database, file, etc.
        state["status"] = "Report saved successfully"
    else:
        state["status"] = "No report to save"
    return state


# create a function to display a report
def display_report_agent(state: AgentState) -> AgentState:
    """Display the generated report"""
    report = state.get("report", "")
    if report:
        print(f"Generated Report ({state.get('language', 'en')}):")
        print("=" * 50)
        print(report)
        print("=" * 50)
        state["status"] = "Report displayed successfully"
    else:
        state["status"] = "No report to display"
    return state


# Agent is ready for use - will be invoked when generate_language_report is called


# # Template loading functions
# def load_templates(language: str = "en") -> Dict[str, Any]:
#     """Load templates for the specified language"""
#     if not JINJA2_AVAILABLE:
#         print("Warning: Jinja2 not available. Using default templates.")
#         return {}
    
#     try:
#         template_dir = Path(f"templates_{language}")
#         if not template_dir.exists():
#             print(f"Warning: Template directory {template_dir} not found. Using English.")
#             template_dir = Path("templates_en")
        
#         env = Environment(loader=FileSystemLoader(template_dir))
        
#         templates = {}
#         for template_name in ["system_prompt", "user_prompt", "user_form"]:
#             try:
#                 template = env.get_template(f"{template_name}.jinja")
#                 templates[template_name] = template
#             except Exception as e:
#                 print(f"Warning: Could not load {template_name} template: {e}")
        
#         return templates
#     except Exception as e:
#         print(f"Warning: Could not load templates: {e}")
#         return {}


# def generate_report_with_templates(
#     llm, 
#     project_data: Dict[str, Any], 
#     language: str = "en"
# ) -> str:
#     """Generate a report using templates and the specified language with agentic flow"""
    
#     # Create initial state
#     initial_state = AgentState(
#         messages=[],
#         project_data=project_data,
#         language=language,
#         templates={},
#         report=None,
#         status="Initialized"
#     )
    
#     # Use agentic flow if LangGraph is available
#     if LANGGRAPH_AVAILABLE and llm and not isinstance(llm, OllamaLLM):
#         try:
#             # Create graph with agentic functions
#             graph = StateGraph(AgentState)
            
#             graph.add_node("load_templates", load_templates_agent)
#             graph.add_node("generate_report", generate_report_agent)
#             graph.add_node("save_report", save_report_agent)
#             graph.add_node("display_report", display_report_agent)

#             graph.add_edge(START, "load_templates")
#             graph.add_edge("load_templates", "generate_report")
#             graph.add_edge("generate_report", "save_report")
#             graph.add_edge("save_report", "display_report")
#             graph.add_edge("display_report", END)
            
#             compiled_graph = graph.compile()
            
#             # Execute the agentic flow
#             result = compiled_graph.invoke(initial_state)
            
#             return result.get("report", "No report generated")
            
#         except Exception as e:
#             print(f"Error in agentic flow: {e}")
#             # Fallback to direct approach
    
#     # Fallback for Ollama or when LangGraph is not available
#     if llm is not None:
#         try:
#             # Load templates directly
#             templates = load_templates(language)
            
#             if not templates:
#                 return "Template rendering not available."
            
#             # Render the user form with project data
#             if "user_form" in templates:
#                 user_form = templates["user_form"].render(**project_data)
#             else:
#                 user_form = str(project_data)
            
#             # Create the system prompt
#             if "system_prompt" in templates:
#                 system_prompt = templates["system_prompt"].render()
#             else:
#                 system_prompt = "You are an expert report writer."
            
#             # Create the user prompt
#             if "user_prompt" in templates:
#                 user_prompt = templates["user_prompt"].render(
#                     input_data=user_form,
#                     project_name=project_data.get("field1", "Project"),
#                     **project_data
#                 )
#             else:
#                 user_prompt = f"Generate a report for: {user_form}"
            
#             # Combine prompts
#             full_prompt = f"{system_prompt}\n\n{user_prompt}"
            
#             # Generate report using LLM
#             response = llm.invoke(full_prompt)
#             return response
                
#         except Exception as e:
#             print(f"Error generating report with templates: {e}")
#             return f"Error generating report: {e}"
#     else:
#         return "LLM not available for report generation."


def generate_language_report(project_data: Dict[str, Any], language: str = "en") -> str:
    """Generate a report using agentic flow with LangGraph"""
    if llm is None:
        return "LLM not available for report generation."
    
    # Create initial state for agentic flow
    initial_state = AgentState(
        messages=[],
        project_data=project_data,
        language=language,
        templates={},
        report=None,
        status="Initialized"
    )
    
    # Use agentic flow if LangGraph is available and LLM is not Ollama
    if LANGGRAPH_AVAILABLE and llm and not isinstance(llm, OllamaLLM):
        try:
            # Create a new graph instance for this specific request
            graph = StateGraph(AgentState)
            
            # Add nodes
            graph.add_node("load_templates", load_templates_agent)
            graph.add_node("generate_report", generate_report_agent)
            graph.add_node("save_report", save_report_agent)
            graph.add_node("display_report", display_report_agent)

            # Add edges
            graph.add_edge(START, "load_templates")
            graph.add_edge("load_templates", "generate_report")
            graph.add_edge("generate_report", "save_report")
            graph.add_edge("save_report", "display_report")
            graph.add_edge("display_report", END)
            
            # Compile and execute
            compiled_graph = graph.compile()
            result = compiled_graph.invoke(initial_state)
            
            return result.get("report", "No report generated from agentic flow")
            
        except Exception as e:
            print(f"Error in agentic flow: {e}")
            # Fallback to direct LLM invocation
    
    # Fallback for Ollama or when LangGraph is not available
    if llm is not None:
        try:
            # Create a comprehensive prompt for direct LLM invocation
            project_name = project_data.get("field1", "Project")
            project_type = project_data.get("field2", "Business")
            location = project_data.get("field3", "Location")
            duration = project_data.get("field4", "Duration")
            budget = project_data.get("field8", "₹0")
            spent = project_data.get("field9", "₹0")
            completion = project_data.get("field11", "0%")
            
            prompt = f"""Generate a comprehensive {language.upper()} report for the following project:

Project Name: {project_name}
Project Type: {project_type}
Location: {location}
Duration: {duration}
Budget: {budget}
Spent: {spent}
Completion: {completion}

Please provide a detailed analysis including:
1. Project overview and objectives
2. Financial analysis and budget utilization
3. Progress assessment and completion status
4. Key achievements and milestones
5. Recommendations for future improvements

Format the report professionally with clear sections and bullet points where appropriate."""

            response = llm.invoke(prompt)
            return response
            
        except Exception as e:
            print(f"Error generating report: {e}")
            return f"Error generating report: {e}"
    else:
        return "LLM not available for report generation."