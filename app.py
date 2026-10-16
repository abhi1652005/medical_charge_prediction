import pickle
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load your model without changing the pkl file name
with open('l_model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return "Linear Regression Model API is running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        
        # Convert text inputs to the numeric format your model expects during training
        # Note: Adjust these mappings if you used a different encoding scheme (like One-Hot Encoding)
        
        # 1. Age & BMI & Children (already numeric, convert to float/int)
        age = float(data['age'])
        bmi = float(data['bmi'])
        children = int(data['children'])
        
        # 2. Sex: female -> 0, male -> 1 (change if your training used opposite)
        sex_text = str(data['sex']).strip().lower()
        sex = 1 if sex_text == 'male' else 0
        
        # 3. Smoker: no -> 0, yes -> 1
        smoker_text = str(data['smoker']).strip().lower()
        smoker = 1 if smoker_text in ['yes', 'true', '1'] else 0
        
        # 4. Region mapping (standard label encoding order)
        region_map = {
            'northeast': 0,
            'northwest': 1,
            'southeast': 2,
            'southwest': 3
        }
        region_text = str(data['region']).strip().lower()
        region = region_map.get(region_text, 2) # Default to 2 (southeast) if unknown
        
        # Assemble features in the exact order the model expects
        features = [age, sex, bmi, children, smoker, region]
        
        # Make prediction
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
