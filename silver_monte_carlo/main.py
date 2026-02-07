import os
import pandas as pd

# Import project modules
from data_fetcher import fetch_silver_data, fetch_inr_data
from data_processor import process_data
from monte_carlo_simulator import run_monte_carlo_simulation
from analyzer import analyze_simulation_results
import visualizer as viz

# --- Configuration ---
SILVER_TICKER = "SI=F"
INR_TICKER = "INR=X"
START_DATE = "2015-01-01"
END_DATE = "2025-12-30" # As per prompt, but will fetch up to today
NUM_SIMULATIONS = 10000
FORECAST_PERIOD = 252  # 1 year of trading days

# --- Output Directories ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
VISUALIZATIONS_DIR = os.path.join(OUTPUT_DIR, "visualizations")
RESULTS_CSV_PATH = os.path.join(OUTPUT_DIR, "simulation_results.csv")
SUMMARY_REPORT_PATH = os.path.join(OUTPUT_DIR, "executive_summary.txt")

def create_output_directories():
    """Creates the necessary output directories if they don't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    if not os.path.exists(VISUALIZATIONS_DIR):
        os.makedirs(VISUALIZATIONS_DIR)

def generate_executive_summary(historical_stats, analysis):
    """Generates a formatted string for the executive summary report."""
    summary = f"""
# Executive Summary: Monte Carlo Simulation of Silver Prices in INR

## 1. Historical Analysis (2015 - Present)
- **Annualized Volatility:** {historical_stats['annualized_volatility']:.2%}
- **Mean Daily Return:** {historical_stats['mean_daily_return']:.5f}
- **Maximum Drawdown:** {historical_stats['max_drawdown']:.2%}
- **Sharpe Ratio:** {historical_stats['sharpe_ratio']:.2f}
- **Latest Price (as of analysis):** {historical_stats['latest_price']:.2f} INR/Gram

## 2. Monte Carlo Simulation Results (1-Year Forecast)
Based on {NUM_SIMULATIONS} simulations over {FORECAST_PERIOD} trading days:

### Price Predictions:
- **Mean Predicted Price:** {analysis['price_predictions']['mean_predicted_price']:.2f} INR/Gram
- **Median Predicted Price:** {analysis['price_predictions']['median_predicted_price']:.2f} INR/Gram
- **Confidence Interval (90%):** The price is expected to be between {analysis['price_predictions']['5th_percentile']:.2f} and {analysis['price_predictions']['95th_percentile']:.2f} INR/Gram.

### Risk Assessment:
- **Value at Risk (VaR 95%):** There is a 5% chance of losing at least {-analysis['risk_metrics']['VaR_95']:.2%} of the investment.
- **Conditional VaR (CVaR 95%):** In the worst 5% of scenarios, the average loss is {-analysis['risk_metrics']['CVaR_95']:.2%}.
- **Probability of Loss:** There is a {analysis['risk_metrics']['prob_loss']:.2%} chance the price will be lower than the current price in one year.

### Potential Upside:
- **Probability of >10% Gain:** {analysis['risk_metrics']['prob_increase_10']:.2%}
- **Probability of >20% Gain:** {analysis['risk_metrics']['prob_increase_20']:.2%}

## 3. Investment Recommendations & Insights
- **Expected Return:** The simulation forecasts an expected return of {analysis['statistical_summary']['expected_return']:.2%} over the next year.
- **Volatility:** The forecasted price distribution shows a standard deviation of {analysis['statistical_summary']['std_dev_forecast']:.2f}, indicating the potential range of outcomes.
- **Insight:** Based on the historical trend and simulation, [Your interpretation here, e.g., "silver shows a positive expected return, but investors should be aware of the significant downside risk as indicated by the VaR and the wide confidence interval."]

This analysis is based on historical data and models with inherent assumptions. It should not be considered as financial advice.
"""
    return summary.strip()


def main():
    """Main function to run the entire data science project."""
    print("Starting Monte Carlo Simulation for Silver Price...\n")
    create_output_directories()

    # 1. Data Collection
    print("Step 1: Fetching historical data...")
    silver_data = fetch_silver_data(SILVER_TICKER, START_DATE, END_DATE)
    inr_data = fetch_inr_data(INR_TICKER, START_DATE, END_DATE)
    if silver_data is None or inr_data is None:
        print("Failed to fetch data. Exiting.")
        return
    print("Data fetched successfully.")

    # 2. Data Preprocessing & Analysis
    print("\nStep 2: Processing data and calculating historical metrics...")
    processed_data, historical_stats = process_data(silver_data, inr_data)
    if processed_data is None:
        print("Failed to process data. Exiting.")
        return
    print("Data processed successfully.")
    print(f"  - Latest Silver Price: {historical_stats['latest_price']:.2f} INR/Gram")
    print(f"  - Annualized Volatility: {historical_stats['annualized_volatility']:.2%}")

    # 3. Monte Carlo Simulation
    print(f"\nStep 3: Running Monte Carlo simulation with {NUM_SIMULATIONS} paths...")
    simulations = run_monte_carlo_simulation(
        start_price=historical_stats['latest_price'],
        drift=historical_stats['drift'],
        volatility=historical_stats['std_dev'],
        forecast_period=FORECAST_PERIOD,
        num_simulations=NUM_SIMULATIONS
    )
    print("Simulation complete.")

    # 4. Analysis & Insights
    print("\nStep 4: Analyzing simulation results...")
    analysis_results = analyze_simulation_results(simulations, historical_stats['latest_price'])
    print("Analysis complete.")
    
    # Save simulation results to CSV
    simulations.to_csv(RESULTS_CSV_PATH)
    print(f"  - Full simulation data saved to '{RESULTS_CSV_PATH}'")

    # 5. Visualization
    print("\nStep 5: Generating visualizations...")
    viz.plot_historical_prices(processed_data, save_path=VISUALIZATIONS_DIR)
    viz.plot_daily_returns_distribution(processed_data, save_path=VISUALIZATIONS_DIR)
    viz.plot_rolling_volatility(processed_data, save_path=VISUALIZATIONS_DIR)
    viz.plot_simulation_paths(simulations, analysis_results, save_path=VISUALIZATIONS_DIR)
    viz.plot_final_price_distribution(analysis_results, save_path=VISUALIZATIONS_DIR)
    viz.plot_fan_chart(simulations, save_path=VISUALIZATIONS_DIR)
    viz.plot_pdf_and_cdf(analysis_results, save_path=VISUALIZATIONS_DIR)
    print(f"Visualizations saved in '{VISUALIZATIONS_DIR}' directory.")

    # 6. Reporting
    print("\nStep 6: Generating executive summary...")
    executive_summary = generate_executive_summary(historical_stats, analysis_results)
    
    with open(SUMMARY_REPORT_PATH, 'w') as f:
        f.write(executive_summary)
    
    print(f"Executive summary saved to '{SUMMARY_REPORT_PATH}'")
    print("\n--- Executive Summary ---")
    print(executive_summary)
    print("\nProject finished successfully!")


if __name__ == '__main__':
    main()
