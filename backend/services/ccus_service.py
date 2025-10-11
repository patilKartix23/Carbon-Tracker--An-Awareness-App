"""
CCUS Service Layer
Handles business logic for Carbon Capture, Utilization and Storage features
"""

from typing import Dict, List, Tuple, Optional
import numpy as np
from datetime import datetime, timedelta
import json
import math

class CCUSPolicyService:
    """Service for CCUS policy integration and government mission alignment"""
    
    def __init__(self):
        self.india_net_zero_target = 2070
        self.current_year = datetime.now().year
        self.years_to_net_zero = self.india_net_zero_target - self.current_year
        
        # India's CCUS mission targets (hypothetical based on government plans)
        self.india_ccus_targets = {
            2025: {'capture_mt': 50, 'storage_mt': 40, 'utilization_mt': 10},
            2030: {'capture_mt': 200, 'storage_mt': 150, 'utilization_mt': 50},
            2035: {'capture_mt': 500, 'storage_mt': 350, 'utilization_mt': 150},
            2040: {'capture_mt': 1000, 'storage_mt': 700, 'utilization_mt': 300},
            2050: {'capture_mt': 2000, 'storage_mt': 1400, 'utilization_mt': 600},
            2070: {'capture_mt': 5000, 'storage_mt': 3500, 'utilization_mt': 1500}
        }

    def assess_policy_alignment(self, annual_capture_potential: float, project_start_year: int = None) -> Dict:
        """Assess how project aligns with India's CCUS mission"""
        if not project_start_year:
            project_start_year = self.current_year + 2  # Assume 2 years for project development
        
        # Find relevant target year
        target_years = [year for year in self.india_ccus_targets.keys() if year >= project_start_year]
        if not target_years:
            target_year = 2070
        else:
            target_year = min(target_years)
        
        target_data = self.india_ccus_targets[target_year]
        project_contribution = (annual_capture_potential / 1000000) / target_data['capture_mt'] * 100  # Convert to MT and percentage
        
        policy_incentives = self._assess_policy_incentives(annual_capture_potential, project_start_year)
        
        return {
            'alignment_assessment': {
                'target_year': target_year,
                'india_target_capture_mt': target_data['capture_mt'],
                'project_annual_capture_mt': round(annual_capture_potential / 1000000, 3),
                'contribution_percentage': round(project_contribution, 4),
                'alignment_score': min(100, project_contribution * 10),  # Scale for scoring
                'years_to_net_zero': self.years_to_net_zero
            },
            'policy_incentives': policy_incentives,
            'recommendations': self._generate_policy_recommendations(project_contribution, target_year)
        }

    def _assess_policy_incentives(self, annual_capture: float, start_year: int) -> Dict:
        """Assess available policy incentives"""
        incentives = {
            'carbon_credit_eligibility': annual_capture > 1000,  # > 1000 tonnes
            'government_subsidy_eligible': annual_capture > 5000,  # > 5000 tonnes
            'priority_sector_status': annual_capture > 10000,  # > 10,000 tonnes
            'estimated_incentive_value_inr': 0
        }
        
        # Calculate estimated incentive value
        if incentives['carbon_credit_eligibility']:
            incentives['estimated_incentive_value_inr'] += annual_capture * 1800  # ₹1800 per tonne
        
        if incentives['government_subsidy_eligible']:
            incentives['estimated_incentive_value_inr'] += annual_capture * 500  # Additional ₹500 per tonne subsidy
        
        if incentives['priority_sector_status']:
            incentives['estimated_incentive_value_inr'] += annual_capture * 300  # Additional ₹300 per tonne priority incentive
        
        return incentives

    def _generate_policy_recommendations(self, contribution_percentage: float, target_year: int) -> List[str]:
        """Generate policy-related recommendations"""
        recommendations = []
        
        if contribution_percentage > 0.01:  # Significant contribution
            recommendations.append(f"Your project significantly contributes to India's {target_year} CCUS targets")
            recommendations.append("Apply for government CCUS mission funding and support")
        
        if contribution_percentage > 0.1:
            recommendations.append("Consider scaling up - your project has high national impact potential")
            recommendations.append("Explore partnerships with NITI Aayog and Ministry of Environment")
        
        recommendations.append("Register with National Carbon Registry for credit certification")
        recommendations.append("Align project timeline with national CCUS mission milestones")
        
        return recommendations

