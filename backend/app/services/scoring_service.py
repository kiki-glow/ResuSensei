"""
Resume Scoring Service
Handles comprehensive resume scoring with role-specific analysis
"""

from typing import Dict, List, Optional

from config.settings import ROLE_KEYWORDS, SCORING_WEIGHTS, ATS_RULES
from app.utils.text_analysis import (
    extract_resume_features,
    check_ats_compatibility,
    analyze_keyword_match,
    extract_skills_from_text,
    calculate_readability_score,
    detect_missing_sections,
    analyze_formatting_quality,
    count_action_verbs
)


class ResumeScorer:
    """
    Comprehensive resume scoring system with role-specific optimization.
    """
    
    def __init__(self):
        self.weights = SCORING_WEIGHTS
    
    def calculate_overall_score(
        self,
        resume_text: str,
        target_role: Optional[str] = None
    ) -> Dict:
        """
        Calculate comprehensive resume score.
        
        Args:
            resume_text: The resume text content
            target_role: Target role for keyword optimization (e.g., 'frontend_developer')
            
        Returns:
            Dictionary containing scores, breakdown, and analysis
        """
        # Extract features
        features = extract_resume_features(resume_text)
        
        # Calculate individual scores
        ats_score = self._score_ats_compatibility(resume_text, features)
        content_score = self._score_content_quality(resume_text, features)
        structure_score = self._score_structure(resume_text, features)
        achievement_score = self._score_achievements(resume_text, features)
        formatting_score = self._score_formatting(resume_text)
        
        # Keyword optimization score (role-specific if provided)
        if target_role and target_role in ROLE_KEYWORDS:
            keyword_score = self._score_keywords_for_role(resume_text, target_role)
        else:
            keyword_score = self._score_keywords_generic(resume_text)
        
        # Calculate weighted overall score
        overall_score = (
            ats_score * self.weights['ats_compatibility'] +
            content_score * self.weights['content_quality'] +
            keyword_score * self.weights['keyword_optimization'] +
            structure_score * self.weights['structure'] +
            achievement_score * self.weights['achievements'] +
            formatting_score * self.weights['formatting']
        )
        
        return {
            'overall_score': round(overall_score),
            'breakdown': {
                'ats_compatibility': round(ats_score),
                'content_quality': round(content_score),
                'keyword_optimization': round(keyword_score),
                'structure': round(structure_score),
                'achievements': round(achievement_score),
                'formatting': round(formatting_score)
            },
            'features': features,
            'grade': self._get_grade(overall_score)
        }
    
    def _score_ats_compatibility(self, text: str, features: Dict) -> float:
        """Score ATS compatibility (0-100)."""
        ats_check = check_ats_compatibility(text)
        base_score = ats_check['score']
        
        # Bonus points for good practices
        if features['has_email'] and features['has_phone']:
            base_score += 5
        
        if features['has_bullet_points']:
            base_score += 5
        
        return min(100, base_score)
    
    def _score_content_quality(self, text: str, features: Dict) -> float:
        """Score content quality based on various factors."""
        score = 70  # Base score
        
        # Word count check
        word_count = features['word_count']
        if 400 <= word_count <= 800:
            score += 15
        elif 300 <= word_count < 400 or 800 < word_count <= 1000:
            score += 10
        elif word_count < 300:
            score -= 20
        
        # Action verbs usage
        action_verb_ratio = features['action_verb_ratio']
        if action_verb_ratio >= 0.02:  # At least 2% action verbs
            score += 10
        elif action_verb_ratio >= 0.01:
            score += 5
        
        # Readability
        readability = calculate_readability_score(text)
        if readability >= 60:  # Good readability
            score += 5
        
        return min(100, max(0, score))
    
    def _score_structure(self, text: str, features: Dict) -> float:
        """Score resume structure and organization."""
        score = 60  # Base score
        
        # Check for required sections
        if features['has_experience']:
            score += 15
        if features['has_education']:
            score += 15
        if features['has_skills']:
            score += 10
        
        # Check for recommended sections
        if features['has_summary']:
            score += 5
        if features['has_certifications']:
            score += 5
        if features['has_projects']:
            score += 5
        
        return min(100, score)
    
    def _score_achievements(self, text: str, features: Dict) -> float:
        """Score quantifiable achievements and impact."""
        score = 50  # Base score
        
        # Check for numbers/metrics
        if features['has_numbers']:
            score += 20
        
        # Check for percentages (growth, improvement)
        if features['percentage_count'] > 0:
            score += 15
        
        # Check for currency (budget, revenue)
        if features['currency_count'] > 0:
            score += 15
        
        # Check for years of experience mentioned
        if features['years_of_experience'] > 0:
            score += 10
        
        return min(100, score)
    
    def _score_formatting(self, text: str) -> float:
        """Score formatting quality."""
        formatting_analysis = analyze_formatting_quality(text)
        return formatting_analysis['score']
    
    def _score_keywords_for_role(self, text: str, role: str) -> float:
        """Score keyword optimization for specific role."""
        role_data = ROLE_KEYWORDS.get(role, {})
        
        essential_keywords = role_data.get('essential_keywords', [])
        preferred_keywords = role_data.get('preferred_keywords', [])
        
        # Analyze essential keywords
        essential_match = analyze_keyword_match(text, essential_keywords)
        
        # Analyze preferred keywords
        preferred_match = analyze_keyword_match(text, preferred_keywords)
        
        # Weighted score (essential keywords are more important)
        score = (
            essential_match['match_percentage'] * 0.7 +
            preferred_match['match_percentage'] * 0.3
        )
        
        return min(100, score)
    
    def _score_keywords_generic(self, text: str) -> float:
        """Generic keyword scoring when no role specified."""
        extracted_skills = extract_skills_from_text(text)
        
        # Base score on number of skills found
        if len(extracted_skills) >= 15:
            return 90
        elif len(extracted_skills) >= 10:
            return 75
        elif len(extracted_skills) >= 5:
            return 60
        else:
            return 40
    
    def _get_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 70:
            return 'C'
        elif score >= 60:
            return 'D'
        else:
            return 'F'


