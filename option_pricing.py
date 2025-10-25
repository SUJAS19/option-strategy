"""
Advanced Option Pricing Models
Implements Black-Scholes, Binomial, and Monte Carlo pricing models
"""
import numpy as np
import pandas as pd
from scipy.stats import norm
from scipy.optimize import minimize_scalar
import logging
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class OptionParams:
    """Option parameters container"""
    spot_price: float
    strike_price: float
    time_to_expiry: float  # in years
    risk_free_rate: float
    volatility: float
    dividend_yield: float = 0.0

class BlackScholesPricer:
    """Black-Scholes option pricing model"""
    
    @staticmethod
    def calculate_price(params: OptionParams, option_type: str) -> float:
        """Calculate option price using Black-Scholes formula"""
        S = params.spot_price
        K = params.strike_price
        T = params.time_to_expiry
        r = params.risk_free_rate
        sigma = params.volatility
        q = params.dividend_yield
        
        if T <= 0:
            return max(S - K, 0) if option_type.lower() == 'call' else max(K - S, 0)
        
        d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type.lower() == 'call':
            price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        
        return max(price, 0.0)
    
    @staticmethod
    def calculate_greeks(params: OptionParams, option_type: str) -> Dict[str, float]:
        """Calculate option Greeks"""
        S = params.spot_price
        K = params.strike_price
        T = params.time_to_expiry
        r = params.risk_free_rate
        sigma = params.volatility
        q = params.dividend_yield
        
        if T <= 0:
            return {'delta': 0, 'gamma': 0, 'theta': 0, 'vega': 0, 'rho': 0}
        
        d1 = (np.log(S/K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        # Delta
        if option_type.lower() == 'call':
            delta = np.exp(-q * T) * norm.cdf(d1)
        else:
            delta = -np.exp(-q * T) * norm.cdf(-d1)
        
        # Gamma
        gamma = np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
        
        # Theta
        if option_type.lower() == 'call':
            theta = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                    - r * K * np.exp(-r * T) * norm.cdf(d2) 
                    + q * S * np.exp(-q * T) * norm.cdf(d1)) / 365
        else:
            theta = (-S * np.exp(-q * T) * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                    + r * K * np.exp(-r * T) * norm.cdf(-d2) 
                    - q * S * np.exp(-q * T) * norm.cdf(-d1)) / 365
        
        # Vega
        vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) / 100
        
        # Rho
        if option_type.lower() == 'call':
            rho = K * T * np.exp(-r * T) * norm.cdf(d2) / 100
        else:
            rho = -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        
        return {
            'delta': delta,
            'gamma': gamma,
            'theta': theta,
            'vega': vega,
            'rho': rho
        }
    
    @staticmethod
    def implied_volatility(market_price: float, params: OptionParams, 
                          option_type: str, max_iterations: int = 100) -> float:
        """Calculate implied volatility using Newton-Raphson method"""
        def objective(vol):
            params.volatility = vol
            theoretical_price = BlackScholesPricer.calculate_price(params, option_type)
            return (theoretical_price - market_price) ** 2
        
        try:
            result = minimize_scalar(objective, bounds=(0.01, 5.0), method='bounded')
            return result.x if result.success else None
        except:
            return None

class BinomialPricer:
    """Binomial option pricing model"""
    
    @staticmethod
    def calculate_price(params: OptionParams, option_type: str, 
                       steps: int = 100) -> float:
        """Calculate option price using binomial model"""
        S = params.spot_price
        K = params.strike_price
        T = params.time_to_expiry
        r = params.risk_free_rate
        sigma = params.volatility
        q = params.dividend_yield
        
        if T <= 0:
            return max(S - K, 0) if option_type.lower() == 'call' else max(K - S, 0)
        
        dt = T / steps
        u = np.exp(sigma * np.sqrt(dt))
        d = 1 / u
        p = (np.exp((r - q) * dt) - d) / (u - d)
        
        # Initialize stock prices at maturity
        stock_prices = np.zeros(steps + 1)
        for i in range(steps + 1):
            stock_prices[i] = S * (u ** (steps - i)) * (d ** i)
        
        # Initialize option values at maturity
        option_values = np.zeros(steps + 1)
        for i in range(steps + 1):
            if option_type.lower() == 'call':
                option_values[i] = max(stock_prices[i] - K, 0)
            else:
                option_values[i] = max(K - stock_prices[i], 0)
        
        # Backward induction
        for step in range(steps - 1, -1, -1):
            for i in range(step + 1):
                option_values[i] = (p * option_values[i] + 
                                  (1 - p) * option_values[i + 1]) * np.exp(-r * dt)
        
        return option_values[0]

