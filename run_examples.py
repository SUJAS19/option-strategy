"""
Example Usage Scripts for NIFTY Options Trading System
Demonstrates various features and capabilities
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Import system components
from data_fetcher import NIFTYDataFetcher
from option_pricing import OptionParams, OptionPricingEngine
from option_strategies import StrategySelector, StrategyParams
from ml_models import MLModelManager
from risk_management import RiskManager, Position
from backtesting import BacktestEngine, BacktestAnalyzer
from trading_engine import TradingEngine

def example_option_pricing():
    """Example: Option pricing calculations"""
    print("=" * 60)
    print("OPTION PRICING EXAMPLE")
    print("=" * 60)
    
    # Create option parameters
    params = OptionParams(
        spot_price=18000,
        strike_price=18000,
        time_to_expiry=30/365,  # 30 days
        risk_free_rate=0.05,
        volatility=0.25
    )
    
    # Initialize pricing engine
    pricing_engine = OptionPricingEngine()
    
    # Price call option
    call_result = pricing_engine.price_option(params, 'call')
    print(f"Call Option Price: ₹{call_result['price']:.2f}")
    print(f"Call Option Greeks: {call_result['greeks']}")
    
    # Price put option
    put_result = pricing_engine.price_option(params, 'put')
    print(f"Put Option Price: ₹{put_result['price']:.2f}")
    print(f"Put Option Greeks: {put_result['greeks']}")
    
    # Calculate implied volatility
    market_price = 150.0
    iv = pricing_engine.bs_pricer.implied_volatility(market_price, params, 'call')
    print(f"Implied Volatility: {iv:.2%}")

def example_strategy_analysis():
    """Example: Strategy analysis"""
    print("\n" + "=" * 60)
    print("STRATEGY ANALYSIS EXAMPLE")
    print("=" * 60)
    
    # Initialize strategy selector
    strategy_selector = StrategySelector()
    
    # Create strategy parameters
    strategy_params = StrategyParams(
        spot_price=18000,
        strike_prices=[18000, 18100, 17900],
        expiry_dates=['2024-01-25'],
        option_prices={'call': 150, 'put': 120},
        quantities={'call': 1, 'put': 1},
        risk_free_rate=0.05,
        volatility=0.25
    )
    
    # Analyze straddle strategy
    straddle = strategy_selector.get_strategy('straddle')
    payoff = straddle.calculate_payoff(18500, strategy_params)
    greeks = straddle.calculate_greeks(strategy_params)
    breakeven = straddle.calculate_breakeven(strategy_params)
    
    print(f"Straddle Payoff at ₹18,500: ₹{payoff:.2f}")
    print(f"Straddle Greeks: {greeks}")
    print(f"Breakeven Points: ₹{breakeven[0]:.2f}, ₹{breakeven[1]:.2f}")

def example_risk_management():
    """Example: Risk management"""
    print("\n" + "=" * 60)
    print("RISK MANAGEMENT EXAMPLE")
    print("=" * 60)
    
    # Initialize risk manager
    risk_manager = RiskManager()
    
    # Create sample positions
    position1 = Position(
        symbol="NIFTY18000CE",
        option_type='call',
        strike_price=18000,
        expiry_date='2024-01-25',
        quantity=10,
        entry_price=150.0,
        current_price=200.0,
        entry_time=datetime.now(),
        strategy_name='straddle'
    )
    
    position2 = Position(
        symbol="NIFTY18000PE",
        option_type='put',
        strike_price=18000,
        expiry_date='2024-01-25',
        quantity=10,
        entry_price=120.0,
        current_price=80.0,
        entry_time=datetime.now(),
        strategy_name='straddle'
    )
    
    # Add positions
    risk_manager.add_position(position1)
    risk_manager.add_position(position2)
    
    # Check risk limits
    current_prices = {"NIFTY18000CE": 200.0, "NIFTY18000PE": 80.0}
    alerts = risk_manager.check_risk_limits(current_prices)
    
    print(f"Risk Alerts: {len(alerts)}")
    for alert in alerts:
        print(f"  - {alert['type']}: {alert['message']}")
    
    # Calculate portfolio metrics
    metrics = risk_manager.calculate_portfolio_metrics(current_prices)
    print(f"Portfolio Value: ₹{metrics.portfolio_value:,.2f}")
    print(f"Total Delta: {metrics.total_delta:.2f}")
    print(f"Total Gamma: {metrics.total_gamma:.2f}")

def example_ml_predictions():
    """Example: Machine learning predictions"""
    print("\n" + "=" * 60)
    print("MACHINE LEARNING EXAMPLE")
    print("=" * 60)
    
    # Initialize ML manager
    ml_manager = MLModelManager()
    
    # Create sample market data
    market_data = {
        'spot_price': 18000,
        'volatility': 0.25,
        'trend': 0.1,
        'volume_ratio': 1.2,
        'rsi': 55,
        'macd': 0.05
    }
    
    # Get predictions
    predictions = ml_manager.get_predictions(market_data, 18000)
    
    print(f"Predicted Volatility: {predictions['volatility']:.2%}")
    print(f"Predicted Price: ₹{predictions['price']:,.0f}")
    print(f"Recommended Strategy: {predictions['strategy']}")

def example_backtesting():
    """Example: Backtesting"""
    print("\n" + "=" * 60)
    print("BACKTESTING EXAMPLE")
    print("=" * 60)
    
    # Create sample historical data
    dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
    np.random.seed(42)
    prices = 18000 + np.cumsum(np.random.randn(len(dates)) * 50)
    
    historical_data = pd.DataFrame({
        'Open': prices * 0.99,
        'High': prices * 1.02,
        'Low': prices * 0.98,
        'Close': prices,
        'Volume': np.random.randint(1000000, 5000000, len(dates))
    }, index=dates)
    
    # Initialize backtest engine
    backtest_engine = BacktestEngine(initial_capital=1000000)
    
    # Run backtest
    result = backtest_engine.run_backtest(
        historical_data,
        '2023-01-01',
        '2023-12-31',
        strategies=['straddle']
    )
    
    print(f"Total Return: {result.total_return:.2%}")
    print(f"Sharpe Ratio: {result.sharpe_ratio:.2f}")
    print(f"Max Drawdown: {result.max_drawdown:.2%}")
    print(f"Win Rate: {result.win_rate:.2%}")

def example_data_fetching():
    """Example: Data fetching"""
    print("\n" + "=" * 60)
    print("DATA FETCHING EXAMPLE")
    print("=" * 60)
    
    # Initialize data fetcher
    data_fetcher = NIFTYDataFetcher()
    
    # Get market indicators
    market_indicators = data_fetcher.get_market_indicators()
    print("Market Indicators:")
    for key, value in market_indicators.items():
        print(f"  {key}: {value}")
    
    # Get options chain
    options_chain = data_fetcher.get_options_chain()
    if not options_chain.empty:
        print(f"\nOptions Chain Shape: {options_chain.shape}")
        print("Sample Options Data:")
        print(options_chain.head())
    else:
        print("No options chain data available")

def main():
    """Run all examples"""
    print("NIFTY OPTIONS TRADING SYSTEM - EXAMPLES")
    print("=" * 60)
    
    try:
        # Run examples
        example_option_pricing()
        example_strategy_analysis()
        example_risk_management()
        example_ml_predictions()
        example_backtesting()
        example_data_fetching()
        
        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
