from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from PIL import Image
import io

app = Flask(__name__)

def predict_suitability(image, latitude, longitude):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    edges = cv2.Canny(image, 100, 200)
    
    rooftop_area = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
    
    suitability_score = round(min(100, max(0, rooftop_area * 150)), 3)
    recommended_capacity = round(suitability_score * 0.05, 3)
    
    return suitability_score, recommended_capacity

@app.route('/predict', methods=['POST'])
def predict():
    try:
        latitude = float(request.form.get('latitude'))
        longitude = float(request.form.get('longitude'))
        file = request.files['image']
        
        image = Image.open(io.BytesIO(file.read()))
        
        suitability_score, recommended_capacity = predict_suitability(image, latitude, longitude)
        
        return jsonify({
            "latitude": latitude,
            "longitude": longitude,
            "suitability_score": suitability_score,
            "recommended_capacity_kW": recommended_capacity
        })
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)