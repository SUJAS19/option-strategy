#!/bin/bash

# NIFTY Options Trading Dashboard Startup Script
# Professional trading dashboard with real-time monitoring

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
    echo -e "${GREEN}[DASHBOARD]${NC} $1"
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

print_dashboard() {
    echo -e "${PURPLE}[DASHBOARD]${NC} $1"
}

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██████╗  █████╗ ███████╗██╗  ██╗██████╗  ██████╗ ██████╗  ║
║    ██╔══██╗██╔══██╗██╔════╝██║  ██║██╔══██╗██╔═══██╗██╔══██╗║
║    ██║  ██║███████║███████╗███████║██║  ██║██║   ██║██████╔╝║
║    ██║  ██║██╔══██║╚════██║██╔══██║██║  ██║██║   ██║██╔═══╝ ║
║    ██████╔╝██║  ██║███████║██║  ██║██████╔╝╚██████╔╝██║     ║
║    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ║
║                                                              ║
║              NIFTY OPTIONS TRADING DASHBOARD                 ║
║                    📊 Real-Time Monitoring 📊                ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "🚀 Starting NIFTY Options Trading Dashboard..."
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
print_info "📊 Dashboard Information:"
echo "  • Python Version: $(python --version)"
echo "  • Working Directory: $(pwd)"
echo "  • Virtual Environment: $(which python)"
echo "  • Dashboard Port: 8050"
echo ""

# Check if port 8050 is available
if lsof -Pi :8050 -sTCP:LISTEN -t >/dev/null 2>&1; then
    print_warning "⚠️  Port 8050 is already in use. Trying port 8051..."
    export DASHBOARD_PORT=8051
else
    export DASHBOARD_PORT=8050
fi

# Display dashboard features
print_info "🎯 Dashboard Features:"
echo "  • Real-time NIFTY spot price and volatility"
echo "  • Live portfolio performance and P&L"
echo "  • Interactive trading controls"
echo "  • Risk metrics and alerts"
echo "  • Strategy performance charts"
echo "  • Options chain data"
echo "  • Market indicators and analysis"
echo ""

# Start the dashboard
print_dashboard "🌐 Starting NIFTY Options Trading Dashboard..."
print_dashboard "📊 Dashboard URL: http://localhost:$DASHBOARD_PORT"
print_dashboard "🔄 Auto-refresh: Every 30 seconds"
print_dashboard "📱 Mobile-friendly interface"
echo ""

# Create a dashboard session log
session_log="logs/dashboard_session_$(date +%Y%m%d_%H%M%S).log"
print_info "📝 Dashboard log: $session_log"

# Function to handle cleanup on exit
cleanup() {
    print_warning "🛑 Shutting down dashboard..."
    print_info "📊 Dashboard session ended"
    print_info "📈 Thank you for using NIFTY Options Trading Dashboard!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Start the dashboard
print_success "🚀 Dashboard starting successfully!"
print_info "Press Ctrl+C to stop dashboard"
echo ""

# Run the dashboard with enhanced output
python dashboard.py 2>&1 | tee -a "$session_log"
