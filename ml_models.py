"""
Machine Learning Models for Options Trading
Implements ML models for strategy selection, volatility prediction, and price forecasting
"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import xgboost as xgb
import lightgbm as lgb
from typing import Dict, List, Tuple, Optional
import joblib
import logging
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

logger = logging.getLogger(__name__)

class FeatureEngineer:
    """Feature engineering for ML models"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
    
    def create_technical_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create technical indicators as features"""
        df = df.copy()
        
        # Price-based features
        df['returns'] = df['Close'].pct_change()
        df['log_returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df['price_change'] = df['Close'] - df['Open']
        df['price_range'] = df['High'] - df['Low']
        df['body_size'] = abs(df['Close'] - df['Open'])
        df['upper_shadow'] = df['High'] - df[['Open', 'Close']].max(axis=1)
        df['lower_shadow'] = df[['Open', 'Close']].min(axis=1) - df['Low']
        
        # Moving averages
        for window in [5, 10, 20, 50]:
            df[f'sma_{window}'] = df['Close'].rolling(window=window).mean()
            df[f'ema_{window}'] = df['Close'].ewm(span=window).mean()
        
        # Bollinger Bands
        df['bb_middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
        df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
        df['bb_width'] = df['bb_upper'] - df['bb_lower']
        df['bb_position'] = (df['Close'] - df['bb_lower']) / (df['bb_upper'] - df['bb_lower'])
        
        # RSI
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = df['Close'].ewm(span=12).mean()
        exp2 = df['Close'].ewm(span=26).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9).mean()
        df['macd_histogram'] = df['macd'] - df['macd_signal']
        
        # Volatility features
        df['volatility_5'] = df['returns'].rolling(window=5).std() * np.sqrt(252)
        df['volatility_10'] = df['returns'].rolling(window=10).std() * np.sqrt(252)
        df['volatility_20'] = df['returns'].rolling(window=20).std() * np.sqrt(252)
        
        # Volume features
        if 'Volume' in df.columns:
            df['volume_sma_10'] = df['Volume'].rolling(window=10).mean()
            df['volume_ratio'] = df['Volume'] / df['volume_sma_10']
            df['price_volume'] = df['Close'] * df['Volume']
        
        # Time-based features
        df['day_of_week'] = pd.to_datetime(df.index).dayofweek
        df['month'] = pd.to_datetime(df.index).month
        df['quarter'] = pd.to_datetime(df.index).quarter
        
        return df
    
    def create_options_features(self, spot_price: float, strike_prices: List[float], 
                              option_prices: Dict, volatility: float, 
                              time_to_expiry: float) -> Dict:
        """Create features specific to options trading"""
        features = {}
        
        # Moneyness features
        for strike in strike_prices:
            moneyness = spot_price / strike
            features[f'moneyness_{strike}'] = moneyness
            features[f'log_moneyness_{strike}'] = np.log(moneyness)
        
        # Volatility features
        features['volatility'] = volatility
        features['volatility_squared'] = volatility ** 2
        features['sqrt_time'] = np.sqrt(time_to_expiry)
        
        # Time decay features
        features['time_to_expiry'] = time_to_expiry
        features['time_squared'] = time_to_expiry ** 2
        
        # Price level features
        features['spot_price'] = spot_price
        features['log_spot'] = np.log(spot_price)
        
        return features
    
    def prepare_ml_dataset(self, df: pd.DataFrame, target_column: str) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare dataset for ML training"""
        # Create technical features
        df_features = self.create_technical_features(df)
        
        # Select feature columns
        feature_columns = [col for col in df_features.columns 
                         if col not in ['Open', 'High', 'Low', 'Close', 'Volume', target_column]]
        
        # Remove rows with NaN values
        df_clean = df_features[feature_columns + [target_column]].dropna()
        
        X = df_clean[feature_columns].values
        y = df_clean[target_column].values
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y

