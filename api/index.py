from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add parent directory to path to find the disease_analyzer module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.disease_analyzer import DiseaseAnalyzer

app = Flask(__name__)
CORS(app)

analyzer = DiseaseAnalyzer()

@app.route('/', methods=['GET'])
def home():
    return "Disease Diagnosis API is running!"

@app.route('/api/diagnose', methods=['POST'])
def analyze():
    try:
        symptoms = request.json.get('symptoms', [])
        results = analyzer.diagnose(symptoms)
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Required for Vercel
app.debug = True
