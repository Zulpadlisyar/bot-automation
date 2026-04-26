"""Utilitas untuk deteksi platform dari URL."""


def get_platform_from_url(url: str) -> str:
    """Deteksi nama platform berdasarkan domain URL.

    Args:
        url: URL lowongan yang akan dideteksi.

    Returns:
        Nama platform (Instagram, TikTok, X, Threads) atau "Unknown".
    """
    url_lower = url.lower()
    if "instagram.com" in url_lower:
        return "Instagram"
    if "tiktok.com" in url_lower:
        return "TikTok"
    if "x.com" in url_lower or "twitter.com" in url_lower:
        return "X"
    if "threads.net" in url_lower:
        return "Threads"
    return "Unknown"

