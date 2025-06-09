#!/bin/bash

# NFO Standard Web Importer Deployment Script

echo "NFO Standard Web Importer Deployment"
echo "===================================="

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for API keys
if [ -z "$TMDB_API_KEY" ]; then
    echo "Warning: TMDB_API_KEY not set. API calls to TMDB will fail."
fi

if [ -z "$OMDB_API_KEY" ]; then
    echo "Warning: OMDB_API_KEY not set. API calls to OMDB will fail."
fi

if [ -z "$TVDB_API_KEY" ]; then
    echo "Warning: TVDB_API_KEY not set. API calls to TVDB will fail."
fi

# Start options
echo ""
echo "Deployment Options:"
echo "1. Run API server only (for production)"
echo "2. Run API server and open browser (for development)"
echo "3. Static files only (mock data mode)"
echo ""
read -p "Select option (1-3): " option

case $option in
    1)
        echo "Starting API server on port 5000..."
        python3 api_server.py
        ;;
    2)
        echo "Starting API server and opening browser..."
        python3 api_server.py &
        SERVER_PID=$!
        sleep 2
        
        # Update config to use local server
        sed -i.bak 's/API_SERVER: null/API_SERVER: "http:\/\/localhost:5000"/' config.js
        sed -i.bak 's/USE_MOCK_DATA: true/USE_MOCK_DATA: false/' config.js
        
        # Open in browser
        if command -v open &> /dev/null; then
            open index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open index.html
        else
            echo "Please open index.html in your browser"
        fi
        
        echo "Press Ctrl+C to stop the server"
        wait $SERVER_PID
        
        # Restore config
        mv config.js.bak config.js
        ;;
    3)
        echo "Static deployment mode - no API server needed"
        echo "Opening index.html in browser..."
        
        if command -v open &> /dev/null; then
            open index.html
        elif command -v xdg-open &> /dev/null; then
            xdg-open index.html
        else
            echo "Please open index.html in your browser"
        fi
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac