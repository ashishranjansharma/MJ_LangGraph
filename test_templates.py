#!/usr/bin/env python3
"""
Test script for template-based report generation
"""

from report_agent import generate_language_report

# Sample project data
sample_project_data = {
    "field1": "Organic Farming Project",
    "field2": "Agriculture",
    "field3": "Karnataka, India",
    "field4": "12 months",
    "field5": "Rajesh Kumar",
    "field6": "15 years in farming",
    "field7": "BSc in Agriculture, experienced farmer",
    "field8": "₹50,00,000",
    "field9": "₹30,00,000",
    "field10": "₹45,00,000",
    "field11": "50%",
    "field12": "Establish organic farming practices",
    "field13": "Certified organic produce",
    "field14": "Weather dependency, market fluctuations",
    "field15": "Growing demand for organic food",
    "format": "business_plan",
    "language": "en"
}

def test_english_report():
    """Test English report generation"""
    print("=" * 50)
    print("TESTING ENGLISH REPORT GENERATION")
    print("=" * 50)
    
    try:
        report = generate_language_report(sample_project_data, "en")
        print("English Report Generated Successfully!")
        print("\nReport Preview (first 500 chars):")
        print("-" * 30)
        print(report[:500] + "..." if len(report) > 500 else report)
    except Exception as e:
        print(f"Error generating English report: {e}")

def test_kannada_report():
    """Test Kannada report generation"""
    print("\n" + "=" * 50)
    print("TESTING KANNADA REPORT GENERATION")
    print("=" * 50)
    
    try:
        # Update language for Kannada
        kannada_data = sample_project_data.copy()
        kannada_data["language"] = "kn"
        
        report = generate_language_report(kannada_data, "kn")
        print("Kannada Report Generated Successfully!")
        print("\nReport Preview (first 500 chars):")
        print("-" * 30)
        print(report[:500] + "..." if len(report) > 500 else report)
    except Exception as e:
        print(f"Error generating Kannada report: {e}")

def test_template_loading():
    """Test template loading functionality"""
    print("\n" + "=" * 50)
    print("TESTING TEMPLATE LOADING")
    print("=" * 50)
    
    from report_agent import load_templates
    
    # Test English templates
    en_templates = load_templates("en")
    print(f"English templates loaded: {list(en_templates.keys())}")
    
    # Test Kannada templates
    kn_templates = load_templates("kn")
    print(f"Kannada templates loaded: {list(kn_templates.keys())}")
    
    # Test fallback to English
    invalid_templates = load_templates("invalid")
    print(f"Invalid language fallback: {list(invalid_templates.keys())}")

if __name__ == "__main__":
    test_template_loading()
    test_english_report()
    test_kannada_report() 