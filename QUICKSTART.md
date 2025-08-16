# 🚀 Quick Start Guide

Get the AI Farmer Assistant running in under 5 minutes!

## ⚡ Super Quick Start

### Option 1: Using the startup script (Recommended)
```bash
./start.sh
```

### Option 2: Manual start
```bash
pip install -r requirements.txt
python app.py
```

### Option 3: Using Docker
```bash
docker-compose up --build
```

## 🌐 Access the Application

Open your web browser and go to: **http://localhost:5000**

## 🧪 Test the Application

Run the test script to verify everything is working:
```bash
python test_app.py
```

## 📱 What You Can Do

### 🔍 **Disease Detection**
- Upload a crop photo
- Get instant disease identification
- Receive treatment recommendations

### 💡 **Farming Advice**
- Get planting tips for current season
- Learn about soil management
- Understand irrigation best practices

### 💰 **Market Prices**
- Check fair prices for your crops
- Find potential buyers
- Get quality-based pricing

## 🛠️ Troubleshooting

### **Port already in use**
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

### **Dependencies not found**
```bash
# Upgrade pip first
pip install --upgrade pip
# Then install requirements
pip install -r requirements.txt
```

### **Permission denied on start.sh**
```bash
chmod +x start.sh
```

## 🔄 Restart the Application

1. Press `Ctrl+C` to stop
2. Run `./start.sh` again

## 📁 Project Structure

```
ai-farmer-assistant/
├── app.py              # Main application
├── requirements.txt    # Python dependencies
├── start.sh           # Startup script
├── test_app.py        # Test script
├── Dockerfile         # Docker configuration
├── docker-compose.yml # Docker compose
├── README.md          # Full documentation
└── .env.example       # Configuration template
```

## 🆘 Need Help?

- Check the full [README.md](README.md)
- Run the test script to diagnose issues
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed

---

**Happy Farming! 🌾**