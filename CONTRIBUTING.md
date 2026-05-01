# Contributing to Magang Tracker Bot

Terima kasih atas minat Anda untuk berkontribusi! 🎉

## Cara Berkontribusi

### 1. Fork & Clone

```bash
# Fork repository di GitHub, lalu clone
gh repo fork zulpadlisyar/magang-tracker-bot --clone=true
cd magang-tracker-bot
```

### 2. Setup Environment

```bash
# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau: venv\Scripts\activate  # Windows

# Install dependencies
make install
```

### 3. Buat Branch Baru

```bash
git checkout -b feature/nama-fitur-anda
# atau
git checkout -b fix/nama-bug-yang-diperbaiki
```

### 4. Kode & Commit

- Ikuti standar [PEP 8](https://peps.python.org/pep-0008/)
- Gunakan [Conventional Commits](https://www.conventionalcommits.org/)
- Pastikan kode lolos linting: `make lint`
- Format otomatis: `make format`

Contoh pesan commit:
```
feat: tambah dukungan platform LinkedIn
fix: perbaiki error saat link tidak valid
docs: update README dengan contoh penggunaan
```

### 5. Push & Pull Request

```bash
git push origin feature/nama-fitur-anda
```

Buka Pull Request di GitHub dengan deskripsi yang jelas:
- Apa yang diubah?
- Mengapa diubah?
- Cara testing

## Standar Kode

- Python 3.10+
- Type hints untuk fungsi baru
- Docstring untuk modul dan fungsi publik
- Maksimal 88 karakter per baris (Black default)

## Melaporkan Bug

Gunakan [GitHub Issues](https://github.com/zulpadlisyar/magang-tracker-bot/issues) dengan template:

- **Deskripsi**: Apa masalahnya?
- **Reproduksi**: Langkah-langkah untuk memunculkan bug
- **Expected**: Seharusnya seperti apa?
- **Actual**: Kenyataannya seperti apa?
- **Environment**: OS, Python version, versi library

## Pertanyaan?

Silakan buat [Discussion](https://github.com/zulpadlisyar/magang-tracker-bot/discussions) atau hubungi maintainer.

