"""
Risk Management System for Options Trading
Implements comprehensive risk management for NIFTY options strategies
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class RiskLevel(Enum):
    """Risk level enumeration"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Position:
    """Position data structure"""
    symbol: str
    option_type: str  # 'call' or 'put'
    strike_price: float
    expiry_date: str
    quantity: int
    entry_price: float
    current_price: float
    entry_time: datetime
    strategy_name: str

@dataclass
class RiskMetrics:
    """Risk metrics container"""
    portfolio_value: float
    total_delta: float
    total_gamma: float
    total_theta: float
    total_vega: float
    total_rho: float
    var_95: float  # Value at Risk 95%
    var_99: float  # Value at Risk 99%
    max_drawdown: float
    sharpe_ratio: float
    beta: float

class RiskManager:
    """Main risk management class"""
    
    def __init__(self, max_position_size: float = 1000000, 
                 max_daily_loss: float = 50000,
                 stop_loss_pct: float = 0.02,
                 take_profit_pct: float = 0.05):
        self.max_position_size = max_position_size
        self.max_daily_loss = max_daily_loss
        self.stop_loss_pct = stop_loss_pct
        self.take_profit_pct = take_profit_pct
        self.daily_pnl = 0.0
        self.positions = []
        self.risk_alerts = []
        
    def add_position(self, position: Position):
        """Add a new position to the portfolio"""
        self.positions.append(position)
        logger.info(f"Added position: {position.symbol} {position.option_type} {position.strike_price}")
    
    def remove_position(self, position_id: str):
        """Remove a position from the portfolio"""
        self.positions = [p for p in self.positions if p.symbol != position_id]
        logger.info(f"Removed position: {position_id}")
    
    def calculate_portfolio_metrics(self, current_prices: Dict[str, float]) -> RiskMetrics:
        """Calculate comprehensive portfolio risk metrics"""
        if not self.positions:
            return RiskMetrics(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        
        # Calculate portfolio value
        portfolio_value = sum(
            pos.quantity * current_prices.get(pos.symbol, pos.current_price) 
            for pos in self.positions
        )
        
        # Calculate Greeks (simplified)
        total_delta = sum(pos.quantity * self._calculate_delta(pos) for pos in self.positions)
        total_gamma = sum(pos.quantity * self._calculate_gamma(pos) for pos in self.positions)
        total_theta = sum(pos.quantity * self._calculate_theta(pos) for pos in self.positions)
        total_vega = sum(pos.quantity * self._calculate_vega(pos) for pos in self.positions)
        total_rho = sum(pos.quantity * self._calculate_rho(pos) for pos in self.positions)
        
        # Calculate VaR
        var_95, var_99 = self._calculate_var(portfolio_value)
        
        # Calculate other metrics
        max_drawdown = self._calculate_max_drawdown()
        sharpe_ratio = self._calculate_sharpe_ratio()
        beta = self._calculate_beta()
        
        return RiskMetrics(
            portfolio_value=portfolio_value,
            total_delta=total_delta,
            total_gamma=total_gamma,
            total_theta=total_theta,
            total_vega=total_vega,
            total_rho=total_rho,
            var_95=var_95,
            var_99=var_99,
            max_drawdown=max_drawdown,
            sharpe_ratio=sharpe_ratio,
            beta=beta
        )
    
    def check_risk_limits(self, current_prices: Dict[str, float]) -> List[Dict]:
        """Check if any risk limits are breached"""
        alerts = []
        metrics = self.calculate_portfolio_metrics(current_prices)
        
        # Check position size limit
        if abs(metrics.portfolio_value) > self.max_position_size:
            alerts.append({
                'type': 'position_size',
                'level': RiskLevel.CRITICAL,
                'message': f'Portfolio value {metrics.portfolio_value} exceeds limit {self.max_position_size}',
                'action': 'reduce_positions'
            })
        
        # Check daily loss limit
        if self.daily_pnl < -self.max_daily_loss:
            alerts.append({
                'type': 'daily_loss',
                'level': RiskLevel.CRITICAL,
                'message': f'Daily loss {self.daily_pnl} exceeds limit {self.max_daily_loss}',
                'action': 'close_all_positions'
            })
        
        # Check delta exposure
        if abs(metrics.total_delta) > self.max_position_size * 0.1:  # 10% of max position
            alerts.append({
                'type': 'delta_exposure',
                'level': RiskLevel.HIGH,
                'message': f'Delta exposure {metrics.total_delta} is too high',
                'action': 'hedge_delta'
            })
        
        # Check gamma exposure
        if abs(metrics.total_gamma) > self.max_position_size * 0.01:  # 1% of max position
            alerts.append({
                'type': 'gamma_exposure',
                'level': RiskLevel.MEDIUM,
                'message': f'Gamma exposure {metrics.total_gamma} is high',
                'action': 'monitor_closely'
            })
        
        # Check theta decay
        if metrics.total_theta < -self.max_position_size * 0.001:  # 0.1% of max position
            alerts.append({
                'type': 'theta_decay',
                'level': RiskLevel.MEDIUM,
                'message': f'High theta decay {metrics.total_theta}',
                'action': 'consider_rolling'
            })
        
        # Check VaR limits
        if metrics.var_95 > self.max_position_size * 0.05:  # 5% of max position
            alerts.append({
                'type': 'var_limit',
                'level': RiskLevel.HIGH,
                'message': f'VaR 95% {metrics.var_95} exceeds limit',
                'action': 'reduce_risk'
            })
        
        self.risk_alerts = alerts
        return alerts
    
    def calculate_position_sizing(self, strategy_params: Dict, 
                                 available_capital: float) -> int:
        """Calculate optimal position size based on risk parameters"""
        try:
            # Kelly Criterion for position sizing
            win_rate = strategy_params.get('win_rate', 0.5)
            avg_win = strategy_params.get('avg_win', 100)
            avg_loss = strategy_params.get('avg_loss', 100)
            
            if avg_loss == 0:
                return 0
            
            kelly_fraction = (win_rate * avg_win - (1 - win_rate) * avg_loss) / avg_win
            kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
            
            # Calculate position size
            risk_per_trade = available_capital * kelly_fraction
            max_loss_per_contract = strategy_params.get('max_loss', 1000)
            
            if max_loss_per_contract == 0:
                return 0
            
            position_size = int(risk_per_trade / max_loss_per_contract)
            
            # Apply additional risk limits
            max_position = int(available_capital * 0.1 / max_loss_per_contract)  # Max 10% of capital
            position_size = min(position_size, max_position)
            
            return max(0, position_size)
            
        except Exception as e:
            logger.error(f"Error calculating position size: {e}")
            return 0
    
    def calculate_stop_loss_level(self, entry_price: float, option_type: str) -> float:
        """Calculate stop loss level for a position"""
        if option_type.lower() == 'call':
            return entry_price * (1 - self.stop_loss_pct)
        else:
            return entry_price * (1 + self.stop_loss_pct)
    
    def calculate_take_profit_level(self, entry_price: float, option_type: str) -> float:
        """Calculate take profit level for a position"""
        if option_type.lower() == 'call':
            return entry_price * (1 + self.take_profit_pct)
        else:
            return entry_price * (1 - self.take_profit_pct)
    
    def should_exit_position(self, position: Position, current_price: float) -> Tuple[bool, str]:
        """Determine if a position should be exited"""
        # Check stop loss
        stop_loss_level = self.calculate_stop_loss_level(position.entry_price, position.option_type)
        if position.option_type.lower() == 'call' and current_price <= stop_loss_level:
            return True, 'stop_loss'
        elif position.option_type.lower() == 'put' and current_price >= stop_loss_level:
            return True, 'stop_loss'
        
        # Check take profit
        take_profit_level = self.calculate_take_profit_level(position.entry_price, position.option_type)
        if position.option_type.lower() == 'call' and current_price >= take_profit_level:
            return True, 'take_profit'
        elif position.option_type.lower() == 'put' and current_price <= take_profit_level:
            return True, 'take_profit'
        
        # Check time decay (exit if less than 7 days to expiry)
        days_to_expiry = (datetime.strptime(position.expiry_date, '%Y-%m-%d') - datetime.now()).days
        if days_to_expiry <= 7:
            return True, 'time_decay'
        
        return False, 'hold'
    
    def get_hedging_recommendations(self, metrics: RiskMetrics) -> List[Dict]:
        """Get recommendations for hedging portfolio risk"""
        recommendations = []
        
        # Delta hedging
        if abs(metrics.total_delta) > self.max_position_size * 0.05:
            if metrics.total_delta > 0:
                recommendations.append({
                    'type': 'delta_hedge',
                    'action': 'buy_puts',
                    'quantity': int(abs(metrics.total_delta) / 50),  # Assuming 50 delta per contract
                    'reason': 'Reduce positive delta exposure'
                })
            else:
                recommendations.append({
                    'type': 'delta_hedge',
                    'action': 'buy_calls',
                    'quantity': int(abs(metrics.total_delta) / 50),
                    'reason': 'Reduce negative delta exposure'
                })
        
        # Gamma hedging
        if abs(metrics.total_gamma) > self.max_position_size * 0.005:
            recommendations.append({
                'type': 'gamma_hedge',
                'action': 'reduce_position_size',
                'quantity': int(abs(metrics.total_gamma) / 10),
                'reason': 'Reduce gamma exposure'
            })
        
        # Theta hedging
        if metrics.total_theta < -self.max_position_size * 0.0005:
            recommendations.append({
                'type': 'theta_hedge',
                'action': 'roll_positions',
                'quantity': 'all',
                'reason': 'Reduce theta decay'
            })
        
        return recommendations
    
    def _calculate_delta(self, position: Position) -> float:
        """Calculate delta for a position (simplified)"""
        # This is a simplified delta calculation
        # In practice, use the actual option pricing model
        if position.option_type.lower() == 'call':
            return 0.5  # Simplified
        else:
            return -0.5  # Simplified
    
    def _calculate_gamma(self, position: Position) -> float:
        """Calculate gamma for a position (simplified)"""
        return 0.01  # Simplified
    
    def _calculate_theta(self, position: Position) -> float:
        """Calculate theta for a position (simplified)"""
        return -0.1  # Simplified
    
    def _calculate_vega(self, position: Position) -> float:
        """Calculate vega for a position (simplified)"""
        return 0.2  # Simplified
    
    def _calculate_rho(self, position: Position) -> float:
        """Calculate rho for a position (simplified)"""
        return 0.05  # Simplified
    
    def _calculate_var(self, portfolio_value: float, confidence_level: float = 0.95) -> Tuple[float, float]:
        """Calculate Value at Risk"""
        # Simplified VaR calculation
        # In practice, use historical simulation or Monte Carlo
        volatility = 0.2  # Assume 20% volatility
        var_95 = portfolio_value * volatility * 1.645  # 95% VaR
        var_99 = portfolio_value * volatility * 2.326  # 99% VaR
        return var_95, var_99
    
    def _calculate_max_drawdown(self) -> float:
        """Calculate maximum drawdown"""
        # Simplified calculation
        return 0.1  # 10% max drawdown
    
    def _calculate_sharpe_ratio(self) -> float:
        """Calculate Sharpe ratio"""
        # Simplified calculation
        return 1.5  # Assume 1.5 Sharpe ratio
    
    def _calculate_beta(self) -> float:
        """Calculate portfolio beta"""
        # Simplified calculation
        return 1.0  # Market beta

class PortfolioOptimizer:
    """Portfolio optimization for options strategies"""
    
    def __init__(self):
        self.risk_free_rate = 0.05
        self.market_volatility = 0.2
    
    def optimize_portfolio(self, strategies: List[Dict], 
                           available_capital: float) -> Dict:
        """Optimize portfolio allocation across strategies"""
        try:
            # Calculate expected returns and risks for each strategy
            strategy_metrics = []
            for strategy in strategies:
                expected_return = strategy.get('expected_return', 0.1)
                volatility = strategy.get('volatility', 0.2)
                sharpe_ratio = (expected_return - self.risk_free_rate) / volatility
                
                strategy_metrics.append({
                    'name': strategy['name'],
                    'expected_return': expected_return,
                    'volatility': volatility,
                    'sharpe_ratio': sharpe_ratio,
                    'max_allocation': strategy.get('max_allocation', 0.3)
                })
            
            # Sort by Sharpe ratio
            strategy_metrics.sort(key=lambda x: x['sharpe_ratio'], reverse=True)
            
            # Allocate capital based on Sharpe ratio
            total_allocation = 0
            allocations = {}
            
            for strategy in strategy_metrics:
                if total_allocation >= 1.0:
                    break
                
                # Allocate based on Sharpe ratio
                allocation = min(
                    strategy['sharpe_ratio'] / sum(s['sharpe_ratio'] for s in strategy_metrics),
                    strategy['max_allocation'],
                    1.0 - total_allocation
                )
                
                allocations[strategy['name']] = {
                    'allocation': allocation,
                    'capital': available_capital * allocation,
                    'expected_return': strategy['expected_return'],
                    'volatility': strategy['volatility']
                }
                
                total_allocation += allocation
            
            return {
                'allocations': allocations,
                'total_allocation': total_allocation,
                'expected_portfolio_return': sum(
                    a['capital'] * a['expected_return'] for a in allocations.values()
                ) / available_capital,
                'expected_portfolio_volatility': np.sqrt(sum(
                    (a['capital'] * a['volatility']) ** 2 for a in allocations.values()
                )) / available_capital
            }
            
        except Exception as e:
            logger.error(f"Error optimizing portfolio: {e}")
            return {}
    
    def calculate_correlation_matrix(self, strategies: List[Dict]) -> np.ndarray:
        """Calculate correlation matrix between strategies"""
        # Simplified correlation calculation
        # In practice, use historical returns data
        n_strategies = len(strategies)
        correlation_matrix = np.eye(n_strategies)
        
        # Add some correlation between similar strategies
        for i in range(n_strategies):
            for j in range(i+1, n_strategies):
                if strategies[i]['type'] == strategies[j]['type']:
                    correlation_matrix[i, j] = 0.7
                    correlation_matrix[j, i] = 0.7
                else:
                    correlation_matrix[i, j] = 0.3
                    correlation_matrix[j, i] = 0.3
        
        return correlation_matrix
