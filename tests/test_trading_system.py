"""
Test suite for NIFTY Options Trading System
Comprehensive testing of all components
"""
import unittest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from option_pricing import OptionParams, OptionPricingEngine, BlackScholesPricer
from option_strategies import StrategySelector, StraddleStrategy, StrategyParams
from risk_management import RiskManager, Position
from data_fetcher import NIFTYDataFetcher
from ml_models import MLModelManager

class TestOptionPricing(unittest.TestCase):
    """Test option pricing models"""
    
    def setUp(self):
        self.params = OptionParams(
            spot_price=18000,
            strike_price=18000,
            time_to_expiry=30/365,
            risk_free_rate=0.05,
            volatility=0.25
        )
        self.pricing_engine = OptionPricingEngine()
    
    def test_black_scholes_call(self):
        """Test Black-Scholes call option pricing"""
        result = self.pricing_engine.price_option(self.params, 'call')
        self.assertIsInstance(result['price'], float)
        self.assertGreater(result['price'], 0)
        self.assertIn('greeks', result)
    
    def test_black_scholes_put(self):
        """Test Black-Scholes put option pricing"""
        result = self.pricing_engine.price_option(self.params, 'put')
        self.assertIsInstance(result['price'], float)
        self.assertGreater(result['price'], 0)
        self.assertIn('greeks', result)
    
    def test_greeks_calculation(self):
        """Test Greeks calculation"""
        greeks = self.pricing_engine.bs_pricer.calculate_greeks(self.params, 'call')
        self.assertIn('delta', greeks)
        self.assertIn('gamma', greeks)
        self.assertIn('theta', greeks)
        self.assertIn('vega', greeks)
        self.assertIn('rho', greeks)
    
    def test_implied_volatility(self):
        """Test implied volatility calculation"""
        market_price = 150.0
        iv = self.pricing_engine.bs_pricer.implied_volatility(market_price, self.params, 'call')
        self.assertIsNotNone(iv)
        self.assertGreater(iv, 0)

class TestTradingStrategies(unittest.TestCase):
    """Test trading strategies"""
    
    def setUp(self):
        self.strategy_selector = StrategySelector()
        self.straddle = StraddleStrategy()
        self.strategy_params = StrategyParams(
            spot_price=18000,
            strike_prices=[18000],
            expiry_dates=['2024-01-25'],
            option_prices={'call': 150, 'put': 120},
            quantities={'call': 1, 'put': 1},
            risk_free_rate=0.05,
            volatility=0.25
        )
    
    def test_straddle_payoff(self):
        """Test straddle payoff calculation"""
        payoff = self.straddle.calculate_payoff(18500, self.strategy_params)
        self.assertIsInstance(payoff, float)
        self.assertGreaterEqual(payoff, 0)
    
    def test_straddle_greeks(self):
        """Test straddle Greeks calculation"""
        greeks = self.straddle.calculate_greeks(self.strategy_params)
        self.assertIn('delta', greeks)
        self.assertIn('gamma', greeks)
        self.assertIn('theta', greeks)
        self.assertIn('vega', greeks)
        self.assertIn('rho', greeks)
    
    def test_straddle_breakeven(self):
        """Test straddle breakeven calculation"""
        breakeven = self.straddle.calculate_breakeven(self.strategy_params)
        self.assertIsInstance(breakeven, list)
        self.assertEqual(len(breakeven), 2)
        self.assertLess(breakeven[0], breakeven[1])
    
    def test_strategy_selection(self):
        """Test strategy selection"""
        market_conditions = {
            'volatility': 0.3,
            'trend': 'neutral',
            'time_to_expiry': 30
        }
        strategy = self.strategy_selector.select_strategy(market_conditions)
        self.assertIn(strategy, ['straddle', 'strangle', 'iron_condor', 'butterfly'])

