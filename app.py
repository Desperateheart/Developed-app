from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
import os
from datetime import datetime
import random

app = Flask(__name__)
CORS(app)

# Mock disease detection model (in production, you'd use a trained TensorFlow model)
class DiseaseDetector:
    def __init__(self):
        self.diseases = {
            'healthy': 'Plant appears healthy',
            'leaf_blight': 'Leaf blight detected - Remove affected leaves and apply fungicide',
            'powdery_mildew': 'Powdery mildew detected - Apply sulfur-based fungicide',
            'rust': 'Rust disease detected - Remove infected parts and apply copper fungicide',
            'root_rot': 'Root rot detected - Improve drainage and reduce watering',
            'aphids': 'Aphid infestation detected - Apply neem oil or insecticidal soap'
        }
    
    def detect_disease(self, image):
        # Mock detection - in production, this would use a real ML model
        # For now, randomly select a disease for demonstration
        detected_disease = random.choice(list(self.diseases.keys()))
        confidence = random.uniform(0.7, 0.95)
        
        return {
            'disease': detected_disease,
            'confidence': round(confidence, 2),
            'description': self.diseases[detected_disease],
            'treatment': self.get_treatment(detected_disease)
        }
    
    def get_treatment(self, disease):
        treatments = {
            'healthy': 'Continue current care routine',
            'leaf_blight': 'Remove affected leaves, apply fungicide, improve air circulation',
            'powdery_mildew': 'Apply sulfur-based fungicide, reduce humidity, increase sunlight',
            'rust': 'Remove infected parts, apply copper fungicide, avoid overhead watering',
            'root_rot': 'Improve soil drainage, reduce watering frequency, repot if necessary',
            'aphids': 'Apply neem oil, introduce beneficial insects, use insecticidal soap'
        }
        return treatments.get(disease, 'Consult with agricultural expert')

# Farming advice system
class FarmingAdvisor:
    def __init__(self):
        self.advice_db = {
            'planting': {
                'spring': 'Plant cool-season crops like lettuce, spinach, and peas. Start seeds indoors 6-8 weeks before last frost.',
                'summer': 'Plant warm-season crops like tomatoes, peppers, and cucumbers. Ensure adequate irrigation.',
                'fall': 'Plant fall crops like kale, carrots, and radishes. Consider cover crops for soil health.',
                'winter': 'Focus on indoor gardening or cold frames. Plan next season\'s garden.'
            },
            'soil': {
                'testing': 'Test soil pH and nutrient levels every 2-3 years. Ideal pH range: 6.0-7.0 for most crops.',
                'amendment': 'Add organic matter like compost or aged manure. Consider crop rotation for soil health.',
                'drainage': 'Ensure good drainage. Add sand or organic matter to heavy clay soils.',
                'nutrients': 'Use balanced fertilizer (NPK 10-10-10) or organic alternatives like fish emulsion.'
            },
            'irrigation': {
                'frequency': 'Water deeply but infrequently. Most crops need 1-2 inches of water per week.',
                'timing': 'Water early morning to reduce evaporation and fungal diseases.',
                'method': 'Use drip irrigation or soaker hoses for efficient water use.',
                'monitoring': 'Check soil moisture with finger test or moisture meter.'
            }
        }
    
    def get_advice(self, category, season=None):
        if category in self.advice_db:
            if season and season in self.advice_db[category]:
                return self.advice_db[category][season]
            elif category == 'planting':
                current_month = datetime.now().month
                if current_month in [3, 4, 5]:
                    season = 'spring'
                elif current_month in [6, 7, 8]:
                    season = 'summer'
                elif current_month in [9, 10, 11]:
                    season = 'fall'
                else:
                    season = 'winter'
                return self.advice_db[category][season]
            else:
                return self.advice_db[category]
        return "Advice not available for this category"

