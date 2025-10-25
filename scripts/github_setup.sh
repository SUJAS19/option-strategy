#!/bin/bash

# GitHub Repository Setup Script for NIFTY Options Trading System
# This script sets up the complete GitHub repository with all necessary files

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
    echo -e "${GREEN}[GITHUB]${NC} $1"
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

print_github() {
    echo -e "${PURPLE}[GITHUB]${NC} $1"
}

# ASCII Art Banner
echo -e "${CYAN}"
cat << "EOF"
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗██████╗              ║
║    ██╔══██╗██║╚══██╔══╝██║  ██║██║   ██║██╔══██╗             ║
║    ██████╔╝██║   ██║   ███████║██║   ██║██████╔╝             ║
║    ██╔══██╗██║   ██║   ██╔══██║██║   ██║██╔══██╗             ║
║    ██████╔╝██║   ██║   ██║  ██║╚██████╔╝██████╔╝             ║
║    ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝              ║
║                                                              ║
║              NIFTY OPTIONS TRADING SYSTEM                    ║
║                    🚀 GitHub Repository Setup 🚀             ║
╚══════════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

print_info "🚀 Setting up NIFTY Options Trading System for GitHub..."
print_info "📅 Date: $(date)"
print_info "🕐 Time: $(date +%H:%M:%S)"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    print_error "Git is not installed. Please install Git first."
    exit 1
fi

print_status "Git is available ✓"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
else
    print_status "Git repository already exists ✓"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    print_status "Creating .gitignore file..."
    # .gitignore content is already created above
    print_success ".gitignore created"
else
    print_status ".gitignore already exists ✓"
fi

# Set up Git configuration
print_status "Setting up Git configuration..."
git config user.name "NIFTY Options Trading System" || true
git config user.email "trading@niftyoptions.com" || true

# Add all files to Git
print_status "Adding files to Git repository..."
git add .

# Create initial commit
print_status "Creating initial commit..."
git commit -m "Initial commit: NIFTY Options Trading System

🚀 Complete algorithmic trading system for NIFTY options
📈 Features:
- Advanced option pricing models (Black-Scholes, Binomial, Monte Carlo)
- Multiple trading strategies (Straddle, Strangle, Iron Condor, Butterfly)
- Machine learning integration (Strategy selection, Volatility prediction)
- Comprehensive risk management system
- Historical backtesting framework
- Real-time trading engine
- Interactive web dashboard
- Docker support
- CI/CD pipeline

🤖 AI-Powered Trading with Python, Machine Learning, and Data Science
📊 Professional-grade system for current NIFTY options trading"

print_success "Initial commit created"

# Create GitHub repository setup instructions
print_status "Creating GitHub setup instructions..."

cat > GITHUB_SETUP.md << 'EOF'
# GitHub Repository Setup Instructions

## 🚀 Quick Start

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository"
3. Repository name: `nifty-options-trading`
4. Description: `Advanced Algorithmic Trading System for NIFTY Options with Machine Learning`
5. Make it Public
6. Don't initialize with README (we already have one)
7. Click "Create repository"

### 2. Connect Local Repository to GitHub
```bash
# Add remote origin (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Set Up GitHub Actions
The repository includes GitHub Actions for:
- Continuous Integration (CI)
- Automated testing
- Code quality checks
- Security scanning
- Docker builds

### 4. Configure Repository Settings
1. Go to repository Settings
2. Enable Issues and Discussions
3. Set up branch protection rules
4. Configure security alerts
5. Set up GitHub Pages (optional)

## 📋 Repository Structure

```
nifty-options-trading/
├── 📁 .github/
│   └── 📁 workflows/
│       └── ci.yml
├── 📁 scripts/
│   ├── setup.sh
│   ├── run_trading.sh
│   ├── run_dashboard.sh
│   ├── run_backtest.sh
│   └── run_examples.sh
├── 📁 tests/
│   └── test_trading_system.py
├── 📄 main.py
├── 📄 dashboard.py
├── 📄 requirements.txt
├── 📄 Dockerfile
├── 📄 docker-compose.yml
├── 📄 Makefile
├── 📄 README.md
├── 📄 LICENSE
└── 📄 CONTRIBUTING.md
```

## 🔧 Development Workflow

### 1. Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/nifty-options-trading.git
cd nifty-options-trading
```

