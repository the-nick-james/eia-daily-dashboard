# Screenshots and Visual Examples

This directory would contain screenshots of the EIA Daily Dashboard in action.

## Expected Screenshots

### 1. Main Dashboard View
![Main Dashboard](screenshots/main_dashboard.png)
- Shows the main interface with multiple energy price series selected
- Interactive Plotly charts with zoom and hover capabilities
- Date range selector in the sidebar

### 2. Price Charts Tab
![Price Charts](screenshots/price_charts.png)
- Multiple overlaid price series for comparison
- Interactive legend to show/hide series
- Time range slider at the bottom

### 3. Statistics Tab
![Statistics](screenshots/statistics_tab.png)
- Current price metrics
- Min/max values for the selected period
- Average prices
- Period change with percentage

### 4. Data Table Tab
![Data Table](screenshots/data_table.png)
- Raw data in tabular format
- Download CSV button
- Pivoted view with dates as rows and series as columns

### 5. Series Selection
![Series Selection](screenshots/series_selection.png)
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
