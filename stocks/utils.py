import os
import time
import datetime

def get_latest_downloaded_files(directory_path, num_files=10):
    """
    Returns the N most recent files in a directory, sorted by modification time.

    Args:
        directory_path (str): The path to the directory to search.
        num_files (int): The number of files to list (default: 10).

    Returns:
        list: A list of tuples, where each tuple contains:
              (filename, file_size_bytes, last_modified_time)
              Returns an empty list if the directory doesn't exist or is empty.
    """

    # Check if the directory exists
    if not os.path.exists(directory_path):
        return []

    # Get a list of all files in the directory
    file_list = []
    try:
        # Iterate over all files in the directory
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            # Check if the file is a regular file (not a directory)
            if os.path.isfile(filepath):
                # Get the size of the file
                file_size = os.path.getsize(filepath)
                # Get the last modification time of the file
                last_modified_time = os.path.getmtime(filepath)
                # Add the file to the list
                file_list.append((filename, file_size, last_modified_time))

        # Sort the list of files by modification time
        file_list.sort(key=lambda x: x[2], reverse=True)

        # Return the top N files
        return file_list[:num_files]
    except OSError:
        # If there is an error, return an empty list
        return []




import numpy as np
import pandas as pd
import empyrical  
import warnings

warnings.filterwarnings("ignore", message="Module \"zipline.assets\" not found.*")