### 2. Set Up Development Environment
```bash
# Make setup script executable
chmod +x scripts/setup.sh

# Run setup
./scripts/setup.sh
```

### 3. Run Examples
```bash
# Make examples script executable
chmod +x scripts/run_examples.sh

# Run examples
./scripts/run_examples.sh
```

### 4. Start Trading System
```bash
# Make trading script executable
chmod +x scripts/run_trading.sh

# Start live trading
./scripts/run_trading.sh
```

### 5. Start Dashboard
```bash
# Make dashboard script executable
chmod +x scripts/run_dashboard.sh

# Start dashboard
./scripts/run_dashboard.sh
```

## 🐳 Docker Support

### Build and Run with Docker
```bash
# Build Docker image
docker build -t nifty-options-trading .

# Run with Docker Compose
docker-compose up -d
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
make test

# Run specific test
python -m pytest tests/test_trading_system.py -v
```

### Code Quality
```bash
# Run linting
make lint

# Format code
make format
```

## 📊 Monitoring

### GitHub Actions
- Automated testing on every push
- Code quality checks
- Security scanning
- Docker builds

### Repository Insights
- Code frequency
- Contributors
- Traffic
- Community health

## 🔒 Security

### Repository Security
- Enable security alerts
- Set up branch protection
- Require pull request reviews
- Enable dependency scanning

### API Keys
- Never commit API keys
- Use GitHub Secrets for sensitive data
- Use environment variables

## 📈 Performance

### Repository Optimization
- Use .gitignore for large files
- Compress images
- Optimize Docker images
- Use GitHub LFS for large files

## 🎯 Best Practices

### Git Workflow
1. Create feature branches
2. Make small, focused commits
3. Write descriptive commit messages
4. Use pull requests for changes
5. Keep main branch stable

### Code Quality
1. Write tests for new features
2. Follow coding standards
3. Document your code
4. Review code before merging
5. Keep dependencies updated

## 🚀 Deployment

### GitHub Pages
- Enable GitHub Pages
- Deploy dashboard automatically
- Use custom domain (optional)

### Docker Hub
- Build and push Docker images
- Use GitHub Actions for automation
- Tag releases properly

## 📞 Support

### Getting Help
- Check GitHub Issues
- Read documentation
- Ask questions in Discussions
- Contact maintainers

### Contributing
- Fork the repository
- Create feature branches
- Submit pull requests
- Follow contribution guidelines

## 🎉 Success!

Your NIFTY Options Trading System is now ready for GitHub! 🚀📈
EOF

print_success "GitHub setup instructions created"

# Create GitHub repository creation script
print_status "Creating GitHub repository creation script..."

cat > create_github_repo.sh << 'EOF'
#!/bin/bash

# GitHub Repository Creation Script
# This script helps create the GitHub repository

set -e

echo "🚀 Creating GitHub Repository for NIFTY Options Trading System..."

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI found"
    
    # Create repository using GitHub CLI
    gh repo create nifty-options-trading \
        --public \
        --description "Advanced Algorithmic Trading System for NIFTY Options with Machine Learning" \
        --source=. \
        --remote=origin \
        --push
    
    echo "🎉 Repository created successfully!"
    echo "📊 Repository URL: https://github.com/$(gh api user --jq .login)/nifty-options-trading"
    
else
    echo "❌ GitHub CLI not found"
    echo "📋 Please create the repository manually:"
    echo "1. Go to https://github.com/new"
    echo "2. Repository name: nifty-options-trading"
    echo "3. Description: Advanced Algorithmic Trading System for NIFTY Options with Machine Learning"
    echo "4. Make it Public"
    echo "5. Don't initialize with README"
    echo "6. Click Create repository"
    echo ""
    echo "Then run:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git"
    echo "git branch -M main"
    echo "git push -u origin main"
