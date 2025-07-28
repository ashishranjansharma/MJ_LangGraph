from pydantic import BaseModel
import json
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


class TaskInfo(BaseModel):
    id: str
    name: str
    status: str
    assigned_to: str
    start_date: date
    due_date: date
    completion_percentage: float
    priority: str


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

SAMPLE_TASKS = [
    TaskInfo(
        id="task_001",
        name="UI/UX Design",
        status="Completed",
        assigned_to="Alice Johnson",
        start_date=date(2024, 1, 15),
        due_date=date(2024, 2, 15),
        completion_percentage=100.0,
        priority="High"
    ),
    TaskInfo(
        id="task_002",
        name="Frontend Development",
        status="In Progress",
        assigned_to="Bob Smith",
        start_date=date(2024, 2, 16),
        due_date=date(2024, 5, 15),
        completion_percentage=70.0,
        priority="High"
    ),
    TaskInfo(
        id="task_003",
        name="Backend API Development",
        status="In Progress",
        assigned_to="Carol Davis",
        start_date=date(2024, 2, 1),
        due_date=date(2024, 4, 30),
        completion_percentage=85.0,
        priority="Medium"
    )
]


# Helper functions
def get_project_by_id(project_id: str) -> Optional[ProjectInfo]:
    """Get project by ID from sample data"""
    return next((p for p in SAMPLE_PROJECTS if p.id == project_id), None)


def generate_summary_report(projects: List[ProjectInfo], include_tasks: bool = True) -> Dict[str, Any]:
    """Generate a summary report for projects"""
    total_budget = sum(p.budget for p in projects)
    total_spent = sum(p.spent for p in projects)
    avg_completion = sum(p.completion_percentage for p in projects) / len(projects) if projects else 0

    status_counts = {}
    for project in projects:
        status = project.status
        status_counts[status] = status_counts.get(status, 0) + 1

    report_data = {
        "total_projects": len(projects),
        "total_budget": total_budget,
        "total_spent": total_spent,
        "budget_utilization": (total_spent / total_budget * 100) if total_budget > 0 else 0,
        "average_completion": avg_completion,
        "status_breakdown": status_counts,
        "projects": [p.dict() for p in projects]
    }

    if include_tasks:
        report_data["tasks"] = [t.dict() for t in SAMPLE_TASKS]
        report_data["total_tasks"] = len(SAMPLE_TASKS)

    return report_data


def generate_financial_report(projects: List[ProjectInfo]) -> Dict[str, Any]:
    """Generate a financial report for projects"""
    financial_data = []
    total_budget = 0
    total_spent = 0

    for project in projects:
        remaining_budget = project.budget - project.spent
        budget_variance = ((project.spent - project.budget) / project.budget * 100) if project.budget > 0 else 0

        financial_data.append({
            "project_id": project.id,
            "project_name": project.name,
            "budget": project.budget,
            "spent": project.spent,
            "remaining": remaining_budget,
            "budget_variance_percent": budget_variance,
            "status": "Over Budget" if project.spent > project.budget else "Within Budget"
        })

        total_budget += project.budget
        total_spent += project.spent

    return {
        "financial_summary": {
            "total_budget": total_budget,
            "total_spent": total_spent,
            "total_remaining": total_budget - total_spent,
            "overall_variance_percent": ((total_spent - total_budget) / total_budget * 100) if total_budget > 0 else 0
        },
        "project_financials": financial_data
    }


def generate_performance_report(projects: List[ProjectInfo]) -> Dict[str, Any]:
    """Generate a performance report for projects"""
    performance_data = []

    for project in projects:
        days_since_start = (datetime.now().date() - project.start_date).days
        expected_completion = min(100, (days_since_start / 180) * 100)  # Assuming 6-month projects
        performance_variance = project.completion_percentage - expected_completion

        performance_data.append({
            "project_id": project.id,
            "project_name": project.name,
            "actual_completion": project.completion_percentage,
            "expected_completion": expected_completion,
            "performance_variance": performance_variance,
            "status": "Ahead of Schedule" if performance_variance > 0 else "Behind Schedule",
            "team_size": project.team_size,
            "days_active": days_since_start
        })

    avg_performance = sum(p["performance_variance"] for p in performance_data) / len(
        performance_data) if performance_data else 0

    return {
        "performance_summary": {
            "average_performance_variance": avg_performance,
            "projects_ahead": len([p for p in performance_data if p["performance_variance"] > 0]),
            "projects_behind": len([p for p in performance_data if p["performance_variance"] <= 0])
        },
        "project_performance": performance_data
    }


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
