import pandas as pd
import numpy as np

def process_data(silver_data, inr_data):
    """
    Cleans, preprocesses, and calculates statistical metrics for the silver price data.

    Args:
        silver_data (pd.DataFrame): DataFrame with historical silver prices in USD.
        inr_data (pd.DataFrame): DataFrame with historical USD/INR exchange rates.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Processed data with prices in INR, returns, etc.
            - dict: A dictionary of calculated statistical metrics.
    """
    if silver_data is None or inr_data is None:
        return None, None

    # Combine data and handle missing values
    data = pd.concat([gold_data['Close'], inr_data['Close']], axis=1)
    data.columns = ['Silver_USD_Ounce', 'USD_INR']
    data.ffill(inplace=True)
    data.dropna(inplace=True)

    # Convert silver price to INR per gram
    # 1 ounce = 31.1035 grams
    data['Silver_INR_Gram'] = (data['Silver_USD_Ounce'] / 31.1035) * data['USD_INR']

    # Calculate daily returns
    data['Log_Returns'] = np.log(data['Silver_INR_Gram'] / data['Silver_INR_Gram'].shift(1))
    data.dropna(inplace=True)

    # Calculate statistical metrics
    mean_daily_return = data['Log_Returns'].mean()
    std_dev = data['Log_Returns'].std()
    drift = mean_daily_return - 0.5 * std_dev**2
    annualized_volatility = std_dev * np.sqrt(252) # Assuming 252 trading days
    
    # Maximum Drawdown
    cumulative_returns = (1 + data['Log_Returns']).cumprod()
    peak = cumulative_returns.expanding(min_periods=1).max()
    drawdown = (cumulative_returns/peak) - 1
    max_drawdown = drawdown.min()

    # Sharpe Ratio (assuming risk-free rate is 0)
    sharpe_ratio = (mean_daily_return * 252) / annualized_volatility

    stats = {
        'mean_daily_return': mean_daily_return,
        'std_dev': std_dev,
        'drift': drift,
        'annualized_volatility': annualized_volatility,
        'max_drawdown': max_drawdown,
        'sharpe_ratio': sharpe_ratio,
        'latest_price': data['Silver_INR_Gram'].iloc[-1]
    }

    return data, stats

if __name__ == '__main__':
    # Example usage with dummy data:
    from data_fetcher import fetch_silver_data, fetch_inr_data

    silver_prices = fetch_silver_data()
    inr_rates = fetch_inr_data()
    
    processed_data, statistics = process_data(silver_prices, inr_rates)

    if processed_data is not None:
        print("Processed Data:")
        print(processed_data.head())
        print("\nCalculated Statistics:")
        for key, value in statistics.items():
            print(f"{key}: {value}")
