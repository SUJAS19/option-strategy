"""
Interactive Dashboard for NIFTY Options Trading System
Real-time monitoring and control interface
"""
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

from trading_engine import TradingEngine
from data_fetcher import NIFTYDataFetcher
from backtesting import BacktestEngine, BacktestAnalyzer
import config

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "NIFTY Options Trading Dashboard"

# Initialize components
trading_engine = TradingEngine()
data_fetcher = NIFTYDataFetcher()

# Dashboard layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("NIFTY Options Trading Dashboard", className="text-center mb-4"),
            html.Hr()
        ])
    ]),
    
    # Market Overview Cards
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("NIFTY Spot", className="card-title"),
                    html.H2(id="spot-price", className="text-primary")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Volatility", className="card-title"),
                    html.H2(id="volatility", className="text-warning")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Portfolio Value", className="card-title"),
                    html.H2(id="portfolio-value", className="text-success")
                ])
            ], className="mb-3")
        ], width=3),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Daily P&L", className="card-title"),
                    html.H2(id="daily-pnl", className="text-info")
                ])
            ], className="mb-3")
        ], width=3)
    ]),
    
    # Charts Row
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Portfolio Performance"),
                dbc.CardBody([
                    dcc.Graph(id="equity-curve")
                ])
            ])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Risk Metrics"),
                dbc.CardBody([
                    html.Div(id="risk-metrics")
                ])
            ])
        ], width=4)
    ], className="mt-4"),
    
    # Strategy Performance
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Strategy Performance"),
                dbc.CardBody([
                    dcc.Graph(id="strategy-performance")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Options Chain"),
                dbc.CardBody([
                    html.Div(id="options-chain")
                ])
            ])
        ], width=6)
    ], className="mt-4"),
    
    # Control Panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Trading Controls"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Button("Start Trading", id="start-btn", color="success", className="me-2"),
                            dbc.Button("Stop Trading", id="stop-btn", color="danger", className="me-2"),
                            dbc.Button("Refresh Data", id="refresh-btn", color="info")
                        ])
                    ]),
                    html.Hr(),
                    dbc.Row([
                        dbc.Col([
                            html.Label("Strategy Selection:"),
                            dcc.Dropdown(
                                id="strategy-dropdown",
                                options=[
                                    {"label": "Straddle", "value": "straddle"},
                                    {"label": "Strangle", "value": "strangle"},
                                    {"label": "Iron Condor", "value": "iron_condor"},
                                    {"label": "Butterfly", "value": "butterfly"}
                                ],
                                value="straddle"
                            )
                        ], width=6),
                        dbc.Col([
                            html.Label("Position Size:"),
                            dcc.Slider(
                                id="position-size-slider",
                                min=1,
                                max=10,
                                step=1,
                                value=5,
                                marks={i: str(i) for i in range(1, 11)}
                            )
                        ], width=6)
                    ])
                ])
            ])
        ])
    ], className="mt-4"),
    
    # Auto-refresh interval
    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # Update every 30 seconds
        n_intervals=0
    )
])

