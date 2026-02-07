import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def plot_historical_prices(data, save_path="visualizations"):
    """Plots historical silver prices with a trend line."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data['Silver_INR_Gram'], label='Silver Price (INR/Gram)')
    
    # Trend line
    z = np.polyfit(range(len(data)), data['Silver_INR_Gram'], 1)
    p = np.poly1d(z)
    plt.plot(data.index, p(range(len(data))), "r--", label="Trend Line")
    
    plt.title('Historical Silver Prices in INR (2015-2025)')
    plt.xlabel('Date')
    plt.ylabel('Price (INR per Gram)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'historical_prices.png'))
    plt.close()

def plot_daily_returns_distribution(data, save_path="visualizations"):
    """Plots the distribution of daily log returns."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Log_Returns'], bins=50, kde=True)
    plt.title('Distribution of Daily Log Returns')
    plt.xlabel('Log Return')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'daily_returns_distribution.png'))
    plt.close()

def plot_rolling_volatility(data, save_path="visualizations"):
    """Plots the rolling volatility of daily returns."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    rolling_volatility = data['Log_Returns'].rolling(window=252).std() * np.sqrt(252)
    plt.figure(figsize=(12, 6))
    plt.plot(rolling_volatility.index, rolling_volatility)
    plt.title('Rolling Annualized Volatility (1-Year Window)')
    plt.xlabel('Date')
    plt.ylabel('Annualized Volatility')
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'rolling_volatility.png'))
    plt.close()

def plot_simulation_paths(simulations, analysis_results, save_path="visualizations"):
    """Plots sample simulation paths with confidence intervals."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    plt.figure(figsize=(12, 6))
    # Plot a sample of paths
    plt.plot(simulations.iloc[:, :100], color='grey', alpha=0.1)
    
    # Plot mean and confidence intervals
    plt.plot(simulations.mean(axis=1), color='red', label='Mean Forecast')
    plt.plot(simulations.quantile(0.05, axis=1), 'b--', label='5th Percentile')
    plt.plot(simulations.quantile(0.95, axis=1), 'b--', label='95th Percentile')

    plt.title('Monte Carlo Simulation of Silver Prices (100 Sample Paths)')
    plt.xlabel('Days')
    plt.ylabel('Price (INR per Gram)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'simulation_paths.png'))
    plt.close()

def plot_final_price_distribution(analysis_results, save_path="visualizations"):
    """Plots the distribution of final prices with percentile markers."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    final_prices = analysis_results['final_prices']
    preds = analysis_results['price_predictions']

    plt.figure(figsize=(10, 6))
    sns.histplot(final_prices, bins=100, kde=True)
    
    plt.axvline(preds['5th_percentile'], color='red', linestyle='--', label=f"5th Percentile: {preds['5th_percentile']:.2f}")
    plt.axvline(preds['median_predicted_price'], color='green', linestyle='-', label=f"Median: {preds['median_predicted_price']:.2f}")
    plt.axvline(preds['95th_percentile'], color='red', linestyle='--', label=f"95th Percentile: {preds['95th_percentile']:.2f}")

    plt.title('Distribution of Final Simulated Prices')
    plt.xlabel('Price (INR per Gram)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'final_price_distribution.png'))
    plt.close()

def plot_fan_chart(simulations, save_path="visualizations"):
    """Creates a fan chart showing confidence intervals over time."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        
    plt.figure(figsize=(12, 6))
    
    percentiles = [5, 20, 50, 80, 95]
    colors = ['lightblue', 'skyblue', 'blue', 'skyblue', 'lightblue']
    
    for i in range(len(percentiles) - 1):
        plt.fill_between(simulations.index, 
                         simulations.quantile(percentiles[i]/100, axis=1), 
                         simulations.quantile(percentiles[i+1]/100, axis=1), 
                         color=colors[i],
                         label=f'{percentiles[i]}-{percentiles[i+1]}th Percentile')

    plt.plot(simulations.quantile(0.5, axis=1), color='darkblue', label='Median (50th Percentile)')
    
    plt.title('Fan Chart of Simulated Price Confidence Intervals')
    plt.xlabel('Days')
    plt.ylabel('Price (INR per Gram)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(save_path, 'fan_chart.png'))
    plt.close()

def plot_pdf_and_cdf(analysis_results, save_path="visualizations"):
    """Plots the PDF and CDF of simulated returns."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    final_prices = analysis_results['final_prices']
    returns = final_prices / final_prices.iloc[0] - 1

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # PDF
    sns.histplot(returns, bins=50, kde=True, stat="density", ax=ax1)
    ax1.set_title('Probability Density Function (PDF) of Returns')
    ax1.set_xlabel('Return')
    ax1.set_ylabel('Density')
    ax1.grid(True)
    
    # CDF
    sns.ecdfplot(returns, ax=ax2)
    ax2.set_title('Cumulative Distribution Function (CDF) of Returns')
    ax2.set_xlabel('Return')
    ax2.set_ylabel('Cumulative Probability')
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, 'pdf_cdf_of_returns.png'))
    plt.close()