fi
EOF

chmod +x create_github_repo.sh

print_success "GitHub repository creation script created"

# Create deployment script
print_status "Creating deployment script..."

cat > deploy.sh << 'EOF'
#!/bin/bash

# Deployment Script for NIFTY Options Trading System
# This script deploys the system to production

set -e

echo "🚀 Deploying NIFTY Options Trading System..."

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
    
    # Build Docker image
    echo "📦 Building Docker image..."
    docker build -t nifty-options-trading .
    
    # Run with Docker Compose
    echo "🐳 Starting services..."
    docker-compose up -d
    
    echo "🎉 Deployment completed successfully!"
    echo "📊 Dashboard: http://localhost:8050"
    echo "📈 Trading System: Running in background"
    
else
    echo "❌ Docker not found"
    echo "📋 Please install Docker and Docker Compose"
    echo "Then run: docker-compose up -d"
fi
EOF

chmod +x deploy.sh

print_success "Deployment script created"

# Create release script
print_status "Creating release script..."

cat > release.sh << 'EOF'
#!/bin/bash

# Release Script for NIFTY Options Trading System
# This script creates a new release

set -e

echo "🚀 Creating Release for NIFTY Options Trading System..."

# Get current version
VERSION=$(python -c "import setup; print(setup.__version__)" 2>/dev/null || echo "1.0.0")

echo "📦 Current version: $VERSION"

# Create release notes
cat > RELEASE_NOTES.md << 'EOL'
# Release Notes - Version $VERSION

## 🚀 New Features
- Advanced option pricing models
- Multiple trading strategies
- Machine learning integration
- Comprehensive risk management
- Historical backtesting
- Real-time trading engine
- Interactive dashboard
- Docker support

## 🐛 Bug Fixes
- Fixed option pricing calculations
- Improved risk management
- Enhanced error handling
- Updated documentation

## 📈 Performance Improvements
- Optimized data processing
- Improved ML model accuracy
- Enhanced backtesting speed
- Better memory usage

## 🔧 Technical Changes
- Updated dependencies
- Improved code structure
- Enhanced testing
- Better logging

## 📚 Documentation
- Updated README
- Added examples
- Improved API documentation
- Added contribution guidelines
EOL

echo "📝 Release notes created"

# Create tag
echo "🏷️  Creating tag v$VERSION..."
git tag -a "v$VERSION" -m "Release version $VERSION"

# Push tag
echo "📤 Pushing tag..."
git push origin "v$VERSION"

echo "🎉 Release v$VERSION created successfully!"
echo "📊 Release URL: https://github.com/YOUR_USERNAME/nifty-options-trading/releases/tag/v$VERSION"
EOF

chmod +x release.sh

print_success "Release script created"

# Display final instructions
print_success "🎉 GitHub setup completed successfully!"
echo ""
print_info "📋 Next Steps:"
echo "1. Create GitHub repository:"
echo "   - Go to https://github.com/new"
echo "   - Repository name: nifty-options-trading"
echo "   - Description: Advanced Algorithmic Trading System for NIFTY Options with Machine Learning"
echo "   - Make it Public"
echo "   - Don't initialize with README"
echo "   - Click Create repository"
echo ""
echo "2. Connect local repository:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/nifty-options-trading.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "3. Set up GitHub Actions:"
echo "   - Go to repository Settings"
echo "   - Enable Issues and Discussions"
echo "   - Set up branch protection rules"
echo "   - Configure security alerts"
echo ""
print_info "📁 Files created:"
echo "  • GITHUB_SETUP.md - Detailed setup instructions"
echo "  • create_github_repo.sh - Automated repository creation"
echo "  • deploy.sh - Deployment script"
echo "  • release.sh - Release creation script"
echo ""
print_info "🔧 Available commands:"
echo "  • ./create_github_repo.sh - Create GitHub repository"
echo "  • ./deploy.sh - Deploy system"
echo "  • ./release.sh - Create release"
echo ""
print_success "🚀 Your NIFTY Options Trading System is ready for GitHub! 📈🎉"
