#!/bin/bash

# Railway Deployment Helper Script

echo "🚂 Railway Deployment Helper"
echo "=============================="
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found"
    echo "📦 Install it with: npm i -g @railway/cli"
    echo ""
    exit 1
fi

echo "✅ Railway CLI found"
echo ""

# Function to deploy backend
deploy_backend() {
    echo "🔧 Deploying Backend..."
    cd backend || exit
    
    echo "📋 Checking if project exists..."
    if [ ! -f ".railway" ]; then
        echo "🆕 Initializing new Railway project..."
        railway init
    fi
    
    echo "📤 Deploying backend..."
    railway up
    
    echo "🌐 Getting backend URL..."
    BACKEND_URL=$(railway status --json | grep -o '"url":"[^"]*"' | head -1 | sed 's/"url":"//;s/"//')
    
    echo ""
    echo "✅ Backend deployed!"
    echo "🔗 Backend URL: $BACKEND_URL"
    echo ""
    echo "📝 Save this URL for frontend deployment"
    echo ""
    
    cd ..
}

# Function to deploy frontend
deploy_frontend() {
    echo "🎨 Deploying Frontend..."
    
    if [ -z "$1" ]; then
        echo "❌ Backend URL required"
        echo "Usage: ./railway-deploy.sh frontend <backend-url>"
        exit 1
    fi
    
    BACKEND_URL=$1
    cd frontend || exit
    
    echo "📋 Checking if project exists..."
    if [ ! -f ".railway" ]; then
        echo "🆕 Initializing new Railway project..."
        railway init
    fi
    
    echo "🔧 Setting environment variable..."
    railway variables --set NEXT_PUBLIC_API_BASE="$BACKEND_URL"
    
    echo "📤 Deploying frontend..."
    railway up
    
    echo ""
    echo "✅ Frontend deployed!"
    railway open
    
    cd ..
}

# Main menu
case "$1" in
    backend)
        deploy_backend
        ;;
    frontend)
        deploy_frontend "$2"
        ;;
    all)
        deploy_backend
        echo ""
        echo "⏸️  Press Enter after noting the backend URL..."
        read -r
        echo "Enter the backend URL from above:"
        read -r BACKEND_URL
        deploy_frontend "$BACKEND_URL"
        ;;
    *)
        echo "Usage:"
        echo "  ./railway-deploy.sh backend           # Deploy backend only"
        echo "  ./railway-deploy.sh frontend <url>    # Deploy frontend with backend URL"
        echo "  ./railway-deploy.sh all               # Deploy both (interactive)"
        echo ""
        echo "Example:"
        echo "  ./railway-deploy.sh backend"
        echo "  ./railway-deploy.sh frontend https://your-backend.railway.app"
        ;;
esac
