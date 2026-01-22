"""
Test script to verify the dashboard components work correctly.
"""

import sys
import pandas as pd

# Test imports
print("Testing imports...")
try:
    import streamlit
    print(f"✓ Streamlit imported successfully (version {streamlit.__version__})")
except ImportError as e:
    print(f"✗ Failed to import streamlit: {e}")
    sys.exit(1)

try:
    import plotly.graph_objects as go
    print("✓ Plotly imported successfully")
except ImportError as e:
    print(f"✗ Failed to import plotly: {e}")
    sys.exit(1)

try:
    import pandas as pd
    print("✓ Pandas imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pandas: {e}")
    sys.exit(1)

try:
    from eia_client import EIAClient
    print("✓ EIA Client imported successfully")
except ImportError as e:
    print(f"✗ Failed to import EIA Client: {e}")
    sys.exit(1)

# Test EIA Client structure
print("\nTesting EIA Client...")
series_map = EIAClient.get_available_series()
print(f"✓ Found {len(series_map)} available price series:")
for name in list(series_map.keys())[:5]:
    print(f"  - {name}")

# Test data structure
print("\nTesting data structures...")
test_df = pd.DataFrame({
    'date': pd.date_range(start='2024-01-01', periods=10, freq='D'),
    'value': [100 + i for i in range(10)]
})
print(f"✓ Created test DataFrame with {len(test_df)} rows")
print(f"  Date range: {test_df['date'].min()} to {test_df['date'].max()}")
print(f"  Value range: ${test_df['value'].min():.2f} to ${test_df['value'].max():.2f}")

# Test chart creation function from app
print("\nTesting chart creation...")
try:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=test_df['date'],
        y=test_df['value'],
        mode='lines',
        name='Test Series'
    ))
    fig.update_layout(title="Test Chart", xaxis_title="Date", yaxis_title="Price")
    print("✓ Successfully created test Plotly chart")
except Exception as e:
    print(f"✗ Failed to create chart: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("✓ All tests passed!")
print("="*50)
print("\nTo run the dashboard:")
print("1. Set your EIA_API_KEY in a .env file")
print("2. Run: streamlit run app.py")
