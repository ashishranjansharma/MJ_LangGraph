# use langgraph to create a report agent

import os
from typing import Optional, Any

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