"""Custom exceptions for Magang Tracker Bot."""


class MagangTrackerBotError(Exception):
    """Base exception for Magang Tracker Bot."""

    pass


class ConfigurationError(MagangTrackerBotError):
    """Raised when there's a configuration issue."""

    pass


class DataExtractionError(MagangTrackerBotError):
    """Raised when data extraction fails."""

    pass


class ExcelOperationError(MagangTrackerBotError):
    """Raised when Excel operations fail."""

    pass


class ScrapingError(MagangTrackerBotError):
    """Raised when web scraping fails."""

    pass


class UnsupportedPlatformError(MagangTrackerBotError):
    """Raised when an unsupported platform is encountered."""

    pass