class StrategySelectorML:
    """ML-based strategy selection"""
    
    def __init__(self):
        self.model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.feature_engineer = FeatureEngineer()
        self.is_trained = False
    
    def prepare_training_data(self, historical_data: pd.DataFrame, 
                            strategy_performance: Dict) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for strategy selection"""
        # Create features from market data
        df_features = self.feature_engineer.create_technical_features(historical_data)
        
        # Add strategy performance as target
        df_features['strategy_performance'] = 0.0
        
        # Map strategy performance to historical data
        for date, performance in strategy_performance.items():
            if date in df_features.index:
                df_features.loc[date, 'strategy_performance'] = performance
        
        # Select features
        feature_columns = [col for col in df_features.columns 
                         if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'strategy_performance']]
        
        X = df_features[feature_columns].dropna()
        y = df_features.loc[X.index, 'strategy_performance']
        
        # Scale features
        X_scaled = self.feature_engineer.scaler.fit_transform(X)
        
        return X_scaled, y.values
    
    def train(self, historical_data: pd.DataFrame, strategy_performance: Dict):
        """Train the strategy selection model"""
        try:
            X, y = self.prepare_training_data(historical_data, strategy_performance)
            
            if len(X) == 0:
                logger.warning("No training data available")
                return
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            train_score = self.model.score(X_train, y_train)
            test_score = self.model.score(X_test, y_test)
            
            logger.info(f"Strategy selector training - Train score: {train_score:.4f}, Test score: {test_score:.4f}")
            
            self.is_trained = True
            
        except Exception as e:
            logger.error(f"Error training strategy selector: {e}")
    
    def predict_best_strategy(self, market_data: Dict) -> str:
        """Predict best strategy for current market conditions"""
        if not self.is_trained:
            return 'straddle'  # Default strategy
        
        try:
            # Create feature vector
            features = self._create_prediction_features(market_data)
            features_scaled = self.feature_engineer.scaler.transform([features])
            
            # Predict strategy
            prediction = self.model.predict(features_scaled)[0]
            
            # Map prediction to strategy name
            strategy_map = {0: 'straddle', 1: 'strangle', 2: 'iron_condor', 3: 'butterfly'}
            return strategy_map.get(prediction, 'straddle')
            
        except Exception as e:
            logger.error(f"Error predicting strategy: {e}")
            return 'straddle'
    
    def _create_prediction_features(self, market_data: Dict) -> List[float]:
        """Create feature vector for prediction"""
        features = []
        
        # Market features
        features.append(market_data.get('volatility', 0.2))
        features.append(market_data.get('trend', 0))
        features.append(market_data.get('volume_ratio', 1.0))
        features.append(market_data.get('rsi', 50))
        features.append(market_data.get('macd', 0))
        
        return features

class VolatilityPredictor:
    """ML model for volatility prediction"""
    
    def __init__(self):
        self.model = lgb.LGBMRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
        self.feature_engineer = FeatureEngineer()
        self.is_trained = False
    
    def prepare_training_data(self, historical_data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for volatility prediction"""
        # Create features
        df_features = self.feature_engineer.create_technical_features(historical_data)
        
        # Calculate realized volatility as target
        df_features['realized_vol'] = df_features['returns'].rolling(window=20).std() * np.sqrt(252)
        
        # Select features
        feature_columns = [col for col in df_features.columns 
                         if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'realized_vol']]
        
        # Remove NaN values
        df_clean = df_features[feature_columns + ['realized_vol']].dropna()
        
        X = df_clean[feature_columns].values
        y = df_clean['realized_vol'].values
        
        # Scale features
        X_scaled = self.feature_engineer.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train(self, historical_data: pd.DataFrame):
        """Train the volatility prediction model"""
        try:
            X, y = self.prepare_training_data(historical_data)
            
            if len(X) == 0:
                logger.warning("No training data available for volatility prediction")
                return
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logger.info(f"Volatility predictor training - MSE: {mse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")
            
            self.is_trained = True
            
        except Exception as e:
            logger.error(f"Error training volatility predictor: {e}")
    
    def predict_volatility(self, market_data: Dict) -> float:
        """Predict future volatility"""
        if not self.is_trained:
            return 0.2  # Default volatility
        
        try:
            # Create feature vector
            features = self._create_prediction_features(market_data)
            features_scaled = self.feature_engineer.scaler.transform([features])
            
            # Predict volatility
            prediction = self.model.predict(features_scaled)[0]
            return max(prediction, 0.01)  # Ensure positive volatility
            
        except Exception as e:
            logger.error(f"Error predicting volatility: {e}")
            return 0.2
    
    def _create_prediction_features(self, market_data: Dict) -> List[float]:
        """Create feature vector for volatility prediction"""
        features = []
        
        # Market features
        features.append(market_data.get('current_volatility', 0.2))
        features.append(market_data.get('avg_volatility', 0.2))
        features.append(market_data.get('rsi', 50))
        features.append(market_data.get('macd', 0))
        features.append(market_data.get('bb_width', 0))
        features.append(market_data.get('volume_ratio', 1.0))
        
        return features

