"""
Data Fetcher for NIFTY Options Data
Handles real-time and historical data fetching from multiple sources
"""
import pandas as pd
import numpy as np
import yfinance as yf
from nsepy import get_history
from datetime import datetime, timedelta
import requests
import time
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class NIFTYDataFetcher:
    """Fetches NIFTY options data from multiple sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def get_nifty_spot_price(self) -> float:
        """Get current NIFTY spot price"""
        try:
            nifty = yf.Ticker("^NSEI")
            data = nifty.history(period="1d")
            return float(data['Close'].iloc[-1])
        except Exception as e:
            logger.error(f"Error fetching NIFTY spot price: {e}")
            return None
    
    def get_options_chain(self, expiry_date: str = None) -> pd.DataFrame:
        """Get options chain for NIFTY"""
        try:
            if not expiry_date:
                # Get next Thursday (NIFTY expiry)
                today = datetime.now()
                days_ahead = (3 - today.weekday()) % 7  # Thursday is 3
                if days_ahead == 0:
                    days_ahead = 7
                expiry_date = (today + timedelta(days=days_ahead)).strftime('%d-%b-%Y')
            
            # This is a simplified version - in practice, you'd use NSE API
            # For now, we'll create synthetic data
            spot_price = self.get_nifty_spot_price()
            if not spot_price:
                return pd.DataFrame()
            
            # Generate synthetic options data
            strikes = np.arange(int(spot_price * 0.8), int(spot_price * 1.2), 50)
            options_data = []
            
            for strike in strikes:
                # Call options
                call_price = self._calculate_option_price(spot_price, strike, 0.2, 0.05, 15, 'call')
                options_data.append({
                    'strike': strike,
                    'type': 'CE',
                    'price': call_price,
                    'volume': np.random.randint(100, 1000),
                    'oi': np.random.randint(1000, 10000)
                })
                
                # Put options
                put_price = self._calculate_option_price(spot_price, strike, 0.2, 0.05, 15, 'put')
                options_data.append({
                    'strike': strike,
                    'type': 'PE',
                    'price': put_price,
                    'volume': np.random.randint(100, 1000),
                    'oi': np.random.randint(1000, 10000)
                })
            
            return pd.DataFrame(options_data)
            
        except Exception as e:
            logger.error(f"Error fetching options chain: {e}")
            return pd.DataFrame()
    
    def get_historical_data(self, symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
        """Get historical data for NIFTY"""
        try:
            data = get_history(
                symbol=symbol,
                start=datetime.strptime(start_date, '%Y-%m-%d'),
                end=datetime.strptime(end_date, '%Y-%m-%d')
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data: {e}")
            return pd.DataFrame()
    
    def get_volatility_data(self, days: int = 30) -> pd.DataFrame:
        """Get historical volatility data"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            data = self.get_historical_data("NIFTY 50", start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
            
            if data.empty:
                return pd.DataFrame()
            
            # Calculate daily returns and volatility
            data['returns'] = data['Close'].pct_change()
            data['volatility'] = data['returns'].rolling(window=20).std() * np.sqrt(252)
            
            return data[['Close', 'returns', 'volatility']].dropna()
            
        except Exception as e:
            logger.error(f"Error fetching volatility data: {e}")
            return pd.DataFrame()
    
    def _calculate_option_price(self, spot: float, strike: float, iv: float, 
                              risk_free_rate: float, days_to_expiry: int, 
                              option_type: str) -> float:
        """Calculate option price using Black-Scholes model"""
        from scipy.stats import norm
        
        S = spot
        K = strike
        r = risk_free_rate
        T = days_to_expiry / 365.0
        sigma = iv
        
        d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type.lower() == 'call':
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return max(price, 0.05)  # Minimum price of 5 paisa
    
    def get_market_indicators(self) -> Dict:
        """Get various market indicators"""
        try:
            spot_price = self.get_nifty_spot_price()
            volatility_data = self.get_volatility_data(30)
            
            indicators = {
                'spot_price': spot_price,
                'current_volatility': volatility_data['volatility'].iloc[-1] if not volatility_data.empty else 0.2,
                'avg_volatility': volatility_data['volatility'].mean() if not volatility_data.empty else 0.2,
                'vix': self._get_vix()  # Simplified VIX calculation
            }
            
            return indicators
            
        except Exception as e:
            logger.error(f"Error fetching market indicators: {e}")
            return {}
    
    def _get_vix(self) -> float:
        """Get VIX equivalent for Indian markets"""
        try:
            # This is a simplified VIX calculation
            # In practice, you'd use NSE VIX data
            return 20.0  # Placeholder
        except:
            return 20.0
