"""Test cases for data models."""

import pytest

from src.models.internship import ExcelRow, InternshipData


class TestInternshipData:
    """Test cases for InternshipData model."""

    def test_default_creation(self):
        """Test creating InternshipData with defaults."""
        data = InternshipData()
        assert data.company == ""
        assert data.position == ""
        assert data.is_valid() is False

    def test_creation_with_data(self):
        """Test creating InternshipData with data."""
        data = InternshipData(
            company="PT Tech Indonesia",
            position="Software Engineer",
            location="Jakarta",
        )
        assert data.company == "PT Tech Indonesia"
        assert data.position == "Software Engineer"
        assert data.is_valid() is True

    def test_to_dict(self):
        """Test converting to dictionary."""
        data = InternshipData(company="PT Tech", position="Developer")
        result = data.to_dict()

        assert isinstance(result, dict)
        assert result["company"] == "PT Tech"
        assert result["position"] == "Developer"

    def test_from_dict(self):
        """Test creating from dictionary."""
        input_dict = {
            "company": "PT Tech",
            "position": "Developer",
            "location": "Jakarta",
        }
        data = InternshipData.from_dict(input_dict)

        assert data.company == "PT Tech"
        assert data.position == "Developer"
        assert data.location == "Jakarta"

    def test_is_valid_with_company(self):
        """Test validation with company only."""
        data = InternshipData(company="PT Tech")
        assert data.is_valid() is True

    def test_is_valid_with_position(self):
        """Test validation with position only."""
        data = InternshipData(position="Developer")
        assert data.is_valid() is True

    def test_is_valid_with_description(self):
        """Test validation with description only."""
        data = InternshipData(description="Great opportunity")
        assert data.is_valid() is True

    def test_is_valid_empty(self):
        """Test validation with empty data."""
        data = InternshipData()
        assert data.is_valid() is False


class TestExcelRow:
    """Test cases for ExcelRow model."""

    def test_default_creation(self):
        """Test creating ExcelRow with required fields."""
        row = ExcelRow(
            no=1,
            company="PT Tech",
            position="Developer",
            division="Engineering",
            location="Jakarta",
            work_type="Hybrid",
            platform="Instagram",
            deadline="2024-12-31",
            link="https://example.com",
        )

        assert row.no == 1
        assert row.company == "PT Tech"
        assert row.status == "Baru"  # Default value

    def test_to_list(self):
        """Test converting to list for Excel."""
        row = ExcelRow(
            no=1,
            company="PT Tech",
            position="Developer",
            division="Engineering",
            location="Jakarta",
            work_type="Hybrid",
            platform="Instagram",
            deadline="2024-12-31",
            link="https://example.com",
        )

        result = row.to_list()
        assert isinstance(result, list)
        assert len(result) == 16  # Should have 16 columns
        assert result[0] == 1  # No column
        assert result[1] == "PT Tech"  # Company column
