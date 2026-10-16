import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load your model using the exact pkl file name
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "Linear Regression Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Extract features based on your model's feature names:
        # ['age', 'sex', 'bmi', 'children', 'smoker', 'region']
        features = [
            data['age'],
            data['sex'],
            data['bmi'],
            data['children'],
            data['smoker'],
            data['region']
        ]
        
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
