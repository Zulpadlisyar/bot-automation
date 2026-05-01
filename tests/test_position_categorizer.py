"""Test cases for position categorization utilities."""

import pytest
from src.services.position_categorizer import PositionCategorizer


class TestPositionCategorizer:
    """Test cases for PositionCategorizer."""
    
    def test_categorize_frontend_positions(self):
        """Test frontend position categorization."""
        positions = [
            "Frontend Developer",
            "Front End Developer", 
            "React Developer",
            "Vue Developer",
            "UI Developer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["Frontend", "Frontend Engineer"]
    
    def test_categorize_backend_positions(self):
        """Test backend position categorization."""
        positions = [
            "Backend Developer",
            "Back End Developer",
            "API Developer",
            "Server Developer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["Backend", "Backend Engineer"]
    
    def test_categorize_fullstack_positions(self):
        """Test fullstack position categorization."""
        positions = [
            "Fullstack Developer",
            "Full Stack Developer",
            "Full-stack Developer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized == "Fullstack"
    
    def test_categorize_mobile_positions(self):
        """Test mobile position categorization."""
        positions = [
            "Mobile Developer",
            "iOS Developer", 
            "Android Developer",
            "React Native Developer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["Mobile Developer", "Mobile Engineer"]
    
    def test_categorize_data_positions(self):
        """Test data position categorization."""
        positions = [
            "Data Scientist",
            "Data Analyst",
            "ML Engineer",
            "AI Engineer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["Data Scientist", "Machine Learning"]
    
    def test_categorize_devops_positions(self):
        """Test DevOps position categorization."""
        positions = [
            "DevOps Engineer",
            "Site Reliability Engineer",
            "Cloud Engineer",
            "Infrastructure Engineer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["DevOps", "Cloud Engineer", "DevOps"]
    
    def test_categorize_qa_positions(self):
        """Test QA position categorization."""
        positions = [
            "QA Engineer",
            "Test Engineer",
            "Quality Assurance Engineer",
            "Automation Engineer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Tech"
            assert normalized in ["QA Engineer", "QA Tester"]
    
    def test_categorize_non_tech_positions(self):
        """Test non-tech position categorization."""
        positions = [
            "Marketing Manager",
            "Sales Executive",
            "HR Assistant",
            "Content Writer"
        ]
        
        for position in positions:
            category, normalized = PositionCategorizer.categorize_position(position)
            assert category == "Non-Tech"
    
    def test_normalize_generic_positions(self):
        """Test normalization of generic positions."""
        test_cases = [
            ("Software Engineer Intern", "Software Engineer Intern"),
            ("Junior Developer", "Junior Software Engineer"),
            ("Senior Developer", "Senior Software Engineer"),
            ("Tech Lead", "Tech Lead"),
            ("Engineering Manager", "Engineering Manager"),
            ("Software Architect", "Software Architect"),
            ("Random Developer", "Software Engineer")
        ]
        
        for input_pos, expected in test_cases:
            result = PositionCategorizer._normalize_generic_position(input_pos)
            assert result == expected
    
    def test_extract_tech_stack(self):
        """Test tech stack extraction."""
        description = "We are looking for a developer with experience in React, Node.js, Python, and AWS. Knowledge of Docker and Kubernetes is a plus."
        
        tech_stack = PositionCategorizer.extract_tech_stack(description)
        
        expected_tech = ["Aws", "Docker", "Kubernetes", "Node.js", "Python", "React"]
        assert all(tech in tech_stack for tech in expected_tech)
    
    def test_suggest_division_frontend(self):
        """Test division suggestion for frontend roles."""
        division = PositionCategorizer.suggest_division("Frontend Developer", ["React", "JavaScript"])
        assert division == "Frontend"
    
    def test_suggest_division_backend(self):
        """Test division suggestion for backend roles."""
        division = PositionCategorizer.suggest_division("Backend Developer", ["Python", "Node.js"])
        assert division == "Backend"
    
    def test_suggest_division_mobile(self):
        """Test division suggestion for mobile roles."""
        division = PositionCategorizer.suggest_division("Mobile Developer", ["React Native"])
        assert division == "Mobile"
    
    def test_suggest_division_data(self):
        """Test division suggestion for data roles."""
        division = PositionCategorizer.suggest_division("Data Scientist", ["Python", "TensorFlow"])
        assert division == "Data Science"
    
    def test_suggest_division_devops(self):
        """Test division suggestion for DevOps roles."""
        division = PositionCategorizer.suggest_division("DevOps Engineer", ["Docker", "Kubernetes"])
        assert division == "DevOps"
    
    def test_suggest_division_fallback(self):
        """Test fallback division suggestion."""
        division = PositionCategorizer.suggest_division("Software Engineer", [])
        assert division == "Engineering"
