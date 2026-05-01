"""Company name extraction utilities."""

import re
from typing import Optional, List


class CompanyExtractor:
    """Extracts company names from job posting titles and descriptions."""
    
    # Common company name patterns and indicators
    COMPANY_PATTERNS = [
        r'PT\s+([A-Za-z\s&]+?)(?:\s+[-–—]|\s+\||\s+at\s+|$)',  # PT Company Name
        r'CV\s+([A-Za-z\s&]+?)(?:\s+[-–—]|\s+\||\s+at\s+|$)',   # CV Company Name
        r'([A-Za-z\s&]+?)(?:\s+[-–—]\s+(?:Lowongan|Karir|We are hiring))',  # Company - Lowongan
        r'([A-Za-z\s&]+?)(?:\s+\|\s+(?:Lowongan|Karir|Hiring))',  # Company | Lowongan
        r'(?:[A-Za-z\s&]+?)\s+at\s+(PT\s+[A-Za-z\s&]+?)(?:\s+[-–—]|\s+\||\s+at\s+|$)',  # Position at PT Company
        r'(?:[A-Za-z\s&]+?)\s+at\s+(CV\s+[A-Za-z\s&]+?)(?:\s+[-–—]|\s+\||\s+at\s+|$)',  # Position at CV Company
        r'(?:[A-Za-z\s&]+?)\s+at\s+([A-Za-z\s&]+?)(?:\s+[-–—]|\s+\||\s+at\s+|$)',  # Position at Company
        r'([A-Za-z\s&]+?)(?:\s+is hiring)',  # Company is hiring
    ]
    
    # Words that are NOT company names
    EXCLUDE_WORDS = {
        'lowongan', 'karir', 'hiring', 'we', 'are', 'looking', 'for', 'join', 'team',
        'internship', 'magang', 'program', 'batch', 'generation', 'talent', 'recruitment',
        'career', 'opportunity', 'position', 'job', 'role', 'vacancy', 'opening',
        'immediate', 'urgent', 'needed', 'required', 'wanted', 'searching'
    }
    
    # Tech company indicators
    TECH_COMPANY_INDICATORS = {
        'tech', 'digital', 'software', 'solutions', 'studio', 'labs', 'systems',
        'innovations', 'creative', 'interactive', 'media', 'agency', 'consulting',
        'development', 'technology', 'data', 'cloud', 'cyber', 'security'
    }
    
    @classmethod
    def extract_company(cls, title: str, description: str = "") -> Optional[str]:
        """Extract company name from title and description.
        
        Args:
            title: Job title/posting title
            description: Job description
            
        Returns:
            Extracted company name or None if not found
        """
        # Combine title and description for better extraction
        text = f"{title} {description}".strip()
        
        # Try each pattern
        for pattern in cls.COMPANY_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                company = cls._clean_company_name(match.strip())
                if company and cls._is_valid_company(company):
                    return company
        
        # Try to find company names in description
        if description:
            desc_companies = cls._extract_from_description(description)
            if desc_companies:
                return desc_companies[0]
        
        return None
    
    @classmethod
    def _clean_company_name(cls, name: str) -> str:
        """Clean and normalize company name."""
        # Remove common suffixes and prefixes (but keep PT/CV)
        name = re.sub(r'\s+(?:is hiring|are hiring|hiring|looking for).*$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'^(?:we are|we\'re)\s+', '', name, flags=re.IGNORECASE)
        name = re.sub(r'\s+(?:indonesia|id)\s*$', '', name, flags=re.IGNORECASE)
        
        # Clean up extra spaces and special chars
        name = re.sub(r'\s+', ' ', name)
        name = name.strip(' -|')
        
        return name
    
    @classmethod
    def _is_valid_company(cls, name: str) -> bool:
        """Check if extracted name is likely a valid company name."""
        if not name or len(name) < 2:
            return False
        
        # Check if it's in exclude list
        name_lower = name.lower()
        if name_lower in cls.EXCLUDE_WORDS:
            return False
        
        # Check if contains exclude words
        for word in cls.EXCLUDE_WORDS:
            if word in name_lower:
                return False
        
        # Check if it's too generic (single common word)
        if len(name.split()) == 1 and name_lower in {'tech', 'digital', 'studio', 'agency'}:
            return False
        
        # Must have at least one letter
        if not re.search(r'[A-Za-z]', name):
            return False
        
        return True
    
    @classmethod
    def _extract_from_description(cls, description: str) -> List[str]:
        """Extract potential company names from description."""
        companies = []
        
        # Look for patterns like "About Company Name", "Company Name is", etc.
        patterns = [
            r'([A-Z][a-zA-Z\s&]+?)\s+is\s+(?:a|an)\s+(?:tech|digital|software|consulting)',
            r'About\s+([A-Z][a-zA-Z\s&]+?)(?:\.|\n|$)',
            r'([A-Z][a-zA-Z\s&]+?)\s+(?:is|are)\s+(?:looking|hiring|seeking)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, description)
            for match in matches:
                company = cls._clean_company_name(match.strip())
                if company and cls._is_valid_company(company):
                    companies.append(company)
        
        return companies
