from flask import Flask, render_template, request, redirect, url_for, session
import pickle
from pdf_parser import extract_text_from_pdf, parse_cancer_report
import traceback

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required to use session

model = pickle.load(open('model.pkl', 'rb'))

prediction_mapping = {
    "Low": "There is 55% chance the patient can survive for 5 years(Stage 1 cancer)",
    "Medium": "There is 25% chance the patient can survive for 5 years(Stage 2 cancer)",
    "High": "There is 5% chance the patient can survive for 5 years(Stage 4 cancer)"
}

expected_order = [
    'Age', 'Gender', 'Air', 'Alcohol', 'Dust', 'Occupational', 'Genetic',
    'Chronic', 'Balanced', 'Obesity', 'Smoking', 'Passive', 'Chest',
    'Coughing', 'Fatigue', 'Weight', 'Shortness', 'Wheezing', 'Swallowing',
    'Clubbing', 'Frequent', 'Dry', 'Snoring', 'Record', 'Patient'
]

key_mapping = {
    'Age': 'Age',
    'Gender': 'Gender',
    'Air': 'Air',
    'Alcohol': 'Alcohol',
    'Dust': 'Dust',
    'Occupational': 'Occupational',
    'Genetic': 'Genetic',
    'Chronic': 'Chronic',
    'Balanced': 'Balanced',
    'Obesity': 'Obesity',
    'Smoking': 'Smoking',
    'Passive': 'Passive',
    'Chest': 'Chest',
    'Coughing': 'Coughing',
    'Fatigue': 'Fatigue',
    'Weight': 'Weight',
    'Shortness': 'Shortness',
    'Wheezing': 'Wheezing',
    'Swallowing': 'Swallowing',
    'Clubbing': 'Clubbing',
    'Frequent': 'Frequent',
    'Dry': 'Dry',
    'Snoring': 'Snoring',
    'Record': 'Record',
    'Patient': 'Patient'
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        pdf_file = request.files['pdf_file']
        if not pdf_file:
            return render_template('index.html', error="No file uploaded.")

        text = extract_text_from_pdf(pdf_file)
        parsed_data = parse_cancer_report(text)

        mapped_data = {}
        for real_key, model_key in key_mapping.items():
            if real_key in parsed_data:
                mapped_data[model_key] = parsed_data[real_key]

        features = [mapped_data.get(key, 0) for key in expected_order]
        prediction = model.predict([features])[0]
        result = prediction_mapping.get(prediction, "Unknown")

        # Store results in session and redirect
        session['cancer_report'] = mapped_data
        session['prediction'] = result
        return redirect(url_for('result'))

    except Exception as e:
        print("❌ ERROR while processing:")
        traceback.print_exc()
        return render_template('index.html', error=f"Error processing PDF: {e}")

@app.route('/result')
def result():
    cancer_report = session.get('cancer_report', {})
    prediction = session.get('prediction', None)
    if not prediction:
        return redirect(url_for('index'))
    return render_template('result.html', cancer_report=cancer_report, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
