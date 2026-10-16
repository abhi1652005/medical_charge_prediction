import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load model without changing the pkl file name[cite: 1]
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Modern UI Design Template contained directly within app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Insurance Cost Estimator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #4F46E5;
            --primary-hover: #4338CA;
            --bg: #F3F4F6;
            --card-bg: #FFFFFF;
            --text-main: #1F2937;
            --text-muted: #6B7280;
            --border: #E5E7EB;
            --accent-green: #059669;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', sans-serif;
        }

        body {
            background-color: var(--bg);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .card {
            background: var(--card-bg);
            width: 100%;
            max-width: 480px;
            padding: 32px;
            border-radius: 16px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01);
        }

        .header {
            text-align: center;
            margin-bottom: 28px;
        }

        .header h1 {
            font-size: 24px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
        }

        .header p {
            font-size: 14px;
            color: var(--text-muted);
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }

        .full-width {
            grid-column: span 2;
        }

        .form-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-main);
            margin-bottom: 6px;
        }

        input, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid var(--border);
            border-radius: 8px;
            font-size: 14px;
            color: var(--text-main);
            background-color: #FAFAFA;
            outline: none;
            transition: all 0.2s ease;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            background-color: #FFFFFF;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.15);
        }

        button {
            width: 100%;
            padding: 12px;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: background-color 0.2s ease, transform 0.1s ease;
            margin-top: 20px;
        }

        button:hover {
            background-color: var(--primary-hover);
        }

        button:active {
            transform: scale(0.98);
        }

        .result-box {
            margin-top: 24px;
            padding: 16px;
            border-radius: 12px;
            background-color: #ECFDF5;
            border: 1px solid #A7F3D0;
            text-align: center;
            display: none;
        }

        .result-box.active {
            display: block;
            animation: fadeIn 0.3s ease;
        }

        .result-title {
            font-size: 13px;
            font-weight: 500;
            color: #065F46;
            margin-bottom: 4px;
        }

        .result-price {
            font-size: 28px;
            font-weight: 700;
            color: var(--accent-green);
        }

        .error-box {
            margin-top: 24px;
            padding: 12px;
            border-radius: 8px;
            background-color: #FEF2F2;
            border: 1px solid #FCA5A5;
            color: #991B1B;
            font-size: 13px;
            text-align: center;
            display: none;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 480px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .full-width {
                grid-column: span 1;
            }
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="header">
            <h1>Medical Charge Predictor</h1>
            <p>Enter individual details to estimate medical expenses</p>
        </div>

        <form id="prediction-form">
            <div class="form-grid">
                <div class="form-group">
                    <label for="age">Age</label>
                    <input type="number" id="age" required value="30" placeholder="e.g. 30">
                </div>

                <div class="form-group">
                    <label for="sex">Gender</label>
                    <select id="sex">
                        <option value="male">Male</option>
                        <option value="female">Female</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="bmi">BMI</label>
                    <input type="number" step="0.1" id="bmi" required value="25.5" placeholder="e.g. 25.5">
                </div>

                <div class="form-group">
                    <label for="children">Children</label>
                    <input type="number" id="children" required value="1" placeholder="e.g. 0">
                </div>

                <div class="form-group full-width">
                    <label for="smoker">Smoker Status</label>
                    <select id="smoker">
                        <option value="no">Non-Smoker</option>
                        <option value="yes">Smoker</option>
                    </select>
                </div>

                <div class="form-group full-width">
                    <label for="region">Region</label>
                    <select id="region">
                        <option value="southeast">Southeast</option>
                        <option value="southwest">Southwest</option>
                        <option value="northeast">Northeast</option>
                        <option value="northwest">Northwest</option>
                    </select>
                </div>
            </div>

            <button type="button" id="btn" onclick="predictPrice()">Calculate Charge</button>
        </form>

        <div class="result-box" id="result-box">
            <div class="result-title">Estimated Annual Medical Expense</div>
            <div class="result-price" id="prediction-text">$0.00</div>
        </div>

        <div class="error-box" id="error-box"></div>
    </div>

    <script>
        async function predictPrice() {
            const btn = document.getElementById('btn');
            const resultBox = document.getElementById('result-box');
            const errorBox = document.getElementById('error-box');

            resultBox.classList.remove('active');
            errorBox.style.display = 'none';
            btn.innerText = 'Calculating...';

            const data = {
                age: document.getElementById('age').value,
                sex: document.getElementById('sex').value,
                bmi: document.getElementById('bmi').value,
                children: document.getElementById('children').value,
                smoker: document.getElementById('smoker').value,
                region: document.getElementById('region').value
            };

            try {
                const response = await fetch('/predict', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                btn.innerText = 'Calculate Charge';

                if (result.success) {
                    const formattedPrice = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD'
                    }).format(result.prediction);

                    document.getElementById('prediction-text').innerText = formattedPrice;
                    resultBox.classList.add('active');
                } else {
                    errorBox.innerText = 'Error: ' + result.error;
                    errorBox.style.display = 'block';
                }
            } catch (err) {
                btn.innerText = 'Calculate Charge';
                errorBox.innerText = 'Failed to connect to the server.';
                errorBox.style.display = 'block';
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
            'prediction': float(prediction[0])
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