class CCUSGamificationService:
    """Service for gamification features in CCUS application"""
    
    def __init__(self):
        self.achievement_levels = {
            'carbon_capturer': [100, 500, 1000, 5000, 10000],  # tonnes CO2
            'storage_specialist': [50, 250, 500, 2500, 5000],
            'utilization_innovator': [25, 100, 250, 1000, 2500],
            'policy_advocate': [1, 5, 10, 25, 50]  # number of policy submissions
        }
        
        self.leaderboard_categories = [
            'individual_lifestyle_offset',
            'school_college_initiative',
            'industry_implementation',
            'city_municipal_project',
            'state_level_impact'
        ]

    def calculate_user_score(self, user_activities: Dict) -> Dict:
        """Calculate comprehensive user score based on CCUS activities"""
        scores = {
            'carbon_offset_score': 0,
            'awareness_score': 0,
            'action_score': 0,
            'total_score': 0
        }
        
        # Carbon offset score (based on CO2 captured/offset)
        co2_offset = user_activities.get('total_co2_offset_tonnes', 0)
        scores['carbon_offset_score'] = min(1000, co2_offset * 10)  # Max 1000 points
        
        # Awareness score (based on content viewed, shared)
        content_interactions = user_activities.get('content_interactions', 0)
        scores['awareness_score'] = min(500, content_interactions * 5)
        
        # Action score (based on actual implementations, suggestions submitted)
        actions_taken = user_activities.get('actions_taken', 0)
        scores['action_score'] = min(500, actions_taken * 25)
        
        scores['total_score'] = sum(scores.values())
        
        # Determine level and achievements
        level_info = self._calculate_user_level(scores['total_score'])
        achievements = self._check_achievements(user_activities)
        
        return {
            'scores': scores,
            'level_info': level_info,
            'achievements': achievements,
            'next_milestone': self._get_next_milestone(scores['total_score'])
        }

    def _calculate_user_level(self, total_score: int) -> Dict:
        """Calculate user level based on total score"""
        level_thresholds = [0, 100, 300, 600, 1000, 1500, 2000]
        level_names = ['Beginner', 'Aware', 'Active', 'Advocate', 'Champion', 'Expert', 'Master']
        
        for i, threshold in enumerate(level_thresholds):
            if total_score < threshold:
                return {
                    'level': max(1, i),
                    'level_name': level_names[max(0, i-1)],
                    'current_score': total_score,
                    'level_threshold': threshold,
                    'progress_to_next': total_score / threshold if threshold > 0 else 1.0
                }
        
        return {
            'level': len(level_names),
            'level_name': level_names[-1],
            'current_score': total_score,
            'level_threshold': level_thresholds[-1],
            'progress_to_next': 1.0
        }

    def _check_achievements(self, user_activities: Dict) -> List[Dict]:
        """Check user achievements"""
        achievements = []
        
        co2_offset = user_activities.get('total_co2_offset_tonnes', 0)
        for i, threshold in enumerate(self.achievement_levels['carbon_capturer']):
            if co2_offset >= threshold:
                achievements.append({
                    'type': 'carbon_capturer',
                    'level': i + 1,
                    'title': f'Carbon Capturer Level {i + 1}',
                    'description': f'Offset {threshold}+ tonnes of CO2',
                    'earned_date': datetime.now().isoformat()
                })
        
        return achievements

    def _get_next_milestone(self, current_score: int) -> Dict:
        """Get next milestone for user"""
        milestones = [100, 300, 600, 1000, 1500, 2000]
        
        for milestone in milestones:
            if current_score < milestone:
                return {
                    'target_score': milestone,
                    'points_needed': milestone - current_score,
                    'estimated_actions': math.ceil((milestone - current_score) / 25)
                }
        
        return {
            'target_score': 2000,
            'points_needed': 0,
            'estimated_actions': 0,
            'message': 'Congratulations! You have reached the highest level!'
        }

