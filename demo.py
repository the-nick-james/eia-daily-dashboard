"""
Demo script to showcase the EIA dashboard functionality with mock data.
This demonstrates the dashboard features without requiring an API key.
"""

import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import argparse

# Generate mock price data
def generate_mock_data(start_date, end_date, base_price=80, volatility=5, seed=42):
    """Generate realistic-looking mock price data.
    
    Args:
        start_date: Start date for data generation
        end_date: End date for data generation
        base_price: Starting price for the series
        volatility: Price volatility factor
        seed: Random seed for reproducibility (default: 42 for consistent demos)
    """
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate prices with some random walk and trend
    # Note: Seed is set to 42 by default for reproducible demonstrations
    # Pass a different seed value to generate varied mock datasets
    np.random.seed(seed)
    prices = [base_price]
    for _ in range(len(dates) - 1):
        change = np.random.normal(0, volatility)
        new_price = max(prices[-1] + change, 10)  # Keep prices positive
        prices.append(new_price)
    
    return pd.DataFrame({
        'date': dates,
        'value': prices
    })

# Parse command line arguments
parser = argparse.ArgumentParser(description='Generate mock EIA price data for demonstration')
parser.add_argument('--seed', type=int, default=42, 
                    help='Random seed for data generation (default: 42 for reproducibility)')
args = parser.parse_args()

# Generate sample data for different series
print(f"Generating mock EIA price data (seed={args.seed})...")
end_date = datetime.now()
start_date = end_date - timedelta(days=90)

mock_data = {
    "WTI Crude Oil Spot Price": generate_mock_data(start_date, end_date, base_price=75, volatility=2, seed=args.seed),
    "Brent Crude Oil Spot Price": generate_mock_data(start_date, end_date, base_price=78, volatility=2.2, seed=args.seed+1),
    "Natural Gas Henry Hub": generate_mock_data(start_date, end_date, base_price=3.5, volatility=0.3, seed=args.seed+2),
    "U.S. Regular Gasoline Price": generate_mock_data(start_date, end_date, base_price=3.2, volatility=0.15, seed=args.seed+3),
}

# Display statistics
print("\n" + "="*70)
print("MOCK EIA DASHBOARD - SAMPLE DATA STATISTICS")
print("="*70)

for series_name, df in mock_data.items():
    current = df['value'].iloc[-1]
    min_val = df['value'].min()
    max_val = df['value'].max()
    mean_val = df['value'].mean()
    change = df['value'].iloc[-1] - df['value'].iloc[0]
    change_pct = (change / df['value'].iloc[0]) * 100
    
    print(f"\n{series_name}:")
    print(f"  Current Price: ${current:.2f}")
    print(f"  90-Day Range: ${min_val:.2f} - ${max_val:.2f}")
    print(f"  Average: ${mean_val:.2f}")
    print(f"  Change: ${change:+.2f} ({change_pct:+.1f}%)")

# Create sample visualization
print("\n" + "="*70)
print("Creating sample visualization...")

fig = go.Figure()

colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']

for idx, (series_name, df) in enumerate(mock_data.items()):
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['value'],
        mode='lines',
        name=series_name,
        line=dict(color=colors[idx], width=2)
    ))

fig.update_layout(
    title="Mock EIA Energy Price Comparison (Last 90 Days)",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    hovermode='x unified',
    height=600,
    template="plotly_white",
    legend=dict(x=0.01, y=0.99)
)

# Save as HTML for viewing
output_file = "demo_chart.html"
fig.write_html(output_file)
print(f"✓ Sample chart saved to: {output_file}")

print("\n" + "="*70)
print("DASHBOARD FEATURES DEMONSTRATED:")
print("="*70)
print("✓ Multiple price series comparison")
print("✓ Historical price data visualization")
print("✓ Statistical analysis (current, min, max, average, change)")
print("✓ Interactive charts with Plotly")
print("✓ Date range filtering capabilities")
print("\n" + "="*70)
print("TO USE WITH REAL DATA:")
print("="*70)
print("1. Register for a free API key at: https://www.eia.gov/opendata/register.php")
print("2. Update .env file with your API key: EIA_API_KEY=your_actual_key")
print("3. Run the dashboard: streamlit run app.py")
print("4. Select series and date ranges to explore real EIA data")
print("="*70)
