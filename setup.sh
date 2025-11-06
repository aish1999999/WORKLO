#!/bin/bash

# Automated Resume Tailor - Setup Script
# This script helps you set up the application quickly

set -e

echo "🚀 Automated Resume Tailor - Setup Script"
echo "=========================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Node.js
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓${NC} Node.js is installed: $NODE_VERSION"
else
    echo -e "${RED}✗${NC} Node.js is not installed"
    echo "   Please install Node.js from https://nodejs.org/"
    exit 1
fi

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python is installed: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python is not installed"
    echo "   Please install Python from https://python.org/"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip is installed"
else
    echo -e "${RED}✗${NC} pip is not installed"
    echo "   Please install pip"
    exit 1
fi

echo ""
echo "📦 Installing dependencies..."

# Install Node.js dependencies
echo "Installing Node.js packages..."
npm install
cd apps/worklo
npm install
cd ../..
echo -e "${GREEN}✓${NC} Node.js dependencies installed"

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r requirements.txt
echo -e "${GREEN}✓${NC} Python dependencies installed"

echo ""
echo "⚙️  Setting up environment..."

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Created .env file from .env.example"
    echo -e "${YELLOW}⚠${NC}  Please edit .env with your actual API keys"
else
    echo -e "${YELLOW}⚠${NC}  .env file already exists, skipping creation"
fi

echo ""
echo "🗄️  Setting up database..."

# Setup Prisma
cd apps/worklo
npx prisma generate
echo -e "${GREEN}✓${NC} Prisma client generated"

# Ask if user wants to push database schema
read -p "Do you want to push database schema to Supabase now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    npx prisma db push
    echo -e "${GREEN}✓${NC} Database schema pushed"
else
    echo -e "${YELLOW}⚠${NC}  Skipped database push. Run 'npx prisma db push' later"
fi
cd ../..

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - OPENAI_API_KEY (from https://platform.openai.com/api-keys)"
echo "   - GOOGLE_CLIENT_SECRETS_FILE (OAuth credentials)"
echo "   - NEXT_PUBLIC_SUPABASE_URL (from https://supabase.com)"
echo "   - DATABASE_URL (Supabase connection string)"
echo ""
echo "2. Start the Python backend:"
echo "   python python_api/main.py"
echo ""
echo "3. Start the Next.js frontend (in a new terminal):"
echo "   cd apps/worklo && npm run dev"
echo ""
echo "4. Open http://localhost:3000/dashboard"
echo ""
echo "📚 For detailed instructions, see README.md"
echo ""
echo "Happy Resume Tailoring! 🎯"