class CCUSEducationalService:
    """Service for educational content and awareness features"""
    
    def __init__(self):
        self.educational_modules = {
            'ccus_basics': {
                'title': 'CCUS Fundamentals',
                'content': self._get_ccus_basics_content(),
                'difficulty': 'beginner',
                'duration_minutes': 15
            },
            'capture_technologies': {
                'title': 'CO2 Capture Technologies',
                'content': self._get_capture_tech_content(),
                'difficulty': 'intermediate',
                'duration_minutes': 25
            },
            'storage_geology': {
                'title': 'Geological Storage Principles',
                'content': self._get_storage_content(),
                'difficulty': 'intermediate',
                'duration_minutes': 20
            },
            'utilization_pathways': {
                'title': 'CO2 Utilization Pathways',
                'content': self._get_utilization_content(),
                'difficulty': 'intermediate',
                'duration_minutes': 30
            },
            'india_ccus_mission': {
                'title': 'India\'s CCUS Mission & Policy',
                'content': self._get_india_mission_content(),
                'difficulty': 'advanced',
                'duration_minutes': 20
            }
        }

    def get_educational_content(self, module_id: str, user_level: str = 'beginner') -> Dict:
        """Get educational content based on module and user level"""
        if module_id not in self.educational_modules:
            return {'error': f'Module {module_id} not found'}
        
        module = self.educational_modules[module_id]
        
        # Filter content based on user level
        filtered_content = self._filter_content_by_level(module['content'], user_level)
        
        return {
            'module_info': {
                'id': module_id,
                'title': module['title'],
                'difficulty': module['difficulty'],
                'duration_minutes': module['duration_minutes'],
                'suitable_for_level': user_level
            },
            'content': filtered_content,
            'quiz_questions': self._generate_quiz_questions(module_id),
            'related_modules': self._get_related_modules(module_id)
        }

    def _get_ccus_basics_content(self) -> List[Dict]:
        """Basic CCUS educational content"""
        return [
            {
                'type': 'introduction',
                'title': 'What is CCUS?',
                'content': 'Carbon Capture, Utilization and Storage (CCUS) is a technology that captures CO2 from industrial sources, either uses it for valuable products or stores it safely underground.',
                'level': 'beginner'
            },
            {
                'type': 'process_flow',
                'title': 'CCUS Process Steps',
                'content': '1. CAPTURE: Extract CO2 from industrial emissions\n2. TRANSPORT: Move CO2 via pipelines or trucks\n3. UTILIZE or STORE: Convert to products or store underground',
                'level': 'beginner'
            },
            {
                'type': 'benefits',
                'title': 'Why CCUS Matters for India',
                'content': 'India aims for Net Zero by 2070. CCUS can help reduce emissions from hard-to-abate sectors like cement, steel, and chemicals while creating economic opportunities.',
                'level': 'beginner'
            },
            {
                'type': 'examples',
                'title': 'Real-world Applications',
                'content': 'Cement plants capturing CO2 to make building blocks, steel mills storing CO2 in underground formations, chemical plants using CO2 to make fuels.',
                'level': 'intermediate'
            }
        ]

    def _get_capture_tech_content(self) -> List[Dict]:
        """Capture technology educational content"""
        return [
            {
                'type': 'technology_overview',
                'title': 'CO2 Capture Methods',
                'content': 'Three main approaches: Post-combustion (after burning), Pre-combustion (before burning), and Oxy-fuel combustion (burning with pure oxygen).',
                'level': 'intermediate'
            },
            {
                'type': 'efficiency_comparison',
                'title': 'Capture Efficiency by Industry',
                'content': 'Cement: 90%, Steel: 85%, Power plants: 85-90%, Chemical plants: 87%. Higher efficiency means more CO2 captured per unit of energy.',
                'level': 'intermediate'
            }
        ]

    def _get_storage_content(self) -> List[Dict]:
        """Storage educational content"""
        return [
            {
                'type': 'storage_types',
                'title': 'Types of CO2 Storage',
                'content': 'Saline aquifers (underground saltwater), Depleted oil/gas wells (used up reservoirs), Coal seams (unmineable coal layers).',
                'level': 'intermediate'
            },
            {
                'type': 'india_potential',
                'title': 'India\'s Storage Potential',
                'content': 'Gujarat: 11,850 MT capacity, Rajasthan: 8,000 MT, Jharkhand: 5,500 MT. Total estimated capacity exceeds 50,000 MT across India.',
                'level': 'intermediate'
            }
        ]

    def _get_utilization_content(self) -> List[Dict]:
        """Utilization educational content"""
        return [
            {
                'type': 'utilization_pathways',
                'title': 'Ways to Use Captured CO2',
                'content': 'Enhanced Oil Recovery, Building materials, Synthetic fuels, Chemicals/plastics, Carbon fiber, Algae cultivation for biofuels.',
                'level': 'intermediate'
            }
        ]

    def _get_india_mission_content(self) -> List[Dict]:
        """India CCUS mission content"""
        return [
            {
                'type': 'mission_overview',
                'title': 'India\'s CCUS Mission',
                'content': 'Government planning comprehensive CCUS roadmap aligned with Net Zero 2070 target. Focus on industrial clusters and policy incentives.',
                'level': 'advanced'
            }
        ]

    def _filter_content_by_level(self, content: List[Dict], user_level: str) -> List[Dict]:
        """Filter content based on user level"""
        level_hierarchy = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        user_level_num = level_hierarchy.get(user_level, 1)
        
        return [item for item in content if level_hierarchy.get(item['level'], 1) <= user_level_num]

    def _generate_quiz_questions(self, module_id: str) -> List[Dict]:
        """Generate quiz questions for a module"""
        quiz_bank = {
            'ccus_basics': [
                {
                    'question': 'What does CCUS stand for?',
                    'options': ['Carbon Control Universal System', 'Carbon Capture, Utilization and Storage', 'Climate Carbon Utility Service'],
                    'correct_answer': 1,
                    'explanation': 'CCUS stands for Carbon Capture, Utilization and Storage'
                }
            ],
            'capture_technologies': [
                {
                    'question': 'Which industry typically has the highest CO2 capture efficiency?',
                    'options': ['Steel industry (85%)', 'Cement industry (90%)', 'Chemical plants (87%)'],
                    'correct_answer': 1,
                    'explanation': 'Cement industry can achieve up to 90% capture efficiency'
                }
            ]
        }
        
        return quiz_bank.get(module_id, [])

    def _get_related_modules(self, module_id: str) -> List[str]:
        """Get related educational modules"""
        relationships = {
            'ccus_basics': ['capture_technologies', 'storage_geology'],
            'capture_technologies': ['ccus_basics', 'utilization_pathways'],
            'storage_geology': ['ccus_basics', 'india_ccus_mission'],
            'utilization_pathways': ['capture_technologies', 'india_ccus_mission'],
            'india_ccus_mission': ['storage_geology', 'utilization_pathways']
        }
        
        return relationships.get(module_id, [])

