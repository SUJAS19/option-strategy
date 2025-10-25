# NIFTY Options Trading System Makefile
# Professional development and deployment commands

.PHONY: help install setup test lint format clean run-trading run-dashboard run-backtest run-examples docker-build docker-run docker-stop

# Default target
help:
	@echo "🚀 NIFTY Options Trading System - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "📦 Setup & Installation:"
	@echo "  make install     - Install dependencies"
	@echo "  make setup       - Complete system setup"
	@echo "  make test        - Run tests"
	@echo "  make lint        - Run linting"
	@echo "  make format      - Format code"
	@echo ""
	@echo "🚀 Trading Commands:"
	@echo "  make run-trading    - Start live trading"
	@echo "  make run-dashboard  - Start web dashboard"
	@echo "  make run-backtest   - Run backtesting"
	@echo "  make run-examples   - Run examples"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run with Docker"
	@echo "  make docker-stop   - Stop Docker containers"
	@echo ""
	@echo "🧹 Maintenance:"
	@echo "  make clean         - Clean up files"
	@echo "  make logs          - View logs"
	@echo "  make status        - Check system status"

# Installation and setup
install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

setup:
	@echo "🚀 Setting up NIFTY Options Trading System..."
	chmod +x scripts/setup.sh
	./scripts/setup.sh

# Testing and quality
test:
	@echo "🧪 Running tests..."
	python -m pytest tests/ -v --cov=. --cov-report=html

lint:
	@echo "🔍 Running linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .
	mypy . --ignore-missing-imports

format:
	@echo "✨ Formatting code..."
	black .
	isort .

# Trading commands
run-trading:
	@echo "📈 Starting live trading..."
	chmod +x scripts/run_trading.sh
	./scripts/run_trading.sh

run-dashboard:
	@echo "📊 Starting dashboard..."
	chmod +x scripts/run_dashboard.sh
	./scripts/run_dashboard.sh

run-backtest:
	@echo "📈 Running backtest..."
	chmod +x scripts/run_backtest.sh
	./scripts/run_backtest.sh

run-examples:
	@echo "🧪 Running examples..."
	chmod +x scripts/run_examples.sh
	./scripts/run_examples.sh

# Docker commands
docker-build:
	@echo "🐳 Building Docker image..."
	docker build -t nifty-options-trading .

docker-run:
	@echo "🐳 Running with Docker..."
	docker-compose up -d

docker-stop:
	@echo "🛑 Stopping Docker containers..."
	docker-compose down

# Maintenance
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/

logs:
	@echo "📝 Viewing logs..."
	tail -f logs/trading.log

status:
	@echo "📊 System Status:"
	@echo "  Python: $(shell python --version)"
	@echo "  Virtual Env: $(shell which python)"
	@echo "  Working Dir: $(shell pwd)"
	@echo "  Logs: $(shell ls -la logs/ | wc -l) files"
	@echo "  Data: $(shell ls -la data/ | wc -l) files"

# Development commands
dev-install:
	@echo "🔧 Installing development dependencies..."
	pip install -r requirements.txt
	pip install pytest pytest-cov black flake8 mypy

dev-test:
	@echo "🧪 Running development tests..."
	python -m pytest tests/ -v --cov=. --cov-report=html --cov-report=term

dev-lint:
	@echo "🔍 Running development linting..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	black --check .
	mypy . --ignore-missing-imports

# Quick start
quick-start: install setup
	@echo "🚀 Quick start completed!"
	@echo "Run 'make run-examples' to see the system in action"

# Production deployment
deploy:
	@echo "🚀 Deploying to production..."
	docker-compose -f docker-compose.yml up -d --build

# Backup
backup:
	@echo "💾 Creating backup..."
	tar -czf backup_$(shell date +%Y%m%d_%H%M%S).tar.gz data/ logs/ models/ *.py

# Update
update:
	@echo "🔄 Updating system..."
	git pull origin main
	make install
	make setup
