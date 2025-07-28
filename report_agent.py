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

# Get API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize LLM only if API key is available
llm: Optional[Any] = None
if GEMINI_API_KEY and LANGCHAIN_AVAILABLE:
    try:
        llm = GoogleGenerativeAI(model="gemini-2.0-flash-001")
    except Exception as e:
        print(f"Warning: Could not initialize Google Generative AI: {e}")
        llm = None
else:
    if not GEMINI_API_KEY:
        print("Warning: GEMINI_API_KEY not set. AI-powered features will be disabled.")
    if not LANGCHAIN_AVAILABLE:
        print("Warning: langchain-google-genai not available. AI features disabled.")

# create a state graph
if LANGGRAPH_AVAILABLE and llm:
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
else:
    print("AI features not available - using fallback report generation")
    fallback_report = {"report": "Fallback report - AI features disabled"}
    print(fallback_report["report"])      