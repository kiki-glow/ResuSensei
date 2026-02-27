"""
Utility Functions for Resume Analysis
Handles feature extraction, text processing, and ATS compatibility checks
"""

import re
from typing import Dict, List, Tuple
import numpy as np
from collections import Counter


# Action verbs commonly used in resumes
ACTION_VERBS = [
    "achieved", "implemented", "managed", "developed", "optimized", "led", "created",
    "designed", "built", "delivered", "improved", "increased", "reduced", "launched",
    "architected", "coordinated", "facilitated", "executed", "streamlined", "analyzed",
    "researched", "collaborated", "drove", "spearheaded", "established", "transformed",
    "automated", "migrated", "deployed", "configured", "integrated", "maintained",
    "secured", "enhanced", "resolved", "trained", "mentored", "presented", "authored"
]


def extract_resume_features(text: str) -> Dict:
    """
    Extract comprehensive features from resume text for scoring.
    
    Args:
        text: Resume text content
        
    Returns:
        Dictionary containing various resume features and metrics
    """
    words = text.split()
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    
    features = {
        # Basic metrics
        'word_count': len(words),
        'sentence_count': len(sentences),
        'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
        'avg_sentence_length': len(words) / len(sentences) if sentences else 0,
        
        # Action verbs
        'action_verb_count': count_action_verbs(text),
        'action_verb_ratio': count_action_verbs(text) / len(words) if words else 0,
        
        # Quantifiable achievements
        'has_numbers': 1 if any(char.isdigit() for char in text) else 0,
        'percentage_count': text.count('%'),
        'currency_count': text.count('$') + text.count('€') + text.count('£'),
        'number_count': len(re.findall(r'\d+', text)),
        
        # Section detection
        'has_education': 1 if re.search(r'\beducation\b', text, re.I) else 0,
        'has_experience': 1 if re.search(r'\bexperience\b|\bemployment\b', text, re.I) else 0,
        'has_skills': 1 if re.search(r'\bskills\b|\bcompetencies\b', text, re.I) else 0,
        'has_summary': 1 if re.search(r'\bsummary\b|\bobjective\b|\bprofile\b', text, re.I) else 0,
        'has_projects': 1 if re.search(r'\bprojects\b', text, re.I) else 0,
        'has_certifications': 1 if re.search(r'\bcertifications\b|\bcertificates\b', text, re.I) else 0,
        
        # Formatting indicators
        'has_bullet_points': 1 if ('•' in text or '-' in text or '*' in text) else 0,
        'newline_count': text.count('\n'),
        'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
        
        # Contact information
        'has_email': 1 if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text) else 0,
        'has_phone': 1 if re.search(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text) else 0,
        'has_linkedin': 1 if 'linkedin.com' in text.lower() else 0,
        'has_github': 1 if 'github.com' in text.lower() else 0,
        
        # Professional indicators
        'years_of_experience': extract_years_of_experience(text),
        'education_level': detect_education_level(text),
    }
    
    return features


def count_action_verbs(text: str) -> int:
    """Count the number of action verbs in the text."""
    text_lower = text.lower()
    count = sum(1 for verb in ACTION_VERBS if f" {verb}" in text_lower or f"\n{verb}" in text_lower)
    return count


def extract_years_of_experience(text: str) -> int:
    """
    Extract years of experience from resume text.
    Looks for patterns like "5 years", "5+ years", etc.
    """
    patterns = [
        r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
        r'experience[:\s]+(\d+)\+?\s*years?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return int(match.group(1))
    
    return 0


def detect_education_level(text: str) -> int:
    """
    Detect highest education level (encoded as integer).
    0: None detected, 1: Bachelor's, 2: Master's, 3: PhD
    """
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['phd', 'ph.d', 'doctorate', 'doctoral']):
        return 3
    elif any(word in text_lower for word in ["master's", 'masters', 'msc', 'm.sc', 'mba', 'ma', 'm.a']):
        return 2
    elif any(word in text_lower for word in ["bachelor's", 'bachelors', 'bsc', 'b.sc', 'ba', 'b.a', 'bs', 'b.s']):
        return 1
    
    return 0


def check_ats_compatibility(text: str) -> Dict[str, any]:
    """
    Check ATS (Applicant Tracking System) compatibility.
    
    Returns:
        Dictionary with ATS compatibility score and issues
    """
    issues = []
    score = 100
    
    # Check for problematic characters
    if '•' in text or '→' in text or '©' in text or '®' in text:
        issues.append("Contains special characters that may not be ATS-friendly")
        score -= 5
    
    # Check word count
    word_count = len(text.split())
    if word_count < 300:
        issues.append("Resume is too short (less than 300 words)")
        score -= 10
    elif word_count > 1000:
        issues.append("Resume is too long (more than 1000 words)")
        score -= 5
    
    # Check for standard sections
    required_sections = ['experience', 'education']
    for section in required_sections:
        if section not in text.lower():
            issues.append(f"Missing standard section: {section.title()}")
            score -= 15
    
    # Check for contact information
    if not re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        issues.append("Email address not detected")
        score -= 10
    
    # Check for bullet points
    if not ('•' in text or '-' in text or '*' in text or '\n-' in text):
        issues.append("No bullet points detected - use bullet points for better readability")
        score -= 5
    
    # Check for quantifiable achievements
    if not re.search(r'\d+%|\$\d+|\d+\s*years?', text):
        issues.append("No quantifiable achievements detected")
        score -= 10
    
    # Check for action verbs
    action_verb_count = count_action_verbs(text)
    if action_verb_count < 5:
        issues.append("Too few action verbs - use strong action verbs to describe accomplishments")
        score -= 10
    
    return {
        "score": max(0, score),
        "issues": issues,
        "is_compatible": score >= 70
    }


