import numpy as np
import pandas as pd

def run_monte_carlo_simulation(start_price, drift, volatility, forecast_period=252, num_simulations=10000):
    """
    Runs a Monte Carlo simulation for future asset prices using Geometric Brownian Motion.

    Args:
        start_price (float): The starting price of the asset.
        drift (float): The drift component of the asset's returns.
        volatility (float): The volatility of the asset's returns.
        forecast_period (int): The number of trading days to forecast.
        num_simulations (int): The number of simulations to run.

    Returns:
        pd.DataFrame: A DataFrame where each column represents a simulated price path.
    """
    # Generate random daily returns
    daily_returns = np.exp(drift + volatility * np.random.normal(0, 1, (forecast_period, num_simulations)))
    
    # Create a price path for each simulation
    price_paths = np.zeros_like(daily_returns)
    price_paths[0] = start_price
    for t in range(1, forecast_period):
        price_paths[t] = price_paths[t - 1] * daily_returns[t]
        
    return pd.DataFrame(price_paths)

if __name__ == '__main__':
    # Example usage with dummy data from the previous step
    from data_fetcher import fetch_silver_data, fetch_inr_data
    from data_processor import process_data

    # 1. Fetch data
    silver_prices = fetch_silver_data()
    inr_rates = fetch_inr_data()

    # 2. Process data to get statistics
    processed_data, statistics = process_data(silver_prices, inr_rates)

    if statistics:
        # 3. Run simulation
        start_price = statistics['latest_price']
        drift = statistics['drift']
        volatility = statistics['std_dev']

        simulations = run_monte_carlo_simulation(start_price, drift, volatility)
        
        print("Monte Carlo Simulation Results:")
        print(simulations.head())
        print(f"\nSimulated {simulations.shape[1]} paths over {simulations.shape[0]} days.")