def _calculate_performance_metrics(returns, risk_free_rate=0.0):
    """
    Calculates Sortino Ratio, Sharpe Ratio, and Omega Ratio using PyFolio/Empyrical.

    Args:
        returns (pd.Series or np.array):  Daily returns of the investment.
                                         Must be a Pandas Series with a DatetimeIndex.
        risk_free_rate (float):  The risk-free rate (annualized). Default is 0.0.

    Returns:
        dict: A dictionary containing the calculated ratios.
              Returns None if there is an error or the input is invalid.
    """

    try:
        # Ensure returns is a pandas Series with a DatetimeIndex.  Crucial for pyfolio.
        if not isinstance(returns, pd.Series):
            returns = pd.Series(returns)  # Convert to Series if needed
        if not isinstance(returns.index, pd.DatetimeIndex):
            raise ValueError("Returns must be a Pandas Series with a DatetimeIndex.")

        # Convert annualized risk-free rate to daily rate
        days_per_year = 252  # Standard for financial calculations
        daily_risk_free_rate = risk_free_rate / days_per_year

        # Calculate the Sharpe Ratio using empyrical (as pyfolio's is deprecated)
        sharpe_ratio = empyrical.sharpe_ratio(returns, risk_free=daily_risk_free_rate, annualization=days_per_year)

        # Calculate the Sortino Ratio using empyrical
        sortino_ratio = empyrical.sortino_ratio(returns, required_return=daily_risk_free_rate, annualization=days_per_year)

        # Calculate the Omega Ratio using empyrical
        omega_ratio = empyrical.omega_ratio(returns, risk_free=daily_risk_free_rate, annualization=days_per_year)


        return {
            "Sharpe Ratio": sharpe_ratio,
            "Sortino Ratio": sortino_ratio,
            "Omega Ratio": omega_ratio
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

import pandas as pd
import empyrical  # Make sure empyrical is installed: pip install empyrical

def calculate_performance_metrics(returns, risk_free_rate=0.0):
    """
    Calculates Sortino Ratio, Sharpe Ratio, and Omega Ratio using PyFolio/Empyrical.

    Args:
        returns (pd.Series or np.array):  Daily returns of the investment.
                                         Must be a Pandas Series with a DatetimeIndex.
        risk_free_rate (float):  The risk-free rate (annualized). Default is 0.0.

    Returns:
        dict: A dictionary containing the calculated ratios with modified keys.
              Returns None if there is an error or the input is invalid.
    """

    try:
        # Ensure returns is a pandas Series with a DatetimeIndex.  Crucial for pyfolio.
        if not isinstance(returns, pd.Series):
            returns = pd.Series(returns)  # Convert to Series if needed
        if not isinstance(returns.index, pd.DatetimeIndex):
            raise ValueError("Returns must be a Pandas Series with a DatetimeIndex.")

        # Convert annualized risk-free rate to daily rate
        days_per_year = 252  # Standard for financial calculations
        daily_risk_free_rate = risk_free_rate / days_per_year

        # Calculate the Sharpe Ratio using empyrical (as pyfolio's is deprecated)
        sharpe_ratio = empyrical.sharpe_ratio(returns, risk_free=daily_risk_free_rate, annualization=days_per_year)

        # Calculate the Sortino Ratio using empyrical
        sortino_ratio = empyrical.sortino_ratio(returns, required_return=daily_risk_free_rate, annualization=days_per_year)

        # Calculate the Omega Ratio using empyrical
        omega_ratio = empyrical.omega_ratio(returns, risk_free=daily_risk_free_rate, annualization=days_per_year)

        n = len(returns) + 1  # Calculate n only once

        return {
            f"Sharpe {n}d": sharpe_ratio,
            f"Sortino {n}d": sortino_ratio,
            f"Omega {n}d": omega_ratio
        }

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def calculate_returns(adj_close_prices):
    """
    Calculates daily returns from adjusted close prices.

    Args:
        adj_close_prices (pd.Series): Pandas Series of adjusted close prices with DatetimeIndex.

    Returns:
        pd.Series: Pandas Series of daily returns with DatetimeIndex, sorted by date (oldest to newest).
    """
    try:
        if not isinstance(adj_close_prices, pd.Series):
            raise TypeError("Input must be a Pandas Series.")
        if not isinstance(adj_close_prices.index, pd.DatetimeIndex):
            raise ValueError("Input Series must have a DatetimeIndex.")

        # Sort the index to ensure correct return calculation (oldest to newest)
        adj_close_prices = adj_close_prices.sort_index()

        # Calculate daily returns using pct_change()
        returns = adj_close_prices.pct_change().dropna()  # Drop the first NaN value

        return returns

    except Exception as e:
        print(f"Error calculating returns: {e}")
        return None


def analyze_stock(df, ticker, risk_free_rate=0.0, output_debug_data=False):
    """
    Analyzes a single stock's performance based on its adjusted close prices.

    Args:
        df (pd.DataFrame): Pandas DataFrame containing stock data, including 'Adj Close' column.
        ticker (str): The stock ticker symbol (e.g., 'NVDA').
        risk_free_rate (float): The annualized risk-free rate. Default is 0.0.
        output_debug_data (bool): If True, print Adj Close prices and returns (default: False).

    Returns:
        pd.DataFrame: A DataFrame with the ticker as index and 'Sharpe Ratio', 'Sortino Ratio', and 'Omega Ratio' as columns.
                       Returns None if there is an error.  Crucially changed to return None, not an empty dataframe.
    """
    try:
        # Extract Adj Close prices for the specified ticker
        adj_close_prices = df.loc[ticker]['Adj Close']

        # Check if adj_close_prices is a Series
        if not isinstance(adj_close_prices, pd.Series):
             raise TypeError(f"Expected a Pandas Series for Adj Close prices of {ticker}. Check that {ticker} exists in the DataFrame, and that 'Adj Close' is a valid column")

        # Calculate returns
        returns_series = calculate_returns(adj_close_prices)

        if returns_series is not None:
            # Output debug data if requested
            if output_debug_data:
                print(f"--- Debug Data for {ticker} ---")
                print("\nAdj Close Prices (Dates and Values):")
                print(adj_close_prices)  #This is a Series, prints the index(dates) and values.
                print("\nReturns:")
                print(returns_series)

            # Calculate performance metrics
            performance_metrics = calculate_performance_metrics(returns_series, risk_free_rate=risk_free_rate)

            if performance_metrics:
                # Create a DataFrame from the metrics
                metrics_df = pd.DataFrame(performance_metrics, index=[ticker])
                return metrics_df
            else:
                print(f"Could not calculate performance metrics for {ticker}.")
                return None  # Return None, not an empty DataFrame
        else:
            print(f"Failed to calculate returns for {ticker}.")
            return None # Return None, not an empty DataFrame

    except KeyError:
        print(f"Ticker '{ticker}' not found in DataFrame.")
        return None # Return None, not an empty DataFrame
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        return None # Return None, not an empty DataFrame



def get_recent_rows(df, num_rows=None):

    """
    Returns a DataFrame containing the most recent specified number of rows for each symbol in the input DataFrame.
    If num_rows is None, all rows for each symbol are returned.

    Args:
        df: A pandas DataFrame with a MultiIndex, where the first level is the symbol and the second level is a Timestamp representing the date.
        num_rows: The number of recent rows to include for each symbol.
                  If None (default), all rows for each symbol are returned.

    Returns:
        A pandas DataFrame containing the most recent specified number of rows for each symbol.
        Returns an empty DataFrame if df is empty.
    """

    if df.empty:
        return pd.DataFrame()

    # Sort the DataFrame by symbol and date (within each symbol)
    df = df.sort_index()


    if num_rows is None:
        return df  # Return the entire DataFrame if num_rows is None


    def get_last_n_rows(group):
        return group.tail(num_rows)

    # Group by symbol and apply the function to get the last n rows for each group
    recent_df = df.groupby(level=0, group_keys=False).apply(get_last_n_rows)

    return recent_df


def find_sorted_intersection(list1, list2):
    """
    Finds the intersection of two lists and returns a new sorted list containing
    the common elements.

    Args:
        list1 (list): The first list.
        list2 (list): The second list.

    Returns:
        list: A new sorted list containing the common elements of list1 and list2.
              Returns an empty list if there are no common elements or if either
              input list is None or empty.
    """

    if not list1 or not list2:  # Check for empty or None lists
        return []

    # Convert lists to sets for efficient intersection finding
    set1 = set(list1)
    set2 = set(list2)

    # Find the intersection using set intersection
    intersection_set = set1.intersection(set2)

    # Convert the intersection set to a list and sort it
    intersection_list = sorted(list(intersection_set))

    return intersection_list


def filter_df_dates_to_reference_symbol(df, reference_symbol="AAPL"):
    """
    Filters symbols in a DataFrame based on date index matching a reference symbol (default AAPL)
    and provides analysis of the filtering results.

    Args:
        df (pd.DataFrame): DataFrame with a MultiIndex ('Symbol', 'Date').
        reference_symbol (str): The symbol to use as the reference for date comparison. Defaults to "AAPL".

    Returns:
        pd.DataFrame: The filtered DataFrame.  Prints analysis to standard output.
    """

    # Get the date index for the reference symbol.  Return empty DataFrame if symbol not found
    try:
        reference_dates = df.loc[reference_symbol].index
    except KeyError:
        print(f"Error: Reference symbol '{reference_symbol}' not found in DataFrame.")
        return pd.DataFrame()  # Return an empty DataFrame if reference_symbol is not found
    
    original_symbols = df.index.get_level_values('Symbol').unique().tolist()

    # Filter symbols based on date index matching with the reference symbol
    filtered_symbols = []
    for symbol in original_symbols:
        try: # Handle the case where a symbol might be missing from the df
            symbol_dates = df.loc[symbol].index
        except KeyError:
            continue # Skip to the next symbol if this one is missing

        if (len(symbol_dates) == len(reference_dates) and symbol_dates.equals(reference_dates)):
            filtered_symbols.append(symbol)

    # Create the filtered DataFrame
    df_filtered = df.loc[filtered_symbols]


    # Analyze the filtering results
    print(f"Original number of symbols: {len(original_symbols)}")
    print(f"Number of symbols after filtering: {len(filtered_symbols)}")
    print(f"Number of symbols filtered out: {len(original_symbols) - len(filtered_symbols)}")

    filtered_out_symbols = list(set(original_symbols) - set(filtered_symbols))

    print("\nFirst 10 symbols that were filtered out:")
    print(filtered_out_symbols[:10])

    if filtered_out_symbols:
        print("\nExample of dates for first filtered out symbol:")
        first_filtered_symbol = filtered_out_symbols[0]
        try:  # Handle potential KeyError if the symbol doesn't exist (e.g., due to filtering earlier)
            print(f"\nDates for {first_filtered_symbol}:")
            print(df.loc[first_filtered_symbol].index)
        except KeyError:
            print(f"\nSymbol '{first_filtered_symbol}' not found in the original DataFrame.")


    print("\nFiltered DataFrame info:")
    print(df_filtered.info())

    return df_filtered


