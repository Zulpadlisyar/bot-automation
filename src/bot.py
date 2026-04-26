"""Bot Telegram untuk mencatat lowongan magang secara otomatis."""

from datetime import datetime

from openpyxl import Workbook, load_workbook
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from src.config import EXCEL_FILE, HEADER_ROW, SHEET_NAME, TELEGRAM_TOKEN
from src.services.extractor import extract_with_deepseek
from src.services.scraper import scrape_metadata
from src.utils.platform import get_platform_from_url


async def start(update: Update, context) -> None:
    """Handler untuk perintah /start."""
    await update.message.reply_text(
        "Halo! Kirim link lowongan IG/TikTok/X/Threads untuk dicatat otomatis di sheet 'Data Magang'."
    )


async def handle_link(update: Update, context) -> None:
    """Handler untuk menerima dan memproses link lowongan."""
    url = update.message.text.strip()
    supported_platforms = ["instagram.com", "tiktok.com", "x.com", "threads.net"]

    if not any(p in url for p in supported_platforms):
        await update.message.reply_text("❌ Link tidak didukung.")
        return

    await update.message.reply_text("⏳ Mengekstrak...")
    scraped = scrape_metadata(url)
    data = extract_with_deepseek(url, scraped)
    save_to_excel(data, url)

    reply = (
        f"✅ Tersimpan!\n"
        f"🏢 {data.get('company', '?')}\n"
        f"💼 {data.get('position', '?')}"
    )
    await update.message.reply_text(reply)


def save_to_excel(data: dict, url: str) -> None:
    """Simpan data lowongan ke file Excel.

    Args:
        data: Dictionary hasil ekstraksi informasi lowongan.
        url: URL asal lowongan.
    """
    print(f"DEBUG: Menyimpan ke {EXCEL_FILE} di sheet '{SHEET_NAME}'...")

    try:
        wb = load_workbook(EXCEL_FILE)
    except FileNotFoundError:
        print("DEBUG: File tidak ditemukan, membuat baru...")
        wb = Workbook()
        ws = wb.active
        ws.title = SHEET_NAME
        ws.append(HEADER_ROW)
        wb.save(EXCEL_FILE)
        wb = load_workbook(EXCEL_FILE)

    if SHEET_NAME in wb.sheetnames:
        ws = wb[SHEET_NAME]
    else:
        print(f"DEBUG: Sheet '{SHEET_NAME}' tidak ada, membuat...")
        ws = wb.create_sheet(SHEET_NAME)
        ws.append(HEADER_ROW)

    # Deteksi di mana header berada
    header_row = 1
    max_scan = 5
    for row in range(1, max_scan + 1):
        first_cell = ws.cell(row=row, column=1).value
        if first_cell and str(first_cell).strip() == "No":
            header_row = row
            break
    print(f"DEBUG: Menggunakan header di baris {header_row}")

    # Bangun indeks kolom dari baris header
    col_idx = {}
    for i, cell in enumerate(ws[header_row], start=1):
        if cell.value:
            col_name = str(cell.value).strip()
            col_idx[col_name] = i
    print(f"DEBUG: Kolom ditemukan: {list(col_idx.keys())}")

    # Cari baris kosong pertama setelah header
    next_row = header_row + 1
    while (
        ws.cell(row=next_row, column=1).value is not None
        and str(ws.cell(row=next_row, column=1).value).strip() != ""
    ):
        next_row += 1
    print(f"DEBUG: Menulis di baris {next_row}")

    def set_cell(col_name: str, value) -> None:
        """Set nilai cell berdasarkan nama kolom."""
        if col_name in col_idx:
            ws.cell(row=next_row, column=col_idx[col_name], value=value)
        else:
            print(f"WARNING: Kolom '{col_name}' tidak ditemukan!")

    platform = data.get("platform") or get_platform_from_url(url)

    set_cell("No", next_row - header_row)
    set_cell("Nama Perusahaan", data.get("company"))
    set_cell("Posisi / Jabatan", data.get("position"))
    set_cell("Platform Daftar", platform)
    set_cell("Tgl Daftar", data.get("deadline", ""))
    set_cell("Link Lowongan", url)
    set_cell("Catatan", data.get("description", ""))
    set_cell("Status", "Baru")
    set_cell("Divisi / Tim", data.get("division"))
    set_cell("Kota / Lokasi", data.get("location"))
    set_cell("Tipe Kerja", data.get("work_type"))
    set_cell("Kontak Rekruter", data.get("contact"))

    wb.save(EXCEL_FILE)
    print("✅ Data berhasil disimpan.")


def main() -> None:
    """Entry point utama untuk menjalankan bot."""
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))
    print("Bot berjalan...")
    app.run_polling()


if __name__ == "__main__":
    main()

