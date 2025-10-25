"""
Option Trading Strategies Implementation
Implements various option strategies for NIFTY trading
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from option_pricing import OptionParams, OptionPricingEngine
import logging

logger = logging.getLogger(__name__)

@dataclass
class StrategyParams:
    """Parameters for option strategies"""
    spot_price: float
    strike_prices: List[float]
    expiry_dates: List[str]
    option_prices: Dict[str, float]  # {option_id: price}
    quantities: Dict[str, int]  # {option_id: quantity}
    risk_free_rate: float
    volatility: float

class OptionStrategy:
    """Base class for option strategies"""
    
    def __init__(self, name: str):
        self.name = name
        self.pricing_engine = OptionPricingEngine()
    
    def calculate_payoff(self, spot_price: float, strategy_params: StrategyParams) -> float:
        """Calculate strategy payoff at expiration"""
        raise NotImplementedError
    
    def calculate_greeks(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate strategy Greeks"""
        raise NotImplementedError
    
    def calculate_breakeven(self, strategy_params: StrategyParams) -> List[float]:
        """Calculate breakeven points"""
        raise NotImplementedError
    
    def calculate_max_profit_loss(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate maximum profit and loss"""
        raise NotImplementedError

class StraddleStrategy(OptionStrategy):
    """Long Straddle Strategy"""
    
    def __init__(self):
        super().__init__("Long Straddle")
    
    def calculate_payoff(self, spot_price: float, strategy_params: StrategyParams) -> float:
        """Calculate straddle payoff"""
        strike = strategy_params.strike_prices[0]
        call_payoff = max(spot_price - strike, 0)
        put_payoff = max(strike - spot_price, 0)
        return call_payoff + put_payoff
    
    def calculate_greeks(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate straddle Greeks"""
        strike = strategy_params.strike_prices[0]
        
        # Call option Greeks
        call_params = OptionParams(
            spot_price=strategy_params.spot_price,
            strike_price=strike,
            time_to_expiry=30/365,  # Approximate
            risk_free_rate=strategy_params.risk_free_rate,
            volatility=strategy_params.volatility
        )
        call_greeks = self.pricing_engine.bs_pricer.calculate_greeks(call_params, 'call')
        
        # Put option Greeks
        put_params = OptionParams(
            spot_price=strategy_params.spot_price,
            strike_price=strike,
            time_to_expiry=30/365,
            risk_free_rate=strategy_params.risk_free_rate,
            volatility=strategy_params.volatility
        )
        put_greeks = self.pricing_engine.bs_pricer.calculate_greeks(put_params, 'put')
        
        return {
            'delta': call_greeks['delta'] + put_greeks['delta'],
            'gamma': call_greeks['gamma'] + put_greeks['gamma'],
            'theta': call_greeks['theta'] + put_greeks['theta'],
            'vega': call_greeks['vega'] + put_greeks['vega'],
            'rho': call_greeks['rho'] + put_greeks['rho']
        }
    
    def calculate_breakeven(self, strategy_params: StrategyParams) -> List[float]:
        """Calculate straddle breakeven points"""
        strike = strategy_params.strike_prices[0]
        net_debit = strategy_params.option_prices.get('call', 0) + strategy_params.option_prices.get('put', 0)
        
        return [strike - net_debit, strike + net_debit]
    
    def calculate_max_profit_loss(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate max profit and loss for straddle"""
        net_debit = strategy_params.option_prices.get('call', 0) + strategy_params.option_prices.get('put', 0)
        
        return {
            'max_profit': float('inf'),  # Unlimited profit potential
            'max_loss': net_debit
        }

class StrangleStrategy(OptionStrategy):
    """Long Strangle Strategy"""
    
    def __init__(self):
        super().__init__("Long Strangle")
    
    def calculate_payoff(self, spot_price: float, strategy_params: StrategyParams) -> float:
        """Calculate strangle payoff"""
        call_strike = strategy_params.strike_prices[0]  # Higher strike
        put_strike = strategy_params.strike_prices[1]   # Lower strike
        
        call_payoff = max(spot_price - call_strike, 0)
        put_payoff = max(put_strike - spot_price, 0)
        return call_payoff + put_payoff
    
    def calculate_greeks(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate strangle Greeks"""
        call_strike = strategy_params.strike_prices[0]
        put_strike = strategy_params.strike_prices[1]
        
        # Call option Greeks
        call_params = OptionParams(
            spot_price=strategy_params.spot_price,
            strike_price=call_strike,
            time_to_expiry=30/365,
            risk_free_rate=strategy_params.risk_free_rate,
            volatility=strategy_params.volatility
        )
        call_greeks = self.pricing_engine.bs_pricer.calculate_greeks(call_params, 'call')
        
        # Put option Greeks
        put_params = OptionParams(
            spot_price=strategy_params.spot_price,
            strike_price=put_strike,
            time_to_expiry=30/365,
            risk_free_rate=strategy_params.risk_free_rate,
            volatility=strategy_params.volatility
        )
        put_greeks = self.pricing_engine.bs_pricer.calculate_greeks(put_params, 'put')
        
        return {
            'delta': call_greeks['delta'] + put_greeks['delta'],
            'gamma': call_greeks['gamma'] + put_greeks['gamma'],
            'theta': call_greeks['theta'] + put_greeks['theta'],
            'vega': call_greeks['vega'] + put_greeks['vega'],
            'rho': call_greeks['rho'] + put_greeks['rho']
        }
    
    def calculate_breakeven(self, strategy_params: StrategyParams) -> List[float]:
        """Calculate strangle breakeven points"""
        call_strike = strategy_params.strike_prices[0]
        put_strike = strategy_params.strike_prices[1]
        net_debit = strategy_params.option_prices.get('call', 0) + strategy_params.option_prices.get('put', 0)
        
        return [put_strike - net_debit, call_strike + net_debit]
    
    def calculate_max_profit_loss(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate max profit and loss for strangle"""
        net_debit = strategy_params.option_prices.get('call', 0) + strategy_params.option_prices.get('put', 0)
        
        return {
            'max_profit': float('inf'),
            'max_loss': net_debit
        }

class IronCondorStrategy(OptionStrategy):
    """Iron Condor Strategy"""
    
    def __init__(self):
        super().__init__("Iron Condor")
    
    def calculate_payoff(self, spot_price: float, strategy_params: StrategyParams) -> float:
        """Calculate iron condor payoff"""
        # Strikes: [put_short, put_long, call_short, call_long]
        put_long = strategy_params.strike_prices[0]
        put_short = strategy_params.strike_prices[1]
        call_short = strategy_params.strike_prices[2]
        call_long = strategy_params.strike_prices[3]
        
        # Long put payoff
        long_put_payoff = max(put_long - spot_price, 0)
        # Short put payoff
        short_put_payoff = -max(put_short - spot_price, 0)
        # Short call payoff
        short_call_payoff = -max(spot_price - call_short, 0)
        # Long call payoff
        long_call_payoff = max(spot_price - call_long, 0)
        
        return long_put_payoff + short_put_payoff + short_call_payoff + long_call_payoff
    
    def calculate_greeks(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate iron condor Greeks"""
        put_long = strategy_params.strike_prices[0]
        put_short = strategy_params.strike_prices[1]
        call_short = strategy_params.strike_prices[2]
        call_long = strategy_params.strike_prices[3]
        
        total_delta = 0
        total_gamma = 0
        total_theta = 0
        total_vega = 0
        total_rho = 0
        
        # Calculate Greeks for each leg
        strikes = [put_long, put_short, call_short, call_long]
        option_types = ['put', 'put', 'call', 'call']
        quantities = [1, -1, -1, 1]  # Long put, short put, short call, long call
        
        for strike, opt_type, qty in zip(strikes, option_types, quantities):
            params = OptionParams(
                spot_price=strategy_params.spot_price,
                strike_price=strike,
                time_to_expiry=30/365,
                risk_free_rate=strategy_params.risk_free_rate,
                volatility=strategy_params.volatility
            )
            greeks = self.pricing_engine.bs_pricer.calculate_greeks(params, opt_type)
            
            total_delta += greeks['delta'] * qty
            total_gamma += greeks['gamma'] * qty
            total_theta += greeks['theta'] * qty
            total_vega += greeks['vega'] * qty
            total_rho += greeks['rho'] * qty
        
        return {
            'delta': total_delta,
            'gamma': total_gamma,
            'theta': total_theta,
            'vega': total_vega,
            'rho': total_rho
        }
    
    def calculate_breakeven(self, strategy_params: StrategyParams) -> List[float]:
        """Calculate iron condor breakeven points"""
        put_short = strategy_params.strike_prices[1]
        call_short = strategy_params.strike_prices[2]
        net_credit = (strategy_params.option_prices.get('put_short', 0) + 
                     strategy_params.option_prices.get('call_short', 0) -
                     strategy_params.option_prices.get('put_long', 0) - 
                     strategy_params.option_prices.get('call_long', 0))
        
        return [put_short - net_credit, call_short + net_credit]
    
    def calculate_max_profit_loss(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate max profit and loss for iron condor"""
        net_credit = (strategy_params.option_prices.get('put_short', 0) + 
                     strategy_params.option_prices.get('call_short', 0) -
                     strategy_params.option_prices.get('put_long', 0) - 
                     strategy_params.option_prices.get('call_long', 0))
        
        # Max profit is the net credit received
        # Max loss is the width of the spread minus net credit
        put_long = strategy_params.strike_prices[0]
        put_short = strategy_params.strike_prices[1]
        call_short = strategy_params.strike_prices[2]
        call_long = strategy_params.strike_prices[3]
        
        put_wing_width = put_short - put_long
        call_wing_width = call_long - call_short
        
        return {
            'max_profit': net_credit,
            'max_loss': max(put_wing_width, call_wing_width) - net_credit
        }

class ButterflyStrategy(OptionStrategy):
    """Long Butterfly Strategy"""
    
    def __init__(self):
        super().__init__("Long Butterfly")
    
    def calculate_payoff(self, spot_price: float, strategy_params: StrategyParams) -> float:
        """Calculate butterfly payoff"""
        # Strikes: [lower, middle, upper]
        lower_strike = strategy_params.strike_prices[0]
        middle_strike = strategy_params.strike_prices[1]
        upper_strike = strategy_params.strike_prices[2]
        
        # Long call at lower strike
        long_lower_payoff = max(spot_price - lower_strike, 0)
        # Short 2 calls at middle strike
        short_middle_payoff = -2 * max(spot_price - middle_strike, 0)
        # Long call at upper strike
        long_upper_payoff = max(spot_price - upper_strike, 0)
        
        return long_lower_payoff + short_middle_payoff + long_upper_payoff
    
    def calculate_greeks(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate butterfly Greeks"""
        lower_strike = strategy_params.strike_prices[0]
        middle_strike = strategy_params.strike_prices[1]
        upper_strike = strategy_params.strike_prices[2]
        
        total_delta = 0
        total_gamma = 0
        total_theta = 0
        total_vega = 0
        total_rho = 0
        
        # Calculate Greeks for each leg
        strikes = [lower_strike, middle_strike, upper_strike]
        quantities = [1, -2, 1]  # Long, short 2, long
        
        for strike, qty in zip(strikes, quantities):
            params = OptionParams(
                spot_price=strategy_params.spot_price,
                strike_price=strike,
                time_to_expiry=30/365,
                risk_free_rate=strategy_params.risk_free_rate,
                volatility=strategy_params.volatility
            )
            greeks = self.pricing_engine.bs_pricer.calculate_greeks(params, 'call')
            
            total_delta += greeks['delta'] * qty
            total_gamma += greeks['gamma'] * qty
            total_theta += greeks['theta'] * qty
            total_vega += greeks['vega'] * qty
            total_rho += greeks['rho'] * qty
        
        return {
            'delta': total_delta,
            'gamma': total_gamma,
            'theta': total_theta,
            'vega': total_vega,
            'rho': total_rho
        }
    
    def calculate_breakeven(self, strategy_params: StrategyParams) -> List[float]:
        """Calculate butterfly breakeven points"""
        lower_strike = strategy_params.strike_prices[0]
        middle_strike = strategy_params.strike_prices[1]
        upper_strike = strategy_params.strike_prices[2]
        net_debit = (strategy_params.option_prices.get('lower_call', 0) + 
                    strategy_params.option_prices.get('upper_call', 0) - 
                    2 * strategy_params.option_prices.get('middle_call', 0))
        
        return [lower_strike + net_debit, upper_strike - net_debit]
    
    def calculate_max_profit_loss(self, strategy_params: StrategyParams) -> Dict[str, float]:
        """Calculate max profit and loss for butterfly"""
        lower_strike = strategy_params.strike_prices[0]
        middle_strike = strategy_params.strike_prices[1]
        upper_strike = strategy_params.strike_prices[2]
        net_debit = (strategy_params.option_prices.get('lower_call', 0) + 
                    strategy_params.option_prices.get('upper_call', 0) - 
                    2 * strategy_params.option_prices.get('middle_call', 0))
        
        # Max profit occurs at middle strike
        max_profit = (middle_strike - lower_strike) - net_debit
        
        return {
            'max_profit': max_profit,
            'max_loss': net_debit
        }

class StrategySelector:
    """Strategy selection based on market conditions"""
    
    def __init__(self):
        self.strategies = {
            'straddle': StraddleStrategy(),
            'strangle': StrangleStrategy(),
            'iron_condor': IronCondorStrategy(),
            'butterfly': ButterflyStrategy()
        }
    
    def select_strategy(self, market_conditions: Dict) -> str:
        """Select optimal strategy based on market conditions"""
        volatility = market_conditions.get('volatility', 0.2)
        trend = market_conditions.get('trend', 'neutral')  # bullish, bearish, neutral
        time_to_expiry = market_conditions.get('time_to_expiry', 30)
        
        if volatility > 0.3 and trend == 'neutral':
            return 'straddle'
        elif volatility > 0.25 and trend == 'neutral':
            return 'strangle'
        elif volatility < 0.2 and trend == 'neutral':
            return 'iron_condor'
        elif volatility < 0.15 and trend == 'neutral':
            return 'butterfly'
        else:
            return 'straddle'  # Default strategy
    
    def get_strategy(self, strategy_name: str) -> OptionStrategy:
        """Get strategy instance by name"""
        return self.strategies.get(strategy_name)
    
    def analyze_strategy_performance(self, strategy_name: str, 
                                   strategy_params: StrategyParams,
                                   spot_prices: List[float]) -> Dict:
        """Analyze strategy performance across different spot prices"""
        strategy = self.get_strategy(strategy_name)
        if not strategy:
            return {}
        
        payoffs = [strategy.calculate_payoff(spot, strategy_params) for spot in spot_prices]
        greeks = strategy.calculate_greeks(strategy_params)
        breakeven = strategy.calculate_breakeven(strategy_params)
        max_pnl = strategy.calculate_max_profit_loss(strategy_params)
        
        return {
            'payoffs': payoffs,
            'greeks': greeks,
            'breakeven_points': breakeven,
            'max_profit': max_pnl['max_profit'],
            'max_loss': max_pnl['max_loss']
        }
