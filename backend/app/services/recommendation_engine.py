"""
Recommendation Engine
Generates detailed, actionable recommendations for resume improvement
"""

from typing import Dict, List, Optional

from config.settings import ROLE_KEYWORDS, ATS_RULES
from app.utils.text_analysis import (
    detect_missing_sections,
    count_action_verbs,
    extract_resume_features
)


class RecommendationEngine:
    """
    Generates comprehensive, actionable recommendations for resume improvement.
    """
    
    def generate_recommendations(
        self,
        resume_text: str,
        score_breakdown: Dict,
        role_analysis: Optional[Dict] = None,
        target_role: Optional[str] = None
    ) -> List[Dict]:
        """
        Generate comprehensive recommendations.
        
        Args:
            resume_text: The resume text
            score_breakdown: Score breakdown from ResumeScorer
            role_analysis: Role-specific analysis (if available)
            target_role: Target role key
            
        Returns:
            List of recommendation dictionaries with priority, category, and suggestion
        """
        recommendations = []
        
        # ATS Compatibility Recommendations
        if score_breakdown['ats_compatibility'] < 80:
            recommendations.extend(self._get_ats_recommendations(resume_text))
        
        # Content Quality Recommendations
        if score_breakdown['content_quality'] < 75:
            recommendations.extend(self._get_content_recommendations(resume_text))
        
        # Keyword Optimization Recommendations
        if role_analysis and score_breakdown['keyword_optimization'] < 80:
            recommendations.extend(self._get_keyword_recommendations(role_analysis, target_role))
        
        # Structure Recommendations
        if score_breakdown['structure'] < 75:
            recommendations.extend(self._get_structure_recommendations(resume_text))
        
        # Achievement Recommendations
        if score_breakdown['achievements'] < 70:
            recommendations.extend(self._get_achievement_recommendations(resume_text))
        
        # Formatting Recommendations
        if score_breakdown['formatting'] < 85:
            recommendations.extend(self._get_formatting_recommendations(resume_text))
        
        # Role-Specific Recommendations
        if role_analysis:
            recommendations.extend(self._get_role_specific_recommendations(role_analysis, target_role))
        
        # Sort by priority and return top recommendations
        recommendations.sort(key=lambda x: self._priority_weight(x['priority']), reverse=True)
        
        return recommendations[:15]  # Return top 15 recommendations
    
    def _priority_weight(self, priority: str) -> int:
        """Convert priority to numeric weight for sorting."""
        weights = {'critical': 3, 'high': 2, 'medium': 1, 'low': 0}
        return weights.get(priority, 0)
    
    def _get_ats_recommendations(self, text: str) -> List[Dict]:
        """Generate ATS compatibility recommendations."""
        recommendations = []
        features = extract_resume_features(text)
        
        # Contact information
        if not features['has_email']:
            recommendations.append({
                'priority': 'critical',
                'category': 'ATS Compatibility',
                'title': 'Add Email Address',
                'description': 'Include a professional email address in your contact information. Most ATS systems require this field.',
                'impact': 'High - Essential for ATS parsing'
            })
        
        if not features['has_phone']:
            recommendations.append({
                'priority': 'high',
                'category': 'ATS Compatibility',
                'title': 'Add Phone Number',
                'description': 'Include your phone number in a standard format (e.g., (123) 456-7890 or +1-123-456-7890).',
                'impact': 'Medium - Important for contact information'
            })
        
        # Standard sections
        if not features['has_experience']:
            recommendations.append({
                'priority': 'critical',
                'category': 'ATS Compatibility',
                'title': 'Add Work Experience Section',
                'description': 'Include a dedicated "Work Experience" or "Professional Experience" section with your employment history.',
                'impact': 'High - Critical for ATS parsing'
            })
        
        if not features['has_education']:
            recommendations.append({
                'priority': 'critical',
                'category': 'ATS Compatibility',
                'title': 'Add Education Section',
                'description': 'Include an "Education" section with your degrees, institutions, and graduation dates.',
                'impact': 'High - Critical for ATS parsing'
            })
        
        # Bullet points
        if not features['has_bullet_points']:
            recommendations.append({
                'priority': 'high',
                'category': 'ATS Compatibility',
                'title': 'Use Bullet Points',
                'description': 'Format your achievements and responsibilities using bullet points (•, -, or *) for better ATS readability.',
                'impact': 'Medium - Improves ATS parsing accuracy'
            })
        
        # Word count
        if features['word_count'] < 300:
            recommendations.append({
                'priority': 'high',
                'category': 'ATS Compatibility',
                'title': 'Expand Your Resume Content',
                'description': f'Your resume has {features["word_count"]} words. Aim for 400-800 words to provide sufficient detail for ATS systems.',
                'impact': 'Medium - More content helps ATS matching'
            })
        
        return recommendations
    
    def _get_content_recommendations(self, text: str) -> List[Dict]:
        """Generate content quality recommendations."""
        recommendations = []
        features = extract_resume_features(text)
        action_verb_count = count_action_verbs(text)
        
        # Action verbs
        if action_verb_count < 8:
            recommendations.append({
                'priority': 'high',
                'category': 'Content Quality',
                'title': 'Use Strong Action Verbs',
                'description': 'Start your bullet points with powerful action verbs like "Developed", "Implemented", "Led", "Optimized", "Achieved", etc.',
                'impact': 'High - Makes accomplishments more impactful',
                'examples': [
                    'Instead of: "Responsible for managing team"',
                    'Write: "Led a cross-functional team of 8 engineers"'
                ]
            })
        
        # Professional summary
        if not features['has_summary']:
            recommendations.append({
                'priority': 'medium',
                'category': 'Content Quality',
                'title': 'Add a Professional Summary',
                'description': 'Include a 2-3 sentence professional summary at the top highlighting your experience, key skills, and value proposition.',
                'impact': 'Medium - Helps ATS and recruiters quickly understand your profile',
                'examples': [
                    'Example: "Senior Frontend Developer with 5+ years building scalable web applications. Expert in React, TypeScript, and modern web technologies. Passionate about creating exceptional user experiences."'
                ]
            })
        
        return recommendations
    
    def _get_keyword_recommendations(self, role_analysis: Dict, target_role: str) -> List[Dict]:
        """Generate keyword optimization recommendations."""
        recommendations = []
        
        essential_missing = role_analysis['essential_keywords']['missing'][:5]
        preferred_missing = role_analysis['preferred_keywords']['missing'][:5]
        
        if essential_missing:
            recommendations.append({
                'priority': 'critical',
                'category': 'Keyword Optimization',
                'title': f'Add Essential {role_analysis["role_name"]} Keywords',
                'description': f'Your resume is missing critical keywords for {role_analysis["role_name"]} roles. Add these if applicable to your experience.',
                'impact': 'High - Essential for passing ATS keyword filters',
                'keywords': essential_missing,
                'suggestion': f'Include these keywords naturally in your skills section and throughout your work experience: {", ".join(essential_missing[:3])}'
            })
        
        if preferred_missing:
            recommendations.append({
                'priority': 'high',
                'category': 'Keyword Optimization',
                'title': f'Add Preferred {role_analysis["role_name"]} Keywords',
                'description': 'Including these additional keywords will strengthen your resume for ATS matching.',
                'impact': 'Medium - Improves keyword match score',
                'keywords': preferred_missing,
                'suggestion': f'Consider adding: {", ".join(preferred_missing[:3])}'
            })
        
        # Action verbs specific to role
        action_verbs_missing = role_analysis['action_verbs']['missing'][:4]
        if len(action_verbs_missing) > 0:
            recommendations.append({
                'priority': 'medium',
                'category': 'Keyword Optimization',
                'title': f'Use Role-Specific Action Verbs',
                'description': f'Use action verbs commonly found in {role_analysis["role_name"]} job postings.',
                'impact': 'Medium - Aligns with role expectations',
                'examples': action_verbs_missing
            })
        
        return recommendations
    
    def _get_structure_recommendations(self, text: str) -> List[Dict]:
        """Generate structure recommendations."""
        recommendations = []
        missing_sections = detect_missing_sections(text)
        
        priority_sections = {
            'Professional Summary': 'medium',
            'Skills': 'high',
            'Certifications': 'medium',
            'Projects': 'low'
        }
        
        for section in missing_sections:
            if section in priority_sections:
                recommendations.append({
                    'priority': priority_sections[section],
                    'category': 'Structure',
                    'title': f'Add {section} Section',
                    'description': self._get_section_description(section),
                    'impact': 'Medium - Improves resume completeness'
                })
        
        return recommendations
    
    def _get_section_description(self, section: str) -> str:
        """Get description for missing section."""
        descriptions = {
            'Professional Summary': 'Add a brief 2-3 sentence summary at the top of your resume highlighting your expertise and career objectives.',
            'Skills': 'Include a dedicated skills section listing your technical and soft skills relevant to your target role.',
            'Certifications': 'List any professional certifications, licenses, or relevant training you have completed.',
            'Projects': 'Showcase key projects that demonstrate your skills and achievements, especially if you have limited work experience.'
        }
        return descriptions.get(section, f'Consider adding a {section} section to your resume.')
    
    def _get_achievement_recommendations(self, text: str) -> List[Dict]:
        """Generate achievement-focused recommendations."""
        recommendations = []
        features = extract_resume_features(text)
        
        if not features['has_numbers']:
            recommendations.append({
                'priority': 'high',
                'category': 'Impact & Achievements',
                'title': 'Quantify Your Achievements',
                'description': 'Add numbers, percentages, and metrics to demonstrate the impact of your work.',
                'impact': 'High - Makes achievements concrete and measurable',
                'examples': [
                    'Instead of: "Improved website performance"',
                    'Write: "Improved website performance by 45%, reducing page load time from 3.2s to 1.8s"',
                    '',
                    'Instead of: "Managed a team"',
                    'Write: "Led a team of 12 developers across 3 time zones"'
                ]
            })
        
        if features['percentage_count'] == 0:
            recommendations.append({
                'priority': 'medium',
                'category': 'Impact & Achievements',
                'title': 'Show Growth and Improvement',
                'description': 'Use percentages to show growth, improvements, or efficiency gains.',
                'impact': 'Medium - Demonstrates measurable impact',
                'examples': [
                    '"Increased user engagement by 35%"',
                    '"Reduced deployment time by 60%"',
                    '"Improved code coverage from 45% to 85%"'
                ]
            })
        
        if features['currency_count'] == 0:
            recommendations.append({
                'priority': 'low',
                'category': 'Impact & Achievements',
                'title': 'Include Financial Impact',
                'description': 'Where applicable, mention budget sizes, cost savings, or revenue impact.',
                'impact': 'Low - Adds business context',
                'examples': [
                    '"Managed $2M annual budget"',
                    '"Generated $500K in additional revenue"',
                    '"Reduced operational costs by $150K annually"'
                ]
            })
        
        return recommendations
    
    def _get_formatting_recommendations(self, text: str) -> List[Dict]:
        """Generate formatting recommendations."""
        recommendations = []
        
        # Check for excessive caps
        words = text.split()
        all_caps_words = [w for w in words if w.isupper() and len(w) > 3]
        if len(all_caps_words) > 10:
            recommendations.append({
                'priority': 'medium',
                'category': 'Formatting',
                'title': 'Avoid Excessive Capitalization',
                'description': 'Too many words in ALL CAPS can reduce readability and may confuse ATS systems. Use title case for headers instead.',
                'impact': 'Low - Improves readability'
            })
        
        return recommendations
    
    def _get_role_specific_recommendations(self, role_analysis: Dict, target_role: str) -> List[Dict]:
        """Generate role-specific recommendations."""
        recommendations = []
        
        # Certification recommendations
        if role_analysis['certifications']['suggested']:
            cert_list = role_analysis['certifications']['suggested'][:3]
            recommendations.append({
                'priority': 'low',
                'category': 'Professional Development',
                'title': f'Consider Relevant Certifications for {role_analysis["role_name"]}',
                'description': 'These certifications are valued in your target role and can strengthen your resume.',
                'impact': 'Low - Enhances credibility',
                'certifications': cert_list
            })
        
        # Overall match recommendation
        if role_analysis['overall_match'] < 60:
            recommendations.append({
                'priority': 'high',
                'category': 'Role Alignment',
                'title': 'Improve Role Alignment',
                'description': f'Your resume has a {role_analysis["overall_match"]}% match with {role_analysis["role_name"]} positions. Focus on adding relevant keywords and highlighting transferable skills.',
                'impact': 'High - Critical for role targeting'
            })
        
        return recommendations