# Marketplace system
class Marketplace:
    def __init__(self):
        self.crop_prices = {
            'tomatoes': {'min': 2.50, 'max': 4.00, 'unit': 'per lb'},
            'corn': {'min': 0.80, 'max': 1.20, 'unit': 'per lb'},
            'lettuce': {'min': 1.50, 'max': 2.50, 'unit': 'per head'},
            'carrots': {'min': 1.00, 'max': 1.80, 'unit': 'per lb'},
            'potatoes': {'min': 0.60, 'max': 1.00, 'unit': 'per lb'},
            'onions': {'min': 0.80, 'max': 1.50, 'unit': 'per lb'},
            'cucumbers': {'min': 1.20, 'max': 2.00, 'unit': 'per lb'},
            'peppers': {'min': 2.00, 'max': 3.50, 'unit': 'per lb'}
        }
        
        self.buyers = [
            {'name': 'Fresh Market Co.', 'location': 'Local', 'contact': 'contact@freshmarket.com'},
            {'name': 'Farm to Table', 'location': 'Regional', 'contact': 'info@farmtotable.org'},
            {'name': 'Community Supported Agriculture', 'location': 'Local', 'contact': 'csa@localharvest.org'},
            {'name': 'Restaurant Supply', 'location': 'Local', 'contact': 'orders@restaurantsupply.com'}
        ]
    
    def get_price_suggestion(self, crop, quality='standard'):
        if crop.lower() in self.crop_prices:
            base_price = self.crop_prices[crop.lower()]
            if quality == 'premium':
                price = base_price['max']
            elif quality == 'standard':
                price = (base_price['min'] + base_price['max']) / 2
            else:
                price = base_price['min']
            
            return {
                'crop': crop,
                'suggested_price': round(price, 2),
                'unit': base_price['unit'],
                'price_range': f"${base_price['min']} - ${base_price['max']}",
                'quality': quality
            }
        return None
    
    def get_buyers(self, crop=None):
        if crop:
            # Filter buyers based on crop (mock logic)
            return random.sample(self.buyers, min(2, len(self.buyers)))
        return self.buyers

# Initialize services
disease_detector = DiseaseDetector()
farming_advisor = FarmingAdvisor()
marketplace = Marketplace()

