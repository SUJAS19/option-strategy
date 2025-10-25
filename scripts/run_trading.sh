#!/bin/bash

# NIFTY Options Trading System - Live Trading Script
# This script runs the trading system like a professional human trader

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[TRADING]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_trading() {
    echo -e "${PURPLE}[MARKET]${NC} $1"
}

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███╗   ██╗██╗███████╗████████╗██╗   ██╗    ███████╗███████╗ ║
║    ████╗  ██║██║██╔════╝╚══██╔══╝╚██╗ ██╔╝    ██╔════╝██╔════╝ ║
║    ██╔██╗ ██║██║█████╗     ██║    ╚████╔╝     █████╗  █████╗   ║
║    ██║╚██╗██║██║██╔══╝     ██║     ╚██╔╝      ██╔══╝  ██╔══╝   ║
║    ██║ ╚████║██║██║        ██║      ██║       ███████╗███████╗ ║
║    ╚═╝  ╚═══╝╚═╝╚═╝        ╚═╝      ╚═╝       ╚══════╝╚══════╝ ║
║                                                              ║
║              OPTIONS ALGORITHMIC TRADING SYSTEM              ║
║                    🤖 AI-Powered Trading 🤖                   ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "🚀 Initializing NIFTY Options Trading System..."
print_info "📅 Date: $(date)"
print_info "🕐 Time: $(date +%H:%M:%S)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_error "Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    print_error ".env file not found. Please copy env_example.txt to .env and configure it."
    exit 1
fi

# Check if required directories exist
print_status "Checking project structure..."
mkdir -p data logs backtest_results trades positions screenshots reports models

# Display system information
print_info "📊 System Information:"
echo "  • Python Version: $(python --version)"
echo "  • Working Directory: $(pwd)"
echo "  • Virtual Environment: $(which python)"
echo ""

# Check market hours (simplified)
current_hour=$(date +%H)
current_minute=$(date +%M)
current_time=$((current_hour * 100 + current_minute))

market_open=915  # 9:15 AM
market_close=1530  # 3:30 PM

if [ $current_time -ge $market_open ] && [ $current_time -le $market_close ]; then
    print_success "✅ Market is OPEN - Trading system will start"
    market_status="OPEN"
else
    print_warning "⚠️  Market is CLOSED - Running in simulation mode"
    market_status="CLOSED"
fi

echo ""

# Display trading configuration
print_info "⚙️  Trading Configuration:"
echo "  • Max Position Size: ₹10,00,000"
echo "  • Max Daily Loss: ₹50,000"
echo "  • Stop Loss: 2%"
echo "  • Take Profit: 5%"
echo "  • Strategies: Straddle, Strangle, Iron Condor, Butterfly"
echo ""

# Start the trading system
print_trading "🎯 Starting NIFTY Options Trading Engine..."
print_trading "📈 Market Status: $market_status"
print_trading "🤖 AI Models: Strategy Selection, Volatility Prediction, Price Forecasting"
print_trading "🛡️  Risk Management: Active"
print_trading "📊 Dashboard: http://localhost:8050"
echo ""

# Create a trading session log
session_log="logs/trading_session_$(date +%Y%m%d_%H%M%S).log"
print_info "📝 Session log: $session_log"

# Function to handle cleanup on exit
cleanup() {
    print_warning "🛑 Shutting down trading system..."
    print_info "📊 Final session summary will be saved to $session_log"
    print_info "📈 Thank you for trading with NIFTY Options AI System!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the main trading system
print_success "🚀 Trading system started successfully!"
print_info "Press Ctrl+C to stop trading"
echo ""

# Run the trading system with enhanced output
python main.py live 2>&1 | tee -a "$session_log"