class RoleSpecificAnalyzer:
    """
    Provides role-specific analysis and recommendations.
    """
    
    def analyze_for_role(self, resume_text: str, role: str) -> Dict:
        """
        Analyze resume for a specific role.
        
        Args:
            resume_text: The resume text
            role: Target role key (e.g., 'frontend_developer')
            
        Returns:
            Dictionary with role-specific analysis
        """
        if role not in ROLE_KEYWORDS:
            return {
                "error": f"Role '{role}' not found. Available roles: {list(ROLE_KEYWORDS.keys())}"
            }
        
        role_data = ROLE_KEYWORDS[role]
        
        # Analyze essential keywords
        essential_analysis = analyze_keyword_match(
            resume_text,
            role_data['essential_keywords']
        )
        
        # Analyze preferred keywords
        preferred_analysis = analyze_keyword_match(
            resume_text,
            role_data['preferred_keywords']
        )
        
        # Analyze action verbs
        action_verbs_present = [
            verb for verb in role_data['action_verbs']
            if verb.lower() in resume_text.lower()
        ]
        action_verbs_missing = [
            verb for verb in role_data['action_verbs']
            if verb.lower() not in resume_text.lower()
        ]
        
        # Check for certifications
        certifications_present = [
            cert for cert in role_data.get('certifications', [])
            if cert.lower() in resume_text.lower()
        ]
        certifications_missing = role_data.get('certifications', [])[:5]  # Top 5
        
        return {
            'role_name': role_data['name'],
            'essential_keywords': {
                'present': essential_analysis['present_keywords'],
                'missing': essential_analysis['missing_keywords'][:10],  # Top 10
                'match_percentage': essential_analysis['match_percentage']
            },
            'preferred_keywords': {
                'present': preferred_analysis['present_keywords'],
                'missing': preferred_analysis['missing_keywords'][:10],  # Top 10
                'match_percentage': preferred_analysis['match_percentage']
            },
            'action_verbs': {
                'present': action_verbs_present,
                'missing': action_verbs_missing[:8],  # Top 8
                'usage_percentage': round(len(action_verbs_present) / len(role_data['action_verbs']) * 100, 2)
            },
            'certifications': {
                'present': certifications_present,
                'suggested': certifications_missing
            },
            'overall_match': round(
                (essential_analysis['match_percentage'] * 0.6 +
                 preferred_analysis['match_percentage'] * 0.4),
                2
            )
        }