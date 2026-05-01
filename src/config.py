"""Konfigurasi aplikasi Magang Tracker Bot."""

import os
import sys
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

from src.core.config_validator import ConfigValidator
from src.core.exceptions import ConfigurationError
from src.core.logger import logger

# Load environment variables dari .env
load_dotenv()

# --- Telegram ---
TELEGRAM_TOKEN: str | None = os.getenv("TELEGRAM_TOKEN")

# --- DeepSeek API ---
DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")

# --- File & Sheet Excel ---
EXCEL_FILE: str = "./Tracker_Pendaftaran_Magang.xlsx"
SHEET_NAME: str = "Data Magang"


# Validate configuration
def validate_configuration():
    """Validate all configuration values."""
    try:
        config = {
            "TELEGRAM_TOKEN": TELEGRAM_TOKEN,
            "DEEPSEEK_API_KEY": DEEPSEEK_API_KEY,
            "EXCEL_FILE": EXCEL_FILE,
            "SHEET_NAME": SHEET_NAME,
        }

        ConfigValidator.validate_all_config(config)

        # Set global variables after validation
        if not TELEGRAM_TOKEN:
            raise ConfigurationError("TELEGRAM_TOKEN is required")

        logger.info("✅ Configuration validation completed successfully")
        return True

    except ConfigurationError as e:
        logger.error(f"Configuration validation failed: {e}")
        raise


# Validate configuration on import
validate_configuration()

# --- Header Excel ---
HEADER_ROW: list[str] = [
    "No",
    "Nama Perusahaan",
    "Posisi / Jabatan",
    "Divisi / Tim",
    "Kota / Lokasi",
    "Tipe Kerja",
    "Platform Daftar",
    "Tgl Daftar",
    "Tgl Mulai",
    "Tgl Selesai",
    "Durasi (bln)",
    "Status",
    "Tahap Saat Ini",
    "Kontak Rekruter",
    "Link Lowongan",
    "Catatan",
]

# --- Project Paths ---
PROJECT_ROOT: Path = Path(__file__).parent.parent
