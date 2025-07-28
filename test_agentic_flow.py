#!/usr/bin/env python3
"""
Test script for agentic flow report generation
"""

from report_agent import generate_language_report, AgentState, load_templates_agent, generate_report_agent
from typing import Dict, Any

# Sample project data
sample_project_data = {
    "field1": "AI-Powered Business Analytics Platform",
    "field2": "Technology",
    "field3": "Bangalore, Karnataka, India",
    "field4": "18 months",
    "field5": "Dr. Priya Sharma",
    "field6": "12 years in data science and AI",
    "field7": "PhD in Computer Science, ex-Google AI researcher",
    "field8": "₹200,00,00,000",
    "field9": "₹120,00,00,000",
    "field10": "₹180,00,00,000",
    "field11": "50%",
    "field12": "Develop comprehensive business analytics platform using AI",
    "field13": "Real-time predictive analytics with 95% accuracy",
    "field14": "Data privacy regulations, talent acquisition",
    "field15": "Growing demand for AI solutions, government support",
    "format": "business_plan",
    "language": "en"
}

def test_agentic_state_flow():
    """Test the agentic state flow step by step"""
    print("=" * 60)
    print("TESTING AGENTIC STATE FLOW")
    print("=" * 60)
    
    # Create initial state
    initial_state = AgentState(
        messages=[],
        project_data=sample_project_data,
        language="en",
        templates={},
        report=None,
        status="Initialized"
    )
    
    print(f"Initial State: {initial_state['status']}")
    print(f"Language: {initial_state['language']}")
    print(f"Project: {initial_state['project_data']['field1']}")
    
    # Step 1: Load templates
    print("\n" + "-" * 40)
    print("STEP 1: Loading Templates")
    print("-" * 40)
    
    state_after_templates = load_templates_agent(initial_state)
    print(f"Status: {state_after_templates['status']}")
    print(f"Templates loaded: {list(state_after_templates['templates'].keys())}")
    
    # Step 2: Generate report
    print("\n" + "-" * 40)
    print("STEP 2: Generating Report")
    print("-" * 40)
    
    state_after_generation = generate_report_agent(state_after_templates)
    print(f"Status: {state_after_generation['status']}")
    
    if state_after_generation['report']:
        report_preview = state_after_generation['report'][:300] + "..." if len(state_after_generation['report']) > 300 else state_after_generation['report']
        print(f"Report Preview: {report_preview}")
    else:
        print("No report generated")
    
    return state_after_generation

def test_language_comparison():
    """Test report generation in different languages"""
    print("\n" + "=" * 60)
    print("TESTING LANGUAGE COMPARISON")
    print("=" * 60)
    
    # English report
    print("\n--- ENGLISH REPORT ---")
    en_report = generate_language_report(sample_project_data, "en")
    print(f"English Report Length: {len(en_report)} characters")
    print(f"Preview: {en_report[:200]}...")
    
    # Kannada report
    print("\n--- KANNADA REPORT ---")
    kn_data = sample_project_data.copy()
    kn_data["language"] = "kn"
    kn_report = generate_language_report(kn_data, "kn")
    print(f"Kannada Report Length: {len(kn_report)} characters")
    print(f"Preview: {kn_report[:200]}...")

def test_error_handling():
    """Test error handling in agentic flow"""
    print("\n" + "=" * 60)
    print("TESTING ERROR HANDLING")
    print("=" * 60)
    
    # Test with invalid language
    print("\n--- Invalid Language Test ---")
    invalid_report = generate_language_report(sample_project_data, "invalid")
    print(f"Invalid Language Result: {invalid_report[:100]}...")
    
    # Test with empty project data
    print("\n--- Empty Project Data Test ---")
    empty_report = generate_language_report({}, "en")
    print(f"Empty Data Result: {empty_report[:100]}...")

def test_agentic_vs_direct():
    """Compare agentic flow vs direct approach"""
    print("\n" + "=" * 60)
    print("TESTING AGENTIC VS DIRECT APPROACH")
    print("=" * 60)
    
    # Agentic approach
    print("\n--- Agentic Approach ---")
    agentic_result = test_agentic_state_flow()
    
    # Direct approach
    print("\n--- Direct Approach ---")
    direct_result = generate_language_report(sample_project_data, "en")
    
    print(f"\nAgentic Report Length: {len(agentic_result.get('report', ''))}")
    print(f"Direct Report Length: {len(direct_result)}")
    
    # Compare results
    if agentic_result.get('report') and direct_result:
        similarity = "Similar" if len(agentic_result['report']) > 0 and len(direct_result) > 0 else "Different"
        print(f"Result Comparison: {similarity}")

if __name__ == "__main__":
    test_agentic_state_flow()
    test_language_comparison()
    test_error_handling()
    test_agentic_vs_direct()
    
    print("\n" + "=" * 60)
    print("AGENTIC FLOW TESTING COMPLETE")
    print("=" * 60) 