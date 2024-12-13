import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class DiseaseProfile:
    primary_symptoms: List[str]
    secondary_symptoms: List[str]
    severity_weights: Dict[str, float]

class DiseaseAnalyzer:
    def __init__(self):
        self.symptom_map = {
            'high_fever': 'HF',
            'biphasic_fever': 'BF',
            'intermittent_fever': 'IF',
            'continuous_fever': 'CF',
            'severe_headache': 'SH',
            'retro_orbital_pain': 'ROP',
            'muscle_joint_pain': 'MJP',
            'abdominal_pain': 'AP',
            'cough': 'CG',
            'shortness_breath': 'SOB',
            'sore_throat': 'ST',
            'rapid_breathing': 'RB',
            'loss_smell': 'LS',
            'loss_taste': 'LT',
            'maculopapular_rash': 'MPR',
            'petechiae': 'PT',
            'bleeding_gums': 'BG',
            'nose_bleeds': 'NB',
            'gi_bleeding': 'GIB',
            'persistent_vomiting': 'PV',
            'nausea': 'NA',
            'diarrhea': 'DI',
            'constipation': 'CN',
            'fatigue': 'FT',
            'chills': 'CH',
            'profuse_sweating': 'PS',
            'muscle_aches': 'MA',
            'weakness': 'WK',
            'confusion': 'CF',
            'restlessness': 'RT',
            'rose_spots': 'RS',
            'jaundice': 'JD',
            'splenomegaly': 'SP',
            'cyanosis': 'CY',
            'relative_bradycardia': 'RB'
        }

        # Enhanced disease profiles with primary and secondary symptoms
        self.disease_profiles = {
            'dengue': DiseaseProfile(
                primary_symptoms=['HF', 'BF', 'ROP', 'MPR', 'PT'],
                secondary_symptoms=['MJP', 'AP', 'BG', 'NB', 'GIB', 'PV', 'RT'],
                severity_weights={'PT': 1.5, 'GIB': 1.8, 'BG': 1.3}
            ),
            'malaria': DiseaseProfile(
                primary_symptoms=['IF', 'CH', 'PS', 'JD'],
                secondary_symptoms=['SH', 'NA', 'PV', 'MA', 'SP', 'CF'],
                severity_weights={'JD': 1.4, 'SP': 1.3}
            ),
            'typhoid': DiseaseProfile(
                primary_symptoms=['CF', 'RS', 'RB'],
                secondary_symptoms=['AP', 'CN', 'DI', 'WK', 'PV'],
                severity_weights={'CF': 1.3, 'RS': 1.2}
            ),
            'covid19': DiseaseProfile(
                primary_symptoms=['CG', 'SOB', 'LS', 'LT'],
                secondary_symptoms=['ST', 'HF', 'CH', 'MA', 'NA', 'DI', 'CY', 'CF'],
                severity_weights={'SOB': 1.6, 'CY': 1.5}
            )
        }

        # Generate co-infection profiles dynamically
        self._generate_coinfection_profiles()

    def _generate_coinfection_profiles(self):
        single_diseases = ['dengue', 'malaria', 'typhoid', 'covid19']
        
        for i in range(len(single_diseases)):
            for j in range(i + 1, len(single_diseases)):
                disease1, disease2 = single_diseases[i], single_diseases[j]
                coinfection_name = f"{disease1}_{disease2}"
                
                # Combine profiles with special handling for overlapping symptoms
                self.disease_profiles[coinfection_name] = self._merge_disease_profiles(
                    self.disease_profiles[disease1],
                    self.disease_profiles[disease2]
                )

    def _merge_disease_profiles(self, profile1: DiseaseProfile, profile2: DiseaseProfile) -> DiseaseProfile:
        # Combine and deduplicate symptoms
        primary_symptoms = list(set(profile1.primary_symptoms + profile2.primary_symptoms))
        secondary_symptoms = list(set(profile1.secondary_symptoms + profile2.secondary_symptoms))
        
        # Merge severity weights, taking the higher value for overlapping symptoms
        severity_weights = {**profile1.severity_weights, **profile2.severity_weights}
        
        return DiseaseProfile(
            primary_symptoms=primary_symptoms,
            secondary_symptoms=secondary_symptoms,
            severity_weights=severity_weights
        )

    def needleman_wunsch(self, seq1: List[str], seq2: List[str]) -> float:
        match_score = 3
        mismatch_score = -1
        gap_penalty = -2

        m, n = len(seq1), len(seq2)
        score_matrix = np.zeros((m + 1, n + 1))

        # Initialize first row and column
        score_matrix[0] = [gap_penalty * j for j in range(n + 1)]
        score_matrix[:, 0] = [gap_penalty * i for i in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                match = score_matrix[i-1][j-1] + (match_score if seq1[i-1] == seq2[j-1] else mismatch_score)
                delete = score_matrix[i-1][j] + gap_penalty
                insert = score_matrix[i][j-1] + gap_penalty
                score_matrix[i][j] = max(match, delete, insert)

        return score_matrix[m][n]

    def calculate_symptom_match_score(self, patient_symptoms: List[str], disease_profile: DiseaseProfile) -> float:
    # Enhanced scoring weights
      primary_weight = 3.0
      secondary_weight = 1.5
      severity_multiplier = 1.2

    # Primary symptoms matching
      primary_matches = set(patient_symptoms) & set(disease_profile.primary_symptoms)
      primary_score = len(primary_matches) * primary_weight
    
    # Secondary symptoms matching
      secondary_matches = set(patient_symptoms) & set(disease_profile.secondary_symptoms)
      secondary_score = len(secondary_matches) * secondary_weight
    
    # Severity consideration
      severity_score = sum(
        disease_profile.severity_weights.get(symptom, 1.0) * severity_multiplier
        for symptom in patient_symptoms
        if symptom in disease_profile.severity_weights
    )

    # Calculate relative match percentage
      total_possible_score = (
        len(disease_profile.primary_symptoms) * primary_weight +
        len(disease_profile.secondary_symptoms) * secondary_weight
    )
    
      actual_score = primary_score + secondary_score + severity_score
    
    # Normalize score to percentage
      confidence = (actual_score / total_possible_score) * 100
    
    # Apply minimum threshold for meaningful scores
      return confidence if confidence > 20 else 20

    def diagnose(self, symptoms: List[str]) -> List[Tuple[str, float]]:
      patient_symptoms = [self.symptom_map.get(s.lower(), '') for s in symptoms if s.lower() in self.symptom_map]
      results = {}

    # First analyze primary diseases
      for disease, profile in self.disease_profiles.items():
        if '_' not in disease:  # Primary diseases
            base_confidence = self.calculate_symptom_match_score(patient_symptoms, profile)
            results[disease] = max(20, min(100, base_confidence))

    # Then analyze potential co-infections
      for disease, profile in self.disease_profiles.items():
        if '_' in disease:  # Co-infections
            diseases = disease.split('_')
            individual_scores = [results.get(d, 0) for d in diseases]
            if individual_scores:
                # Calculate co-infection confidence based on individual scores
                combined_confidence = (sum(individual_scores) * 0.8) / len(individual_scores)
                # Only include if there's significant confidence
                if combined_confidence > 40:
                    results[disease] = combined_confidence

      return sorted(results.items(), key=lambda x: x[1], reverse=True)


