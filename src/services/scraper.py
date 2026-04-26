"""Modul untuk scraping metadata dari halaman web."""

import requests
from bs4 import BeautifulSoup


def scrape_metadata(url: str) -> dict[str, str]:
    """Scrape metadata Open Graph dari URL.

    Args:
        url: URL halaman yang akan di-scrape.

    Returns:
        Dictionary dengan kunci 'title' dan 'description'.
        Jika gagal, mengembalikan string kosong dan pesan error.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        title_tag = soup.find("meta", property="og:title")
        desc_tag = soup.find("meta", property="og:description")

        return {
            "title": title_tag["content"].strip() if title_tag else "",
            "description": desc_tag["content"].strip() if desc_tag else "",
        }
    except Exception as e:
        return {"title": "", "description": f"Error: {e}"}

