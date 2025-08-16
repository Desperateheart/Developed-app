# AI Farmer Assistant 🌱

A comprehensive AI-powered farming solution that helps farmers identify crop diseases, get expert advice, and connect with buyers for fair pricing.

## Features

### 🔬 Crop Disease Detection
- **AI-Powered Analysis**: Upload crop photos for instant disease identification
- **Treatment Recommendations**: Get specific treatment advice for detected diseases
- **Confidence Scoring**: Reliable results with confidence percentages
- **Disease Database**: Covers common crop diseases including blight, rust, mosaic virus, and bacterial spot

### 🧠 Smart Farming Advice
- **Planting Guidance**: Crop-specific planting recommendations
- **Seasonal Tips**: Season-appropriate farming advice
- **Irrigation Optimization**: Water management best practices
- **Soil & Fertilization**: pH requirements and fertilizer recommendations

### 💰 Fair Price Calculator
- **Market-Based Pricing**: Real-time price suggestions based on market trends
- **Quality Adjustments**: Price calculations based on crop quality grades
- **Quantity Discounts**: Bulk pricing considerations
- **Market Trends**: Visual indicators for price movements

### 🤝 Farmer-Buyer Marketplace
- **Direct Connection**: Connect farmers directly with buyers
- **Crop Listings**: Easy-to-use crop listing system
- **Search & Filter**: Find specific crops by type, location, and price
- **Contact Integration**: Direct communication between parties

## Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLite**: Lightweight database for data storage
- **OpenCV**: Computer vision for image processing
- **TensorFlow**: Machine learning framework for disease detection
- **Pillow**: Image processing library

### Frontend
- **HTML5/CSS3**: Modern responsive design
- **Bootstrap 5**: UI framework for responsive layout
- **JavaScript (ES6+)**: Interactive functionality
- **Font Awesome**: Icon library

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-farmer-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### Disease Detection
- `POST /api/detect-disease` - Upload image for disease analysis
  - Parameters: `image` (file), `crop_name` (optional)
  - Returns: Disease type, confidence score, treatment recommendation

### Farming Advice
- `GET /api/farming-advice` - Get farming recommendations
  - Parameters: `type` (planting/seasonal), `crop`, `season`, `location`
  - Returns: Specific advice based on request type

### Price Suggestions
- `GET /api/price-suggestion` - Calculate fair crop prices
  - Parameters: `crop`, `quantity`, `quality`
  - Returns: Suggested price, market trends, price range

### User Registration
- `POST /api/register-farmer` - Register as a farmer
- `POST /api/register-buyer` - Register as a buyer

### Marketplace
- `POST /api/list-crop` - List crops for sale
- `GET /api/search-crops` - Search available crops
  - Parameters: `crop_name`, `location`, `max_price`

## Usage Guide

### For Farmers

1. **Register**: Create a farmer account to access all features
2. **Disease Detection**: 
   - Upload clear photos of affected crops
   - Get instant analysis and treatment recommendations
   - Track disease history in your dashboard
3. **Get Advice**:
   - Access planting guides for different crops
   - Get seasonal farming tips
   - Learn irrigation best practices
4. **Price Your Crops**:
   - Use the fair price calculator
   - Consider quality grades and market trends
   - List crops in the marketplace

### For Buyers

1. **Register**: Create a buyer account
2. **Browse Crops**: Search for available produce
3. **Contact Farmers**: Direct communication for negotiations
4. **Track Preferences**: Save crop preferences for better matches

## Database Schema

### Tables
- **farmers**: Farmer registration and profile information
- **buyers**: Buyer registration and preferences
- **crop_listings**: Available crops for sale
- **disease_reports**: Disease detection history

## Development Features

### Disease Detection Algorithm
The current implementation uses basic image analysis for demonstration. In production, this would be replaced with:
- Pre-trained CNN models for crop disease classification
- Transfer learning on agricultural datasets
- Integration with agricultural research databases

### Future Enhancements
- **Weather Integration**: Real-time weather data for farming advice
- **IoT Sensors**: Integration with soil moisture and pH sensors
- **Mobile App**: Native mobile applications for field use
- **Advanced Analytics**: Crop yield predictions and optimization
- **Blockchain**: Transparent supply chain tracking
- **Multi-language**: Support for local languages

## Configuration

### Environment Variables
Create a `.env` file for production configuration:
```
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
WEATHER_API_KEY=your-weather-api-key
```

### Production Deployment
For production deployment, consider:
- Using PostgreSQL instead of SQLite
- Implementing proper authentication and authorization
- Adding rate limiting and security headers
- Using a production WSGI server like Gunicorn
- Setting up proper logging and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation wiki

## Acknowledgments

- Agricultural research institutions for disease data
- Open-source computer vision libraries
- Bootstrap and Font Awesome for UI components
- The farming community for valuable feedback

---

**Built with ❤️ for farmers worldwide** 🌾