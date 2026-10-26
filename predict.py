import pickle
import pandas as pd
from flask import Flask, request, jsonify

# 1. Load the model
model_file = 'model_paris_traffic.bin'

with open(model_file, 'rb') as f_in:
    model = pickle.load(f_in)

app = Flask('traffic-prediction')

@app.route('/predict', methods=['POST'])
def predict():
    road_data = request.get_json()
    
    # Convert incoming dictionary into a DataFrame
    df = pd.DataFrame([road_data])
    
    # Ensure columns match the exact names and order the model was trained on
    if hasattr(model, 'feature_names_in_'):
        df = df.reindex(columns=model.feature_names_in_, fill_value=0)
    
    # Make prediction
    pred = model.predict(df)[0]
    
    result = {
        'predicted_AADT': float(pred)
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)