def analyze_keyword_match(resume_text: str, target_keywords: List[str]) -> Dict:
    """
    Analyze how well resume keywords match target role keywords.
    
    Args:
        resume_text: The resume text
        target_keywords: List of keywords for the target role
        
    Returns:
        Dictionary with keyword analysis results
    """
    resume_lower = resume_text.lower()
    
    present_keywords = []
    missing_keywords = []
    
    for keyword in target_keywords:
        if keyword.lower() in resume_lower:
            present_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    match_percentage = (len(present_keywords) / len(target_keywords) * 100) if target_keywords else 0
    
    return {
        "present_keywords": present_keywords,
        "missing_keywords": missing_keywords,
        "match_percentage": round(match_percentage, 2),
        "present_count": len(present_keywords),
        "missing_count": len(missing_keywords),
        "total_keywords": len(target_keywords)
    }


def extract_skills_from_text(text: str) -> List[str]:
    """
    Extract potential skills from resume text.
    This is a simple implementation - can be enhanced with NER models.
    """
    # Common technical and soft skills
    common_skills = [
        # Programming Languages
        'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'ruby', 'go', 'rust',
        'php', 'swift', 'kotlin', 'r', 'matlab', 'scala', 'perl',
        
        # Web Technologies
        'html', 'css', 'react', 'angular', 'vue', 'node.js', 'express', 'django',
        'flask', 'spring boot', 'asp.net', 'laravel', 'rails',
        
        # Databases
        'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra',
        'oracle', 'sql server', 'dynamodb', 'firebase',
        
        # Cloud & DevOps
        'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'ci/cd',
        'terraform', 'ansible', 'linux', 'nginx', 'apache',
        
        # Data Science & ML
        'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
        'pandas', 'numpy', 'tableau', 'power bi', 'spark', 'hadoop',
        
        # Soft Skills
        'leadership', 'communication', 'teamwork', 'problem solving', 'project management',
        'agile', 'scrum', 'analytical', 'creative', 'time management'
    ]
    
    text_lower = text.lower()
    found_skills = [skill for skill in common_skills if skill in text_lower]
    
    return found_skills


def calculate_readability_score(text: str) -> float:
    """
    Calculate a simple readability score (Flesch Reading Ease approximation).
    Higher score = easier to read (0-100 scale)
    """
    words = text.split()
    sentences = [s for s in text.split('.') if s.strip()]
    
    if not words or not sentences:
        return 0.0
    
    total_words = len(words)
    total_sentences = len(sentences)
    total_syllables = sum(count_syllables(word) for word in words)
    
    avg_sentence_length = total_words / total_sentences
    avg_syllables_per_word = total_syllables / total_words
    
    # Flesch Reading Ease formula (simplified)
    score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
    
    return max(0, min(100, score))


def count_syllables(word: str) -> int:
    """
    Estimate syllable count for a word.
    """
    word = word.lower()
    vowels = 'aeiou'
    syllable_count = 0
    previous_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel
    
    # Adjust for silent 'e'
    if word.endswith('e'):
        syllable_count -= 1
    
    # Ensure at least one syllable
    if syllable_count == 0:
        syllable_count = 1
    
    return syllable_count


def detect_missing_sections(text: str) -> List[str]:
    """
    Detect which standard resume sections are missing.
    """
    text_lower = text.lower()
    
    sections_to_check = {
        'Professional Summary': ['summary', 'objective', 'profile', 'about'],
        'Work Experience': ['experience', 'employment', 'work history'],
        'Education': ['education', 'academic', 'degree'],
        'Skills': ['skills', 'competencies', 'expertise'],
        'Certifications': ['certifications', 'certificates', 'licensed'],
        'Projects': ['projects', 'portfolio']
    }
    
    missing_sections = []
    
    for section_name, keywords in sections_to_check.items():
        if not any(keyword in text_lower for keyword in keywords):
            missing_sections.append(section_name)
    
    return missing_sections


def extract_contact_info(text: str) -> Dict[str, str]:
    """
    Extract contact information from resume.
    """
    contact_info = {}
    
    # Email
    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    if email_match:
        contact_info['email'] = email_match.group()
    
    # Phone
    phone_match = re.search(r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
    if phone_match:
        contact_info['phone'] = phone_match.group()
    
    # LinkedIn
    linkedin_match = re.search(r'linkedin\.com/in/[\w-]+', text, re.I)
    if linkedin_match:
        contact_info['linkedin'] = linkedin_match.group()
    
    # GitHub
    github_match = re.search(r'github\.com/[\w-]+', text, re.I)
    if github_match:
        contact_info['github'] = github_match.group()
    
    return contact_info


def analyze_formatting_quality(text: str) -> Dict:
    """
    Analyze the formatting quality of the resume.
    """
    issues = []
    score = 100
    
    # Check for excessive whitespace
    if '\n\n\n' in text:
        issues.append("Excessive blank lines detected")
        score -= 5
    
    # Check for inconsistent spacing
    lines = text.split('\n')
    if any(line.startswith(' ' * 5) for line in lines):  # Deep indentation
        issues.append("Inconsistent indentation detected")
        score -= 5
    
    # Check for all caps (except section headers)
    words = text.split()
    all_caps_words = [w for w in words if w.isupper() and len(w) > 3]
    if len(all_caps_words) > 10:
        issues.append("Too many words in ALL CAPS")
        score -= 5
    
    # Check for proper bullet point usage
    bullet_patterns = [r'^\s*[-•*]\s', r'^\s*\d+\.\s']
    has_bullets = any(re.search(pattern, text, re.M) for pattern in bullet_patterns)
    if not has_bullets:
        issues.append("No bullet points detected - use bullets for lists")
        score -= 10
    
    return {
        "score": max(0, score),
        "issues": issues
    }