# 🌾 AI Farmer Assistant

An intelligent web application that helps farmers with crop disease detection, farming advice, and market price suggestions.

## 🚀 Features

### 🔍 **Crop Disease Detection**
- Upload photos of crops to identify diseases
- Get detailed disease descriptions and treatment recommendations
- Support for common crop diseases (leaf blight, powdery mildew, rust, root rot, aphids)
- Confidence scoring for detection accuracy

### 💡 **Real-Time Farming Advice**
- **Planting Guidance**: Season-specific planting recommendations
- **Soil Management**: Testing, amendment, drainage, and nutrient advice
- **Irrigation Tips**: Watering frequency, timing, methods, and monitoring
- Context-aware advice based on current season

### 💰 **Marketplace & Pricing**
- Fair price suggestions for various crops
- Quality-based pricing (basic, standard, premium)
- Buyer connection system
- Support for common crops (tomatoes, corn, lettuce, carrots, potatoes, onions, cucumbers, peppers)

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Image Processing**: OpenCV, PIL (Pillow)
- **Machine Learning**: TensorFlow (ready for real model integration)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Data Format**: JSON APIs
- **Deployment**: Gunicorn ready

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Modern web browser with JavaScript enabled

## 🚀 Installation & Setup

### 1. Clone or Download the Project
```bash
# If using git
git clone <repository-url>
cd ai-farmer-assistant

# Or simply download and extract the files
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🌐 Usage

### **Disease Detection**
1. Navigate to the Disease Detection section
2. Drag & drop an image or click to browse
3. Click "Analyze Image" to process
4. View results including disease type, confidence, and treatment

### **Farming Advice**
1. Select advice category (Planting, Soil Management, or Irrigation)
2. Click "Get Advice" for relevant recommendations
3. Advice automatically considers current season for planting tips

### **Market Prices**
1. Select crop type and quality level
2. Click "Get Price" for pricing suggestions
3. Click "Find Buyers" to see potential buyers
4. View contact information for market connections

## 🔧 API Endpoints

### Disease Detection
- `POST /detect_disease` - Analyze crop images for diseases

### Farming Advice
- `GET /get_advice/<category>` - Get advice for specific categories

### Marketplace
- `GET /get_price/<crop>/<quality>` - Get price suggestions
- `GET /get_buyers` - Get list of potential buyers

### Health Check
- `GET /health` - Service status check

## 🎯 Future Enhancements

### **Real ML Model Integration**
- Replace mock disease detection with trained TensorFlow models
- Support for more crop types and diseases
- Improved accuracy and confidence scoring

### **Advanced Features**
- Weather integration for localized advice
- Crop yield prediction
- Pest management recommendations
- Soil testing result analysis
- Mobile app development

### **Marketplace Expansion**
- Real-time price updates from agricultural markets
- Direct buyer-seller communication
- Contract management
- Payment processing integration

## 🚀 Deployment

### **Production Deployment**
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Docker Deployment**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the API documentation
- Review the code comments for implementation details

## 🔒 Security Notes

- The current implementation uses mock data for demonstration
- In production, implement proper authentication and authorization
- Secure file upload handling for image processing
- API rate limiting for production use
- Input validation and sanitization

---

**Built with ❤️ for the farming community**