class TestRiskManagement(unittest.TestCase):
    """Test risk management system"""
    
    def setUp(self):
        self.risk_manager = RiskManager()
        self.position = Position(
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
    
    def test_add_position(self):
        """Test adding position"""
        initial_count = len(self.risk_manager.positions)
        self.risk_manager.add_position(self.position)
        self.assertEqual(len(self.risk_manager.positions), initial_count + 1)
    
    def test_remove_position(self):
        """Test removing position"""
        self.risk_manager.add_position(self.position)
        initial_count = len(self.risk_manager.positions)
        self.risk_manager.remove_position(self.position.symbol)
        self.assertEqual(len(self.risk_manager.positions), initial_count - 1)
    
    def test_risk_limits_check(self):
        """Test risk limits checking"""
        self.risk_manager.add_position(self.position)
        current_prices = {self.position.symbol: self.position.current_price}
        alerts = self.risk_manager.check_risk_limits(current_prices)
        self.assertIsInstance(alerts, list)
    
    def test_position_sizing(self):
        """Test position sizing calculation"""
        strategy_params = {
            'win_rate': 0.6,
            'avg_win': 1000,
            'avg_loss': 500,
            'max_loss': 1000
        }
        position_size = self.risk_manager.calculate_position_sizing(strategy_params, 1000000)
        self.assertIsInstance(position_size, int)
        self.assertGreaterEqual(position_size, 0)
    
    def test_stop_loss_calculation(self):
        """Test stop loss calculation"""
        stop_loss = self.risk_manager.calculate_stop_loss_level(150.0, 'call')
        self.assertIsInstance(stop_loss, float)
        self.assertLess(stop_loss, 150.0)
    
    def test_take_profit_calculation(self):
        """Test take profit calculation"""
        take_profit = self.risk_manager.calculate_take_profit_level(150.0, 'call')
        self.assertIsInstance(take_profit, float)
        self.assertGreater(take_profit, 150.0)

class TestDataFetcher(unittest.TestCase):
    """Test data fetching functionality"""
    
    def setUp(self):
        self.data_fetcher = NIFTYDataFetcher()
    
    def test_market_indicators(self):
        """Test market indicators fetching"""
        indicators = self.data_fetcher.get_market_indicators()
        self.assertIsInstance(indicators, dict)
        self.assertIn('spot_price', indicators)
        self.assertIn('current_volatility', indicators)
    
    def test_options_chain(self):
        """Test options chain fetching"""
        options_chain = self.data_fetcher.get_options_chain()
        self.assertIsInstance(options_chain, pd.DataFrame)
    
    def test_volatility_data(self):
        """Test volatility data fetching"""
        volatility_data = self.data_fetcher.get_volatility_data(30)
        self.assertIsInstance(volatility_data, pd.DataFrame)

class TestMLModels(unittest.TestCase):
    """Test machine learning models"""
    
    def setUp(self):
        self.ml_manager = MLModelManager()
        self.market_data = {
            'spot_price': 18000,
            'volatility': 0.25,
            'trend': 0.1,
            'volume_ratio': 1.2,
            'rsi': 55,
            'macd': 0.05
        }
    
    def test_predictions(self):
        """Test ML predictions"""
        predictions = self.ml_manager.get_predictions(self.market_data, 18000)
        self.assertIsInstance(predictions, dict)
        self.assertIn('volatility', predictions)
        self.assertIn('price', predictions)
        self.assertIn('strategy', predictions)
    
    def test_strategy_selector(self):
        """Test strategy selector"""
        self.assertIsNotNone(self.ml_manager.strategy_selector)
        self.assertIsNotNone(self.ml_manager.volatility_predictor)
        self.assertIsNotNone(self.ml_manager.price_predictor)

class TestIntegration(unittest.TestCase):
    """Test system integration"""
    
    def test_system_components(self):
        """Test that all system components can be imported"""
        try:
            from trading_engine import TradingEngine
            from backtesting import BacktestEngine
            from dashboard import app
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Failed to import system components: {e}")
    
    def test_config_loading(self):
        """Test configuration loading"""
        try:
            import config
            self.assertTrue(hasattr(config, 'SYMBOL'))
            self.assertTrue(hasattr(config, 'STRATEGIES'))
            self.assertTrue(hasattr(config, 'ML_MODELS'))
        except ImportError as e:
            self.fail(f"Failed to load configuration: {e}")

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestOptionPricing))
    test_suite.addTest(unittest.makeSuite(TestTradingStrategies))
    test_suite.addTest(unittest.makeSuite(TestRiskManagement))
    test_suite.addTest(unittest.makeSuite(TestDataFetcher))
    test_suite.addTest(unittest.makeSuite(TestMLModels))
    test_suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*60}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
