from flask import Flask, render_template_string, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the model without changing the pkl filename
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

# HTML template with a clean form for the 6 features
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Linear Regression Model Deployment</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; padding: 50px; }
        .container { max-width: 500px; background: white; padding: 30px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); margin: auto; }
        h2 { text-align: center; color: #333; }
        label { display: block; margin-top: 15px; font-weight: bold; color: #555; }
        input, select { width: 100%; padding: 8px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; background-color: #007BFF; color: white; padding: 10px; border: none; border-radius: 4px; margin-top: 20px; font-size: 16px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        .result { margin-top: 20px; padding: 15px; background: #e2f0d9; border: 1px solid #c8e6c9; color: #276527; text-align: center; border-radius: 4px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Model Prediction</h2>
        <form method="POST">
            <label>Age:</label>
            <input type="number" name="age" step="any" required>

            <label>Sex (e.g., 0 for female, 1 for male):</label>
            <input type="number" name="sex" required>

            <label>BMI:</label>
            <input type="number" name="bmi" step="any" required>

            <label>Children:</label>
            <input type="number" name="children" required>

            <label>Smoker (e.g., 0 for no, 1 for yes):</label>
            <input type="number" name="smoker" required>

            <label>Region (encoded numerical value):</label>
            <input type="number" name="region" required>

            <button type="submit">Predict</button>
        </form>

        {% if prediction is not none %}
            <div class="result">
                Predicted Output: {{ prediction }}
            </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            # Extract features in the exact order trained by the model
            age = float(request.form['age'])
            sex = float(request.form['sex'])
            bmi = float(request.form['bmi'])
            children = float(request.form['children'])
            smoker = float(request.form['smoker'])
            region = float(request.form['region'])

            # Reshape into a 2D array for the model
            features = np.array([[age, sex, bmi, children, smoker, region]])
            
            # Make prediction
            prediction = round(float(model.predict(features)[0]), 2)
        except Exception as e:
            prediction = f"Error in calculation: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
