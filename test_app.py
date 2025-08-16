#!/usr/bin/env python3
"""
Test script for AI Farmer Assistant API endpoints
"""

import requests
import json
import base64
from PIL import Image
import io
import numpy as np

def create_test_image():
    """Create a simple test image for disease detection"""
    # Create a simple 100x100 test image
    img_array = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='JPEG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{img_str}"

def test_health_check():
    """Test the health check endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get('http://localhost:5000/health')
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
        else:
            print("❌ Health check failed:", response.status_code)
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Is the app running?")
        return False
    return True

def test_disease_detection():
    """Test the disease detection endpoint"""
    print("\n🔍 Testing disease detection...")
    try:
        test_image = create_test_image()
        data = {'image': test_image}
        response = requests.post('http://localhost:5000/detect_disease', 
                               json=data, 
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Disease detection passed:")
            print(f"   Disease: {result['disease']}")
            print(f"   Confidence: {result['confidence']}")
            print(f"   Description: {result['description']}")
        else:
            print("❌ Disease detection failed:", response.status_code)
            print("   Response:", response.text)
    except Exception as e:
        print(f"❌ Disease detection error: {e}")

def test_farming_advice():
    """Test the farming advice endpoint"""
    print("\n💡 Testing farming advice...")
    categories = ['planting', 'soil', 'irrigation']
    
    for category in categories:
        try:
            response = requests.get(f'http://localhost:5000/get_advice/{category}')
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {category.capitalize()} advice: {result['advice'][:100]}...")
            else:
                print(f"❌ {category} advice failed:", response.status_code)
        except Exception as e:
            print(f"❌ {category} advice error: {e}")

def test_marketplace():
    """Test the marketplace endpoints"""
    print("\n💰 Testing marketplace...")
    
    # Test price suggestions
    crops = ['tomatoes', 'corn', 'lettuce']
    qualities = ['standard', 'premium']
    
    for crop in crops:
        for quality in qualities:
            try:
                response = requests.get(f'http://localhost:5000/get_price/{crop}/{quality}')
                if response.status_code == 200:
                    result = response.json()
                    price_info = result['price_suggestion']
                    print(f"✅ {crop} ({quality}): ${price_info['suggested_price']} {price_info['unit']}")
                else:
                    print(f"❌ Price for {crop} ({quality}) failed:", response.status_code)
            except Exception as e:
                print(f"❌ Price error for {crop} ({quality}): {e}")
    
    # Test buyers
    try:
        response = requests.get('http://localhost:5000/get_buyers')
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Found {len(result['buyers'])} potential buyers")
        else:
            print("❌ Buyers list failed:", response.status_code)
    except Exception as e:
        print(f"❌ Buyers error: {e}")

def main():
    """Run all tests"""
    print("🧪 AI Farmer Assistant API Tests")
    print("=" * 40)
    
    # Test health first
    if not test_health_check():
        print("\n❌ Server is not running. Please start the application first:")
        print("   python app.py")
        return
    
    # Run all tests
    test_disease_detection()
    test_farming_advice()
    test_marketplace()
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()