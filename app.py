from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np
# import tensorflow as tf
# from tensorflow import keras
import requests
from datetime import datetime, timedelta
import json
import sqlite3
from PIL import Image
import base64
import io
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ai-farmer-assistant-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)
os.makedirs('templates', exist_ok=True)

# Allowed file extensions for image upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize database
def init_db():
    conn = sqlite3.connect('farmer_assistant.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            location TEXT,
            farm_size REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buyers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            email TEXT UNIQUE NOT NULL,
            phone TEXT,
            location TEXT,
            crop_preferences TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crop_listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            crop_name TEXT NOT NULL,
            quantity REAL NOT NULL,
            price_per_unit REAL,
            harvest_date DATE,
            quality_grade TEXT,
            location TEXT,
            description TEXT,
            status TEXT DEFAULT 'available',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disease_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER,
            crop_name TEXT,
            disease_detected TEXT,
            confidence_score REAL,
            image_path TEXT,
            treatment_recommended TEXT,
            report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Disease detection model (placeholder - in production, use a trained model)
class DiseaseDetector:
    def __init__(self):
        self.diseases = {
            'healthy': {'confidence': 0.95, 'treatment': 'No treatment needed. Continue good farming practices.'},
            'blight': {'confidence': 0.85, 'treatment': 'Apply copper-based fungicide. Remove affected leaves.'},
            'rust': {'confidence': 0.80, 'treatment': 'Use rust-resistant varieties. Apply appropriate fungicide.'},
            'mosaic_virus': {'confidence': 0.75, 'treatment': 'Remove infected plants. Control aphid vectors.'},
            'bacterial_spot': {'confidence': 0.82, 'treatment': 'Apply copper bactericide. Improve air circulation.'}
        }
    
    def detect_disease(self, image_path):
        # Placeholder implementation - in production, use a trained CNN model
        # This would analyze the image using computer vision
        try:
            img = cv2.imread(image_path)
            if img is None:
                return {'disease': 'unknown', 'confidence': 0.0, 'treatment': 'Unable to analyze image.'}
            
            # Simulate disease detection based on image properties
            # In reality, this would be a trained model prediction
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            mean_intensity = np.mean(gray)
            
            if mean_intensity < 50:
                disease = 'blight'
            elif mean_intensity > 200:
                disease = 'healthy'
            elif np.std(gray) > 50:
                disease = 'rust'
            else:
                disease = 'bacterial_spot'
            
            result = self.diseases.get(disease, self.diseases['healthy'])
            return {
                'disease': disease,
                'confidence': result['confidence'],
                'treatment': result['treatment']
            }
        except Exception as e:
            logger.error(f"Error in disease detection: {str(e)}")
            return {'disease': 'error', 'confidence': 0.0, 'treatment': 'Error analyzing image.'}

disease_detector = DiseaseDetector()

# Farming advice system
class FarmingAdvisor:
    def __init__(self):
        self.crop_data = {
            'tomato': {
                'planting_season': 'Spring (March-May) or Fall (August-September)',
                'soil_ph': '6.0-6.8',
                'water_needs': 'Deep watering 2-3 times per week',
                'fertilizer': 'Balanced NPK (10-10-10) every 2 weeks',
                'spacing': '18-24 inches apart'
            },
            'corn': {
                'planting_season': 'Late spring after last frost (May-June)',
                'soil_ph': '6.0-6.8',
                'water_needs': '1-2 inches per week',
                'fertilizer': 'High nitrogen fertilizer at planting',
                'spacing': '8-12 inches apart in rows'
            },
            'wheat': {
                'planting_season': 'Fall (September-November) for winter wheat',
                'soil_ph': '6.0-7.0',
                'water_needs': '12-15 inches annually',
                'fertilizer': 'Nitrogen in spring, phosphorus at planting',
                'spacing': '1-1.5 inches apart'
            }
        }
    
    def get_planting_advice(self, crop, location):
        advice = self.crop_data.get(crop.lower(), {})
        if not advice:
            return "Crop information not available. Please consult local agricultural extension."
        
        return {
            'crop': crop,
            'planting_season': advice.get('planting_season', 'Consult local extension'),
            'soil_requirements': advice.get('soil_ph', 'pH 6.0-7.0'),
            'irrigation': advice.get('water_needs', 'Regular watering needed'),
            'fertilization': advice.get('fertilizer', 'Balanced fertilizer recommended'),
            'spacing': advice.get('spacing', 'Follow seed packet instructions')
        }
    
    def get_seasonal_advice(self, season, location):
        seasonal_tips = {
            'spring': [
                'Prepare soil by adding compost',
                'Start seeds indoors for warm-season crops',
                'Check and repair irrigation systems',
                'Monitor for early pest activity'
            ],
            'summer': [
                'Maintain consistent watering schedule',
                'Monitor for heat stress in plants',
                'Harvest early crops regularly',
                'Apply mulch to retain moisture'
            ],
            'fall': [
                'Plant cover crops for soil health',
                'Harvest and store crops properly',
                'Clean up garden debris',
                'Plan for next year\'s crops'
            ],
            'winter': [
                'Plan crop rotation for next year',
                'Order seeds and supplies',
                'Maintain equipment',
                'Study and learn about new techniques'
            ]
        }
        return seasonal_tips.get(season.lower(), ['General farming advice not available'])

farming_advisor = FarmingAdvisor()

# Price suggestion system
class PriceAdvisor:
    def __init__(self):
        # Mock market prices - in production, integrate with real market APIs
        self.market_prices = {
            'tomato': {'current': 2.50, 'trend': 'stable', 'high': 3.00, 'low': 2.00},
            'corn': {'current': 4.25, 'trend': 'rising', 'high': 4.80, 'low': 3.70},
            'wheat': {'current': 6.50, 'trend': 'falling', 'high': 7.20, 'low': 6.00},
            'potato': {'current': 1.80, 'trend': 'stable', 'high': 2.20, 'low': 1.40}
        }
    
    def get_fair_price(self, crop, quantity, quality='standard'):
        base_price = self.market_prices.get(crop.lower(), {'current': 2.00, 'trend': 'stable'})
        
        # Quality adjustments
        quality_multipliers = {
            'premium': 1.2,
            'standard': 1.0,
            'fair': 0.8
        }
        
        # Quantity adjustments (bulk discounts)
        if quantity > 1000:
            quantity_multiplier = 0.95
        elif quantity > 500:
            quantity_multiplier = 0.98
        else:
            quantity_multiplier = 1.0
        
        suggested_price = base_price['current'] * quality_multipliers.get(quality, 1.0) * quantity_multiplier
        
        return {
            'crop': crop,
            'suggested_price': round(suggested_price, 2),
            'market_trend': base_price['trend'],
            'price_range': {
                'low': base_price['low'],
                'high': base_price['high']
            },
            'factors': {
                'quality_adjustment': quality_multipliers.get(quality, 1.0),
                'quantity_adjustment': quantity_multiplier
            }
        }

price_advisor = PriceAdvisor()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/detect-disease', methods=['POST'])
def detect_disease():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
        filename = timestamp + filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Detect disease
        result = disease_detector.detect_disease(filepath)
        
        # Save to database (optional farmer_id)
        farmer_id = request.form.get('farmer_id', None)
        crop_name = request.form.get('crop_name', 'unknown')
        
        conn = sqlite3.connect('farmer_assistant.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO disease_reports (farmer_id, crop_name, disease_detected, confidence_score, image_path, treatment_recommended)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (farmer_id, crop_name, result['disease'], result['confidence'], filepath, result['treatment']))
        conn.commit()
        conn.close()
        
        return jsonify({
            'disease': result['disease'],
            'confidence': result['confidence'],
            'treatment': result['treatment'],
            'image_path': filename
        })
    
    return jsonify({'error': 'Invalid file format'}), 400

@app.route('/api/farming-advice', methods=['GET'])
def get_farming_advice():
    crop = request.args.get('crop', '')
    location = request.args.get('location', '')
    advice_type = request.args.get('type', 'planting')
    
    if advice_type == 'planting' and crop:
        advice = farming_advisor.get_planting_advice(crop, location)
        return jsonify(advice)
    elif advice_type == 'seasonal':
        season = request.args.get('season', 'spring')
        tips = farming_advisor.get_seasonal_advice(season, location)
        return jsonify({'season': season, 'tips': tips})
    
    return jsonify({'error': 'Invalid request parameters'}), 400

@app.route('/api/price-suggestion', methods=['GET'])
def get_price_suggestion():
    crop = request.args.get('crop', '')
    quantity = float(request.args.get('quantity', 0))
    quality = request.args.get('quality', 'standard')
    
    if not crop or quantity <= 0:
        return jsonify({'error': 'Invalid crop or quantity'}), 400
    
    price_info = price_advisor.get_fair_price(crop, quantity, quality)
    return jsonify(price_info)

@app.route('/api/register-farmer', methods=['POST'])
def register_farmer():
    data = request.json
    required_fields = ['name', 'email']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        conn = sqlite3.connect('farmer_assistant.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO farmers (name, email, phone, location, farm_size)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data.get('phone'), data.get('location'), data.get('farm_size')))
        farmer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Farmer registered successfully', 'farmer_id': farmer_id})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 400

@app.route('/api/register-buyer', methods=['POST'])
def register_buyer():
    data = request.json
    required_fields = ['name', 'email']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        conn = sqlite3.connect('farmer_assistant.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO buyers (name, company, email, phone, location, crop_preferences)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['name'], data.get('company'), data['email'], data.get('phone'), data.get('location'), data.get('crop_preferences')))
        buyer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Buyer registered successfully', 'buyer_id': buyer_id})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 400

@app.route('/api/list-crop', methods=['POST'])
def list_crop():
    data = request.json
    required_fields = ['farmer_id', 'crop_name', 'quantity']
    
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('farmer_assistant.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO crop_listings (farmer_id, crop_name, quantity, price_per_unit, harvest_date, quality_grade, location, description)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data['farmer_id'], data['crop_name'], data['quantity'], data.get('price_per_unit'), 
          data.get('harvest_date'), data.get('quality_grade', 'standard'), data.get('location'), data.get('description')))
    listing_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Crop listed successfully', 'listing_id': listing_id})

@app.route('/api/search-crops', methods=['GET'])
def search_crops():
    crop_name = request.args.get('crop_name', '')
    location = request.args.get('location', '')
    max_price = request.args.get('max_price', None)
    
    conn = sqlite3.connect('farmer_assistant.db')
    cursor = conn.cursor()
    
    query = '''
        SELECT cl.*, f.name as farmer_name, f.location as farmer_location, f.phone as farmer_phone
        FROM crop_listings cl
        JOIN farmers f ON cl.farmer_id = f.id
        WHERE cl.status = 'available'
    '''
    params = []
    
    if crop_name:
        query += ' AND cl.crop_name LIKE ?'
        params.append(f'%{crop_name}%')
    
    if location:
        query += ' AND (cl.location LIKE ? OR f.location LIKE ?)'
        params.extend([f'%{location}%', f'%{location}%'])
    
    if max_price:
        query += ' AND cl.price_per_unit <= ?'
        params.append(float(max_price))
    
    query += ' ORDER BY cl.created_at DESC'
    
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    
    # Convert to list of dictionaries
    columns = [desc[0] for desc in cursor.description]
    crops = [dict(zip(columns, row)) for row in results]
    
    return jsonify({'crops': crops})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)