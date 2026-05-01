"""Modul untuk ekstraksi informasi lowongan menggunakan AI DeepSeek."""

import json

from openai import OpenAI

from src.config import DEEPSEEK_API_KEY
from src.core.exceptions import DataExtractionError
from src.core.logger import logger
from src.models.internship import InternshipData
from src.services.company_extractor import CompanyExtractor
from src.services.position_categorizer import PositionCategorizer
from src.utils.platform import get_platform_from_url

# Inisialisasi DeepSeek client (opsional)
deepseek: OpenAI | None = None
if DEEPSEEK_API_KEY:
    try:
        deepseek = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        logger.info("✅ DeepSeek API ready")
    except Exception as e:
        logger.error(f"⚠️ Failed to initialize DeepSeek: {e}")
else:
    logger.warning(
        "⚠️ DEEPSEEK_API_KEY not set, extraction will use HTML scraping only"
    )


def extract_with_deepseek(url: str, scraped: dict[str, str]) -> dict[str, str]:
    """Ekstrak informasi lowongan menggunakan DeepSeek AI.

    Args:
        url: URL lowongan.
        scraped: Hasil scraping metadata (title, description).

    Returns:
        Dictionary dengan informasi lowongan yang diekstrak.

    Raises:
        DataExtractionError: If extraction fails.
    """
    if not deepseek:
        logger.debug("DeepSeek not available, using fallback extraction")
        return _fallback_extraction(url, scraped)

    prompt = f"""
Kamu adalah asisten yang membaca halaman lowongan kerja dari media sosial.
URL: {url}
Judul meta: {scraped.get('title')}
Deskripsi meta: {scraped.get('description')}

Ekstrak informasi lowongan dalam JSON dengan kunci:
- platform: (Instagram/TikTok/X/Threads)
- company: nama perusahaan (cari nama perusahaan yang jelas, hindari kata umum seperti "Lowongan", "Karir")
- position: posisi/jabatan (spesifik untuk tech: "Frontend Developer", "Backend Developer", "Fullstack Developer", "UI/UX Designer", "Data Scientist", "DevOps Engineer", "Mobile Developer", "QA Engineer", "Web Developer", "Software Engineer")
- division: divisi/tim (contoh: "Engineering", "Product", "Design", "Data Science", "Marketing")
- location: kota/lokasi penempatan (contoh: "Jakarta", "Remote", "Bandung")
- work_type: tipe kerja (Remote/Hybrid/On-site) – tebak dari konteks
- deadline: batas akhir pendaftaran dalam format YYYY-MM-DD (jika tidak ada, kosongkan)
- contact: kontak rekruter (email/username/nomor)
- description: ringkasan lowongan, maks 200 karakter

PERHATIAN:
1. Untuk company: cari nama perusahaan yang legit (PT, CV, atau brand name yang dikenal)
2. Untuk position: gunakan istilah teknologi yang spesifik, jangan "IT Staff" tapi "Software Engineer"
3. Jika tidak ada company yang jelas, kosongkan saja daripada menebak salah

Hanya keluarkan JSON tanpa teks lain.
"""
    try:
        logger.debug(f"Sending request to DeepSeek for URL: {url}")
        response = deepseek.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=400,
        )
        raw = response.choices[0].message.content.strip()
        logger.debug(f"DeepSeek raw response: {raw[:100]}...")

        # Clean up JSON response
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.endswith("```"):
            raw = raw[:-3]

        result = json.loads(raw)

        # Ensure we always return a dictionary
        if isinstance(result, list):
            logger.warning("DeepSeek returned list, taking first item")
            result = result[0] if result else {}

        if not isinstance(result, dict):
            logger.warning(f"DeepSeek returned {type(result)}, using fallback")
            return _fallback_extraction(url, scraped)

        # Validate and clean the extracted data
        result = _validate_and_clean_data(result, url, scraped)
        logger.info(f"Successfully extracted data for: {url}")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse JSON from DeepSeek: {e}")
        return _fallback_extraction(url, scraped)
    except Exception as e:
        logger.error(f"DeepSeek API error: {e}")
        return _fallback_extraction(url, scraped)