@app.route('/')
def home():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Farmer Assistant</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; color: white; margin-bottom: 40px; }
            .header h1 { font-size: 3rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
            .header p { font-size: 1.2rem; opacity: 0.9; }
            .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; margin-bottom: 40px; }
            .feature-card { background: white; border-radius: 15px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); transition: transform 0.3s ease; }
            .feature-card:hover { transform: translateY(-5px); }
            .feature-card h3 { color: #333; margin-bottom: 15px; font-size: 1.5rem; }
            .feature-card p { color: #666; line-height: 1.6; margin-bottom: 20px; }
            .btn { background: linear-gradient(45deg, #667eea, #764ba2); color: white; padding: 12px 25px; border: none; border-radius: 25px; cursor: pointer; font-size: 1rem; transition: all 0.3s ease; text-decoration: none; display: inline-block; }
            .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.2); }
            .upload-area { border: 2px dashed #ddd; border-radius: 10px; padding: 40px; text-align: center; margin: 20px 0; background: #f9f9f9; }
            .upload-area.dragover { border-color: #667eea; background: #f0f4ff; }
            .result { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 20px 0; border-left: 4px solid #667eea; }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 5px; color: #333; font-weight: 600; }
            .form-group input, .form-group select { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 1rem; }
            .price-card { background: linear-gradient(45deg, #28a745, #20c997); color: white; border-radius: 10px; padding: 20px; margin: 10px 0; }
            .buyer-card { background: #f8f9fa; border-radius: 10px; padding: 20px; margin: 10px 0; border: 1px solid #e9ecef; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🌾 AI Farmer Assistant</h1>
                <p>Your intelligent companion for modern farming</p>
            </div>
            
            <div class="features">
                <div class="feature-card">
                    <h3>🔍 Disease Detection</h3>
                    <p>Upload a photo of your crop to identify diseases and get treatment recommendations.</p>
                    <div class="upload-area" id="uploadArea">
                        <p>📷 Drag & drop an image here or click to browse</p>
                        <input type="file" id="imageInput" accept="image/*" style="display: none;">
                    </div>
                    <button class="btn" onclick="document.getElementById('imageInput').click()">Analyze Image</button>
                    <div id="diseaseResult"></div>
                </div>
                
                <div class="feature-card">
                    <h3>💡 Farming Advice</h3>
                    <p>Get real-time advice on planting, soil management, and irrigation.</p>
                    <div class="form-group">
                        <label for="adviceCategory">Category:</label>
                        <select id="adviceCategory">
                            <option value="planting">Planting</option>
                            <option value="soil">Soil Management</option>
                            <option value="irrigation">Irrigation</option>
                        </select>
                    </div>
                    <button class="btn" onclick="getAdvice()">Get Advice</button>
                    <div id="adviceResult"></div>
                </div>
                
                <div class="feature-card">
                    <h3>💰 Market Prices</h3>
                    <p>Get fair price suggestions and connect with potential buyers.</p>
                    <div class="form-group">
                        <label for="cropType">Crop Type:</label>
                        <select id="cropType">
                            <option value="tomatoes">Tomatoes</option>
                            <option value="corn">Corn</option>
                            <option value="lettuce">Lettuce</option>
                            <option value="carrots">Carrots</option>
                            <option value="potatoes">Potatoes</option>
                            <option value="onions">Onions</option>
                            <option value="cucumbers">Cucumbers</option>
                            <option value="peppers">Peppers</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label for="cropQuality">Quality:</label>
                        <select id="cropQuality">
                            <option value="standard">Standard</option>
                            <option value="premium">Premium</option>
                            <option value="basic">Basic</option>
                        </select>
                    </div>
                    <button class="btn" onclick="getPriceSuggestion()">Get Price</button>
                    <button class="btn" onclick="getBuyers()" style="margin-left: 10px;">Find Buyers</button>
                    <div id="marketResult"></div>
                </div>
            </div>
        </div>

        <script>
            // File upload handling
            const uploadArea = document.getElementById('uploadArea');
            const imageInput = document.getElementById('imageInput');
            const diseaseResult = document.getElementById('diseaseResult');

            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragover');
            });

            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragover');
            });

            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragover');
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    analyzeImage(files[0]);
                }
            });

            imageInput.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    analyzeImage(e.target.files[0]);
                }
            });

            function analyzeImage(file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const img = new Image();
                    img.onload = function() {
                        const canvas = document.createElement('canvas');
                        const ctx = canvas.getContext('2d');
                        canvas.width = img.width;
                        canvas.height = img.height;
                        ctx.drawImage(img, 0, 0);
                        
                        const imageData = canvas.toDataURL('image/jpeg', 0.8);
                        detectDisease(imageData);
                    };
                    img.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }

            async function detectDisease(imageData) {
                try {
                    const response = await fetch('/detect_disease', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({image: imageData})
                    });
                    const result = await response.json();
                    displayDiseaseResult(result);
                } catch (error) {
                    console.error('Error:', error);
                }
            }

            function displayDiseaseResult(result) {
                diseaseResult.innerHTML = `
                    <div class="result">
                        <h4>Analysis Result:</h4>
                        <p><strong>Disease:</strong> ${result.disease}</p>
                        <p><strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%</p>
                        <p><strong>Description:</strong> ${result.description}</p>
                        <p><strong>Treatment:</strong> ${result.treatment}</p>
                    </div>
                `;
            }

            async function getAdvice() {
                const category = document.getElementById('adviceCategory').value;
                try {
                    const response = await fetch(`/get_advice/${category}`);
                    const result = await response.json();
                    document.getElementById('adviceResult').innerHTML = `
                        <div class="result">
                            <h4>Farming Advice:</h4>
                            <p>${result.advice}</p>
                        </div>
                    `;
                } catch (error) {
                    console.error('Error:', error);
                }
            }

            async function getPriceSuggestion() {
                const crop = document.getElementById('cropType').value;
                const quality = document.getElementById('cropQuality').value;
                try {
                    const response = await fetch(`/get_price/${crop}/${quality}`);
                    const result = await response.json();
                    if (result.price_suggestion) {
                        document.getElementById('marketResult').innerHTML = `
                            <div class="price-card">
                                <h4>Price Suggestion for ${result.price_suggestion.crop}</h4>
                                <p><strong>Suggested Price:</strong> $${result.price_suggestion.suggested_price} ${result.price_suggestion.unit}</p>
                                <p><strong>Price Range:</strong> ${result.price_suggestion.price_range}</p>
                                <p><strong>Quality:</strong> ${result.price_suggestion.quality}</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    console.error('Error:', error);
                }
            }

            async function getBuyers() {
                try {
                    const response = await fetch('/get_buyers');
                    const result = await response.json();
                    let buyersHtml = '<div class="result"><h4>Potential Buyers:</h4>';
                    result.buyers.forEach(buyer => {
                        buyersHtml += `
                            <div class="buyer-card">
                                <h5>${buyer.name}</h5>
                                <p><strong>Location:</strong> ${buyer.location}</p>
                                <p><strong>Contact:</strong> ${buyer.contact}</p>
                            </div>
                        `;
                    });
                    buyersHtml += '</div>';
                    document.getElementById('marketResult').innerHTML = buyersHtml;
                } catch (error) {
                    console.error('Error:', error);
                }
            }
        </script>
    </body>
    </html>
    '''
    return html

@app.route('/detect_disease', methods=['POST'])
def detect_disease():
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Remove data URL prefix
        if image_data.startswith('data:image'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        image_bytes = base64.b64decode(image_data)
        image = Image.open(io.BytesIO(image_bytes))
        
        # Convert to numpy array for processing
        image_array = np.array(image)
        
        # Detect disease using our mock model
        result = disease_detector.detect_disease(image_array)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_advice/<category>')
def get_advice(category):
    try:
        advice = farming_advisor.get_advice(category)
        return jsonify({'advice': advice})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_price/<crop>/<quality>')
def get_price(crop, quality):
    try:
        price_suggestion = marketplace.get_price_suggestion(crop, quality)
        if price_suggestion:
            return jsonify({'price_suggestion': price_suggestion})
        else:
            return jsonify({'error': 'Crop not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_buyers')
def get_buyers():
    try:
        buyers = marketplace.get_buyers()
        return jsonify({'buyers': buyers})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'AI Farmer Assistant'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)