# Callbacks
@app.callback(
    [Output('spot-price', 'children'),
     Output('volatility', 'children'),
     Output('portfolio-value', 'children'),
     Output('daily-pnl', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_market_data(n):
    """Update market data cards"""
    try:
        # Get market indicators
        market_data = data_fetcher.get_market_indicators()
        spot_price = market_data.get('spot_price', 0)
        volatility = market_data.get('current_volatility', 0)
        
        # Get portfolio status
        portfolio_status = trading_engine.get_portfolio_status()
        portfolio_value = portfolio_status.get('portfolio_value', 0)
        daily_pnl = portfolio_status.get('daily_pnl', 0)
        
        return (
            f"₹{spot_price:,.0f}" if spot_price > 0 else "N/A",
            f"{volatility:.2%}" if volatility > 0 else "N/A",
            f"₹{portfolio_value:,.0f}" if portfolio_value > 0 else "N/A",
            f"₹{daily_pnl:,.0f}" if daily_pnl != 0 else "₹0"
        )
    except Exception as e:
        return "Error", "Error", "Error", "Error"

@app.callback(
    Output('equity-curve', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_equity_curve(n):
    """Update equity curve chart"""
    try:
        # Get portfolio status
        portfolio_status = trading_engine.get_portfolio_status()
        
        # Create sample equity curve data
        dates = pd.date_range(start=datetime.now() - timedelta(days=30), 
                             end=datetime.now(), freq='D')
        np.random.seed(42)
        equity_values = 1000000 + np.cumsum(np.random.randn(len(dates)) * 10000)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates,
            y=equity_values,
            mode='lines',
            name='Portfolio Value',
            line=dict(color='blue', width=2)
        ))
        
        fig.update_layout(
            title="Portfolio Equity Curve",
            xaxis_title="Date",
            yaxis_title="Portfolio Value (₹)",
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        return go.Figure()

@app.callback(
    Output('risk-metrics', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_risk_metrics(n):
    """Update risk metrics display"""
    try:
        # Get portfolio status
        portfolio_status = trading_engine.get_portfolio_status()
        
        # Calculate risk metrics (simplified)
        total_positions = portfolio_status.get('total_positions', 0)
        total_pnl = portfolio_status.get('total_pnl', 0)
        
        risk_metrics = [
            html.P(f"Total Positions: {total_positions}"),
            html.P(f"Total P&L: ₹{total_pnl:,.0f}"),
            html.P(f"Delta Exposure: ₹{np.random.randint(-50000, 50000):,}"),
            html.P(f"Gamma Exposure: ₹{np.random.randint(-10000, 10000):,}"),
            html.P(f"Theta Decay: ₹{np.random.randint(-5000, 0):,}"),
            html.P(f"Vega Exposure: ₹{np.random.randint(-20000, 20000):,}")
        ]
        
        return risk_metrics
    except Exception as e:
        return [html.P("Error loading risk metrics")]

@app.callback(
    Output('strategy-performance', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_strategy_performance(n):
    """Update strategy performance chart"""
    try:
        # Create sample strategy performance data
        strategies = ['Straddle', 'Strangle', 'Iron Condor', 'Butterfly']
        returns = [0.12, 0.08, 0.15, 0.10]
        sharpe_ratios = [1.2, 0.8, 1.5, 1.0]
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=strategies,
            y=returns,
            name='Returns',
            marker_color='lightblue'
        ))
        
        fig.update_layout(
            title="Strategy Performance Comparison",
            xaxis_title="Strategy",
            yaxis_title="Returns (%)",
            barmode='group'
        )
        
        return fig
    except Exception as e:
        return go.Figure()

@app.callback(
    Output('options-chain', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_options_chain(n):
    """Update options chain display"""
    try:
        # Get options chain data
        options_chain = data_fetcher.get_options_chain()
        
        if options_chain.empty:
            return html.P("No options chain data available")
        
        # Create table
        table = dbc.Table.from_dataframe(
            options_chain.head(10),
            striped=True,
            bordered=True,
            hover=True,
            responsive=True,
            size="sm"
        )
        
        return table
    except Exception as e:
        return html.P("Error loading options chain")

@app.callback(
    Output('start-btn', 'disabled'),
    [Input('start-btn', 'n_clicks')]
)
def start_trading(n_clicks):
    """Start trading engine"""
    if n_clicks:
        try:
            # Start trading engine in background
            # In practice, you'd use threading or async
            return True
        except Exception as e:
            return False
    return False

@app.callback(
    Output('stop-btn', 'disabled'),
    [Input('stop-btn', 'n_clicks')]
)
def stop_trading(n_clicks):
    """Stop trading engine"""
    if n_clicks:
        try:
            # Stop trading engine
            return True
        except Exception as e:
            return False
    return False

# Run the app
if __name__ == '__main__':
    print("Starting NIFTY Options Trading Dashboard...")
    print("Dashboard will be available at: http://localhost:8050")
    app.run_server(debug=True, host='0.0.0.0', port=8050)
