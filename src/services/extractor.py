"""Modul untuk ekstraksi informasi lowongan menggunakan AI DeepSeek."""

import json

from openai import OpenAI

from src.config import DEEPSEEK_API_KEY
from src.utils.platform import get_platform_from_url

# Inisialisasi DeepSeek client (opsional)
deepseek: OpenAI | None = None
if DEEPSEEK_API_KEY:
    try:
        deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        print("✅ DeepSeek API siap")
    except Exception as e:
        print(f"⚠️ Gagal inisialisasi DeepSeek: {e}")
else:
    print("⚠️ DEEPSEEK_API_KEY tidak diset, ekstraksi hanya pakai scraping HTML")


def extract_with_deepseek(url: str, scraped: dict[str, str]) -> dict[str, str]:
    """Ekstrak informasi lowongan menggunakan DeepSeek AI.

    Args:
        url: URL lowongan.
        scraped: Hasil scraping metadata (title, description).

    Returns:
        Dictionary dengan informasi lowongan yang diekstrak.
    """
    if not deepseek:
        return _fallback_extraction(url, scraped)

    prompt = f"""
Kamu adalah asisten yang membaca halaman lowongan kerja dari media sosial.
URL: {url}
Judul meta: {scraped.get('title')}
Deskripsi meta: {scraped.get('description')}

Ekstrak informasi lowongan dalam JSON dengan kunci:
- platform: (Instagram/TikTok/X/Threads)
- company: nama perusahaan
- position: posisi/jabatan
- division: divisi/tim (contoh: "Marketing", "Engineering")
- location: kota/lokasi penempatan (contoh: "Jakarta", "Remote")
- work_type: tipe kerja (Remote/Hybrid/On-site) – tebak dari konteks
- deadline: batas akhir pendaftaran dalam format YYYY-MM-DD (jika tidak ada, kosongkan)
- contact: kontak rekruter (email/username/nomor)
- description: ringkasan lowongan, maks 200 karakter

Hanya keluarkan JSON tanpa teks lain.
"""
    try:
        response = deepseek.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=400,
        )
        raw = response.choices[0].message.content.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]
        return json.loads(raw)
    except Exception as e:
        print(f"DeepSeek error: {e}")
        return _fallback_extraction(url, scraped)


def _fallback_extraction(url: str, scraped: dict[str, str]) -> dict[str, str]:
    """Ekstraksi fallback jika DeepSeek tidak tersedia atau gagal.

    Args:
        url: URL lowongan.
        scraped: Hasil scraping metadata.

    Returns:
        Dictionary dengan informasi dasar dari scraping.
    """
    return {
        "platform": get_platform_from_url(url),
        "company": "",
        "position": scraped.get("title", ""),
        "division": "",
        "location": "",
        "work_type": "",
        "deadline": "",
        "contact": "",
        "description": scraped.get("description", "")[:200],
    }

