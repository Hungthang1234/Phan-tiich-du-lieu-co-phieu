# SUMMARY OF UPDATES

## Files Updated After Dashboard Implementation

### 1. requirements.txt
- Added Flask>=3.0.0
- Added Flask-CORS>=4.0.0
- Purpose: Web dashboard dependencies

### 2. README.md
- Added section: "Cách 2.5: Xem Kết Quả Trên Web Dashboard"
  - Instructions to run dashboard_server.py
  - Access at http://localhost:5000
- Added section 5: "Web Dashboard" in output results
  - Lists dashboard features:
    - Stock selection dropdown
    - Metrics display (Total Return, Max Drawdown, Sharpe Ratio)
    - Strategy vs Buy & Hold comparison
    - 6 charts per stock with descriptions

### 3. setup_and_run.bat
- Updated package list to include Flask and Flask-CORS
- Line: "Dang cai dat: pandas, numpy, ... Flask, Flask-CORS"

### 4. install_packages.bat
- Updated package list to include Flask and Flask-CORS
- Line: "Dang cai: pandas, numpy, ... Flask, Flask-CORS"

### 5. run_pipeline.py
- Updated check_required_modules() function
- Added 'flask' and 'flask_cors' to required_modules list
- Now validates Flask packages before pipeline execution

### 6. dashboard.html
- Updated to use Flask API instead of direct CSV loading
- Added plots section with grid layout
- Added plot descriptions below each chart
- Updated JavaScript to fetch data from API endpoints

### 7. dashboard_server.py
- Created Flask API server with 7 endpoints:
  - GET /api/symbols - list available stocks
  - GET /api/data/<symbol> - get metrics for stock
  - GET /api/all-results - get all results
  - GET /api/plots/<symbol> - list plots for stock
  - GET /plots/<path> - serve PNG images
  - GET /dashboard.html - serve dashboard UI
  - GET / - redirect to dashboard
- Added plot descriptions mapping
- CORS enabled for cross-origin requests

### 8. run_dashboard.bat (Created)
- New file for running dashboard
- Checks for Flask/Flask-CORS packages
- Starts server and opens browser automatically
- Accessible at http://localhost:5000

### 9. NOTICE.bat (Created)
- Quick reference guide for running the project
- 3 main options:
  1. setup_and_run.bat - first time setup
  2. run.bat - run pipeline
  3. run_dashboard.bat - view results on web
- References README.md for detailed instructions

## Summary of Features

Dashboard now includes:
✅ Interactive web UI at localhost:5000
✅ Stock selection dropdown
✅ Metrics display (ML Strategy vs Buy & Hold)
✅ Comparison charts
✅ 6 detailed plots per stock:
  - Price actual vs predicted
  - Prediction error (VND)
  - Prediction error (%)
  - Buy/Sell signals
  - Probability forecast
  - Equity curve
✅ Descriptions for each plot
✅ Responsive design
✅ REST API for data access
✅ Automatic browser opening on startup

## How to Use

1. First time: `setup_and_run.bat` (installs packages + runs pipeline + opens dashboard)
2. Run pipeline: `run.bat` or `python run_pipeline.py`
3. View dashboard: `run_dashboard.bat` (opens http://localhost:5000)
