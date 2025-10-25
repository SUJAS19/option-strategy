"""
Main Application for NIFTY Options Algo Trading System
Entry point for the complete trading system
"""
import sys
import argparse
import logging
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from trading_engine import TradingEngine
from backtesting import BacktestEngine, BacktestAnalyzer
from data_fetcher import NIFTYDataFetcher
from ml_models import MLModelManager
import config

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )

def run_backtest():
    """Run backtesting on historical data"""
    print("=" * 60)
    print("NIFTY OPTIONS ALGO TRADING SYSTEM - BACKTESTING")
    print("=" * 60)
    
    try:
        # Initialize components
        data_fetcher = NIFTYDataFetcher()
        backtest_engine = BacktestEngine(initial_capital=1000000)
        analyzer = BacktestAnalyzer()
        
        # Get historical data
        print("Fetching historical data...")
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        
        historical_data = data_fetcher.get_historical_data("NIFTY 50", start_date, end_date)
        
        if historical_data.empty:
            print("No historical data available. Using synthetic data...")
            # Create synthetic data for demonstration
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)
            prices = 18000 + np.cumsum(np.random.randn(len(dates)) * 50)
            
            historical_data = pd.DataFrame({
                'Open': prices * 0.99,
                'High': prices * 1.02,
                'Low': prices * 0.98,
                'Close': prices,
                'Volume': np.random.randint(1000000, 5000000, len(dates))
            }, index=dates)
        
        print(f"Historical data shape: {historical_data.shape}")
        
        # Run backtest for different strategies
        strategies = ['straddle', 'strangle', 'iron_condor', 'butterfly']
        results = {}
        
        for strategy in strategies:
            print(f"\nRunning backtest for {strategy.upper()} strategy...")
            
            # Create new backtest engine for each strategy
            engine = BacktestEngine(initial_capital=1000000)
            result = engine.run_backtest(
                historical_data, 
                start_date, 
                end_date, 
                strategies=[strategy]
            )
            
            results[strategy] = result
            analyzer.add_result(result, strategy)
            
            # Generate report
            report = analyzer.generate_report(result, strategy)
            print(report)
        
        # Compare strategies
        print("\n" + "=" * 60)
        print("STRATEGY COMPARISON")
        print("=" * 60)
        comparison_df = analyzer.compare_strategies()
        print(comparison_df.to_string(index=False))
        
        # Plot equity curves
        print("\nGenerating equity curve plots...")
        for strategy in strategies:
            if hasattr(backtest_engine, 'equity_curve') and backtest_engine.equity_curve:
                analyzer.plot_equity_curve(backtest_engine.equity_curve, f"{strategy.upper()} Equity Curve")
        
        print("\nBacktesting completed successfully!")
        
    except Exception as e:
        print(f"Error in backtesting: {e}")
        logging.error(f"Backtesting error: {e}")

def run_live_trading():
    """Run live trading system"""
    print("=" * 60)
    print("NIFTY OPTIONS ALGO TRADING SYSTEM - LIVE TRADING")
    print("=" * 60)
    
    try:
        # Initialize trading engine
        trading_engine = TradingEngine()
        
        print("Starting live trading engine...")
        print("Press Ctrl+C to stop")
        
        # Start trading
        trading_engine.start()
        
    except KeyboardInterrupt:
        print("\nTrading stopped by user")
    except Exception as e:
        print(f"Error in live trading: {e}")
        logging.error(f"Live trading error: {e}")

def run_ml_training():
    """Train ML models"""
    print("=" * 60)
    print("NIFTY OPTIONS ALGO TRADING SYSTEM - ML TRAINING")
    print("=" * 60)
    
    try:
        # Initialize components
        data_fetcher = NIFTYDataFetcher()
        ml_manager = MLModelManager()
        
        # Get historical data for training
        print("Fetching historical data for ML training...")
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')  # 2 years
        
        historical_data = data_fetcher.get_historical_data("NIFTY 50", start_date, end_date)
        
        if historical_data.empty:
            print("No historical data available. Creating synthetic data...")
            # Create synthetic data for demonstration
            dates = pd.date_range(start=start_date, end=end_date, freq='D')
            np.random.seed(42)
            prices = 18000 + np.cumsum(np.random.randn(len(dates)) * 50)
            
            historical_data = pd.DataFrame({
                'Open': prices * 0.99,
                'High': prices * 1.02,
                'Low': prices * 0.98,
                'Close': prices,
                'Volume': np.random.randint(1000000, 5000000, len(dates))
            }, index=dates)
        
        print(f"Training data shape: {historical_data.shape}")
        
        # Create synthetic strategy performance data
        strategy_performance = {}
        for date in historical_data.index:
            # Simulate strategy performance based on market conditions
            volatility = historical_data.loc[date, 'Close'] * 0.01  # Simplified volatility
            performance = np.random.normal(0.001, volatility)  # Random performance
            strategy_performance[date] = performance
        
        # Train ML models
        print("Training ML models...")
        ml_manager.train_all_models(historical_data, strategy_performance)
        
        # Save models
        ml_manager.save_models('models.pkl')
        print("ML models trained and saved successfully!")
        
    except Exception as e:
        print(f"Error in ML training: {e}")
        logging.error(f"ML training error: {e}")

def run_data_analysis():
    """Run data analysis and visualization"""
    print("=" * 60)
    print("NIFTY OPTIONS ALGO TRADING SYSTEM - DATA ANALYSIS")
    print("=" * 60)
    
    try:
        # Initialize data fetcher
        data_fetcher = NIFTYDataFetcher()
        
        # Get current market data
        print("Fetching current market data...")
        market_indicators = data_fetcher.get_market_indicators()
        
        print("Current Market Indicators:")
        for key, value in market_indicators.items():
            print(f"  {key}: {value}")
        
        # Get options chain
        print("\nFetching options chain...")
        options_chain = data_fetcher.get_options_chain()
        
        if not options_chain.empty:
            print(f"Options chain shape: {options_chain.shape}")
            print("\nSample options data:")
            print(options_chain.head())
        else:
            print("No options chain data available")
        
        # Get volatility data
        print("\nFetching volatility data...")
        volatility_data = data_fetcher.get_volatility_data(30)
        
        if not volatility_data.empty:
            print(f"Volatility data shape: {volatility_data.shape}")
            print(f"Current volatility: {volatility_data['volatility'].iloc[-1]:.4f}")
            print(f"Average volatility: {volatility_data['volatility'].mean():.4f}")
        else:
            print("No volatility data available")
        
        print("\nData analysis completed!")
        
    except Exception as e:
        print(f"Error in data analysis: {e}")
        logging.error(f"Data analysis error: {e}")

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description='NIFTY Options Algo Trading System')
    parser.add_argument('mode', choices=['backtest', 'live', 'train', 'analyze'], 
                       help='Mode to run the application')
    parser.add_argument('--config', type=str, help='Configuration file path')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    print("NIFTY OPTIONS ALGORITHMIC TRADING SYSTEM")
    print("Advanced Options Trading with Machine Learning")
    print("=" * 60)
    
    if args.mode == 'backtest':
        run_backtest()
    elif args.mode == 'live':
        run_live_trading()
    elif args.mode == 'train':
        run_ml_training()
    elif args.mode == 'analyze':
        run_data_analysis()
    else:
        print("Invalid mode specified")
        sys.exit(1)

if __name__ == "__main__":
    main()
