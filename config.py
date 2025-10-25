"""
Configuration file for NIFTY Options Algo Trading System
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
NSE_API_BASE = "https://www.nseindia.com/api"
ZERODHA_API_BASE = "https://api.kite.trade"

# Trading Configuration
SYMBOL = "NIFTY"
EXCHANGE = "NSE"
LOT_SIZE = 50
MARGIN_MULTIPLIER = 1.2

# Risk Management
MAX_POSITION_SIZE = 1000000  # Maximum position size in INR
MAX_DAILY_LOSS = 50000  # Maximum daily loss in INR
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.05  # 5% take profit

# Strategy Parameters
STRATEGIES = {
    'STRADDLE': {
        'enabled': True,
        'min_iv': 0.15,
        'max_iv': 0.50,
        'min_dte': 7,
        'max_dte': 30
    },
    'STRANGLE': {
        'enabled': True,
        'delta_range': (0.2, 0.3),
        'min_dte': 7,
        'max_dte': 30
    },
    'IRON_CONDOR': {
        'enabled': True,
        'wing_width': 100,
        'min_dte': 7,
        'max_dte': 30
    },
    'BUTTERFLY': {
        'enabled': True,
        'wing_width': 50,
        'min_dte': 7,
        'max_dte': 30
    }
}

# Machine Learning Configuration
ML_MODELS = {
    'strategy_selector': 'xgboost',
    'volatility_predictor': 'lightgbm',
    'price_predictor': 'random_forest'
}

# Data Configuration
DATA_SOURCES = {
    'primary': 'nsepy',
    'backup': 'yfinance'
}

# Logging Configuration
LOG_LEVEL = 'INFO'
LOG_FILE = 'trading.log'

# Database Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///trading.db')

# Environment Variables
ZERODHA_API_KEY = os.getenv('ZERODHA_API_KEY')
ZERODHA_ACCESS_TOKEN = os.getenv('ZERODHA_ACCESS_TOKEN')
ZERODHA_USER_ID = os.getenv('ZERODHA_USER_ID')
ZERODHA_PASSWORD = os.getenv('ZERODHA_PASSWORD')
ZERODHA_TOTP_SECRET = os.getenv('ZERODHA_TOTP_SECRET')
