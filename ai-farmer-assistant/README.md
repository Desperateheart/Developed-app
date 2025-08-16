# AI Farmer Assistant 🌾

A comprehensive AI-powered farming assistant application that helps farmers detect crop diseases, get real-time farming advice, and connect with marketplace buyers.

## Features

### 🔬 Disease Detection
- **AI-Powered Analysis**: Upload photos of crops to instantly detect diseases
- **Confidence Scoring**: Get accuracy percentages for disease identification
- **Treatment Recommendations**: Receive both organic and chemical treatment options
- **Severity Assessment**: Understand the extent of disease spread
- **Prevention Tips**: Learn how to prevent future occurrences

### 🌱 Farming Advice
- **Planting Guidance**: Get optimal planting times and techniques for different crops
- **Irrigation Management**: Receive water management recommendations based on weather and soil
- **Soil Health**: Understand soil requirements and improvement strategies
- **Fertilizer Recommendations**: Get NPK ratios and application schedules

### 💰 Marketplace
- **Price Suggestions**: Get fair market prices based on quality and quantity
- **Buyer Connections**: Find verified buyers for your produce
- **Market Trends**: Track price trends and market demand
- **Listing Creation**: Create and manage produce listings

### ☁️ Weather Integration
- **Real-time Weather**: Current conditions and 7-day forecasts
- **Farming Alerts**: Weather-based alerts for farming activities
- **Disease Risk Warnings**: Humidity and temperature-based disease predictions
- **Optimal Activity Windows**: Best times for planting, spraying, and harvesting

### 📊 Analytics
- **Yield Tracking**: Monitor crop performance over time
- **Revenue Analysis**: Track income and expenses
- **Disease History**: Review past detections and treatments
- **Performance Metrics**: Compare yields against averages

## Technology Stack

### Backend
- **FastAPI**: High-performance Python web framework
- **PyTorch**: Deep learning for disease detection
- **OpenCV**: Image processing and analysis
- **SQLAlchemy**: Database ORM
- **JWT Authentication**: Secure user authentication

### Frontend
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **Material-UI**: Beautiful, responsive components
- **Recharts**: Data visualization
- **React Router**: Navigation

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### Backend Setup

1. Navigate to the project directory:
```bash
cd /workspace/ai-farmer-assistant
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
export SECRET_KEY="your-secret-key-here"
export DATABASE_URL="sqlite:///./farmer_assistant.db"  # Or your database URL
```

5. Run the backend server:
```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd /workspace/ai-farmer-assistant/frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The application will open at `http://localhost:3000`

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for interactive API documentation.

### Key Endpoints

- `POST /api/disease/detect` - Upload image for disease detection
- `GET /api/disease/history` - Get detection history
- `POST /api/advice/planting` - Get planting advice
- `POST /api/advice/irrigation` - Get irrigation recommendations
- `GET /api/marketplace/prices` - Get current market prices
- `POST /api/marketplace/price-suggestion` - Get fair price suggestions
- `GET /api/marketplace/buyers` - Find potential buyers
- `GET /api/weather/current` - Get current weather
- `GET /api/weather/forecast` - Get weather forecast
- `GET /api/weather/alerts` - Get farming alerts

## Usage

### Disease Detection
1. Navigate to the Disease Detection page
2. Upload a clear photo of the affected crop
3. Click "Detect Disease"
4. Review the results and treatment recommendations
5. Follow the suggested organic or chemical treatments

### Getting Farming Advice
1. Go to the Farming Advice section
2. Select the type of advice needed (Planting, Irrigation, Soil, Fertilizer)
3. Enter your crop type and conditions
4. Receive personalized recommendations

### Using the Marketplace
1. Check current market prices for your crops
2. Get fair price suggestions based on quality
3. Search for verified buyers in your area
4. Create listings for your produce

### Weather Monitoring
1. View current weather conditions
2. Check 7-day forecast
3. Review farming-specific alerts
4. Plan activities based on weather windows

## Project Structure

```
ai-farmer-assistant/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── services/
│   │   ├── disease_detection.py
│   │   ├── farming_advice.py
│   │   ├── marketplace.py
│   │   └── weather.py
│   ├── models/
│   │   └── database.py
│   ├── schemas.py
│   └── auth.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── requirements.txt
├── package.json
└── README.md
```

## Features in Detail

### Disease Detection Algorithm
- Uses ResNet-50 architecture for image classification
- Fallback heuristic analysis using color detection
- Identifies 15+ common crop diseases
- Provides confidence scores and severity analysis

### Market Price Algorithm
- Real-time price tracking
- Quality-based pricing adjustments
- Quantity discounts/premiums
- Location-based price variations
- Historical trend analysis

### Weather Integration
- Farming-specific weather alerts
- Disease risk predictions based on humidity
- Irrigation recommendations
- Optimal activity timing

## Contributing

Contributions are welcome! Please feel free to submit pull requests.

## License

This project is licensed under the MIT License.

## Support

For issues or questions, please create an issue in the repository.

## Acknowledgments

- Built with FastAPI and React
- Uses PyTorch for deep learning
- Material-UI for beautiful components
- OpenCV for image processing

---

**Note**: This is a demonstration project. In production, you would need to:
- Train the disease detection model with real agricultural data
- Connect to real weather APIs
- Integrate with actual market price feeds
- Implement proper security measures
- Add comprehensive error handling
- Set up proper database migrations
- Configure production deployment