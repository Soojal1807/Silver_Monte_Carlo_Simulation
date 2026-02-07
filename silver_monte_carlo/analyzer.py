import numpy as np
from scipy.stats import skew, kurtosis

def analyze_simulation_results(simulations, start_price):
    """
    Analyzes the results of a Monte Carlo simulation.

    Args:
        simulations (pd.DataFrame): A DataFrame of simulated price paths.
        start_price (float): The starting price of the asset for comparison.

    Returns:
        dict: A dictionary containing the analysis results.
    """
    final_prices = simulations.iloc[-1]
    
    # Price Predictions
    price_predictions = {
        'mean_predicted_price': final_prices.mean(),
        'median_predicted_price': final_prices.median(),
        '5th_percentile': final_prices.quantile(0.05),
        '25th_percentile': final_prices.quantile(0.25),
        '75th_percentile': final_prices.quantile(0.75),
        '95th_percentile': final_prices.quantile(0.95),
    }
    
    # Risk Metrics
    returns = final_prices / start_price - 1
    
    var_95 = returns.quantile(0.05)
    var_99 = returns.quantile(0.01)
    
    cvar_95 = returns[returns <= var_95].mean()
    cvar_99 = returns[returns <= var_99].mean()
    
    risk_metrics = {
        'VaR_95': var_95,
        'VaR_99': var_99,
        'CVaR_95': cvar_95,
        'CVaR_99': cvar_99,
        'prob_loss': (final_prices < start_price).mean(),
        'prob_increase_10': (final_prices > start_price * 1.1).mean(),
        'prob_increase_20': (final_prices > start_price * 1.2).mean(),
        'prob_increase_30': (final_prices > start_price * 1.3).mean(),
    }
    
    # Statistical Summary
    statistical_summary = {
        'expected_return': returns.mean(),
        'std_dev_forecast': final_prices.std(),
        'skewness': skew(final_prices),
        'kurtosis': kurtosis(final_prices),
    }
    
    analysis = {
        "price_predictions": price_predictions,
        "risk_metrics": risk_metrics,
        "statistical_summary": statistical_summary,
        "final_prices": final_prices # For plotting
    }

    return analysis

if __name__ == '__main__':
    # Example usage with dummy data
    from data_fetcher import fetch_silver_data, fetch_inr_data
    from data_processor import process_data
    from monte_carlo_simulator import run_monte_carlo_simulation

    # 1. Fetch and process data
    silver_prices = fetch_silver_data()
    inr_rates = fetch_inr_data()
    _, statistics = process_data(silver_prices, inr_rates)

    if statistics:
        # 2. Run simulation
        simulations = run_monte_carlo_simulation(
            start_price=statistics['latest_price'],
            drift=statistics['drift'],
            volatility=statistics['std_dev']
        )
        
        # 3. Analyze results
        analysis_results = analyze_simulation_results(simulations, statistics['latest_price'])

        print("Simulation Analysis:")
        for section, metrics in analysis_results.items():
            if section != 'final_prices':
                print(f"\n----- {section.replace('_', ' ').title()} -----")
                for key, value in metrics.items():
                    print(f"{key}: {value:.4f}")
