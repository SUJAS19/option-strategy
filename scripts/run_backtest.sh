#!/bin/bash

# NIFTY Options Trading Backtest Script
# Comprehensive backtesting with professional analysis

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
    echo -e "${GREEN}[BACKTEST]${NC} $1"
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

print_backtest() {
    echo -e "${PURPLE}[BACKTEST]${NC} $1"
}

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██████╗  █████╗  ██████╗██╗  ██╗███████╗████████╗███████╗ ║
║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔════╝╚══██╔══╝██╔════╝ ║
║    ██████╔╝███████║██║     ███████║█████╗     ██║   █████╗   ║
║    ██╔══██╗██╔══██║██║     ██╔══██║██╔══╝     ██║   ██╔══╝   ║
║    ██████╔╝██║  ██║╚██████╗██║  ██║███████╗   ██║   ███████╗ ║
║    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝ ║
║                                                              ║
║              NIFTY OPTIONS TRADING BACKTEST                  ║
║                    📈 Historical Analysis 📈                 ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "🚀 Starting NIFTY Options Trading Backtest..."
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

# Display backtest configuration
print_info "📊 Backtest Configuration:"
echo "  • Initial Capital: ₹10,00,000"
echo "  • Test Period: 1 Year (365 days)"
echo "  • Strategies: Straddle, Strangle, Iron Condor, Butterfly"
echo "  • Risk Management: Active"
echo "  • ML Models: Strategy Selection, Volatility Prediction"
echo ""

# Display strategies to be tested
print_info "🎯 Strategies to be Tested:"
echo "  • Long Straddle - High volatility strategy"
echo "  • Long Strangle - Similar to straddle with different strikes"
echo "  • Iron Condor - Low volatility, limited risk strategy"
echo "  • Long Butterfly - Range-bound strategy"
echo ""

# Create backtest results directory
backtest_dir="backtest_results/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backtest_dir"

print_backtest "📈 Starting comprehensive backtest analysis..."
print_backtest "📊 Results will be saved to: $backtest_dir"
echo ""

# Create a backtest session log
session_log="logs/backtest_session_$(date +%Y%m%d_%H%M%S).log"
print_info "📝 Backtest log: $session_log"

# Function to handle cleanup on exit
cleanup() {
    print_warning "🛑 Stopping backtest..."
    print_info "📊 Backtest results saved to: $backtest_dir"
    print_info "📈 Thank you for using NIFTY Options Backtest System!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the backtest
print_success "🚀 Backtest starting successfully!"
print_info "Press Ctrl+C to stop backtest"
echo ""

# Run the backtest with enhanced output
python main.py backtest 2>&1 | tee -a "$session_log"

# Move results to backtest directory
if [ -f "backtest_results/*.csv" ]; then
    mv backtest_results/*.csv "$backtest_dir/"
fi

if [ -f "backtest_results/*.png" ]; then
    mv backtest_results/*.png "$backtest_dir/"
fi

if [ -f "backtest_results/*.html" ]; then
    mv backtest_results/*.html "$backtest_dir/"
fi

# Generate backtest summary
print_success "📊 Backtest completed successfully!"
print_info "📁 Results saved to: $backtest_dir"
print_info "📝 Log saved to: $session_log"
echo ""

# Display summary
print_info "📈 Backtest Summary:"
echo "  • Test Period: 1 Year"
echo "  • Strategies Tested: 4"
echo "  • Results Directory: $backtest_dir"
echo "  • Log File: $session_log"
echo ""

print_success "🎉 Backtest analysis complete!"
print_info "📊 Check the results directory for detailed analysis"
print_info "📈 Happy Trading! 🚀"
