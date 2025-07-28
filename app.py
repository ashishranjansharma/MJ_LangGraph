from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import tempfile
import os
from util import ProjectInfo, ReportType, ReportFormat, ReportRequest, ReportResponse, SAMPLE_PROJECTS, get_project_by_id, convert_to_csv
from report_agent import generate_language_report


# Initialize FastAPI app
app = FastAPI(
    title="Project Report API",
    description="API for generating various project reports",
    version="1.0.0"
)


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Project Report API",
        "version": "1.0.0",
        "endpoints": {
            "generate_report": "/reports/generate",
            "download_report": "/reports/download/{report_id}",
            "projects": "/projects",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now()}

@app.get("/projects", response_model=List[ProjectInfo])
async def get_projects():
    """Get all available projects"""
    return SAMPLE_PROJECTS

@app.get("/projects/{project_id}", response_model=ProjectInfo)
async def get_project(project_id: str):
    """Get a specific project by ID"""
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.post("/reports/generate", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    """Generate a project report based on the request parameters"""
    
    # Validate project IDs
    projects = []
    for project_id in request.project_ids:
        project = get_project_by_id(project_id)
        if not project:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
        projects.append(project)
    
    # Generate report using template-based AI generation
    project_data = {
        "field1": projects[0].name if projects else "Project",
        "field2": "Business",
        "field3": "Karnataka, India",
        "field4": "12 months",
        "field5": "Project Manager",
        "field6": "5 years experience",
        "field7": "Experienced professional",
        "field8": f"₹{sum(p.budget for p in projects):,.0f}" if projects else "₹0",
        "field9": f"₹{sum(p.spent for p in projects):,.0f}" if projects else "₹0",
        "field10": f"₹{sum(p.budget - p.spent for p in projects):,.0f}" if projects else "₹0",
        "field11": f"{sum(p.completion_percentage for p in projects) / len(projects):.1f}%" if projects else "0%",
        "field12": f"Generate {request.report_type.value} report for {len(projects)} projects",
        "field13": "Comprehensive project analysis",
        "field14": "Data accuracy and completeness",
        "field15": "Improved project management",
        "format": "business_plan",
        "language": "en"
    }
    
    # Generate AI-powered report
    report_content = generate_language_report(project_data, "en")
    
    # Structure the response data
    report_data = {
        "report_type": request.report_type.value,
        "total_projects": len(projects),
        "total_budget": sum(p.budget for p in projects) if projects else 0,
        "total_spent": sum(p.spent for p in projects) if projects else 0,
        "average_completion": sum(p.completion_percentage for p in projects) / len(projects) if projects else 0,
        "projects": [p.dict() for p in projects],
        "ai_generated_content": report_content
    }
    
    # Generate unique report ID
    report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{request.report_type.value}"
    
    return ReportResponse(
        report_id=report_id,
        generated_at=datetime.now(),
        report_type=request.report_type,
        data=report_data
    )

@app.get("/reports/download")
async def download_report(
    project_ids: List[str] = Query(..., description="List of project IDs"),
    report_type: ReportType = Query(ReportType.SUMMARY, description="Type of report to generate"),
    format: ReportFormat = Query(ReportFormat.JSON, description="Output format"),
    include_tasks: bool = Query(True, description="Include task information"),
    include_financial: bool = Query(True, description="Include financial information")
):
    """Download a report in the specified format"""
    
    # Create report request
    request = ReportRequest(
        project_ids=project_ids,
        report_type=report_type,
        include_tasks=include_tasks,
        include_financial=include_financial
    )
    
    # Generate report
    report_response = await generate_report(request)
    
    # Return based on format
    if format == ReportFormat.JSON:
        return JSONResponse(
            content=report_response.dict(),
            headers={"Content-Disposition": f"attachment; filename={report_response.report_id}.json"}
        )
    elif format == ReportFormat.CSV:
        csv_content = convert_to_csv(report_response.data)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            tmp_file.write(csv_content)
            tmp_file_path = tmp_file.name
        
        return FileResponse(
            path=tmp_file_path,
            filename=f"{report_response.report_id}.csv",
            media_type="text/csv",
            background=lambda: os.unlink(tmp_file_path)  # Clean up temp file
        )
    else:
        raise HTTPException(status_code=400, detail="PDF format not implemented yet")

@app.get("/reports/types")
async def get_report_types():
    """Get available report types and formats"""
    return {
        "report_types": [{"value": rt.value, "name": rt.value.title()} for rt in ReportType],
        "formats": [{"value": rf.value, "name": rf.value.upper()} for rf in ReportFormat]
    }


@app.post("/reports/generate-template")
async def generate_template_report(request: Dict[str, Any]):
    """Generate a report using templates and AI"""
    try:
        # Extract project data and language
        project_data = request.get("project_data", {})
        language = request.get("language", "en")
        
        # Validate language
        if language not in ["en", "kn"]:
            raise HTTPException(status_code=400, detail="Language must be 'en' or 'kn'")
        
        # Generate report using templates
        report = generate_language_report(project_data, language)
        
        # Generate unique report ID
        report_id = f"template_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{language}"
        
        return {
            "report_id": report_id,
            "generated_at": datetime.now(),
            "language": language,
            "report": report,
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating template report: {str(e)}")


@app.get("/reports/languages")
async def get_supported_languages():
    """Get supported languages for template reports"""
    return {
        "supported_languages": [
            {"code": "en", "name": "English"},
            {"code": "kn", "name": "ಕನ್ನಡ (Kannada)"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
