# Silver Monte Carlo Simulation

## Project Overview

This project implements a Monte Carlo simulation to forecast future prices of Silver in Indian Rupees (INR) based on historical data. It provides tools for data fetching, preprocessing, running simulations, analyzing results, generating visualizations, and producing an executive summary.

## Features

-   **Historical Data Fetching:** Retrieves historical Silver prices (`SI=F`) and USD/INR exchange rates (`INR=X`) from Yahoo Finance.
-   **Data Preprocessing:** Cleans and processes raw data, calculates daily log returns, drift, volatility, and other statistical metrics.
-   **Monte Carlo Simulation:** Simulates thousands of potential future price paths for Silver using Geometric Brownian Motion.
-   **Results Analysis:** Analyzes simulation outcomes, providing price predictions (mean, median, confidence intervals), risk metrics (VaR, CVaR, probability of loss), and potential upside probabilities.
-   **Dynamic Visualizations:** Generates various plots including historical prices, daily returns distribution, rolling volatility, simulation paths with confidence intervals, final price distribution, and fan charts.
-   **Executive Summary:** Compiles key historical and simulation-based insights into a readable text report.

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Soojal1807/Silver_Monte_Carlo_Simulation.git
    cd Silver_Monte_Carlo_Simulation
    ```
    *(Note: If you have already set up the project, you can skip this step and ensure you are in the project's root directory.)*

2.  **Navigate to the project directory:**
    ```bash
    cd silver_monte_carlo
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    venv\Scripts\activate   # On Windows
    # source venv/bin/activate  # On macOS/Linux
    ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the Monte Carlo simulation and generate all reports and visualizations:

1.  Ensure your virtual environment is activated (if you created one).
2.  Navigate to the `silver_monte_carlo` directory.
3.  Execute the main script:
    ```bash
    python main.py
    ```

The script will fetch data, run the simulation, generate all output files, and print an executive summary to the console.

## Output

All generated output files are saved in the `silver_monte_carlo/output/` directory:

-   `executive_summary.txt`: A detailed text report summarizing historical analysis and simulation results.
-   `simulation_results.csv`: A CSV file containing the raw data for all simulated price paths.
-   `visualizations/`: A subdirectory containing various `.png` image files of the generated plots:
    -   `historical_prices.png`
    -   `daily_returns_distribution.png`
    -   `rolling_volatility.png`
    -   `simulation_paths.png`
    -   `final_price_distribution.png`
    -   `fan_chart.png`
    -   `pdf_cdf_of_returns.png`

## Project Structure

```
Silver_Monte_Carlo_Simulation/
├── silver_monte_carlo/
│   ├── analyzer.py             # Analyzes simulation results (VaR, CVaR, etc.)
│   ├── data_fetcher.py         # Fetches historical Silver and INR data
│   ├── data_processor.py       # Processes raw data, calculates metrics
│   ├── main.py                 # Main script to run the entire simulation pipeline
│   ├── monte_carlo_simulator.py# Implements the Monte Carlo simulation logic
│   ├── requirements.txt        # Python dependencies
│   ├── visualizer.py           # Generates various plots and charts
│   └── output/                 # Generated reports and visualizations (after running main.py)
│       ├── executive_summary.txt
│       ├── simulation_results.csv
│       └── visualizations/
│           └── (PNG image files)
└── README.md                   # This file
```

## Disclaimer

This project is for educational and informational purposes only and should not be considered financial advice. Monte Carlo simulations are based on historical data and certain assumptions, and past performance is not indicative of future results. Always consult with a qualified financial professional before making investment decisions.
