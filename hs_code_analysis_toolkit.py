
# HS Code Analysis and Econometric Toolkit
# This script includes tools for preprocessing, econometric modeling, ARIMA forecasting, and saving results.

import pandas as pd
import numpy as np
import os
from statsmodels.formula.api import ols
from statsmodels.tsa.arima.model import ARIMA
from openpyxl import Workbook

def preprocess_data(df, columns_to_keep, hs_column="HSCode"):
    # Processes HS codes into 2-digit and 4-digit levels and keeps specified columns
    df["HS2"] = df[hs_column].astype(str).str[:2]
    df["HS4"] = df[hs_column].astype(str).str[:4]
    return df[columns_to_keep].dropna()

def save_to_excel(df, filepath, sheet_name="Results"):
    # Saves a DataFrame to an Excel file with the specified sheet name
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name
    for r in df.itertuples(index=False, name=None):
        ws.append(r)
    wb.save(filepath)
    print(f"Saved results to {filepath}")

def run_fixed_effects_model(data, formula, feature_set_name, save_path):
    # Runs a fixed effects regression model and saves the coefficients to Excel
    model = ols(formula, data=data).fit()
    results = pd.DataFrame({
        "Feature": model.params.index,
        "Coefficient": model.params.values,
        "Std Error": model.bse.values,
        "P-Value": model.pvalues.values,
    })
    save_to_excel(results, save_path, sheet_name=feature_set_name)
    print(f"Fixed Effects Model Results saved to {save_path}")

def forecast_variable(data, column, steps=5, save_path=None):
    # Forecasts a column using ARIMA and optionally saves the forecast to an Excel file
    series = data[column].dropna()
    model = ARIMA(series, order=(1, 1, 1))
    fitted_model = model.fit()
    forecast = pd.DataFrame(fitted_model.forecast(steps=steps), columns=["Forecast"])
    if save_path:
        save_to_excel(forecast, save_path, sheet_name=f"{column}_Forecast")
    print(f"Forecast for {column} saved to {save_path}")
    return forecast

def analyze_data(df, formula, feature_sets, hs_column="HSCode", output_dir="results"):
    # Processes data, runs fixed effects models for multiple feature sets, and forecasts key variables
    os.makedirs(output_dir, exist_ok=True)
    df = preprocess_data(df, ["year", "log_dollar", "log_weight", hs_column], hs_column)

    for feature_set_name, features in feature_sets.items():
        current_formula = f"{formula} + {' + '.join(features)}"
        save_path = os.path.join(output_dir, f"{feature_set_name}_results.xlsx")
        run_fixed_effects_model(df, current_formula, feature_set_name, save_path)

    forecast_save_path = os.path.join(output_dir, "Forecast.xlsx")
    forecast_variable(df, "log_dollar", steps=5, save_path=forecast_save_path)

if __name__ == "__main__":
    # Example Usage
    input_file = "data.csv"  # Replace with your actual data file path
    data = pd.read_csv(input_file)

    feature_sets = {
        "Set1": ["log_weight", "log_distance"],
        "Set2": ["log_gdp_partner", "log_cpi_us"],
    }

    analyze_data(data, "log_dollar ~ C(year) + C(HS2)", feature_sets)
