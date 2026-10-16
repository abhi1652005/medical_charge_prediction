import pickle
import numpy as np
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Load model without changing the pkl file name[cite: 1]
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Attractive Dark-Mode Gradient UI Design Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Medical Insurance Cost Estimator</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-gradient: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #311042 100%);
            --card-bg: rgba(30, 41, 59, 0.7);
            --card-border: rgba(255, 255, 255, 0.1);
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --input-bg: rgba(15, 23, 42, 0.6);
            --input-border: rgba(255, 255, 255, 0.12);
            --accent-green: #10b981;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }

        body {
            background: var(--bg-gradient);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--card-border);
            width: 100%;
            max-width: 500px;
            padding: 36px;
            border-radius: 24px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        }

        .header {
            text-align: center;
            margin-bottom: 32px;
        }

        .header h1 {
            font-size: 26px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 8px;
            letter-spacing: -0.5px;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            font-size: 14px;
            color: var(--text-muted);
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
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
            font-weight: 500;
            color: var(--text-muted);
            margin-bottom: 8px;
        }

        input, select {
            width: 100%;
            padding: 12px 14px;
            border: 1px solid var(--input-border);
            border-radius: 12px;
            font-size: 14px;
            color: var(--text-main);
            background-color: var(--input-bg);
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            border-color: var(--primary);
            box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.2);
            background-color: rgba(15, 23, 42, 0.8);
        }

        select option {
            background-color: #1e293b;
            color: var(--text-main);
        }

        button {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 24px;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.6);
        }

        button:active {
            transform: translateY(0);
        }

        .result-box {
            margin-top: 24px;
            padding: 20px;
            border-radius: 16px;
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            text-align: center;
            display: none;
        }

        .result-box.active {
            display: block;
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .result-title {
            font-size: 13px;
            font-weight: 500;
            color: #34d399;
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .result-price {
            font-size: 32px;
            font-weight: 700;
            color: #6ee7b7;
        }

        .error-box {
            margin-top: 24px;
            padding: 14px;
            border-radius: 12px;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            font-size: 13px;
            text-align: center;
            display: none;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 480px) {
            .form-grid {
                grid-template-columns: 1fr;
            }
            .full-width {
                grid-column: span 1;
            }
            .card {
                padding: 24px;
            }
        }
    </style>
</head>
<body>

    <div class="card">
        <div class="header">
            <h1>Medical Expense Predictor</h1>
            <p>Advanced AI model estimation for healthcare costs</p>
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
                    <input type="number" id="children" required value="1" placeholder="e.g. 1">
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
            <div class="result-title">Estimated Annual Expense</div>
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
