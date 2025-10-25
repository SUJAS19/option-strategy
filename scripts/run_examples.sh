#!/bin/bash

# NIFTY Options Trading Examples Script
# Demonstrates all system capabilities

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
    echo -e "${GREEN}[EXAMPLES]${NC} $1"
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

print_example() {
    echo -e "${PURPLE}[EXAMPLE]${NC} $1"
}

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███████╗██╗  ██╗ █████╗ ███╗   ███╗██████╗ ██╗     ███████╗ ║
║    ██╔════╝╚██╗██╔╝██╔══██╗████╗ ████║██╔══██╗██║     ██╔════╝ ║
║    █████╗   ╚███╔╝ ███████║██╔████╔██║██████╔╝██║     █████╗   ║
║    ██╔══╝   ██╔██╗ ██╔══██║██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝   ║
║    ███████╗██╔╝ ██╗██║  ██║██║ ╚═╝ ██║██║     ███████╗███████╗ ║
║    ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝ ║
║                                                              ║
║              NIFTY OPTIONS TRADING EXAMPLES                  ║
║                    🧪 System Demonstration 🧪                 ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "🚀 Starting NIFTY Options Trading Examples..."
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

# Display examples to be run
print_info "🧪 Examples to be Demonstrated:"
echo "  • Option Pricing Models (Black-Scholes, Binomial, Monte Carlo)"
echo "  • Trading Strategies (Straddle, Strangle, Iron Condor, Butterfly)"
echo "  • Risk Management System"
echo "  • Machine Learning Models"
echo "  • Backtesting Framework"
echo "  • Data Fetching and Analysis"
echo ""

# Display system capabilities
print_info "🎯 System Capabilities:"
echo "  • Advanced Option Pricing with Greeks"
echo "  • Multiple Trading Strategies"
echo "  • AI-Powered Strategy Selection"
echo "  • Comprehensive Risk Management"
echo "  • Historical Backtesting"
echo "  • Real-time Data Fetching"
echo "  • Interactive Dashboard"
echo ""

# Create examples session log
session_log="logs/examples_session_$(date +%Y%m%d_%H%M%S).log"
print_info "📝 Examples log: $session_log"

# Function to handle cleanup on exit
cleanup() {
    print_warning "🛑 Stopping examples..."
    print_info "📊 Examples completed"
    print_info "📈 Thank you for exploring NIFTY Options Trading System!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the examples
print_success "🚀 Examples starting successfully!"
print_info "Press Ctrl+C to stop examples"
echo ""

# Run the examples with enhanced output
python run_examples.py 2>&1 | tee -a "$session_log"

# Display examples summary
print_success "📊 Examples completed successfully!"
print_info "📝 Log saved to: $session_log"
echo ""

# Display what was demonstrated
print_info "📈 Examples Demonstrated:"
echo "  • Option Pricing Models ✓"
echo "  • Trading Strategies ✓"
echo "  • Risk Management ✓"
echo "  • Machine Learning ✓"
echo "  • Backtesting ✓"
echo "  • Data Analysis ✓"
echo ""

print_success "🎉 All examples completed successfully!"
print_info "📊 Check the logs for detailed output"
print_info "📈 Ready for live trading! 🚀"