class MonteCarloPricer:
    """Monte Carlo option pricing model"""
    
    @staticmethod
    def calculate_price(params: OptionParams, option_type: str, 
                      simulations: int = 100000) -> Tuple[float, float]:
        """Calculate option price using Monte Carlo simulation"""
        S = params.spot_price
        K = params.strike_price
        T = params.time_to_expiry
        r = params.risk_free_rate
        sigma = params.volatility
        q = params.dividend_yield
        
        if T <= 0:
            payoff = max(S - K, 0) if option_type.lower() == 'call' else max(K - S, 0)
            return payoff, 0.0
        
        # Generate random stock prices
        np.random.seed(42)  # For reproducibility
        Z = np.random.standard_normal(simulations)
        ST = S * np.exp((r - q - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)
        
        # Calculate payoffs
        if option_type.lower() == 'call':
            payoffs = np.maximum(ST - K, 0)
        else:
            payoffs = np.maximum(K - ST, 0)
        
        # Discount to present value
        option_price = np.exp(-r * T) * np.mean(payoffs)
        standard_error = np.exp(-r * T) * np.std(payoffs) / np.sqrt(simulations)
        
        return option_price, standard_error

class VolatilitySurface:
    """Volatility surface for options pricing"""
    
    def __init__(self):
        self.surface_data = {}
    
    def add_volatility_point(self, strike: float, expiry: float, iv: float):
        """Add a volatility point to the surface"""
        key = (strike, expiry)
        self.surface_data[key] = iv
    
    def get_volatility(self, strike: float, expiry: float) -> float:
        """Get volatility for given strike and expiry"""
        key = (strike, expiry)
        if key in self.surface_data:
            return self.surface_data[key]
        
        # Interpolate if not found
        return self._interpolate_volatility(strike, expiry)
    
    def _interpolate_volatility(self, strike: float, expiry: float) -> float:
        """Interpolate volatility from surface data"""
        if not self.surface_data:
            return 0.2  # Default volatility
        
        # Simple interpolation - in practice, use more sophisticated methods
        strikes = [k[0] for k in self.surface_data.keys()]
        expiries = [k[1] for k in self.surface_data.keys()]
        
        # Find closest points
        closest_strike = min(strikes, key=lambda x: abs(x - strike))
        closest_expiry = min(expiries, key=lambda x: abs(x - expiry))
        
        return self.surface_data.get((closest_strike, closest_expiry), 0.2)

class OptionPricingEngine:
    """Main option pricing engine"""
    
    def __init__(self):
        self.bs_pricer = BlackScholesPricer()
        self.binomial_pricer = BinomialPricer()
        self.mc_pricer = MonteCarloPricer()
        self.vol_surface = VolatilitySurface()
    
    def price_option(self, params: OptionParams, option_type: str, 
                    method: str = 'black_scholes') -> Dict:
        """Price an option using specified method"""
        try:
            if method == 'black_scholes':
                price = self.bs_pricer.calculate_price(params, option_type)
                greeks = self.bs_pricer.calculate_greeks(params, option_type)
                return {
                    'price': price,
                    'greeks': greeks,
                    'method': 'black_scholes'
                }
            elif method == 'binomial':
                price = self.binomial_pricer.calculate_price(params, option_type)
                return {
                    'price': price,
                    'method': 'binomial'
                }
            elif method == 'monte_carlo':
                price, std_error = self.mc_pricer.calculate_price(params, option_type)
                return {
                    'price': price,
                    'standard_error': std_error,
                    'method': 'monte_carlo'
                }
            else:
                raise ValueError(f"Unknown pricing method: {method}")
                
        except Exception as e:
            logger.error(f"Error pricing option: {e}")
            return {'price': 0, 'error': str(e)}
    
    def calculate_portfolio_greeks(self, positions: List[Dict]) -> Dict[str, float]:
        """Calculate portfolio Greeks"""
        total_delta = 0
        total_gamma = 0
        total_theta = 0
        total_vega = 0
        total_rho = 0
        
        for position in positions:
            params = OptionParams(
                spot_price=position['spot_price'],
                strike_price=position['strike_price'],
                time_to_expiry=position['time_to_expiry'],
                risk_free_rate=position['risk_free_rate'],
                volatility=position['volatility']
            )
            
            greeks = self.bs_pricer.calculate_greeks(params, position['option_type'])
            quantity = position['quantity']
            
            total_delta += greeks['delta'] * quantity
            total_gamma += greeks['gamma'] * quantity
            total_theta += greeks['theta'] * quantity
            total_vega += greeks['vega'] * quantity
            total_rho += greeks['rho'] * quantity
        
        return {
            'delta': total_delta,
            'gamma': total_gamma,
            'theta': total_theta,
            'vega': total_vega,
            'rho': total_rho
        }