class CCUSRecommendationService:
    """Service for generating personalized CCUS recommendations"""
    
    def __init__(self):
        self.user_categories = {
            'individual': 'Individual citizen/student',
            'educational_institution': 'School/College/University',
            'small_business': 'Small business/startup',
            'industry': 'Industrial facility',
            'government': 'Government agency/NGO',
            'researcher': 'Research institution'
        }

    def generate_personalized_recommendations(self, user_profile: Dict, location_data: Dict) -> Dict:
        """Generate personalized CCUS recommendations based on user profile and location"""
        user_category = user_profile.get('category', 'individual')
        annual_emissions = user_profile.get('annual_emissions_tonnes', 0)
        location_state = location_data.get('state')
        interests = user_profile.get('interests', [])
        
        recommendations = {
            'immediate_actions': [],
            'medium_term_goals': [],
            'long_term_vision': [],
            'educational_content': [],
            'local_opportunities': []
        }
        
        # Category-specific recommendations
        if user_category == 'individual':
            recommendations = self._get_individual_recommendations(annual_emissions, location_state)
        elif user_category == 'educational_institution':
            recommendations = self._get_educational_recommendations(location_state)
        elif user_category == 'industry':
            recommendations = self._get_industry_recommendations(annual_emissions, location_state)
        elif user_category == 'government':
            recommendations = self._get_government_recommendations(location_state)
        
        # Add interest-based content
        if 'technology' in interests:
            recommendations['educational_content'].extend(['capture_technologies', 'utilization_pathways'])
        if 'policy' in interests:
            recommendations['educational_content'].append('india_ccus_mission')
        
        return {
            'user_category': user_category,
            'personalized_recommendations': recommendations,
            'priority_score': self._calculate_priority_score(user_profile),
            'next_steps': self._generate_next_steps(recommendations)
        }

    def _get_individual_recommendations(self, emissions: float, state: str) -> Dict:
        """Recommendations for individual users"""
        return {
            'immediate_actions': [
                'Calculate your personal carbon footprint',
                'Learn about CCUS basics through our educational modules',
                'Share CCUS awareness with friends and family',
                'Support businesses implementing CCUS technologies'
            ],
            'medium_term_goals': [
                'Advocate for CCUS projects in your community',
                'Choose products made with captured CO2',
                'Participate in local environmental initiatives'
            ],
            'long_term_vision': [
                'Pursue career opportunities in clean technology',
                'Become a CCUS advocate in your community',
                'Support policy changes for CCUS deployment'
            ]
        }

    def _get_educational_recommendations(self, state: str) -> Dict:
        """Recommendations for educational institutions"""
        return {
            'immediate_actions': [
                'Integrate CCUS curriculum in science/engineering programs',
                'Organize CCUS awareness workshops',
                'Set up student research projects on carbon capture',
                'Partner with local industries for CCUS field trips'
            ],
            'medium_term_goals': [
                'Establish CCUS research lab or center',
                'Develop industry partnerships for student internships',
                'Create campus-wide carbon offset programs'
            ],
            'long_term_vision': [
                'Become a regional CCUS research hub',
                'Graduate CCUS specialists for industry',
                'Lead community CCUS initiatives'
            ]
        }

    def _get_industry_recommendations(self, emissions: float, state: str) -> Dict:
        """Recommendations for industrial users"""
        return {
            'immediate_actions': [
                'Conduct detailed emissions assessment',
                'Evaluate CCUS feasibility for your industry',
                'Explore government incentives and funding',
                'Connect with CCUS technology providers'
            ],
            'medium_term_goals': [
                'Implement pilot CCUS project',
                'Develop carbon credit revenue streams',
                'Establish partnerships with storage providers'
            ],
            'long_term_vision': [
                'Achieve significant emission reductions',
                'Become industry leader in CCUS implementation',
                'Contribute to India\'s Net Zero goals'
            ]
        }

    def _get_government_recommendations(self, state: str) -> Dict:
        """Recommendations for government users"""
        return {
            'immediate_actions': [
                'Assess regional CCUS potential and infrastructure needs',
                'Develop state-level CCUS policies and incentives',
                'Facilitate stakeholder consultations',
                'Create public awareness campaigns'
            ],
            'medium_term_goals': [
                'Establish CCUS industrial clusters',
                'Develop regulatory framework',
                'Create funding mechanisms for CCUS projects'
            ],
            'long_term_vision': [
                'Position state as CCUS leader in India',
                'Achieve state emission reduction targets',
                'Attract CCUS investments and industries'
            ]
        }

    def _calculate_priority_score(self, user_profile: Dict) -> int:
        """Calculate priority score for recommendations"""
        score = 0
        
        # Higher emissions = higher priority
        emissions = user_profile.get('annual_emissions_tonnes', 0)
        score += min(50, emissions / 1000)  # Max 50 points
        
        # Industry/government get higher priority
        category = user_profile.get('category', 'individual')
        if category in ['industry', 'government']:
            score += 30
        elif category == 'educational_institution':
            score += 20
        else:
            score += 10
        
        # Engagement level
        engagement = user_profile.get('engagement_level', 'low')
        if engagement == 'high':
            score += 20
        elif engagement == 'medium':
            score += 10
        
        return min(100, score)

    def _generate_next_steps(self, recommendations: Dict) -> List[str]:
        """Generate immediate next steps"""
        next_steps = []
        
        if recommendations['immediate_actions']:
            next_steps.append(f"Start with: {recommendations['immediate_actions'][0]}")
        
        if recommendations['educational_content']:
            next_steps.append("Complete recommended educational modules")
        
        next_steps.append("Set up progress tracking and monitoring")
        next_steps.append("Connect with local CCUS community")
        
        return next_steps[:3]  # Return top 3 next steps
