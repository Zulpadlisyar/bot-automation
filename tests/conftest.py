"""Pytest configuration and fixtures."""

import os
import tempfile
from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def temp_excel_file():
    """Create a temporary Excel file for testing."""
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        yield tmp.name
    os.unlink(tmp.name)


@pytest.fixture
def mock_telegram_update():
    """Create a mock Telegram update for testing."""
    update = Mock()
    update.message = Mock()
    update.message.text = "https://instagram.com/p/ABC123"
    update.message.reply_text = Mock()
    return update


@pytest.fixture
def mock_telegram_context():
    """Create a mock Telegram context for testing."""
    context = Mock()
    return context


@pytest.fixture
def sample_scraped_data():
    """Sample scraped data for testing."""
    return {
        "title": "Software Engineer Intern at PT Tech Indonesia",
        "description": "Looking for talented software engineering interns to join our team in Jakarta. Great opportunity to learn and grow!",
    }


@pytest.fixture
def sample_internship_data():
    """Sample internship data for testing."""
    return {
        "company": "PT Tech Indonesia",
        "position": "Software Engineer Intern",
        "division": "Engineering",
        "location": "Jakarta",
        "work_type": "Hybrid",
        "deadline": "2024-12-31",
        "contact": "hr@pttech.com",
        "description": "Great internship opportunity",
        "platform": "Instagram",
        "url": "https://instagram.com/p/ABC123",
    }
