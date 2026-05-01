"""Test cases for data extraction service."""

from unittest.mock import Mock, patch

import pytest

from src.services.extractor import _fallback_extraction, extract_with_deepseek


class TestExtractor:
    """Test cases for data extraction."""

    def test_fallback_extraction(self):
        """Test fallback extraction without AI."""
        url = "https://instagram.com/p/ABC123"
        scraped = {
            "title": "Software Engineer Intern at PT Tech",
            "description": "Looking for talented interns to join our team",
        }

        result = _fallback_extraction(url, scraped)

        assert isinstance(result, dict)
        assert result["platform"] == "Instagram"
        assert result["position"] == scraped["title"]
        assert result["description"] == scraped["description"][:200]
        assert result["company"] == ""

    @patch("src.services.extractor.deepseek")
    def test_extract_with_deepseek_success(self, mock_deepseek):
        """Test successful extraction with DeepSeek."""
        # Mock DeepSeek response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = (
            '{"company": "PT Tech", "position": "Developer"}'
        )

        mock_deepseek.chat.completions.create.return_value = mock_response

        url = "https://instagram.com/p/ABC123"
        scraped = {"title": "Internship", "description": "Great opportunity"}

        result = extract_with_deepseek(url, scraped)

        assert isinstance(result, dict)
        assert result["company"] == "PT Tech"
        assert result["position"] == "Developer"

    @patch("src.services.extractor.deepseek")
    def test_extract_with_deepseek_list_response(self, mock_deepseek):
        """Test handling list response from DeepSeek."""
        # Mock DeepSeek response that returns a list
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = (
            '[{"company": "PT Tech", "position": "Developer"}]'
        )

        mock_deepseek.chat.completions.create.return_value = mock_response

        url = "https://instagram.com/p/ABC123"
        scraped = {"title": "Internship", "description": "Great opportunity"}

        result = extract_with_deepseek(url, scraped)

        # Should handle list by taking first item
        assert isinstance(result, dict)
        assert result["company"] == "PT Tech"

    @patch("src.services.extractor.deepseek", None)
    def test_extract_without_deepseek(self):
        """Test extraction when DeepSeek is not available."""
        url = "https://instagram.com/p/ABC123"
        scraped = {"title": "Software Engineer", "description": "Great role"}

        result = extract_with_deepseek(url, scraped)

        # Should fall back to basic extraction
        assert isinstance(result, dict)
        assert result["platform"] == "Instagram"
        assert result["position"] == "Software Engineer"

    @patch("src.services.extractor.deepseek")
    def test_extract_with_deepseek_error(self, mock_deepseek):
        """Test extraction when DeepSeek raises an error."""
        mock_deepseek.chat.completions.create.side_effect = Exception("API Error")

        url = "https://instagram.com/p/ABC123"
        scraped = {"title": "Software Engineer", "description": "Great role"}

        result = extract_with_deepseek(url, scraped)

        # Should fall back to basic extraction on error
        assert isinstance(result, dict)
        assert result["platform"] == "Instagram"
        assert result["position"] == "Software Engineer"
