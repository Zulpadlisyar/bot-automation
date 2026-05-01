"""Tech position categorization utilities."""

import re
from typing import Dict, List, Optional, Tuple


class PositionCategorizer:
    """Categorizes and normalizes tech position names."""
    
    # Tech position mappings for better categorization
    POSITION_MAPPINGS = {
        # Frontend
        'frontend': ['frontend developer', 'front end developer', 'ui developer', 'web frontend', 'react developer', 'vue developer', 'angular developer'],
        'frontend engineer': ['frontend engineer', 'front end engineer', 'ui engineer'],
        'ui/ux designer': ['ui designer', 'ux designer', 'ui/ux designer', 'product designer', 'interface designer'],
        
        # Backend
        'backend': ['backend developer', 'back end developer', 'server developer', 'api developer'],
        'backend engineer': ['backend engineer', 'back end engineer', 'server engineer', 'api engineer'],
        
        # Fullstack
        'fullstack': ['fullstack developer', 'full stack developer', 'full-stack developer', 'fullstack engineer', 'full stack engineer'],
        
        # Mobile
        'mobile developer': ['mobile developer', 'ios developer', 'android developer', 'react native developer', 'flutter developer'],
        'mobile engineer': ['mobile engineer', 'ios engineer', 'android engineer'],
        
        # Data
        'data scientist': ['data scientist', 'data science', 'data analyst', 'data engineer'],
        'machine learning': ['ml engineer', 'machine learning engineer', 'ai engineer', 'artificial intelligence'],
        
        # DevOps & Infrastructure
        'DevOps': ['devops engineer', 'devops', 'site reliability engineer', 'sre', 'infrastructure engineer'],
        'Cloud Engineer': ['cloud engineer', 'aws engineer', 'azure engineer', 'gcp engineer'],
        
        # QA & Testing
        'QA Engineer': ['qa engineer', 'quality assurance engineer', 'test engineer', 'automation engineer'],
        'QA Tester': ['qa tester', 'quality assurance tester', 'software tester'],
        
        # General Software
        'software engineer': ['software engineer', 'software developer', 'programmer', 'coder', 'software developer'],
        'web developer': ['web developer', 'web programmer', 'website developer'],
        
        # Other Tech
        'game developer': ['game developer', 'unity developer', 'unreal developer'],
        'blockchain': ['blockchain developer', 'web3 developer', 'smart contract developer'],
        'cybersecurity': ['cybersecurity', 'security engineer', 'information security'],
        'database': ['database administrator', 'dba', 'database engineer'],
    }
    
    # Non-tech positions to exclude or categorize differently
    NON_TECH_POSITIONS = {
        'marketing', 'sales', 'hr', 'human resources', 'finance', 'accounting', 'admin',
        'administrative', 'customer service', 'support', 'content writer', 'graphic designer',
        'social media', 'community manager', 'project manager', 'product manager'
    }
    
    @classmethod
    def categorize_position(cls, position: str) -> Tuple[str, str]:
        """Categorize position into tech category and normalized name.
        
        Args:
            position: Raw position string
            
        Returns:
            Tuple of (category, normalized_position)
        """
        if not position:
            return 'Unknown', ''
        
        position_lower = position.lower().strip()
        
        # Check if it's non-tech
        for non_tech in cls.NON_TECH_POSITIONS:
            if non_tech in position_lower:
                return 'Non-Tech', position.title()
        
        # Check tech position mappings
        for category, variations in cls.POSITION_MAPPINGS.items():
            for variation in variations:
                if variation in position_lower:
                    return 'Tech', category.title()
        
        # Check for general tech keywords
        tech_keywords = ['developer', 'engineer', 'programmer', 'coder', 'tech', 'it', 'software']
        if any(keyword in position_lower for keyword in tech_keywords):
            return 'Tech', cls._normalize_generic_position(position)
        
        return 'Unknown', position.title()
    
    @classmethod
    def _normalize_generic_position(cls, position: str) -> str:
        """Normalize generic tech positions."""
        position_lower = position.lower()
        
        # Common normalizations
        if 'intern' in position_lower or 'magang' in position_lower:
            return 'Software Engineer Intern'
        elif 'junior' in position_lower or 'jr' in position_lower:
            return 'Junior Software Engineer'
        elif 'senior' in position_lower or 'sr' in position_lower:
            return 'Senior Software Engineer'
        elif 'lead' in position_lower:
            return 'Tech Lead'
        elif 'manager' in position_lower:
            return 'Engineering Manager'
        elif 'architect' in position_lower:
            return 'Software Architect'
        else:
            return 'Software Engineer'
    
    @classmethod
    def extract_tech_stack(cls, description: str) -> List[str]:
        """Extract tech stack from description.
        
        Args:
            description: Job description
            
        Returns:
            List of technologies mentioned
        """
        if not description:
            return []
        
        # Common tech stack keywords with proper casing
        tech_stack = {
            'react': 'React',
            'vue': 'Vue', 
            'angular': 'Angular',
            'javascript': 'JavaScript',
            'typescript': 'TypeScript',
            'nodejs': 'Node.js',
            'node.js': 'Node.js',
            'python': 'Python',
            'java': 'Java',
            'c++': 'C++',
            'c#': 'C#',
            'go': 'Go',
            'rust': 'Rust',
            'php': 'PHP',
            'ruby': 'Ruby',
            'swift': 'Swift',
            'kotlin': 'Kotlin',
            'aws': 'AWS',
            'azure': 'Azure',
            'gcp': 'GCP',
            'docker': 'Docker',
            'kubernetes': 'Kubernetes',
            'jenkins': 'Jenkins',
            'git': 'Git',
            'linux': 'Linux',
            'mysql': 'MySQL',
            'postgresql': 'PostgreSQL',
            'mongodb': 'MongoDB',
            'redis': 'Redis',
            'firebase': 'Firebase',
            'graphql': 'GraphQL',
            'rest api': 'REST API',
            'flutter': 'Flutter',
            'react native': 'React Native',
            'ios': 'iOS',
            'android': 'Android',
            'unity': 'Unity',
            'unreal': 'Unreal',
            'blockchain': 'Blockchain',
            'machine learning': 'Machine Learning',
            'ai': 'AI',
            'data science': 'Data Science',
            'tensorflow': 'TensorFlow',
            'pytorch': 'PyTorch',
            'nlp': 'NLP'
        }
        
        found_tech = []
        description_lower = description.lower()
        
        for tech_lower, tech_proper in tech_stack.items():
            if tech_lower in description_lower:
                found_tech.append(tech_proper)
        
        return sorted(found_tech)
    
    @classmethod
    def suggest_division(cls, position: str, tech_stack: List[str]) -> str:
        """Suggest division based on position and tech stack.
        
        Args:
            position: Categorized position
            tech_stack: List of technologies
            
        Returns:
            Suggested division/team
        """
        position_lower = position.lower()
        tech_stack_lower = [tech.lower() for tech in tech_stack]
        
        # Frontend division
        if any(keyword in position_lower for keyword in ['frontend', 'ui', 'ux', 'web']):
            return 'Frontend'
        
        # Backend division
        if any(keyword in position_lower for keyword in ['backend', 'server', 'api']):
            return 'Backend'
        
        # Mobile division
        if any(keyword in position_lower for keyword in ['mobile', 'ios', 'android']):
            return 'Mobile'
        
        # Data division
        if any(keyword in position_lower for keyword in ['data', 'ml', 'ai', 'machine learning']):
            return 'Data Science'
        
        # DevOps division
        if any(keyword in position_lower for keyword in ['devops', 'infrastructure', 'cloud', 'sre']):
            return 'DevOps'
        
        # Check tech stack for clues
        if any(tech in tech_stack_lower for tech in ['react', 'vue', 'angular', 'javascript']):
            return 'Frontend'
        elif any(tech in tech_stack_lower for tech in ['python', 'java', 'nodejs', 'go']):
            return 'Backend'
        elif any(tech in tech_stack_lower for tech in ['aws', 'azure', 'docker', 'kubernetes']):
            return 'DevOps'
        elif any(tech in tech_stack_lower for tech in ['tensorflow', 'pytorch', 'machine learning']):
            return 'Data Science'
        
        return 'Engineering'
