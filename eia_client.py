"""
EIA API Client for fetching energy price data from the U.S. Energy Information Administration.
"""

import os
import logging
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)


class EIAClient:
    """Client for interacting with the EIA API v2."""
    
    BASE_URL = "https://api.eia.gov/v2"
    
    # Common daily price series IDs
    SERIES_MAP = {
        "WTI Crude Oil Spot Price": {
            "route": "petroleum/pri/spt",
            "series": "RWTC",
            "frequency": "daily",
            "description": "Cushing, OK WTI Spot Price FOB (Dollars per Barrel)"
        },
        "Brent Crude Oil Spot Price": {
            "route": "petroleum/pri/spt",
            "series": "RBRTE",
            "frequency": "daily",
            "description": "Europe Brent Spot Price FOB (Dollars per Barrel)"
        },
        "NY Harbor Conventional Gasoline": {
            "route": "petroleum/pri/spt",
            "series": "EER_EPMRU_PF4_Y35NY_DPG",
            "frequency": "daily",
            "description": "New York Harbor Conventional Gasoline Regular Spot Price (Dollars per Gallon)"
        },
        "U.S. Regular Gasoline Price": {
            "route": "petroleum/pri/gnd",
            "series": "EMD_EPD2D_PTE_NUS_DPG",
            "frequency": "daily",
            "description": "U.S. Regular All Formulations Retail Gasoline Prices (Dollars per Gallon)"
        },
        "U.S. Diesel Price": {
            "route": "petroleum/pri/gnd",
            "series": "EMD_EPD2DXL0_PTE_NUS_DPG",
            "frequency": "daily",
            "description": "U.S. No 2 Diesel Retail Prices (Dollars per Gallon)"
        },
        "Heating Oil NY Harbor": {
            "route": "petroleum/pri/spt",
            "series": "EER_EPD2F_PF4_Y35NY_DPG",
            "frequency": "daily",
            "description": "New York Harbor No. 2 Heating Oil Spot Price (Dollars per Gallon)"
        },
        "Natural Gas Henry Hub": {
            "route": "natural-gas/pri/fut",
            "series": "RNGC1",
            "frequency": "daily",
            "description": "Henry Hub Natural Gas Spot Price (Dollars per Million Btu)"
        },
        "Propane Mont Belvieu": {
            "route": "petroleum/pri/spt",
            "series": "EER_EPLLPA_PF4_Y44MB_DPG",
            "frequency": "daily",
            "description": "Mont Belvieu, TX Propane Spot Price (Dollars per Gallon)"
        }
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the EIA client.
        
        Args:
            api_key: EIA API key. If not provided, will look for EIA_API_KEY environment variable.
        """
        self.api_key = api_key or os.getenv("EIA_API_KEY")
        if not self.api_key:
            raise ValueError(
                "EIA API key is required. Set EIA_API_KEY environment variable "
                "or pass api_key parameter. Get your free key at "
                "https://www.eia.gov/opendata/register.php"
            )
    
    def get_series_data(
        self,
        route: str,
        series: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        frequency: str = "daily"
    ) -> pd.DataFrame:
        """
        Fetch data for a specific series from the EIA API.
        
        Args:
            route: API route (e.g., 'petroleum/pri/spt')
            series: Series ID (e.g., 'RWTC')
            start_date: Start date in YYYY-MM-DD format (defaults to 90 days ago)
            end_date: End date in YYYY-MM-DD format (defaults to today)
            frequency: Data frequency (default: 'daily')
            
        Returns:
            DataFrame with date and value columns
        """
        # Set default date range if not provided
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        
        # Construct API URL
        url = f"{self.BASE_URL}/{route}/data/"
        
        params = {
            "api_key": self.api_key,
            "frequency": frequency,
            "data[0]": "value",
            "facets[series][]": series,
            "start": start_date,
            "end": end_date,
            "sort[0][column]": "period",
            "sort[0][direction]": "asc",
            "offset": 0,
            "length": 5000
        }
        
        # Configure timeout and retry parameters
        timeout = 15  # Reduced from 30s for better UX
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, params=params, timeout=timeout)
                response.raise_for_status()
                data = response.json()
                
                if "response" not in data or "data" not in data["response"]:
                    return pd.DataFrame(columns=["date", "value"])
                
                records = data["response"]["data"]
                if not records:
                    return pd.DataFrame(columns=["date", "value"])
                
                # Convert to DataFrame
                df = pd.DataFrame(records)
                df = df.rename(columns={"period": "date"})
                df["date"] = pd.to_datetime(df["date"])
                df["value"] = pd.to_numeric(df["value"], errors="coerce")
                df = df[["date", "value"]].sort_values("date")
                
                return df
                
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                    logger.warning(f"Request timeout (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                    import time
                    time.sleep(wait_time)
                else:
                    logger.error(f"Request timed out after {max_retries} attempts")
                    raise
            except requests.exceptions.RequestException as e:
                logger.error(f"Error fetching data from EIA API: {e}", exc_info=True)
                raise
    
    def get_price_data(
        self,
        series_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch price data for a named series.
        
        Args:
            series_name: Name of the series from SERIES_MAP
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            DataFrame with date and value columns
        """
        if series_name not in self.SERIES_MAP:
            raise ValueError(f"Unknown series: {series_name}. Available: {list(self.SERIES_MAP.keys())}")
        
        series_info = self.SERIES_MAP[series_name]
        return self.get_series_data(
            route=series_info["route"],
            series=series_info["series"],
            start_date=start_date,
            end_date=end_date,
            frequency=series_info["frequency"]
        )
    
    def get_multiple_series(
        self,
        series_names: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, pd.DataFrame]:
        """
        Fetch data for multiple series.
        
        Args:
            series_names: List of series names from SERIES_MAP
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary mapping series names to DataFrames
        """
        results = {}
        for series_name in series_names:
            results[series_name] = self.get_price_data(series_name, start_date, end_date)
        return results
    
    @classmethod
    def get_available_series(cls) -> Dict[str, Dict]:
        """Get information about all available series."""
        return cls.SERIES_MAP