class PricePredictor:
    """ML model for price prediction"""
    
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_engineer = FeatureEngineer()
        self.is_trained = False
    
    def prepare_training_data(self, historical_data: pd.DataFrame, 
                           prediction_horizon: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """Prepare training data for price prediction"""
        # Create features
        df_features = self.feature_engineer.create_technical_features(historical_data)
        
        # Create target (future price)
        df_features['future_price'] = df_features['Close'].shift(-prediction_horizon)
        
        # Select features
        feature_columns = [col for col in df_features.columns 
                         if col not in ['Open', 'High', 'Low', 'Close', 'Volume', 'future_price']]
        
        # Remove NaN values
        df_clean = df_features[feature_columns + ['future_price']].dropna()
        
        X = df_clean[feature_columns].values
        y = df_clean['future_price'].values
        
        # Scale features
        X_scaled = self.feature_engineer.scaler.fit_transform(X)
        
        return X_scaled, y
    
    def train(self, historical_data: pd.DataFrame, prediction_horizon: int = 5):
        """Train the price prediction model"""
        try:
            X, y = self.prepare_training_data(historical_data, prediction_horizon)
            
            if len(X) == 0:
                logger.warning("No training data available for price prediction")
                return
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Train model
            self.model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = self.model.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            logger.info(f"Price predictor training - MSE: {mse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}")
            
            self.is_trained = True
            
        except Exception as e:
            logger.error(f"Error training price predictor: {e}")
    
    def predict_price(self, market_data: Dict, current_price: float) -> float:
        """Predict future price"""
        if not self.is_trained:
            return current_price
        
        try:
            # Create feature vector
            features = self._create_prediction_features(market_data, current_price)
            features_scaled = self.feature_engineer.scaler.transform([features])
            
            # Predict price
            prediction = self.model.predict(features_scaled)[0]
            return max(prediction, 0)  # Ensure positive price
            
        except Exception as e:
            logger.error(f"Error predicting price: {e}")
            return current_price
    
    def _create_prediction_features(self, market_data: Dict, current_price: float) -> List[float]:
        """Create feature vector for price prediction"""
        features = []
        
        # Price features
        features.append(current_price)
        features.append(np.log(current_price))
        
        # Market features
        features.append(market_data.get('volatility', 0.2))
        features.append(market_data.get('rsi', 50))
        features.append(market_data.get('macd', 0))
        features.append(market_data.get('bb_position', 0.5))
        features.append(market_data.get('volume_ratio', 1.0))
        
        return features

class MLModelManager:
    """Manager for all ML models"""
    
    def __init__(self):
        self.strategy_selector = StrategySelectorML()
        self.volatility_predictor = VolatilityPredictor()
        self.price_predictor = PricePredictor()
        self.models_trained = False
    
    def train_all_models(self, historical_data: pd.DataFrame, 
                        strategy_performance: Dict = None):
        """Train all ML models"""
        try:
            logger.info("Training ML models...")
            
            # Train volatility predictor
            self.volatility_predictor.train(historical_data)
            
            # Train price predictor
            self.price_predictor.train(historical_data)
            
            # Train strategy selector if performance data is available
            if strategy_performance:
                self.strategy_selector.train(historical_data, strategy_performance)
            
            self.models_trained = True
            logger.info("All ML models trained successfully")
            
        except Exception as e:
            logger.error(f"Error training ML models: {e}")
    
    def get_predictions(self, market_data: Dict, current_price: float) -> Dict:
        """Get predictions from all models"""
        predictions = {}
        
        try:
            # Predict volatility
            predictions['volatility'] = self.volatility_predictor.predict_volatility(market_data)
            
            # Predict price
            predictions['price'] = self.price_predictor.predict_price(market_data, current_price)
            
            # Predict best strategy
            predictions['strategy'] = self.strategy_selector.predict_best_strategy(market_data)
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error getting predictions: {e}")
            return {
                'volatility': 0.2,
                'price': current_price,
                'strategy': 'straddle'
            }
    
    def save_models(self, filepath: str):
        """Save trained models"""
        try:
            model_data = {
                'strategy_selector': self.strategy_selector.model,
                'volatility_predictor': self.volatility_predictor.model,
                'price_predictor': self.price_predictor.model,
                'scaler': self.strategy_selector.feature_engineer.scaler
            }
            joblib.dump(model_data, filepath)
            logger.info(f"Models saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    def load_models(self, filepath: str):
        """Load trained models"""
        try:
            model_data = joblib.load(filepath)
            self.strategy_selector.model = model_data['strategy_selector']
            self.volatility_predictor.model = model_data['volatility_predictor']
            self.price_predictor.model = model_data['price_predictor']
            self.strategy_selector.feature_engineer.scaler = model_data['scaler']
            self.models_trained = True
            logger.info(f"Models loaded from {filepath}")
        except Exception as e:
            logger.error(f"Error loading models: {e}")
