# EIA Daily Energy Price Dashboard 📊

An interactive web dashboard for visualizing daily energy prices from the U.S. Energy Information Administration (EIA). Built with Python, Streamlit, and Plotly for real-time data exploration and analysis.

![Dashboard Screenshot](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

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

## Installation

### Prerequisites

- Python 3.8 or higher
- EIA API key (free registration at [EIA Registration](https://www.eia.gov/opendata/register.php))

### Setup

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

## Usage

### Running the Dashboard

Start the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in your default web browser at `http://localhost:8501`.

### Using the Dashboard

1. **Select Price Series**: Use the sidebar to choose one or more energy price series to visualize
2. **Choose Date Range**: Select a preset range (last 7 days, 30 days, etc.) or specify custom dates
3. **Explore Data**: 
   - **Price Charts**: Interactive line charts with zoom and hover features
   - **Statistics**: View key metrics including current price, min/max, average, and change
   - **Data Table**: Browse raw data and download as CSV

### Example Usage

```python
# You can also use the EIA client programmatically
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