class DiseaseUI {
    constructor() {
        this.symptoms = new Set();
        this.symptomCategories = {
            'Fever Patterns': [
                'high_fever', 'biphasic_fever', 'intermittent_fever', 'continuous_fever'
            ],
            'Pain and Discomfort': [
                'severe_headache', 'retro_orbital_pain', 'muscle_joint_pain', 
                'abdominal_pain', 'muscle_aches'
            ],
            'Respiratory Symptoms': [
                'cough', 'shortness_breath', 'sore_throat', 'rapid_breathing'
            ],
            'Sensory Changes': [
                'loss_smell', 'loss_taste'
            ],
            'Skin and Bleeding': [
                'maculopapular_rash', 'petechiae', 'bleeding_gums', 
                'nose_bleeds', 'gi_bleeding'
            ],
            'Gastrointestinal': [
                'persistent_vomiting', 'nausea', 'diarrhea', 'constipation'
            ],
            'General Symptoms': [
                'fatigue', 'chills', 'profuse_sweating', 'weakness', 
                'confusion', 'restlessness'
            ],
            'Clinical Signs': [
                'rose_spots', 'jaundice', 'splenomegaly', 'cyanosis', 
                'relative_bradycardia'
            ]
        };
        
        this.initializeUI();
    }

    initializeUI() {
        const container = document.getElementById('symptom-container');

        Object.entries(this.symptomCategories).forEach(([category, symptoms]) => {
            const section = this.createCategorySection(category, symptoms);
            container.appendChild(section);
        });

        const analyzeButton = this.createAnalyzeButton();
        container.appendChild(analyzeButton);
    }

    createCategorySection(category, symptoms) {
        const section = document.createElement('div');
        section.className = 'symptom-category';

        const heading = document.createElement('h3');
        heading.textContent = category;
        section.appendChild(heading);

        symptoms.forEach(symptom => {
            const item = this.createSymptomItem(symptom);
            section.appendChild(item);
        });

        return section;
    }

    createSymptomItem(symptom) {
        const wrapper = document.createElement('div');
        wrapper.className = 'symptom-item';

        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.id = symptom;
        checkbox.addEventListener('change', () => this.updateSymptoms(symptom));

        const label = document.createElement('label');
        label.htmlFor = symptom;
        label.textContent = this.formatSymptomLabel(symptom);

        wrapper.appendChild(checkbox);
        wrapper.appendChild(label);

        return wrapper;
    }

    createAnalyzeButton() {
        const button = document.createElement('button');
        button.textContent = 'Analyze Symptoms';
        button.className = 'analyze-button';
        button.onclick = () => this.analyzeDisease();
        return button;
    }

    formatSymptomLabel(symptom) {
        return symptom.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    updateSymptoms(symptom) {
        if (this.symptoms.has(symptom)) {
            this.symptoms.delete(symptom);
        } else {
            this.symptoms.add(symptom);
        }
    }

    // Method to analyze disease
    analyzeDisease = async () => {
        if (this.symptoms.size === 0) {
            this.showMessage('Please select at least one symptom');
            return;
        }

        try {
            const response = await fetch('/api/diagnose', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    symptoms: Array.from(this.symptoms)
                })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const results = await response.json();
            this.displayResults(results);
        } catch (error) {
            this.showMessage('Error analyzing symptoms. Please try again.');
            console.error('Analysis error:', error);
        }
    }

    // Method to display results
    displayResults(results) {
        const resultsDiv = document.getElementById('results');
        resultsDiv.innerHTML = '';
    
        const heading = document.createElement('h3');
        heading.textContent = 'Diagnosis Results';
        resultsDiv.appendChild(heading);
    
        // Handle the nested results structure
        const diagnosisResults = results.results || results;
    
        // Separate single diseases and co-infections
        const singleDiseases = [];
        const coInfections = [];
    
        diagnosisResults.forEach(([disease, confidence]) => {
            if (disease.includes('_')) {
                coInfections.push([disease, confidence]);
            } else {
                singleDiseases.push([disease, confidence]);
            }
        });
    
        // Display single diseases
        if (singleDiseases.length > 0) {
            const singleSection = document.createElement('div');
            singleSection.className = 'single-diseases';
            singleSection.innerHTML = '<h4>Primary Disease Possibilities:</h4>';
            
            singleDiseases.forEach(([disease, confidence]) => {
                const resultItem = document.createElement('div');
                resultItem.className = `result-item ${confidence > 60 ? 'high-confidence' : ''}`;
                resultItem.innerHTML = `
                    <strong>${disease.replace('_', ' ')}</strong>: 
                    <span class="confidence">${confidence.toFixed(2)}% confidence</span>
                `;
                singleSection.appendChild(resultItem);
            });
            resultsDiv.appendChild(singleSection);
        }
        function getSeverityLevel(confidence) {
            if (confidence >= 70) return { level: 'Severe', class: 'severe', message: 'Immediate medical attention recommended' };
            if (confidence >= 50) return { level: 'Moderate', class: 'moderate', message: 'Medical consultation advised' };
            return { level: 'Mild', class: 'mild', message: 'Monitor symptoms carefully' };
        }
    
        // Display co-infections if they have significant confidence
        const significantCoInfections = coInfections.filter(([_, confidence]) => confidence > 40);
        
        if (significantCoInfections.length > 0) {
            const coSection = document.createElement('div');
            coSection.className = 'co-infections';
            coSection.innerHTML = '<h4>Possible Co-Infections:</h4>';
            
            significantCoInfections.forEach(([disease, confidence]) => {
                const diseases = disease.split('_');
                const severity = getSeverityLevel(confidence);
                
                const resultItem = document.createElement('div');
                resultItem.className = `result-item co-infection ${severity.class}`;
                resultItem.innerHTML = `
                    <strong>${diseases.join(' + ')}</strong>: 
                    <span class="confidence">${confidence.toFixed(2)}% confidence</span>
                    <div class="severity-indicator">
                        <span class="severity-level">${severity.level}</span>
                        <p class="severity-message">${severity.message}</p>
                    </div>
                `;
                coSection.appendChild(resultItem);
            });
            resultsDiv.appendChild(coSection);
        }
    }

}

document.addEventListener('DOMContentLoaded', () => {
    new DiseaseUI();
});
