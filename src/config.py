"""Konfigurasi aplikasi Magang Tracker Bot."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables dari .env
load_dotenv()

# --- Telegram ---
TELEGRAM_TOKEN: str | None = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN tidak ditemukan di file .env")
    sys.exit(1)

# --- DeepSeek API ---
DEEPSEEK_API_KEY: str | None = os.getenv("DEEPSEEK_API_KEY")

# --- File & Sheet Excel ---
EXCEL_FILE: str = "./Tracker_Pendaftaran_Magang.xlsx"
SHEET_NAME: str = "Data Magang"

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

