import yfinance as yf
import pandas as pd
from datetime import datetime

def fetch_silver_data(ticker="SI=F", start_date="2015-01-01", end_date="2025-12-30"):
    """
    Fetches historical silver price data from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol for silver (default: "SI=F" for Silver futures).
        start_date (str): The start date for the data in "YYYY-MM-DD" format.
        end_date (str): The end date for the data in "YYYY-MM-DD" format. If None, fetches up to the current date.

    Returns:
        pd.DataFrame: A DataFrame containing the historical silver price data, or None if fetching fails.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    try:
        silver_data = yf.download(ticker, start=start_date, end=end_date)
        if silver_data.empty:
            print(f"No data found for ticker {ticker} from {start_date} to {end_date}. "
                  "Please check the ticker symbol and date range.")
            return None
        return silver_data
    except Exception as e:
        print(f"Error fetching silver data: {e}")
        return None

def fetch_inr_data(ticker="INR=X", start_date="2015-01-01", end_date=None):
    """
    Fetches historical USD/INR exchange rate data from Yahoo Finance.

    Args:
        ticker (str): The ticker symbol for USD/INR exchange rate (default: "INR=X").
        start_date (str): The start date for the data in "YYYY-MM-DD" format.
        end_date (str): The end date for the data in "YYYY-MM-DD" format. If None, fetches up to the current date.

    Returns:
        pd.DataFrame: A DataFrame containing the historical exchange rate data, or None if fetching fails.
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")
        
    try:
        inr_data = yf.download(ticker, start=start_date, end=end_date)
        if inr_data.empty:
            print(f"No data found for ticker {ticker} from {start_date} to {end_date}. "
                  "Please check the ticker symbol and date range.")
            return None
        return inr_data
    except Exception as e:
        print(f"Error fetching INR data: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    silver_prices = fetch_silver_data()
    if silver_prices is not None:
        print("Successfully fetched silver prices:")
        print(silver_prices.head())

    inr_rates = fetch_inr_data()
    if inr_rates is not None:
        print("\nSuccessfully fetched USD/INR exchange rates:")
        print(inr_rates.head())