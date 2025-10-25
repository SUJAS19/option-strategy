"""
Backtesting Framework for Options Strategies
Comprehensive backtesting system for NIFTY options strategies
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from option_strategies import StrategySelector, StraddleStrategy, StrangleStrategy, IronCondorStrategy, ButterflyStrategy
from option_pricing import OptionParams, OptionPricingEngine
from risk_management import RiskManager, Position
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

@dataclass
class BacktestResult:
    """Backtest result container"""
    total_return: float
    annualized_return: float
    volatility: float
    sharpe_ratio: float
    max_drawdown: float
    win_rate: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    max_win: float
    max_loss: float

@dataclass
class Trade:
    """Trade data structure"""
    entry_date: datetime
    exit_date: datetime
    strategy: str
    entry_price: float
    exit_price: float
    quantity: int
    pnl: float
    return_pct: float
    duration: int  # days

class BacktestEngine:
    """Main backtesting engine"""
    
    def __init__(self, initial_capital: float = 1000000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.positions = []
        self.trades = []
        self.equity_curve = []
        self.strategy_selector = StrategySelector()
        self.pricing_engine = OptionPricingEngine()
        self.risk_manager = RiskManager()
        
    def run_backtest(self, historical_data: pd.DataFrame, 
                    start_date: str, end_date: str,
                    strategies: List[str] = None) -> BacktestResult:
        """Run comprehensive backtest"""
        try:
            logger.info(f"Starting backtest from {start_date} to {end_date}")
            
            # Filter data by date range
            start_dt = pd.to_datetime(start_date)
            end_dt = pd.to_datetime(end_date)
            data = historical_data[(historical_data.index >= start_dt) & 
                                  (historical_data.index <= end_dt)].copy()
            
            if data.empty:
                logger.error("No data available for backtest period")
                return self._create_empty_result()
            
            # Initialize tracking variables
            self.current_capital = self.initial_capital
            self.positions = []
            self.trades = []
            self.equity_curve = []
            
            # Run backtest day by day
            for i, (date, row) in enumerate(data.iterrows()):
                self._process_day(date, row, data, strategies)
                self._update_equity_curve(date)
            
            # Close any remaining positions
            self._close_all_positions(data.iloc[-1])
            
            # Calculate results
            result = self._calculate_results()
            logger.info(f"Backtest completed. Total return: {result.total_return:.2%}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in backtest: {e}")
            return self._create_empty_result()
    
    def _process_day(self, date: datetime, row: pd.Series, 
                    data: pd.DataFrame, strategies: List[str]):
        """Process a single day of backtesting"""
        try:
            # Check for exit signals on existing positions
            self._check_exit_signals(date, row)
            
            # Check for entry signals
            if self._should_enter_trade(date, row, data):
                strategy = self._select_strategy(date, row, strategies)
                if strategy:
                    self._enter_trade(date, row, strategy)
            
            # Update position values
            self._update_position_values(date, row)
            
        except Exception as e:
            logger.error(f"Error processing day {date}: {e}")
    
    def _should_enter_trade(self, date: datetime, row: pd.Series, 
                           data: pd.DataFrame) -> bool:
        """Determine if we should enter a new trade"""
        # Simple entry logic - can be enhanced with ML models
        if len(self.positions) > 0:
            return False  # Don't open new positions if we have existing ones
        
        # Check if we have enough capital
        if self.current_capital < 100000:  # Minimum capital requirement
            return False
        
        # Check market conditions
        volatility = self._calculate_volatility(data, date)
        if volatility < 0.15 or volatility > 0.5:
            return False
        
        return True
    
    def _select_strategy(self, date: datetime, row: pd.Series, 
                        strategies: List[str]) -> str:
        """Select strategy based on market conditions"""
        if not strategies:
            strategies = ['straddle', 'strangle', 'iron_condor', 'butterfly']
        
        # Simple strategy selection based on volatility
        volatility = self._calculate_volatility(pd.DataFrame([row]), date)
        
        if volatility > 0.3:
            return 'straddle'
        elif volatility > 0.25:
            return 'strangle'
        elif volatility < 0.2:
            return 'iron_condor'
        else:
            return 'butterfly'
    
    def _enter_trade(self, date: datetime, row: pd.Series, strategy: str):
        """Enter a new trade"""
        try:
            spot_price = row['Close']
            strike_price = self._get_atm_strike(spot_price)
            expiry_date = self._get_next_expiry(date)
            
            # Calculate option prices (simplified)
            call_price = self._calculate_option_price(spot_price, strike_price, 
                                                    expiry_date, 'call')
            put_price = self._calculate_option_price(spot_price, strike_price, 
                                                   expiry_date, 'put')
            
            # Calculate position size
            position_size = self._calculate_position_size(call_price + put_price)
            
            if position_size > 0:
                # Create straddle position
                call_position = Position(
                    symbol=f"NIFTY{strike_price}CE",
                    option_type='call',
                    strike_price=strike_price,
                    expiry_date=expiry_date,
                    quantity=position_size,
                    entry_price=call_price,
                    current_price=call_price,
                    entry_time=date,
                    strategy_name=strategy
                )
                
                put_position = Position(
                    symbol=f"NIFTY{strike_price}PE",
                    option_type='put',
                    strike_price=strike_price,
                    expiry_date=expiry_date,
                    quantity=position_size,
                    entry_price=put_price,
                    current_price=put_price,
                    entry_time=date,
                    strategy_name=strategy
                )
                
                self.positions.extend([call_position, put_position])
                self.current_capital -= (call_price + put_price) * position_size * 50  # 50 is lot size
                
                logger.info(f"Entered {strategy} trade: {position_size} contracts at {spot_price}")
                
        except Exception as e:
            logger.error(f"Error entering trade: {e}")
    
    def _check_exit_signals(self, date: datetime, row: pd.Series):
        """Check for exit signals on existing positions"""
        positions_to_close = []
        
        for position in self.positions:
            should_exit, reason = self.risk_manager.should_exit_position(
                position, position.current_price
            )
            
            if should_exit:
                positions_to_close.append((position, reason))
        
        # Close positions
        for position, reason in positions_to_close:
            self._close_position(position, date, row, reason)
    
    def _close_position(self, position: Position, date: datetime, 
                       row: pd.Series, reason: str):
        """Close a position"""
        try:
            # Calculate P&L
            pnl = (position.current_price - position.entry_price) * position.quantity * 50
            return_pct = (position.current_price - position.entry_price) / position.entry_price
            
            # Create trade record
            trade = Trade(
                entry_date=position.entry_time,
                exit_date=date,
                strategy=position.strategy_name,
                entry_price=position.entry_price,
                exit_price=position.current_price,
                quantity=position.quantity,
                pnl=pnl,
                return_pct=return_pct,
                duration=(date - position.entry_time).days
            )
            
            self.trades.append(trade)
            self.current_capital += pnl
            
            # Remove position
            self.positions.remove(position)
            
            logger.info(f"Closed position: {position.symbol} P&L: {pnl:.2f} Reason: {reason}")
            
        except Exception as e:
            logger.error(f"Error closing position: {e}")
    
    def _close_all_positions(self, last_row: pd.Series):
        """Close all remaining positions at the end of backtest"""
        for position in self.positions.copy():
            self._close_position(position, last_row.name, last_row, 'end_of_backtest')
    
    def _update_position_values(self, date: datetime, row: pd.Series):
        """Update current values of all positions"""
        for position in self.positions:
            # Calculate new option price based on current spot
            new_price = self._calculate_option_price(
                row['Close'], position.strike_price, 
                position.expiry_date, position.option_type
            )
            position.current_price = new_price
    
    def _update_equity_curve(self, date: datetime):
        """Update equity curve"""
        position_value = sum(pos.current_price * pos.quantity * 50 for pos in self.positions)
        total_value = self.current_capital + position_value
        self.equity_curve.append({
            'date': date,
            'equity': total_value,
            'capital': self.current_capital,
            'positions': len(self.positions)
        })
    
    def _calculate_results(self) -> BacktestResult:
        """Calculate comprehensive backtest results"""
        if not self.equity_curve:
            return self._create_empty_result()
        
        # Calculate basic metrics
        initial_equity = self.equity_curve[0]['equity']
        final_equity = self.equity_curve[-1]['equity']
        total_return = (final_equity - initial_equity) / initial_equity
        
        # Calculate annualized return
        days = (self.equity_curve[-1]['date'] - self.equity_curve[0]['date']).days
        annualized_return = (1 + total_return) ** (365 / days) - 1
        
        # Calculate volatility
        equity_values = [point['equity'] for point in self.equity_curve]
        returns = np.diff(equity_values) / equity_values[:-1]
        volatility = np.std(returns) * np.sqrt(252)
        
        # Calculate Sharpe ratio
        risk_free_rate = 0.05
        sharpe_ratio = (annualized_return - risk_free_rate) / volatility if volatility > 0 else 0
        
        # Calculate maximum drawdown
        peak = np.maximum.accumulate(equity_values)
        drawdown = (equity_values - peak) / peak
        max_drawdown = np.min(drawdown)
        
        # Calculate trade statistics
        if self.trades:
            winning_trades = [t for t in self.trades if t.pnl > 0]
            losing_trades = [t for t in self.trades if t.pnl < 0]
            
            win_rate = len(winning_trades) / len(self.trades)
            avg_win = np.mean([t.pnl for t in winning_trades]) if winning_trades else 0
            avg_loss = np.mean([t.pnl for t in losing_trades]) if losing_trades else 0
            max_win = max([t.pnl for t in self.trades]) if self.trades else 0
            max_loss = min([t.pnl for t in self.trades]) if self.trades else 0
            
            profit_factor = abs(avg_win / avg_loss) if avg_loss != 0 else float('inf')
        else:
            win_rate = 0
            avg_win = 0
            avg_loss = 0
            max_win = 0
            max_loss = 0
            profit_factor = 0
        
        return BacktestResult(
            total_return=total_return,
            annualized_return=annualized_return,
            volatility=volatility,
            sharpe_ratio=sharpe_ratio,
            max_drawdown=max_drawdown,
            win_rate=win_rate,
            profit_factor=profit_factor,
            total_trades=len(self.trades),
            winning_trades=len([t for t in self.trades if t.pnl > 0]),
            losing_trades=len([t for t in self.trades if t.pnl < 0]),
            avg_win=avg_win,
            avg_loss=avg_loss,
            max_win=max_win,
            max_loss=max_loss
        )
    
    def _create_empty_result(self) -> BacktestResult:
        """Create empty result when backtest fails"""
        return BacktestResult(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    
    def _calculate_volatility(self, data: pd.DataFrame, date: datetime) -> float:
        """Calculate historical volatility"""
        if len(data) < 20:
            return 0.2  # Default volatility
        
        returns = data['Close'].pct_change().dropna()
        return returns.std() * np.sqrt(252)
    
    def _get_atm_strike(self, spot_price: float) -> float:
        """Get at-the-money strike price"""
        return round(spot_price / 50) * 50  # Round to nearest 50
    
    def _get_next_expiry(self, date: datetime) -> str:
        """Get next Thursday expiry date"""
        days_ahead = (3 - date.weekday()) % 7  # Thursday is 3
        if days_ahead == 0:
            days_ahead = 7
        expiry_date = date + timedelta(days=days_ahead)
        return expiry_date.strftime('%Y-%m-%d')
    
    def _calculate_option_price(self, spot: float, strike: float, 
                              expiry: str, option_type: str) -> float:
        """Calculate option price using Black-Scholes"""
        try:
            expiry_date = datetime.strptime(expiry, '%Y-%m-%d')
            time_to_expiry = (expiry_date - datetime.now()).days / 365.0
            
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
    
    def _calculate_position_size(self, option_price: float) -> int:
        """Calculate position size based on risk management"""
        max_risk = self.current_capital * 0.02  # 2% risk per trade
        position_value = option_price * 50  # 50 is lot size
        return int(max_risk / position_value) if position_value > 0 else 0

class BacktestAnalyzer:
    """Analyzer for backtest results"""
    
    def __init__(self):
        self.results = []
    
    def add_result(self, result: BacktestResult, strategy_name: str):
        """Add a backtest result"""
        self.results.append({
            'strategy': strategy_name,
            'result': result
        })
    
    def compare_strategies(self) -> pd.DataFrame:
        """Compare performance of different strategies"""
        if not self.results:
            return pd.DataFrame()
        
        comparison_data = []
        for result_data in self.results:
            result = result_data['result']
            comparison_data.append({
                'Strategy': result_data['strategy'],
                'Total Return': f"{result.total_return:.2%}",
                'Annualized Return': f"{result.annualized_return:.2%}",
                'Volatility': f"{result.volatility:.2%}",
                'Sharpe Ratio': f"{result.sharpe_ratio:.2f}",
                'Max Drawdown': f"{result.max_drawdown:.2%}",
                'Win Rate': f"{result.win_rate:.2%}",
                'Profit Factor': f"{result.profit_factor:.2f}",
                'Total Trades': result.total_trades
            })
        
        return pd.DataFrame(comparison_data)
    
    def plot_equity_curve(self, equity_curve: List[Dict], title: str = "Equity Curve"):
        """Plot equity curve"""
        if not equity_curve:
            return
        
        dates = [point['date'] for point in equity_curve]
        equity = [point['equity'] for point in equity_curve]
        
        plt.figure(figsize=(12, 6))
        plt.plot(dates, equity, linewidth=2)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def plot_drawdown(self, equity_curve: List[Dict], title: str = "Drawdown"):
        """Plot drawdown chart"""
        if not equity_curve:
            return
        
        dates = [point['date'] for point in equity_curve]
        equity = [point['equity'] for point in equity_curve]
        
        peak = np.maximum.accumulate(equity)
        drawdown = (np.array(equity) - peak) / peak * 100
        
        plt.figure(figsize=(12, 6))
        plt.fill_between(dates, drawdown, 0, alpha=0.3, color='red')
        plt.plot(dates, drawdown, color='red', linewidth=1)
        plt.title(title)
        plt.xlabel('Date')
        plt.ylabel('Drawdown (%)')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
    
    def generate_report(self, result: BacktestResult, strategy_name: str) -> str:
        """Generate comprehensive backtest report"""
        report = f"""
        ========================================
        BACKTEST REPORT: {strategy_name.upper()}
        ========================================
        
        PERFORMANCE METRICS:
        -------------------
        Total Return:        {result.total_return:.2%}
        Annualized Return:  {result.annualized_return:.2%}
        Volatility:         {result.volatility:.2%}
        Sharpe Ratio:       {result.sharpe_ratio:.2f}
        Max Drawdown:       {result.max_drawdown:.2%}
        
        TRADE STATISTICS:
        -----------------
        Total Trades:       {result.total_trades}
        Winning Trades:     {result.winning_trades}
        Losing Trades:      {result.losing_trades}
        Win Rate:          {result.win_rate:.2%}
        Profit Factor:     {result.profit_factor:.2f}
        
        TRADE ANALYSIS:
        ---------------
        Average Win:        {result.avg_win:.2f}
        Average Loss:       {result.avg_loss:.2f}
        Max Win:           {result.max_win:.2f}
        Max Loss:          {result.max_loss:.2f}
        
        ========================================
        """
        return report
