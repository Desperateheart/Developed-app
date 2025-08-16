#!/bin/bash

echo "🌾 Starting AI Farmer Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Start the application
echo "🚀 Starting the application..."
echo "🌐 Open your browser and go to: http://localhost:5000"
echo "⏹️  Press Ctrl+C to stop the application"
echo ""

python3 app.py