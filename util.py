from pydantic import BaseModel
import csv
import io
from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime, date


# Enums for report types and formats
class ReportType(str, Enum):
    SUMMARY = "summary"
    DETAILED = "detailed"
    FINANCIAL = "financial"
    PERFORMANCE = "performance"
    TIMELINE = "timeline"


class ReportFormat(str, Enum):
    JSON = "json"
    CSV = "csv"
    PDF = "pdf"


# Pydantic models
class ProjectInfo(BaseModel):
    id: str
    name: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    status: str
    budget: float
    spent: float
    team_size: int
    completion_percentage: float


class ReportRequest(BaseModel):
    project_ids: List[str]
    report_type: ReportType
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    include_tasks: bool = True
    include_financial: bool = True


class ReportResponse(BaseModel):
    report_id: str
    generated_at: datetime
    report_type: ReportType
    data: Dict[str, Any]


# Sample data (in a real application, this would come from a database)
SAMPLE_PROJECTS = [
    ProjectInfo(
        id="proj_001",
        name="Website Redesign",
        description="Complete redesign of company website",
        start_date=date(2024, 1, 15),
        end_date=date(2024, 6, 30),
        status="In Progress",
        budget=50000.0,
        spent=32000.0,
        team_size=8,
        completion_percentage=65.0
    ),
    ProjectInfo(
        id="proj_002",
        name="Mobile App Development",
        description="iOS and Android mobile application",
        start_date=date(2024, 3, 1),
        end_date=date(2024, 12, 15),
        status="In Progress",
        budget=80000.0,
        spent=25000.0,
        team_size=12,
        completion_percentage=30.0
    ),
    ProjectInfo(
        id="proj_003",
        name="Database Migration",
        description="Migration to cloud database infrastructure",
        start_date=date(2024, 2, 1),
        end_date=date(2024, 4, 30),
        status="Completed",
        budget=30000.0,
        spent=28500.0,
        team_size=5,
        completion_percentage=100.0
    )
]


# Helper functions
def get_project_by_id(project_id: str) -> Optional[ProjectInfo]:
    """Get project by ID from sample data"""
    return next((p for p in SAMPLE_PROJECTS if p.id == project_id), None)


def convert_to_csv(data: Dict[str, Any]) -> str:
    """Convert report data to CSV format"""
    output = io.StringIO()

    # Write summary information
    writer = csv.writer(output)
    writer.writerow(["Report Summary"])
    writer.writerow([])

    for key, value in data.items():
        if isinstance(value, (str, int, float)):
            writer.writerow([key, value])
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            writer.writerow([])
            writer.writerow([f"{key.upper()}"])
            if value:
                headers = list(value[0].keys())
                writer.writerow(headers)
                for item in value:
                    writer.writerow([item.get(header, "") for header in headers])

    return output.getvalue()
