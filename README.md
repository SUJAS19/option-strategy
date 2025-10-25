# NIFTY Options Algorithmic Trading System

A comprehensive algorithmic trading system for NIFTY options strategies using Python, Machine Learning, and Data Science.

## 🚀 Features

### Core Components
- **Advanced Option Pricing Models**: Black-Scholes, Binomial, Monte Carlo
- **Multiple Trading Strategies**: Straddle, Strangle, Iron Condor, Butterfly
- **Machine Learning Integration**: Strategy selection, volatility prediction, price forecasting
- **Risk Management**: Comprehensive risk controls and position sizing
- **Backtesting Framework**: Historical strategy performance analysis
- **Live Trading Engine**: Real-time trading with automated execution
- **Interactive Dashboard**: Web-based monitoring and control interface

### Trading Strategies Implemented
1. **Long Straddle**: Profits from high volatility moves in either direction
2. **Long Strangle**: Similar to straddle but with different strike prices
3. **Iron Condor**: Limited profit, limited risk strategy for low volatility
4. **Long Butterfly**: Limited profit strategy for specific price ranges

### Machine Learning Models
- **Strategy Selector**: XGBoost-based model for optimal strategy selection
- **Volatility Predictor**: LightGBM model for volatility forecasting
- **Price Predictor**: Random Forest model for price prediction

## 📋 Requirements

### Python Dependencies
```
numpy==1.24.3
pandas==2.0.3
scipy==1.11.1
scikit-learn==1.3.0
yfinance==0.2.18
plotly==5.15.0
dash==2.11.1
dash-bootstrap-components==1.4.1
requests==2.31.0
beautifulsoup4==4.12.2
nsepy==0.8.0
ta==0.10.2
matplotlib==3.7.2
seaborn==0.12.2
xgboost==1.7.6
lightgbm==4.0.0
optuna==3.2.0
joblib==1.3.2
python-dotenv==1.0.0
schedule==1.2.0
websocket-client==1.6.1
ccxt==4.0.77
```

## 🛠️ Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd option-strategy
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Create .env file
ZERODHA_API_KEY=your_api_key
ZERODHA_ACCESS_TOKEN=your_access_token
ZERODHA_USER_ID=your_user_id
ZERODHA_PASSWORD=your_password
ZERODHA_TOTP_SECRET=your_totp_secret
```

## 🚀 Usage

### 1. Backtesting
Run historical backtesting to evaluate strategy performance:
```bash
python main.py backtest
```

### 2. Live Trading
Start the live trading engine:
```bash
python main.py live
```

### 3. ML Model Training
Train machine learning models:
```bash
python main.py train
```

### 4. Data Analysis
Run data analysis and visualization:
```bash
python main.py analyze
```

### 5. Interactive Dashboard
Launch the web-based dashboard:
```bash
python dashboard.py
```
Access at: http://localhost:8050

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Data Fetcher  │    │  Option Pricing │    │ ML Models       │
│   - NSE API     │    │  - Black-Scholes│    │ - Strategy Sel.  │
│   - Real-time   │    │  - Binomial     │    │ - Vol Prediction│
│   - Historical  │    │  - Monte Carlo  │    │ - Price Forecast│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Trading Engine  │
                    │ - Strategy Exec │
                    │ - Risk Mgmt     │
                    │ - Position Mgmt │
                    └─────────────────┘
                                 │
                    ┌─────────────────┐
                    │   Dashboard     │
                    │ - Real-time    │
                    │ - Controls      │
                    │ - Analytics     │
                    └─────────────────┘
```

## 📈 Strategy Performance

### Backtesting Results
The system provides comprehensive backtesting with metrics:
- **Total Return**: Overall strategy performance
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades
- **Profit Factor**: Ratio of gross profit to gross loss

### Risk Management
- **Position Sizing**: Kelly Criterion-based sizing
- **Stop Loss**: Automated stop-loss implementation
- **Risk Limits**: Portfolio-level risk controls
- **Greeks Management**: Delta, Gamma, Theta, Vega monitoring

## 🔧 Configuration

### Trading Parameters
```python
# config.py
MAX_POSITION_SIZE = 1000000  # Maximum position size in INR
MAX_DAILY_LOSS = 50000      # Maximum daily loss in INR
STOP_LOSS_PERCENTAGE = 0.02  # 2% stop loss
TAKE_PROFIT_PERCENTAGE = 0.05  # 5% take profit
```

### Strategy Parameters
```python
STRATEGIES = {
    'STRADDLE': {
        'enabled': True,
        'min_iv': 0.15,
        'max_iv': 0.50,
        'min_dte': 7,
        'max_dte': 30
    },
    # ... other strategies
}
```

## 📊 Dashboard Features

### Real-time Monitoring
- **Market Data**: Live NIFTY spot price and volatility
- **Portfolio Status**: Current positions and P&L
- **Risk Metrics**: Real-time risk exposure
- **Performance Charts**: Equity curve and drawdown

### Trading Controls
- **Strategy Selection**: Choose from available strategies
- **Position Sizing**: Adjust position sizes
- **Start/Stop Trading**: Control trading engine
- **Risk Alerts**: Monitor risk breaches

## 🧪 Testing

### Backtesting
```python
# Run comprehensive backtest
backtest_engine = BacktestEngine(initial_capital=1000000)
result = backtest_engine.run_backtest(
    historical_data, 
    start_date, 
    end_date, 
    strategies=['straddle', 'strangle']
)
```

### Risk Testing
```python
# Test risk management
risk_manager = RiskManager()
alerts = risk_manager.check_risk_limits(current_prices)
```

## 📚 Documentation

### Key Classes
- **TradingEngine**: Main trading coordinator
- **OptionPricingEngine**: Option pricing calculations
- **StrategySelector**: Strategy selection logic
- **RiskManager**: Risk management system
- **BacktestEngine**: Historical testing framework
- **MLModelManager**: Machine learning models

### API Reference
Detailed API documentation is available in the docstrings of each module.

## ⚠️ Risk Disclaimer

This software is for educational and research purposes only. Options trading involves substantial risk and is not suitable for all investors. Past performance does not guarantee future results. Always consult with a financial advisor before making investment decisions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## 🔄 Updates

### Version 1.0.0
- Initial release with core trading strategies
- Basic ML integration
- Risk management system
- Backtesting framework
- Interactive dashboard

---

**Happy Trading! 📈**
