# Screenshots and Visual Examples

This directory is intended to contain screenshots of the EIA Daily Dashboard in action.

_Note: The screenshots described below are planned placeholders. Actual image files are not yet committed to the repository and will be added once captured._

## Expected Screenshots

### 1. Main Dashboard View
_Planned screenshot: to be added once captured._
- Shows the main interface with multiple energy price series selected
- Interactive Plotly charts with zoom and hover capabilities
- Date range selector in the sidebar

### 2. Price Charts Tab
_Planned screenshot: to be added once captured._
- Multiple overlaid price series for comparison
- Interactive legend to show/hide series
- Time range slider at the bottom

### 3. Statistics Tab
_Planned screenshot: to be added once captured._
- Current price metrics
- Min/max values for the selected period
- Average prices
- Period change with percentage

### 4. Data Table Tab
_Planned screenshot: to be added once captured._
- Raw data in tabular format
- Download CSV button
- Pivoted view with dates as rows and series as columns

### 5. Series Selection
_Planned screenshot: to be added once captured._
- Sidebar with available series
- Multi-select dropdown
- Series information expandable sections

## To Generate Screenshots

1. Ensure you have a valid EIA API key in `.env`
2. Run the dashboard: `streamlit run app.py`
3. Navigate through the different features
4. Take screenshots and save them in the `screenshots/` directory

## Live Demo

For a live demonstration with mock data, run:
```bash
python demo.py
```

This will generate a sample HTML chart saved as `demo_chart.html` that you can open in your browser.
