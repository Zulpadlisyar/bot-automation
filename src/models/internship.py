"""Data models for internship information."""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional


@dataclass
class InternshipData:
    """Data model for internship information."""

    company: str = ""
    position: str = ""
    division: str = ""
    location: str = ""
    work_type: str = ""
    deadline: str = ""
    contact: str = ""
    description: str = ""
    platform: str = ""
    url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            "company": self.company,
            "position": self.position,
            "division": self.division,
            "location": self.location,
            "work_type": self.work_type,
            "deadline": self.deadline,
            "contact": self.contact,
            "description": self.description,
            "platform": self.platform,
            "url": self.url,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InternshipData":
        """Create from dictionary."""
        return cls(**data)

    def is_valid(self) -> bool:
        """Check if the data has minimum required fields."""
        return bool(self.company or self.position or self.description)


@dataclass
class ExcelRow:
    """Data model for Excel row operations."""

    no: int
    company: str
    position: str
    division: str
    location: str
    work_type: str
    platform: str
    deadline: str
    start_date: str = ""
    end_date: str = ""
    duration_months: str = ""
    status: str = "Baru"
    current_stage: str = ""
    contact: str = ""
    link: str = ""
    notes: str = ""

    def to_list(self) -> list:
        """Convert to list format for Excel row."""
        return [
            self.no,
            self.company,
            self.position,
            self.division,
            self.location,
            self.work_type,
            self.platform,
            self.deadline,
            self.start_date,
            self.end_date,
            self.duration_months,
            self.status,
            self.current_stage,
            self.contact,
            self.link,
            self.notes,
        ]
