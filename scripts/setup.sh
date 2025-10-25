#!/bin/bash

# NIFTY Options Trading System Setup Script
# This script sets up the complete trading environment

set -e

echo "🚀 Setting up NIFTY Options Trading System..."
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.8"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $REQUIRED_VERSION or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

print_status "Python version: $PYTHON_VERSION ✓"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip."
    exit 1
fi

print_status "pip3 is available ✓"

# Create virtual environment
print_status "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
print_status "Creating project directories..."
mkdir -p data logs backtest_results trades positions screenshots reports models

# Set up environment file
if [ ! -f .env ]; then
    print_status "Creating environment file..."
    cp env_example.txt .env
    print_warning "Please edit .env file with your API credentials"
fi

# Set up logging
print_status "Setting up logging configuration..."
mkdir -p logs
touch logs/trading.log

# Create initial data files
print_status "Creating initial data files..."
touch data/nifty_data.csv
touch data/options_chain.csv
touch data/volatility_data.csv

# Set permissions
print_status "Setting file permissions..."
chmod +x main.py
chmod +x dashboard.py
chmod +x run_examples.py

# Create systemd service file (for Linux)
if command -v systemctl &> /dev/null; then
    print_status "Creating systemd service file..."
    cat > nifty-trading.service << EOF
[Unit]
Description=NIFTY Options Trading System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/venv/bin
ExecStart=$(pwd)/venv/bin/python main.py live
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
    
    print_warning "To install as system service, run: sudo cp nifty-trading.service /etc/systemd/system/"
    print_warning "Then: sudo systemctl enable nifty-trading && sudo systemctl start nifty-trading"
fi

# Create startup script
print_status "Creating startup script..."
cat > start_trading.sh << 'EOF'
#!/bin/bash
# NIFTY Options Trading System Startup Script

echo "🚀 Starting NIFTY Options Trading System..."

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please copy env_example.txt to .env and configure it."
    exit 1
fi

# Start the trading system
echo "📈 Starting live trading..."
python main.py live
EOF

chmod +x start_trading.sh

# Create stop script
print_status "Creating stop script..."
cat > stop_trading.sh << 'EOF'
#!/bin/bash
# NIFTY Options Trading System Stop Script

echo "🛑 Stopping NIFTY Options Trading System..."

# Kill any running trading processes
pkill -f "main.py live" || true
pkill -f "dashboard.py" || true

echo "✅ Trading system stopped"
EOF

chmod +x stop_trading.sh

# Create dashboard script
print_status "Creating dashboard script..."
cat > start_dashboard.sh << 'EOF'
#!/bin/bash
# NIFTY Options Trading Dashboard Startup Script

echo "📊 Starting NIFTY Options Trading Dashboard..."

# Activate virtual environment
source venv/bin/activate

# Start the dashboard
echo "🌐 Starting dashboard at http://localhost:8050"
python dashboard.py
EOF

chmod +x start_dashboard.sh

# Create backtest script
print_status "Creating backtest script..."
cat > run_backtest.sh << 'EOF'
#!/bin/bash
# NIFTY Options Trading Backtest Script

echo "📈 Running NIFTY Options Trading Backtest..."

# Activate virtual environment
source venv/bin/activate

# Run backtest
python main.py backtest
EOF

chmod +x run_backtest.sh

# Create examples script
print_status "Creating examples script..."
cat > run_examples.sh << 'EOF'
#!/bin/bash
# NIFTY Options Trading Examples Script

echo "🧪 Running NIFTY Options Trading Examples..."

# Activate virtual environment
source venv/bin/activate

# Run examples
python run_examples.py
EOF

chmod +x run_examples.sh

# Test installation
print_status "Testing installation..."
python -c "import numpy, pandas, sklearn, xgboost, lightgbm; print('All dependencies imported successfully ✓')"

print_status "Setup completed successfully! 🎉"
echo ""
echo "📋 Next Steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Run examples: ./run_examples.sh"
echo "3. Run backtest: ./run_backtest.sh"
echo "4. Start trading: ./start_trading.sh"
echo "5. Start dashboard: ./start_dashboard.sh"
echo ""
echo "🔧 Available Commands:"
echo "  ./start_trading.sh    - Start live trading"
echo "  ./start_dashboard.sh  - Start web dashboard"
echo "  ./run_backtest.sh     - Run backtesting"
echo "  ./run_examples.sh     - Run examples"
echo "  ./stop_trading.sh     - Stop trading system"
echo ""
echo "🌐 Dashboard will be available at: http://localhost:8050"
echo "📊 Trading logs: logs/trading.log"
echo ""
print_status "Happy Trading! 📈🚀"
