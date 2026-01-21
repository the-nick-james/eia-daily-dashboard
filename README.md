# EIA Daily Energy Price Dashboard 📊

An interactive web dashboard for visualizing daily energy prices from the U.S. Energy Information Administration (EIA). Built with Python, Streamlit, and Plotly for real-time data exploration and analysis.

![Dashboard Screenshot](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## What This App Does

This dashboard allows you to:
- **Track Energy Prices**: Monitor daily prices for crude oil (WTI, Brent), gasoline, diesel, natural gas, and more
- **Compare Multiple Commodities**: View and compare up to 8 different energy price series side-by-side
- **Analyze Trends**: Interactive charts let you zoom, pan, and explore price movements over time
- **Export Data**: Download historical price data as CSV files for your own analysis
- **View Statistics**: See current prices, historical highs/lows, averages, and percentage changes

All data comes directly from the official U.S. Energy Information Administration API in real-time.

## Dashboard Preview

![EIA Dashboard Interface](https://github.com/user-attachments/assets/b4fb0149-5c77-4428-811f-11fae9b37e80)

*Interactive dashboard interface showing price series selection, date range filters, and visualization tabs*

## Quick Start

### Option 1: Using Dev Container (Recommended)

The easiest way to get started is using the pre-configured dev container with Python 3.12:

1. **Prerequisites**: 
   - [Visual Studio Code](https://code.visualstudio.com/)
   - [Docker Desktop](https://www.docker.com/products/docker-desktop)
   - [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code

2. **Open in Dev Container**:
   ```bash
   git clone https://github.com/the-nick-james/eia-daily-dashboard.git
   cd eia-daily-dashboard
   code .
   ```
   
   When prompted, click "Reopen in Container" (or press `F1` and select "Dev Containers: Reopen in Container")

3. **Configure API Key**:
   - The dev container automatically creates a `.env` file from `.env.example`
   - Edit `.env` and add your EIA API key: `EIA_API_KEY=your_key_here`
   - Get a free API key at [EIA Registration](https://www.eia.gov/opendata/register.php)

4. **Launch the dashboard**:
   ```bash
   streamlit run app.py
   ```
   
   The dashboard will automatically open in your browser at `http://localhost:8501`

**What the dev container does for you:**
- Sets up Python 3.12 environment
- Creates a virtual environment in `.venv`
- Installs all dependencies from `requirements.txt`
- Configures VS Code with Python extensions and settings
- Forwards port 8501 for the Streamlit dashboard

### Option 2: Manual Setup

Get the dashboard running in 3 simple steps:

1. **Get a free EIA API key** (takes 2 minutes): Visit [EIA Registration](https://www.eia.gov/opendata/register.php)

2. **Install and configure**:
   ```bash
   git clone https://github.com/the-nick-james/eia-daily-dashboard.git
   cd eia-daily-dashboard
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your API key: EIA_API_KEY=your_key_here
   ```

3. **Launch the dashboard**:
   ```bash
   streamlit run app.py
   ```
   
   The dashboard will automatically open in your browser at `http://localhost:8501`

## How to Use the Dashboard

Once the dashboard is running:

1. **Select Price Series** (left sidebar): 
   - Choose one or more energy commodities from the dropdown
   - Default selections are WTI and Brent crude oil

2. **Choose Date Range** (left sidebar):
   - Quick options: Last 7/30/90 days, 6 months, or 1 year
   - Or select custom start and end dates

3. **Explore Your Data** (main area):
   - **Price Charts Tab**: Interactive line graphs with zoom/pan, hover for exact values
   - **Statistics Tab**: Current prices, min/max, averages, and period changes
   - **Data Table Tab**: Raw data grid with CSV download button

### Example: Comparing Crude Oil Prices

Want to compare WTI vs Brent crude oil over the last 3 months?
1. Launch the app: `streamlit run app.py`
2. In the sidebar, ensure "WTI Crude Oil Spot Price" and "Brent Crude Oil Spot Price" are selected
3. Choose "Last 90 Days" from the date range dropdown
4. View the overlaid price chart in the Price Charts tab
5. Click the Statistics tab to see the price difference between the two

## Features

- 📈 **Interactive Charts**: Visualize multiple energy price series with zoom, pan, and hover capabilities
- 📊 **Multiple Data Series**: Compare WTI, Brent crude oil, gasoline, diesel, natural gas, and more
- 📅 **Flexible Date Ranges**: Query data for custom time periods or use preset ranges
- 📉 **Statistical Analysis**: View current prices, min/max values, averages, and price changes
- 💾 **Data Export**: Download price data as CSV for further analysis
- ⚡ **Real-time Data**: Fetches the latest prices from EIA's official API
- 🎨 **Responsive Design**: Clean, modern interface that works on any screen size

## Available Price Series

The dashboard provides access to the following daily price series:

- **Crude Oil**: WTI (Cushing, OK) and Brent (Europe) spot prices
- **Gasoline**: NY Harbor conventional gasoline and U.S. retail prices
- **Diesel**: U.S. No. 2 diesel retail prices
- **Heating Oil**: NY Harbor No. 2 heating oil spot price
- **Natural Gas**: Henry Hub spot price
- **Propane**: Mont Belvieu, TX spot price

## Installation (Detailed)

### Prerequisites

- Python 3.8 or higher
- EIA API key (free registration at [EIA Registration](https://www.eia.gov/opendata/register.php))

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/the-nick-james/eia-daily-dashboard.git
   cd eia-daily-dashboard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**:
   
   Create a `.env` file in the project root:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your EIA API key:
   ```
   EIA_API_KEY=your_actual_api_key_here
   ```

4. **Launch the dashboard**:
   ```bash
   streamlit run app.py
   ```
   
   The dashboard will open in your default web browser at `http://localhost:8501`.

## Programmatic Usage (Python API)

You can also use the EIA client directly in your Python scripts:

```python
from eia_client import EIAClient
from datetime import datetime, timedelta

# Initialize client
client = EIAClient(api_key="your_api_key")

# Fetch WTI crude oil prices for the last 30 days
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

data = client.get_price_data(
    "WTI Crude Oil Spot Price",
    start_date=start_date.strftime("%Y-%m-%d"),
    end_date=end_date.strftime("%Y-%m-%d")
)

print(data.head())
```

## Project Structure

```
eia-daily-dashboard/
├── app.py              # Main Streamlit dashboard application
├── eia_client.py       # EIA API client for data fetching
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── .gitignore         # Git ignore rules
├── LICENSE            # MIT License
└── README.md          # This file
```

## Dependencies

- **streamlit**: Web application framework for the dashboard
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive charting library
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

## API Information

This application uses the EIA API v2 to fetch energy price data. The API provides:

- Daily, weekly, monthly, and annual data frequencies
- Historical data for thousands of energy series
- Free access with API key registration
- Rate limit: 1000 requests per hour

For more information, visit the [EIA API Documentation](https://www.eia.gov/opendata/documentation.php).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by the [U.S. Energy Information Administration](https://www.eia.gov/)
- Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/)

## Support

If you encounter any issues or have questions:

1. Check the [EIA API Documentation](https://www.eia.gov/opendata/documentation.php)
2. Ensure your API key is correctly configured in `.env`
3. Verify your internet connection for API access
4. Open an issue on GitHub for bug reports or feature requests

---

**Note**: This is an independent project and is not affiliated with or endorsed by the U.S. Energy Information Administration.