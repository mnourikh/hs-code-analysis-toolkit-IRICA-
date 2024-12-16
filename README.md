
# HS Code Analysis Toolkit

This project provides tools for:
- **HS Code Processing**: Extract 2-digit and 4-digit HS codes for analysis.
- **Econometric Modeling**: Run fixed effects regressions with HS codes as categorical variables.
- **Forecasting**: Predict economic indicators with ARIMA models.

## Features
1. **Preprocessing**: Filter and clean data for econometric analysis.
2. **HS Code Tools**: Automatically extract and process HS codes into different levels.
3. **Fixed Effects Modeling**: Perform econometric modeling with country and year effects.
4. **Forecasting**: Predict future values using ARIMA.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Install the required Python libraries:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Place your dataset as `data.csv` in the working directory.
2. Update the script with your specific columns and parameters.
3. Run the script:
   ```
   python hs_analysis_toolkit.py
   ```

## Requirements
- Python 3.7 or later
- Libraries: pandas, numpy, statsmodels

## License
This project is licensed under the MIT License.
