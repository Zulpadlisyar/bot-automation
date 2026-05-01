"""Configuration validation for Magang Tracker Bot."""

import os
import re
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse

from src.core.exceptions import ConfigurationError
from src.core.logger import logger


class ConfigValidator:
    """Validates and manages application configuration."""

    @staticmethod
    def validate_telegram_token(token: str) -> bool:
        """Validate Telegram bot token format.

        Args:
            token: Telegram bot token to validate

        Returns:
            True if token format is valid

        Raises:
            ConfigurationError: If token format is invalid
        """
        if not token:
            raise ConfigurationError("TELEGRAM_TOKEN is required")

        # Telegram bot tokens are like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz
        pattern = r"^\d+:[A-Za-z0-9_-]{35}$"
        if not re.match(pattern, token):
            raise ConfigurationError(
                "Invalid TELEGRAM_TOKEN format. "
                "Expected format: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz"
            )

        return True

    @staticmethod
    def validate_deepseek_api_key(api_key: Optional[str]) -> bool:
        """Validate DeepSeek API key format.

        Args:
            api_key: DeepSeek API key to validate

        Returns:
            True if API key is valid or None (optional)

        Raises:
            ConfigurationError: If API key format is invalid
        """
        if not api_key:
            logger.info("DEEPSEEK_API_KEY is optional (not provided)")
            return True

        # DeepSeek API keys are typically 48 characters alphanumeric
        if len(api_key) < 20:
            raise ConfigurationError(
                "DEEPSEEK_API_KEY appears to be too short. "
                "Please check your API key from DeepSeek platform."
            )

        return True

    @staticmethod
    def validate_excel_file_path(file_path: str) -> bool:
        """Validate Excel file path and create directory if needed.

        Args:
            file_path: Path to Excel file

        Returns:
            True if path is valid

        Raises:
            ConfigurationError: If path is invalid
        """
        if not file_path:
            raise ConfigurationError("EXCEL_FILE path is required")

        path = Path(file_path)

        # Check if directory exists, create if not
        if not path.parent.exists():
            try:
                path.parent.mkdir(parents=True, exist_ok=True)
                logger.info(f"Created directory: {path.parent}")
            except Exception as e:
                raise ConfigurationError(f"Cannot create directory {path.parent}: {e}")

        # Check if file has valid extension
        if path.suffix.lower() not in [".xlsx", ".xlsm", ".xls"]:
            raise ConfigurationError(
                f"Invalid Excel file extension: {path.suffix}. "
                "Expected: .xlsx, .xlsm, or .xls"
            )

        return True

    @staticmethod
    def validate_sheet_name(sheet_name: str) -> bool:
        """Validate Excel sheet name.

        Args:
            sheet_name: Excel sheet name to validate

        Returns:
            True if sheet name is valid

        Raises:
            ConfigurationError: If sheet name is invalid
        """
        if not sheet_name:
            raise ConfigurationError("SHEET_NAME is required")

        # Excel sheet name restrictions
        if len(sheet_name) > 31:
            raise ConfigurationError("SHEET_NAME cannot be longer than 31 characters")

        invalid_chars = ["\\", "/", "*", "[", "]", ":", "?"]
        for char in invalid_chars:
            if char in sheet_name:
                raise ConfigurationError(
                    f"SHEET_NAME cannot contain '{char}'. "
                    f"Invalid characters: {', '.join(invalid_chars)}"
                )

        return True

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if URL is valid

        Raises:
            ConfigurationError: If URL is invalid
        """
        if not url:
            raise ConfigurationError("URL cannot be empty")

        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                raise ConfigurationError(f"Invalid URL format: {url}")
            return True
        except Exception as e:
            raise ConfigurationError(f"URL validation failed: {e}")

    @classmethod
    def validate_all_config(cls, config: Dict[str, Any]) -> bool:
        """Validate all configuration values.

        Args:
            config: Configuration dictionary

        Returns:
            True if all configurations are valid

        Raises:
            ConfigurationError: If any configuration is invalid
        """
        logger.info("Validating application configuration...")

        # Validate Telegram token
        cls.validate_telegram_token(config.get("TELEGRAM_TOKEN", ""))

        # Validate DeepSeek API key (optional)
        cls.validate_deepseek_api_key(config.get("DEEPSEEK_API_KEY"))

        # Validate Excel file path
        cls.validate_excel_file_path(config.get("EXCEL_FILE", ""))

        # Validate sheet name
        cls.validate_sheet_name(config.get("SHEET_NAME", ""))

        logger.info("✅ All configuration validations passed")
        return True