def _validate_and_clean_data(data: dict[str, str], url: str, scraped: dict[str, str]) -> dict[str, str]:
    """Validate and clean extracted data.
    
    Args:
        data: Raw extracted data
        url: Original URL for fallback
        scraped: Original scraped data for fallback extraction
        
    Returns:
        Validated and cleaned data dictionary
    """
    cleaned = {}
    
    # Define expected fields with default values
    field_defaults = {
        "platform": get_platform_from_url(url),
        "company": "",
        "position": "",
        "division": "",
        "location": "",
        "work_type": "",
        "deadline": "",
        "contact": "",
        "description": ""
    }
    
    # Process each field
    for field, default in field_defaults.items():
        value = data.get(field, default)
        
        # Clean up the value
        if isinstance(value, str):
            value = value.strip()
        elif isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        elif value is None:
            value = default
        else:
            value = str(value)
        
        cleaned[field] = value
    
    # Enhanced company extraction if AI didn't find it
    if not cleaned["company"] or len(cleaned["company"]) < 3:
        extracted_company = CompanyExtractor.extract_company(
            scraped.get("title", ""), 
            scraped.get("description", "")
        )
        if extracted_company:
            cleaned["company"] = extracted_company
            logger.info(f"Extracted company using fallback: {extracted_company}")
    
    # Enhanced position categorization
    if cleaned["position"]:
        category, normalized_position = PositionCategorizer.categorize_position(cleaned["position"])
        cleaned["position"] = normalized_position
        logger.info(f"Categorized position: {normalized_position} ({category})")
        
        # Suggest division if not provided
        if not cleaned["division"]:
            tech_stack = PositionCategorizer.extract_tech_stack(scraped.get("description", ""))
            suggested_division = PositionCategorizer.suggest_division(normalized_position, tech_stack)
            cleaned["division"] = suggested_division
            logger.info(f"Suggested division: {suggested_division}")
    
    # Field-specific validation
    if len(cleaned["description"]) > 200:
        cleaned["description"] = cleaned["description"][:200] + "..."
    
    cleaned["deadline"] = _validate_deadline(cleaned["deadline"])
    cleaned["work_type"] = _validate_work_type(cleaned["work_type"])
    
    return cleaned


def _validate_deadline(deadline: str) -> str:
    """Validate and normalize deadline format."""
    if not deadline or deadline.lower() in ["segera", "immediate", "asap"]:
        return ""

    # Try to parse common date formats
    import re
    from datetime import datetime

    # Common patterns
    patterns = [
        r"(\d{4})-(\d{2})-(\d{2})",  # YYYY-MM-DD
        r"(\d{2})/(\d{2})/(\d{4})",  # DD/MM/YYYY
        r"(\d{2})-(\d{2})-(\d{4})",  # DD-MM-YYYY
    ]

    for pattern in patterns:
        match = re.search(pattern, deadline)
        if match:
            try:
                if pattern == patterns[0]:  # YYYY-MM-DD
                    year, month, day = match.groups()
                else:  # DD/MM/YYYY or DD-MM-YYYY
                    day, month, year = match.groups()

                # Validate date
                datetime(int(year), int(month), int(day))
                return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            except ValueError:
                continue

    return deadline


def _validate_work_type(work_type: str) -> str:
    """Validate and normalize work type."""
    if not work_type:
        return ""

    work_type = work_type.lower().strip()

    # Normalize common variations
    mapping = {
        "remote": "Remote",
        "work from home": "Remote",
        "wfh": "Remote",
        "hybrid": "Hybrid",
        "office": "On-site",
        "onsite": "On-site",
        "on-site": "On-site",
        "offline": "On-site",
    }

    return mapping.get(work_type, work_type.title())


def _fallback_extraction(url: str, scraped: dict[str, str]) -> dict[str, str]:
    """Ekstraksi fallback jika DeepSeek tidak tersedia atau gagal.

    Args:
        url: URL lowongan.
        scraped: Hasil scraping metadata.

    Returns:
        Dictionary dengan informasi dasar dari scraping.
    """
    logger.debug("Using fallback extraction method")
    
    # Extract basic information from title
    title = scraped.get("title", "")
    description = scraped.get("description", "")
    
    # Use enhanced company extraction
    company = CompanyExtractor.extract_company(title, description) or ""
    
    # Extract position (fallback if company was found)
    position = title
    if company:
        # Try to remove company name from title to get position
        position = title.replace(company, "").strip(" -|")
    
    # Categorize position
    if position:
        category, normalized_position = PositionCategorizer.categorize_position(position)
        position = normalized_position
        logger.info(f"Fallback categorized position: {position} ({category})")
    
    # Extract tech stack and suggest division
    tech_stack = PositionCategorizer.extract_tech_stack(description)
    division = PositionCategorizer.suggest_division(position, tech_stack)
    
    return {
        "platform": get_platform_from_url(url),
        "company": company,
        "position": position,
        "division": division,
        "location": "",
        "work_type": "",
        "deadline": "",
        "contact": "",
        "description": description[:200],
    }
