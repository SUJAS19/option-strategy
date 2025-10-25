"""
Live Trading Engine for NIFTY Options
Main trading engine that coordinates all components
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime, timedelta
import logging
import schedule
import time
import json
from dataclasses import asdict

from data_fetcher import NIFTYDataFetcher
from option_pricing import OptionPricingEngine, OptionParams
from option_strategies import StrategySelector, StrategyParams
from ml_models import MLModelManager
from risk_management import RiskManager, Position
from backtesting import BacktestEngine, BacktestAnalyzer
import config

logger = logging.getLogger(__name__)

class TradingEngine:
    """Main trading engine for NIFTY options"""
    
    def __init__(self):
        self.data_fetcher = NIFTYDataFetcher()
        self.pricing_engine = OptionPricingEngine()
        self.strategy_selector = StrategySelector()
        self.ml_manager = MLModelManager()
        self.risk_manager = RiskManager()
        self.backtest_engine = BacktestEngine()
        self.analyzer = BacktestAnalyzer()
        
        self.is_running = False
        self.positions = []
        self.daily_pnl = 0.0
        self.portfolio_value = 0.0
        
        # Initialize logging
        logging.basicConfig(
            level=getattr(logging, config.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
    
    def start(self):
        """Start the trading engine"""
        try:
            logger.info("Starting NIFTY Options Trading Engine...")
            self.is_running = True
            
            # Schedule trading tasks
            schedule.every().minute.at(":00").do(self._market_data_update)
            schedule.every().minute.at(":30").do(self._strategy_analysis)
            schedule.every().hour.at(":00").do(self._risk_check)
            schedule.every().day.at("09:15").do(self._market_open)
            schedule.every().day.at("15:30").do(self._market_close)
            
            # Start main loop
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Trading engine stopped by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in trading engine: {e}")
            self.stop()
    
    def stop(self):
        """Stop the trading engine"""
        logger.info("Stopping trading engine...")
        self.is_running = False
        
        # Close all positions if market is open
        if self._is_market_open():
            self._close_all_positions("engine_stop")
    
    def _market_data_update(self):
        """Update market data and position values"""
        try:
            if not self._is_market_open():
                return
            
            # Get current market data
            market_data = self.data_fetcher.get_market_indicators()
            spot_price = market_data.get('spot_price', 0)
            
            if spot_price == 0:
                logger.warning("Unable to fetch spot price")
                return
            
            # Update position values
            self._update_position_values(spot_price)
            
            # Update portfolio value
            self._update_portfolio_value()
            
            logger.info(f"Market data updated - Spot: {spot_price}, Portfolio: {self.portfolio_value}")
            
        except Exception as e:
            logger.error(f"Error updating market data: {e}")
    
    def _strategy_analysis(self):
        """Analyze market conditions and select strategies"""
        try:
            if not self._is_market_open():
                return
            
            # Get market data
            market_data = self.data_fetcher.get_market_indicators()
            spot_price = market_data.get('spot_price', 0)
            
            if spot_price == 0:
                return
            
            # Get ML predictions
            predictions = self.ml_manager.get_predictions(market_data, spot_price)
            
            # Select strategy based on market conditions
            strategy_name = self._select_strategy(market_data, predictions)
            
            # Check if we should enter new positions
            if self._should_enter_position(market_data, strategy_name):
                self._enter_position(spot_price, strategy_name, market_data)
            
            logger.info(f"Strategy analysis completed - Selected: {strategy_name}")
            
        except Exception as e:
            logger.error(f"Error in strategy analysis: {e}")
    
    def _risk_check(self):
        """Perform comprehensive risk check"""
        try:
            if not self.positions:
                return
            
            # Get current prices
            current_prices = {}
            for position in self.positions:
                current_prices[position.symbol] = position.current_price
            
            # Check risk limits
            risk_alerts = self.risk_manager.check_risk_limits(current_prices)
            
            # Handle risk alerts
            for alert in risk_alerts:
                self._handle_risk_alert(alert)
            
            # Check individual position exits
            self._check_position_exits()
            
            if risk_alerts:
                logger.warning(f"Risk alerts triggered: {len(risk_alerts)} alerts")
            
        except Exception as e:
            logger.error(f"Error in risk check: {e}")
    
    def _market_open(self):
        """Handle market open"""
        logger.info("Market opened - Initializing trading session")
        self.daily_pnl = 0.0
        
        # Load ML models if not already loaded
        if not self.ml_manager.models_trained:
            self._load_ml_models()
    
    def _market_close(self):
        """Handle market close"""
        logger.info("Market closed - Finalizing trading session")
        
        # Close all positions
        self._close_all_positions("market_close")
        
        # Log daily performance
        logger.info(f"Daily P&L: {self.daily_pnl:.2f}")
    
    def _select_strategy(self, market_data: Dict, predictions: Dict) -> str:
        """Select optimal strategy based on market conditions"""
        try:
            # Use ML predictions if available
            if predictions.get('strategy'):
                return predictions['strategy']
            
            # Fallback to rule-based selection
            volatility = market_data.get('current_volatility', 0.2)
            trend = self._determine_trend(market_data)
            
            if volatility > 0.3:
                return 'straddle'
            elif volatility > 0.25:
                return 'strangle'
            elif volatility < 0.2:
                return 'iron_condor'
            else:
                return 'butterfly'
                
        except Exception as e:
            logger.error(f"Error selecting strategy: {e}")
            return 'straddle'  # Default strategy
    
    def _should_enter_position(self, market_data: Dict, strategy_name: str) -> bool:
        """Determine if we should enter a new position"""
        try:
            # Check if we already have positions
            if len(self.positions) > 0:
                return False
            
            # Check capital requirements
            if self.portfolio_value < 100000:  # Minimum capital
                return False
            
            # Check market conditions
            volatility = market_data.get('current_volatility', 0.2)
            if volatility < 0.15 or volatility > 0.5:
                return False
            
            # Check time constraints
            current_time = datetime.now().time()
            if current_time < datetime.strptime("09:30", "%H:%M").time():
                return False
            if current_time > datetime.strptime("15:00", "%H:%M").time():
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking position entry: {e}")
            return False
    
    def _enter_position(self, spot_price: float, strategy_name: str, market_data: Dict):
        """Enter a new position"""
        try:
            # Get strategy instance
            strategy = self.strategy_selector.get_strategy(strategy_name)
            if not strategy:
                logger.error(f"Strategy {strategy_name} not found")
                return
            
            # Calculate strike prices
            strike_prices = self._calculate_strike_prices(spot_price, strategy_name)
            
            # Get options chain
            options_chain = self.data_fetcher.get_options_chain()
            if options_chain.empty:
                logger.warning("No options chain data available")
                return
            
            # Calculate position size
            position_size = self._calculate_position_size(spot_price, strategy_name)
            
            if position_size <= 0:
                logger.warning("Position size too small")
                return
            
            # Create positions based on strategy
            if strategy_name == 'straddle':
                self._create_straddle_position(spot_price, strike_prices[0], position_size)
            elif strategy_name == 'strangle':
                self._create_strangle_position(spot_price, strike_prices, position_size)
            elif strategy_name == 'iron_condor':
                self._create_iron_condor_position(spot_price, strike_prices, position_size)
            elif strategy_name == 'butterfly':
                self._create_butterfly_position(spot_price, strike_prices, position_size)
            
            logger.info(f"Entered {strategy_name} position with {position_size} contracts")
            
        except Exception as e:
            logger.error(f"Error entering position: {e}")
    
    def _create_straddle_position(self, spot_price: float, strike_price: float, quantity: int):
        """Create straddle position"""
        try:
            # Calculate option prices
            call_price = self._calculate_option_price(spot_price, strike_price, 'call')
            put_price = self._calculate_option_price(spot_price, strike_price, 'put')
            
            # Create call position
            call_position = Position(
                symbol=f"NIFTY{strike_price}CE",
                option_type='call',
                strike_price=strike_price,
                expiry_date=self._get_next_expiry(),
                quantity=quantity,
                entry_price=call_price,
                current_price=call_price,
                entry_time=datetime.now(),
                strategy_name='straddle'
            )
            
            # Create put position
            put_position = Position(
                symbol=f"NIFTY{strike_price}PE",
                option_type='put',
                strike_price=strike_price,
                expiry_date=self._get_next_expiry(),
                quantity=quantity,
                entry_price=put_price,
                current_price=put_price,
                entry_time=datetime.now(),
                strategy_name='straddle'
            )
            
            self.positions.extend([call_position, put_position])
            
        except Exception as e:
            logger.error(f"Error creating straddle position: {e}")
    
    def _create_strangle_position(self, spot_price: float, strike_prices: List[float], quantity: int):
        """Create strangle position"""
        try:
            call_strike = strike_prices[0]  # Higher strike
            put_strike = strike_prices[1]   # Lower strike
            
            # Calculate option prices
            call_price = self._calculate_option_price(spot_price, call_strike, 'call')
            put_price = self._calculate_option_price(spot_price, put_strike, 'put')
            
            # Create positions
            call_position = Position(
                symbol=f"NIFTY{call_strike}CE",
                option_type='call',
                strike_price=call_strike,
                expiry_date=self._get_next_expiry(),
                quantity=quantity,
                entry_price=call_price,
                current_price=call_price,
                entry_time=datetime.now(),
                strategy_name='strangle'
            )
            
            put_position = Position(
                symbol=f"NIFTY{put_strike}PE",
                option_type='put',
                strike_price=put_strike,
                expiry_date=self._get_next_expiry(),
                quantity=quantity,
                entry_price=put_price,
                current_price=put_price,
                entry_time=datetime.now(),
                strategy_name='strangle'
            )
            
            self.positions.extend([call_position, put_position])
            
        except Exception as e:
            logger.error(f"Error creating strangle position: {e}")
    
    def _create_iron_condor_position(self, spot_price: float, strike_prices: List[float], quantity: int):
        """Create iron condor position"""
        try:
            # Iron condor has 4 legs: long put, short put, short call, long call
            put_long = strike_prices[0]
            put_short = strike_prices[1]
            call_short = strike_prices[2]
            call_long = strike_prices[3]
            
            # Create all 4 positions
            positions = []
            strikes = [put_long, put_short, call_short, call_long]
            option_types = ['put', 'put', 'call', 'call']
            quantities = [quantity, -quantity, -quantity, quantity]
            
            for strike, opt_type, qty in zip(strikes, option_types, quantities):
                price = self._calculate_option_price(spot_price, strike, opt_type)
                
                position = Position(
                    symbol=f"NIFTY{strike}{'CE' if opt_type == 'call' else 'PE'}",
                    option_type=opt_type,
                    strike_price=strike,
                    expiry_date=self._get_next_expiry(),
                    quantity=qty,
                    entry_price=price,
                    current_price=price,
                    entry_time=datetime.now(),
                    strategy_name='iron_condor'
                )
                
                positions.append(position)
            
            self.positions.extend(positions)
            
        except Exception as e:
            logger.error(f"Error creating iron condor position: {e}")
    
    def _create_butterfly_position(self, spot_price: float, strike_prices: List[float], quantity: int):
        """Create butterfly position"""
        try:
            # Butterfly has 3 legs: long call, short 2 calls, long call
            lower_strike = strike_prices[0]
            middle_strike = strike_prices[1]
            upper_strike = strike_prices[2]
            
            # Create positions
            positions = []
            strikes = [lower_strike, middle_strike, upper_strike]
            quantities = [quantity, -2*quantity, quantity]
            
            for strike, qty in zip(strikes, quantities):
                price = self._calculate_option_price(spot_price, strike, 'call')
                
                position = Position(
                    symbol=f"NIFTY{strike}CE",
                    option_type='call',
                    strike_price=strike,
                    expiry_date=self._get_next_expiry(),
                    quantity=qty,
                    entry_price=price,
                    current_price=price,
                    entry_time=datetime.now(),
                    strategy_name='butterfly'
                )
                
                positions.append(position)
            
            self.positions.extend(positions)
            
        except Exception as e:
            logger.error(f"Error creating butterfly position: {e}")
    
    def _check_position_exits(self):
        """Check if any positions should be exited"""
        try:
            positions_to_close = []
            
            for position in self.positions:
                should_exit, reason = self.risk_manager.should_exit_position(
                    position, position.current_price
                )
                
                if should_exit:
                    positions_to_close.append((position, reason))
            
            # Close positions
            for position, reason in positions_to_close:
                self._close_position(position, reason)
                
        except Exception as e:
            logger.error(f"Error checking position exits: {e}")
    
    def _close_position(self, position: Position, reason: str):
        """Close a position"""
        try:
            # Calculate P&L
            pnl = (position.current_price - position.entry_price) * position.quantity * 50
            self.daily_pnl += pnl
            
            # Remove position
            self.positions.remove(position)
            
            logger.info(f"Closed position {position.symbol}: P&L {pnl:.2f}, Reason: {reason}")
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    def _close_all_positions(self, reason: str):
        """Close all positions"""
        for position in self.positions.copy():
            self._close_position(position, reason)
    
    def _update_position_values(self, spot_price: float):
        """Update current values of all positions"""
        for position in self.positions:
            new_price = self._calculate_option_price(
                spot_price, position.strike_price, position.option_type
            )
            position.current_price = new_price
    
    def _update_portfolio_value(self):
        """Update total portfolio value"""
        position_value = sum(pos.current_price * pos.quantity * 50 for pos in self.positions)
        self.portfolio_value = 1000000 + position_value  # Assuming 1M initial capital
    
    def _calculate_strike_prices(self, spot_price: float, strategy_name: str) -> List[float]:
        """Calculate strike prices for strategy"""
        atm_strike = round(spot_price / 50) * 50
        
        if strategy_name == 'straddle':
            return [atm_strike]
        elif strategy_name == 'strangle':
            return [atm_strike + 100, atm_strike - 100]  # 100 points away
        elif strategy_name == 'iron_condor':
            return [atm_strike - 200, atm_strike - 100, atm_strike + 100, atm_strike + 200]
        elif strategy_name == 'butterfly':
            return [atm_strike - 100, atm_strike, atm_strike + 100]
        else:
            return [atm_strike]
    
    def _calculate_position_size(self, spot_price: float, strategy_name: str) -> int:
        """Calculate position size based on risk management"""
        try:
            # Get risk parameters
            max_risk = self.portfolio_value * 0.02  # 2% risk per trade
            
            # Estimate option price
            option_price = self._calculate_option_price(spot_price, spot_price, 'call')
            position_value = option_price * 50  # 50 is lot size
            
            if position_value == 0:
                return 0
            
            position_size = int(max_risk / position_value)
            return max(0, min(position_size, 10))  # Cap at 10 contracts
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def _calculate_option_price(self, spot: float, strike: float, option_type: str) -> float:
        """Calculate option price using Black-Scholes"""
        try:
            time_to_expiry = 30 / 365.0  # Approximate
            
            params = OptionParams(
                spot_price=spot,
                strike_price=strike,
                time_to_expiry=time_to_expiry,
                risk_free_rate=0.05,
                volatility=0.2
            )
            
            result = self.pricing_engine.price_option(params, option_type)
            return result.get('price', 0.05)
            
        except Exception as e:
            logger.error(f"Error calculating option price: {e}")
            return 0.05
    
    def _get_next_expiry(self) -> str:
        """Get next Thursday expiry date"""
        today = datetime.now()
        days_ahead = (3 - today.weekday()) % 7  # Thursday is 3
        if days_ahead == 0:
            days_ahead = 7
        expiry_date = today + timedelta(days=days_ahead)
        return expiry_date.strftime('%Y-%m-%d')
    
    def _is_market_open(self) -> bool:
        """Check if market is open"""
        now = datetime.now()
        current_time = now.time()
        
        # Market hours: 9:15 AM to 3:30 PM
        market_open = datetime.strptime("09:15", "%H:%M").time()
        market_close = datetime.strptime("15:30", "%H:%M").time()
        
        return market_open <= current_time <= market_close
    
    def _determine_trend(self, market_data: Dict) -> str:
        """Determine market trend"""
        # Simplified trend determination
        return 'neutral'  # Default to neutral
    
    def _handle_risk_alert(self, alert: Dict):
        """Handle risk management alerts"""
        try:
            alert_type = alert.get('type')
            action = alert.get('action')
            
            if action == 'close_all_positions':
                self._close_all_positions('risk_alert')
            elif action == 'reduce_positions':
                # Close half of positions
                positions_to_close = self.positions[:len(self.positions)//2]
                for position in positions_to_close:
                    self._close_position(position, 'risk_reduction')
            
            logger.warning(f"Risk alert handled: {alert_type} - {action}")
            
        except Exception as e:
            logger.error(f"Error handling risk alert: {e}")
    
    def _load_ml_models(self):
        """Load pre-trained ML models"""
        try:
            # Try to load existing models
            self.ml_manager.load_models('models.pkl')
            logger.info("ML models loaded successfully")
        except:
            logger.warning("No pre-trained models found, using rule-based strategies")
    
    def get_portfolio_status(self) -> Dict:
        """Get current portfolio status"""
        try:
            total_value = sum(pos.current_price * pos.quantity * 50 for pos in self.positions)
            total_pnl = sum((pos.current_price - pos.entry_price) * pos.quantity * 50 for pos in self.positions)
            
            return {
                'total_positions': len(self.positions),
                'total_value': total_value,
                'total_pnl': total_pnl,
                'daily_pnl': self.daily_pnl,
                'portfolio_value': self.portfolio_value,
                'positions': [asdict(pos) for pos in self.positions]
            }
        except Exception as e:
            logger.error(f"Error getting portfolio status: {e}")
            return {}
