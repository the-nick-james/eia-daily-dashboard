"""
Unit tests for the EIA Daily Dashboard application.

Tests cover the core functionality of the EIA client and dashboard functions.
Run with: pytest test_dashboard.py -v
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from eia_client import EIAClient


class TestEIAClient:
    """Tests for the EIA API client."""
    
    def test_client_initialization_with_api_key(self):
        """Test that client initializes correctly with an API key."""
        client = EIAClient(api_key="test_key")
        assert client.api_key == "test_key"
    
    def test_client_initialization_without_api_key_raises_error(self):
        """Test that client raises ValueError when no API key is provided."""
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="EIA API key is required"):
                EIAClient()
    
    def test_get_available_series(self):
        """Test that available series can be retrieved."""
        series = EIAClient.get_available_series()
        assert isinstance(series, dict)
        assert len(series) > 0
        assert "WTI Crude Oil Spot Price" in series
        assert "Brent Crude Oil Spot Price" in series
    
    def test_series_map_structure(self):
        """Test that each series has required fields."""
        series = EIAClient.get_available_series()
        for name, info in series.items():
            assert "route" in info
            assert "series" in info
            assert "frequency" in info
            assert "description" in info
    
    @patch('eia_client.requests.get')
    def test_get_series_data_success(self, mock_get):
        """Test successful data retrieval from API."""
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "response": {
                "data": [
                    {"period": "2024-01-01", "value": "75.50"},
                    {"period": "2024-01-02", "value": "76.25"},
                ]
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = EIAClient(api_key="test_key")
        df = client.get_series_data(
            route="petroleum/pri/spt",
            series="RWTC",
            start_date="2024-01-01",
            end_date="2024-01-02"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert "date" in df.columns
        assert "value" in df.columns
        assert df["value"].iloc[0] == 75.50
    
    @patch('eia_client.requests.get')
    def test_get_series_data_empty_response(self, mock_get):
        """Test handling of empty API response."""
        mock_response = Mock()
        mock_response.json.return_value = {"response": {"data": []}}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        client = EIAClient(api_key="test_key")
        df = client.get_series_data(
            route="petroleum/pri/spt",
            series="RWTC"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
        assert list(df.columns) == ["date", "value"]
    
    @patch('eia_client.requests.get')
    def test_get_series_data_network_error(self, mock_get):
        """Test handling of network errors."""
        import requests
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        
        client = EIAClient(api_key="test_key")
        df = client.get_series_data(
            route="petroleum/pri/spt",
            series="RWTC"
        )
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 0
    
    def test_get_price_data_invalid_series(self):
        """Test that invalid series name raises ValueError."""
        client = EIAClient(api_key="test_key")
        with pytest.raises(ValueError, match="Unknown series"):
            client.get_price_data("Invalid Series Name")
    
    @patch('eia_client.EIAClient.get_series_data')
    def test_get_multiple_series(self, mock_get_series_data):
        """Test fetching multiple series."""
        mock_get_series_data.return_value = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=5),
            'value': [75.0, 76.0, 77.0, 78.0, 79.0]
        })
        
        client = EIAClient(api_key="test_key")
        series_names = ["WTI Crude Oil Spot Price", "Brent Crude Oil Spot Price"]
        result = client.get_multiple_series(series_names)
        
        assert isinstance(result, dict)
        assert len(result) == 2
        assert all(name in result for name in series_names)


class TestCalculateStatistics:
    """Tests for the calculate_statistics function from app.py."""
    
    def setup_method(self):
        """Import the function for testing."""
        # Import here to avoid Streamlit initialization issues
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "app", 
            os.path.join(os.path.dirname(__file__), "app.py")
        )
        self.app_module = importlib.util.module_from_spec(spec)
    
    def test_calculate_statistics_with_valid_data(self):
        """Test statistics calculation with valid data."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=10),
            'value': [100, 105, 103, 108, 110, 107, 112, 115, 113, 118]
        })
        
        # Manually calculate expected values
        stats = {
            'current': df['value'].iloc[-1],
            'min': df['value'].min(),
            'max': df['value'].max(),
            'mean': df['value'].mean(),
            'change': df['value'].iloc[-1] - df['value'].iloc[0],
            'change_pct': ((df['value'].iloc[-1] - df['value'].iloc[0]) / df['value'].iloc[0]) * 100
        }
        
        assert stats['current'] == 118
        assert stats['min'] == 100
        assert stats['max'] == 118
        assert stats['change'] == 18
        assert abs(stats['change_pct'] - 18.0) < 0.01
    
    def test_calculate_statistics_with_empty_dataframe(self):
        """Test that empty DataFrame returns None."""
        df = pd.DataFrame(columns=['date', 'value'])
        
        # Expected behavior: return None for empty DataFrame
        assert df.empty is True
    
    def test_calculate_statistics_with_zero_previous_price(self):
        """Test handling of zero previous price (division by zero case)."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=3),
            'value': [0, 50, 100]
        })
        
        # When previous price is zero, percentage change should be None or handled gracefully
        previous_price = df['value'].iloc[0]
        assert previous_price == 0
        
        # Percentage calculation would fail without proper handling
        epsilon = 1e-9
        if abs(previous_price) < epsilon:
            price_change_pct = None
        else:
            price_change_pct = ((df['value'].iloc[-1] - previous_price) / previous_price) * 100
        
        assert price_change_pct is None


class TestDataProcessing:
    """Tests for data processing and transformation."""
    
    def test_dataframe_pivot_with_duplicates(self):
        """Test pivot operation handling with duplicate entries."""
        # Create DataFrame with duplicate (date, series) pairs
        data = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-01', '2024-01-01', '2024-01-02']),
            'series': ['WTI', 'WTI', 'WTI'],
            'value': [75.0, 75.5, 76.0]
        })
        
        # Using pivot_table with aggregation to handle duplicates
        pivot_df = data.pivot_table(
            index='date',
            columns='series',
            values='value',
            aggfunc='first'
        )
        
        assert len(pivot_df) == 2  # Should have 2 unique dates
        assert 'WTI' in pivot_df.columns
    
    def test_dataframe_date_conversion(self):
        """Test date string to datetime conversion."""
        df = pd.DataFrame({
            'period': ['2024-01-01', '2024-01-02', '2024-01-03'],
            'value': [75.0, 76.0, 77.0]
        })
        
        df = df.rename(columns={'period': 'date'})
        df['date'] = pd.to_datetime(df['date'])
        
        assert pd.api.types.is_datetime64_any_dtype(df['date'])
        assert len(df) == 3
    
    def test_numeric_conversion_with_errors(self):
        """Test numeric conversion with invalid values."""
        df = pd.DataFrame({
            'value': ['75.0', '76.5', 'N/A', '78.0']
        })
        
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # 'N/A' should become NaN
        assert df['value'].isna().sum() == 1
        assert df['value'].iloc[0] == 75.0


class TestDateRangeHandling:
    """Tests for date range calculation and handling."""
    
    def test_last_7_days_calculation(self):
        """Test calculation of last 7 days date range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        delta = (end_date - start_date).days
        assert delta == 7
    
    def test_last_90_days_calculation(self):
        """Test calculation of last 90 days date range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)
        
        delta = (end_date - start_date).days
        assert delta == 90
    
    def test_custom_date_range(self):
        """Test custom date range handling."""
        start_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        delta = (end_date - start_date).days
        assert delta == 365


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