def generate_quick_tips(score_breakdown: Dict, target_role: Optional[str] = None) -> List[str]:
    """
    Generate quick, actionable tips based on scores.
    
    Args:
        score_breakdown: Score breakdown dictionary
        target_role: Target role key
        
    Returns:
        List of quick tip strings
    """
    tips = []
    
    if score_breakdown['ats_compatibility'] < 75:
        tips.append("🎯 Use standard section headers like 'Work Experience' and 'Education' for better ATS compatibility")
    
    if score_breakdown['keyword_optimization'] < 70:
        tips.append("🔑 Review the job description and include relevant keywords throughout your resume")
    
    if score_breakdown['achievements'] < 70:
        tips.append("📊 Add numbers and metrics to quantify your achievements (e.g., '30% increase', '$2M budget')")
    
    if score_breakdown['content_quality'] < 70:
        tips.append("✨ Start bullet points with strong action verbs like 'Developed', 'Led', 'Optimized'")
    
    if score_breakdown['structure'] < 70:
        tips.append("📋 Ensure you have all essential sections: Contact Info, Summary, Experience, Education, Skills")
    
    if target_role:
        tips.append(f"🎓 Consider obtaining certifications relevant to {ROLE_KEYWORDS.get(target_role, {}).get('name', target_role)} roles")
    
    return tips[:6]  # Return top 6 tips