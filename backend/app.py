from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from disease_analyzer import DiseaseAnalyzer

app = Flask(__name__, 
    static_folder='../frontend/static',
    template_folder='../frontend/templates')
CORS(app)

analyzer = DiseaseAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/diagnose', methods=['POST'])
def analyze():
    symptoms = request.json.get('symptoms', [])
    results = analyzer.diagnose(symptoms)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
