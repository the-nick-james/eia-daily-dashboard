"""
EIA Daily Dashboard - Interactive dashboard for visualizing daily energy prices from EIA.gov
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from eia_client import EIAClient
import os

# Page configuration
st.set_page_config(
    page_title="EIA Daily Price Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)


def get_eia_client():
    """Initialize the EIA client."""
    try:
        return EIAClient()
    except ValueError as e:
        st.error(str(e))
        st.stop()


# @st.cache_data  # Cache for 1 hour
def fetch_price_data(_client: EIAClient, series_names, start_date_str, end_date_str, frequency=None):
    """Fetch and cache price data."""
    return _client.get_multiple_series(
        series_names,
        start_date=start_date_str,
        end_date=end_date_str,
        frequency=frequency
    )


def create_price_chart(data_dict, title="Energy Prices Over Time"):
    """
    Create an interactive price chart using Plotly.
    
    Args:
        data_dict: Dictionary mapping series names to DataFrames
        title: Chart title
        
    Returns:
        Plotly figure object
    """
    fig = go.Figure()
    
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
        '#9467bd', '#8c564b', '#e377c2', '#7f7f7f'
    ]
    
    for idx, (series_name, df) in enumerate(data_dict.items()):
        if df.empty:
            continue
            
        color = colors[idx % len(colors)]
        
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['value'],
            mode='lines',
            name=series_name,
            line=dict(color=color, width=2),
            hovertemplate=(
                f'<b>{series_name}</b><br>' +
                'Date: %{x|%Y-%m-%d}<br>' +
                'Price: $%{y:.2f}<br>' +
                '<extra></extra>'
            )
        ))
    
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center', font=dict(size=20)),
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        hovermode='x unified',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.8)"
        ),
        height=600,
        template="plotly_white",
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    return fig


def calculate_statistics(df):
    """Calculate statistics for a price series."""
    if df.empty:
        return None
    
    current_price = df['value'].iloc[-1]
    previous_price = df['value'].iloc[0]
    price_change = current_price - previous_price
    # Protect against division by zero or near-zero previous_price
    epsilon = 1e-9
    if abs(previous_price) < epsilon:
        price_change_pct = None
    else:
        price_change_pct = (price_change / previous_price) * 100
    
    return {
        'current': current_price,
        'min': df['value'].min(),
        'max': df['value'].max(),
        'mean': df['value'].mean(),
        'change': price_change,
        'change_pct': price_change_pct
    }


def main():
    """Main application function."""
    
    # Header
    st.title("📊 EIA Daily Energy Price Dashboard")
    st.markdown("""
    Interactive dashboard for visualizing daily energy prices from the 
    [U.S. Energy Information Administration (EIA)](https://www.eia.gov/).
    Select price series and date ranges to explore price trends and patterns.
    """)
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Check for API key
    if not os.getenv("EIA_API_KEY"):
        st.sidebar.warning("⚠️ EIA API key not found!")
        st.sidebar.markdown("""
        To use this dashboard:
        1. Get a free API key at [EIA Registration](https://www.eia.gov/opendata/register.php)
        2. Create a `.env` file in the project root
        3. Add: `EIA_API_KEY=your_key_here`
        """)
        st.stop()
    
    # Get available series
    available_series = EIAClient.get_available_series()
    
    # Series selection
    st.sidebar.subheader("📈 Select Price Series")
    selected_series = st.sidebar.multiselect(
        "Choose one or more series:",
        options=list(available_series.keys()),
        default=["WTI Crude Oil Spot Price", "Brent Crude Oil Spot Price"],
        help="Select multiple series to compare prices"
    )
    
    if not selected_series:
        st.warning("Please select at least one price series from the sidebar.")
        st.stop()
    
    # Date range selection
    st.sidebar.subheader("📅 Date Range")
    
    # Preset date ranges
    date_preset = st.sidebar.selectbox(
        "Quick select:",
        ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "Custom"]
    )
    
    # Initialize date variables based on selection
    if date_preset == "Last 7 Days":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
    elif date_preset == "Last 30 Days":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
    elif date_preset == "Last 90 Days":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
    elif date_preset == "Last 6 Months":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)
    elif date_preset == "Last Year":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
    else:  # Custom
        # Get date inputs (returns date objects)
        col1, col2 = st.sidebar.columns(2)
        current_date = datetime.now()
        
        with col1:
            start_date_input = st.date_input(
                "Start date:",
                value=current_date - timedelta(days=90),
                max_value=current_date
            )
        with col2:
            end_date_input = st.date_input(
                "End date:",
                value=current_date,
                max_value=current_date
            )
        
        # Convert date objects to datetime objects
        start_date = datetime.combine(start_date_input, datetime.min.time())
        end_date = datetime.combine(end_date_input, datetime.min.time())
    
    # Display selected series info
    st.sidebar.subheader("ℹ️ Series Information")
    for series in selected_series:
        with st.sidebar.expander(series):
            st.write(available_series[series]['description'])
    
    # Frequency selection
    st.sidebar.subheader("📊 Data Frequency")
    frequency_options = ["daily", "weekly", "monthly", "annual"]
    
    # Check session state for disabled frequencies
    if "disabled_frequencies" not in st.session_state:
        st.session_state.disabled_frequencies = set()
    
    # Filter out disabled frequencies for the current series selection
    series_key = tuple(sorted(selected_series))
    if "frequency_cache" not in st.session_state:
        st.session_state.frequency_cache = {}
    
    # Get previously disabled frequencies for this series combination
    disabled_for_series = st.session_state.frequency_cache.get(series_key, set())
    available_frequencies = [f for f in frequency_options if f not in disabled_for_series]
    
    if not available_frequencies:
        available_frequencies = frequency_options  # Reset if all disabled
        st.session_state.frequency_cache[series_key] = set()
    
    selected_frequency = st.sidebar.selectbox(
        "Choose frequency:",
        options=available_frequencies,
        index=0,
        help="Select the data frequency. Some series may not support all frequencies."
    )
    
    # Fetch data
    with st.spinner("Fetching data from EIA..."):
        try:
            client = get_eia_client()
            data_dict = fetch_price_data(
                client,
                tuple(selected_series),
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d"),
                selected_frequency
            )
        except Exception as e:
            error_msg = str(e).lower()
            # Check if this is a 400 error indicating invalid frequency
            if "400" in str(e) or "bad request" in error_msg:
                # Mark this frequency as invalid for these series
                if series_key not in st.session_state.frequency_cache:
                    st.session_state.frequency_cache[series_key] = set()
                st.session_state.frequency_cache[series_key].add(selected_frequency)
                
                st.error(f"The '{selected_frequency}' frequency is not available for the selected series. Please choose a different frequency.")
                st.info("Tip: Try 'daily' or 'monthly' as these are commonly available.")
                st.stop()
            else:
                st.error(f"Error fetching data: {e}")
                st.stop()
    
    # Main content area
    tabs = st.tabs(["📈 Price Charts", "📊 Statistics", "📋 Data Table"])
    
    # Tab 1: Price Charts
    with tabs[0]:
        st.subheader("Price Trends")
        
        # Check if we have data
        has_data = any(not df.empty for df in data_dict.values())
        
        if not has_data:
            st.warning("No data available for the selected date range. Try a different date range or series.")
        else:
            # Create and display chart
            fig = create_price_chart(data_dict, "Energy Price Comparison")
            st.plotly_chart(fig, use_container_width=True)
            
            # Individual charts option
            if len(selected_series) > 1:
                st.subheader("Individual Series Charts")
                cols = st.columns(min(len(selected_series), 2))
                for idx, series_name in enumerate(selected_series):
                    df = data_dict[series_name]
                    if not df.empty:
                        with cols[idx % 2]:
                            mini_fig = create_price_chart(
                                {series_name: df},
                                title=series_name
                            )
                            mini_fig.update_layout(height=400, showlegend=False)
                            st.plotly_chart(mini_fig, use_container_width=True)
    
    # Tab 2: Statistics
    with tabs[1]:
        st.subheader("Price Statistics")
        
        for series_name in selected_series:
            df = data_dict[series_name]
            
            if df.empty:
                st.warning(f"No data available for {series_name}")
                continue
            
            stats = calculate_statistics(df)
            
            st.markdown(f"### {series_name}")
            
            cols = st.columns(5)
            
            with cols[0]:
                st.metric(
                    "Current Price",
                    f"${stats['current']:.2f}"
                )
            
            with cols[1]:
                change_pct_display = "N/A" if stats['change_pct'] is None else f"{stats['change_pct']:.2f}%"
                st.metric(
                    "Period Change",
                    f"${stats['change']:.2f}",
                    change_pct_display
                )
            
            with cols[2]:
                st.metric(
                    "Minimum",
                    f"${stats['min']:.2f}"
                )
            
            with cols[3]:
                st.metric(
                    "Maximum",
                    f"${stats['max']:.2f}"
                )
            
            with cols[4]:
                st.metric(
                    "Average",
                    f"${stats['mean']:.2f}"
                )
            
            st.divider()
    
    # Tab 3: Data Table
    with tabs[2]:
        st.subheader("Raw Data")
        
        # Combine all series into one table
        combined_df = pd.DataFrame()
        
        for series_name in selected_series:
            df = data_dict[series_name]
            if not df.empty:
                temp_df = df.copy()
                temp_df['series'] = series_name
                combined_df = pd.concat([combined_df, temp_df], ignore_index=True)
        
        if not combined_df.empty:
            # Pivot for better display; use pivot_table to safely handle any duplicate (date, series) pairs
            pivot_df = combined_df.pivot_table(
                index='date',
                columns='series',
                values='value',
                aggfunc='first'
            )
            pivot_df = pivot_df.sort_index(ascending=False)
            
            st.dataframe(
                pivot_df.style.format("${:.2f}"),
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = pivot_df.to_csv()
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"eia_prices_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.warning("No data available to display.")
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **About**  
    Data source: [U.S. Energy Information Administration](https://www.eia.gov/)  
    Powered by EIA API v2
    """)


if __name__ == "__main__":
    main()
