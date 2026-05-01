<div align="center">

# 🤖 Magang Tracker Bot

[![CI](https://github.com/zulpadlisyar/magang-tracker-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/zulpadlisyar/magang-tracker-bot/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Bot Telegram untuk mencatat lowongan magang secara otomatis dari media sosial.**

Data diekstrak menggunakan AI (DeepSeek) dan disimpan langsung ke spreadsheet Excel.

[Demo](#-demo) • [Fitur](#-fitur) • [Instalasi](#-instalasi) • [Penggunaan](#-penggunaan) • [Kontribusi](#-kontribusi)

</div>

---

## 📸 Demo

```
User: https://www.instagram.com/p/ABC123/
Bot:  ⏳ Mengekstrak...
Bot:  ✅ Tersimpan!
      🏢 PT Teknologi Indonesia
      💼 Software Engineering Intern
```

Data otomatis masuk ke file Excel dengan kolom lengkap:

| No | Nama Perusahaan | Posisi | Divisi | Lokasi | Tipe Kerja | Platform | Status |
|----|-----------------|--------|--------|--------|------------|----------|--------|
| 1  | PT Teknologi ID | Software Engineer Intern | Engineering | Jakarta | Hybrid | Instagram | Baru |

---

## ✨ Fitur

- 📎 **Dukung Multi-platform** — Instagram, TikTok, X (Twitter), Threads
- 🧠 **Ekstraksi Otomatis dengan AI** — Nama perusahaan, posisi, divisi, lokasi, tipe kerja, deadline, kontak rekruter
- 📊 **Simpan ke Excel** — Data langsung masuk ke sheet `Data Magang` dengan format rapi
- 🔒 **Konfigurasi Aman** — Token & API key via `.env`, tidak ikut terupload ke GitHub
- 🧹 **Pendeteksi Baris Kosong** — Data baru ditambahkan tepat di bawah header secara otomatis
- 🔄 **Reset Webhook** — Script utilitas untuk membersihkan pending updates

---

## 🛠️ Tech Stack

| Kategori | Teknologi |
|----------|-----------|
| Bot Framework | [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) |
| AI / LLM | [DeepSeek API](https://platform.deepseek.com/) via [OpenAI SDK](https://github.com/openai/openai-python) |
| Web Scraping | [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) + [Requests](https://requests.readthedocs.io/) |
| Spreadsheet | [OpenPyXL](https://openpyxl.readthedocs.io/) |
| Environment | [python-dotenv](https://saurabh-kumar.com/python-dotenv/) |

---

## 🚀 Instalasi

### Prasyarat

- Python 3.10 atau lebih baru
- Akun Telegram & token bot dari [@BotFather](https://t.me/BotFather)
- (Opsional) API Key dari [DeepSeek Platform](https://platform.deepseek.com/)

### Langkah-langkah

```bash
# 1. Clone repository
git clone https://github.com/zulpadlisyar/magang-tracker-bot.git
cd magang-tracker-bot

# 2. Buat virtual environment
python -m venv venv

# Aktifkan (Linux/Mac)
source venv/bin/activate
# Aktifkan (Windows)
# venv\Scripts\activate

# 3. Install dependencies
make install
# atau: pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env dan isi TELEGRAM_TOKEN serta DEEPSEEK_API_KEY
```

---

## 📖 Penggunaan

### Menjalankan Bot

```bash
make run
# atau: python -m src.bot
```

Kirim link lowongan ke bot Telegram Anda:
- `https://instagram.com/p/...`
- `https://tiktok.com/...`
- `https://x.com/...`
- `https://threads.net/...`

### Reset Webhook (jika bot tidak merespons)

```bash
python -m src.reset_webhook
```

### Perintah Makefile

| Perintah | Keterangan |
|----------|------------|
| `make install` | Install dependencies |
| `make install-dev` | Install + tools development |
| `make run` | Jalankan bot |
| `make lint` | Cek kualitas kode |
| `make format` | Format kode otomatis |
| `make check` | Cek format (untuk CI) |
| `make clean` | Bersihkan cache |

---

## 📁 Struktur Folder

```
magang-tracker-bot/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI
├── src/
│   ├── __init__.py
│   ├── bot.py                  # Entry point bot Telegram
│   ├── config.py               # Konfigurasi & environment
│   ├── reset_webhook.py        # Utilitas reset webhook
│   ├── services/
│   │   ├── scraper.py          # Web scraping metadata
│   │   └── extractor.py        # Ekstraksi AI dengan DeepSeek
│   └── utils/
│       └── platform.py         # Deteksi platform dari URL
├── .env.example                # Template environment variables
├── .gitignore                  # File yang di-ignore Git
├── CHANGELOG.md                # Riwayat perubahan
├── CODE_OF_CONDUCT.md          # Tata tertib komunitas
├── CONTRIBUTING.md             # Panduan kontribusi
├── LICENSE                     # Lisensi MIT
├── Makefile                    # Perintah otomatisasi
├── pyproject.toml              # Konfigurasi project Python
├── README.md                   # Dokumentasi ini
└── requirements.txt            # Daftar dependency
```

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk panduan lengkap.

Ringkasnya:
1. Fork repository
2. Buat branch fitur (`git checkout -b feature/nama-fitur`)
3. Commit perubahan (`git commit -m 'feat: tambah fitur X'`)
4. Push ke branch (`git push origin feature/nama-fitur`)
5. Buka Pull Request

---

## 📄 Lisensi

Project ini dilisensikan di bawah [MIT License](LICENSE).

---

<div align="center">

Dibuat dengan ❤️ untuk memudahkan pencarian magang

⭐ Star repository ini jika bermanfaat!

</div>

