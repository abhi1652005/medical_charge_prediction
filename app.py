import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load your model without changing the pkl file name
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML interface for your browser
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Medical Charge Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; background: #f4f4f9; display: flex; justify-content: center; }
        .container { width: 100%; max-width: 400px; background: white; padding: 25px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
        h2 { text-align: center; color: #333; }
        label { font-weight: bold; display: block; margin-top: 10px; }
        input, select { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #007BFF; color: white; border: none; padding: 10px; width: 100%; border-radius: 4px; cursor: pointer; margin-top: 15px; font-size: 16px; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; font-size: 18px; font-weight: bold; text-align: center; color: #28a745; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Medical Charge Predictor</h2>
        <form id="prediction-form">
            <label>Age:</label>
            <input type="number" id="age" required value="25">
            
            <label>Sex:</label>
            <select id="sex">
                <option value="male">Male</option>
                <option value="female">Female</option>
            </select>

            <label>BMI:</label>
            <input type="number" step="0.1" id="bmi" required value="27.9">

            <label>Children:</label>
            <input type="number" id="children" required value="0">

            <label>Smoker:</label>
            <select id="smoker">
                <option value="no">No</option>
                <option value="yes">Yes</option>
            </select>

            <label>Region:</label>
            <select id="region">
                <option value="southeast">Southeast</option>
                <option value="southwest">Southwest</option>
                <option value="northeast">Northeast</option>
                <option value="northwest">Northwest</option>
            </select>

            <button type="button" onclick="predictPrice()">Calculate Charge</button>
        </form>
        <div class="result" id="result"></div>
    </div>

    <script>
        async function predictPrice() {
            const data = {
                age: document.getElementById('age').value,
                sex: document.getElementById('sex').value,
                bmi: document.getElementById('bmi').value,
                children: document.getElementById('children').value,
                smoker: document.getElementById('smoker').value,
                region: document.getElementById('region').value
            };

            const response = await fetch('/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            const result = await response.json();
            if (result.success) {
                document.getElementById('result').innerText = "Predicted Charge: $" + result.prediction.toFixed(2);
            } else {
                document.getElementById('result').innerText = "Error: " + result.error;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        age = float(data['age'])
        bmi = float(data['bmi'])
        children = int(data['children'])
        
        sex = 1 if str(data['sex']).strip().lower() == 'male' else 0
        smoker = 1 if str(data['smoker']).strip().lower() in ['yes', 'true', '1'] else 0
        
        region_map = {
            'northeast': 0,
            'northwest': 1,
            'southeast': 2,
            'southwest': 3
        }
        region = region_map.get(str(data['region']).strip().lower(), 2)
        
        features = [age, sex, bmi, children, smoker, region]
        prediction = model.predict([features])
        
        return jsonify({
            'success': True,
            'prediction': prediction[0]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
