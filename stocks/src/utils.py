import os
import time
import datetime
import numpy as np
import pandas as pd
import empyrical  
import warnings
from IPython.display import display, Markdown


warnings.filterwarnings("ignore", message="Module \"zipline.assets\" not found.*")

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
        df (pd.DataFrame): MultiIndex DataFrame. df.index.levels[0] are symbols,
        df_cleaned_OHLCV.index.levels[1] are dates.
        df containing stock's Open, High, Low, Close, Adj Close, Volume, Adj Open, Adj High, Adj Low.
        ticker (str): The stock ticker symbol (e.g., 'NVDA').
        risk_free_rate (float): The annualized risk-free rate. Default is 0.0.
        output_debug_data (bool): If True, print Adj Close prices and returns (default: False).

    Returns:
        pd.DataFrame: A DataFrame with the ticker as index and 'Sharpe Ratio', 'Sortino Ratio', and 'Omega Ratio' as columns.
                       Returns None if there is an error.  Crucially changed to return None, not an empty dataframe.
    """
    try:
        # Extract Adj Close prices for ticker, sorted by date oldest to newest
        adj_close_prices = df.loc[ticker]['Adj Close'].sort_index()

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


def get_latest_dfs(df, num_rows):
    """
    Get the latest N rows for each symbol from a multi-index DataFrame, 
    returning multiple filtered DataFrames in a list.

    Processes a DataFrame with multi-level index (Symbol, Date) to return:
    - For each number in num_rows: A DataFrame containing the latest N dates
      for each symbol, sorted by symbol and chronological date order

    Parameters:
    df (pd.DataFrame): Input DataFrame with MultiIndex of (Symbol, Date)
    num_rows (list[int]): List of integers specifying numbers of recent rows to return

    Returns:
    list[pd.DataFrame]: List of filtered DataFrames in the same order as num_rows
                        Example: [df_30, df_60] for num_rows=[30, 60]

    Raises:
    KeyError: If DataFrame doesn't have 'Symbol' and 'Date' index levels
    TypeError: If num_rows contains non-integer values

    Example:
    >>> df = pd.DataFrame(index=pd.MultiIndex.from_product(
    ...     [['AAPL', 'MSFT'], pd.date_range('2020-01-01', periods=100)],
    ...     names=['Symbol', 'Date']
    ... ))
    >>> dfs = get_latest_dfs(df, [30, 60])
    >>> len(dfs[0].loc['AAPL'])
    30
    >>> len(dfs[1].loc['MSFT'])
    60
    """
    result_list = []

    # Validate input types
    if not all(isinstance(n, int) for n in num_rows):
        raise TypeError("All elements in num_rows must be integers")

    for num in num_rows:
        # Group by symbol and process each group
        result = (
            df.groupby(level='Symbol', group_keys=False)
            .apply(lambda group: 
                # Sort group dates descending and take top N rows
                group.sort_index(level='Date', ascending=False).head(num)
            )
        )

        # Global sort for final output:
        # 1. Symbols in alphabetical order (ascending=True)
        # 2. Dates in chronological order (ascending=True) within each symbol
        result = result.sort_index(
            level=['Symbol', 'Date'], 
            ascending=[True, True]
        )

        result_list.append(result)

    return result_list


def filter_symbols_with_missing_values(df):
    """
    Filters out symbols from a MultiIndex DataFrame that have:
    1. Any missing values in any columns
    2. Missing any dates present in the original DataFrame's date index

    Args:
        df (pd.DataFrame): A pandas DataFrame with a MultiIndex, where the first
                           level is the symbol and the second level is the date.

    Returns:
        tuple: A tuple containing:
            - filtered_df (pd.DataFrame): A DataFrame containing only the symbols
              without missing values or dates. Returns empty if none are clean.
            - symbols_with_missing (list): List of symbols with missing data/dates.
    """
    if df.empty:
        return pd.DataFrame(), []

    # Get all unique dates from the original DataFrame
    expected_dates = df.index.levels[1].unique()
    
    symbols_with_missing = []
    filtered_data = []
    kept_symbols = []

    for symbol in df.index.get_level_values(0).unique():
        symbol_df = df.loc[symbol]
        
        # Check for missing values
        has_nan = symbol_df.isnull().any().any()
        
        # Check for missing dates
        missing_dates = expected_dates.difference(symbol_df.index)
        
        if has_nan or len(missing_dates) > 0:
            symbols_with_missing.append(symbol)
        else:
            filtered_data.append(symbol_df)
            kept_symbols.append(symbol)

    if filtered_data:
        filtered_df = pd.concat(
            filtered_data, 
            keys=kept_symbols, 
            names=['Symbol', 'Date']
        )
    else:
        filtered_df = pd.DataFrame()

    return filtered_df, symbols_with_missing


def convert_volume(value):
    """
    Convert a string volume representation with suffix (M/K) to float millions.
    
    Handles values like '51.73M' (51.73 million) or '111.53K' (0.11153 million),
    converting them to float values in millions unit.

    Parameters:
    value (str): Input string value to convert. Can contain 'M' (million) 
                 or 'K' (thousand) suffix. Also handles NaN values.

    Returns:
    float: Numerical value in millions. Returns np.nan for invalid formats,
           unknown suffixes, or non-string inputs.

    Example:
    >>> convert_volume('51.73M')
    51.73
    >>> convert_volume('111.53K')
    0.11153
    >>> convert_volume('invalid')
    nan
    """
    # Handle missing values immediately
    if pd.isna(value):
        return np.nan

    try:
        # Clean and standardize input: remove whitespace, make uppercase
        cleaned = value.strip().upper()
        
        # Extract suffix (last character) and numerical part
        suffix = cleaned[-1]
        number_str = cleaned[:-1]
        
        # Convert numerical part to float
        number = float(number_str)
        
        # Apply conversion based on suffix
        if suffix == 'M':
            # Already in millions, return directly
            return number
        elif suffix == 'K':
            # Convert thousands to millions (divide by 1000)
            return number / 1000
        else:
            # Return NaN for unknown suffixes (e.g., 'B', 'T')
            return np.nan
            
    except (ValueError, IndexError, TypeError):
        # Handle various error scenarios:
        # - ValueError: if number conversion fails
        # - IndexError: if string is empty after cleaning
        # - TypeError: if input isn't string-like
        return np.nan


# ====================

def get_ohlcv_files(dir, create_dir=True):
    """Return list of files matching df_OHLCV_ pattern in specified directory"""
    if create_dir:
        os.makedirs(dir, exist_ok=True)
    try:
        return [f for f in os.listdir(dir) if f.startswith('df_OHLCV_')]
    except FileNotFoundError:
        return []

def process_downloads_dir(downloads_dir, limit=20):
    """Process Downloads directory with time-based file limiting"""
    try:
        # Get all files with their paths and modification times
        all_files = []
        for f in os.listdir(downloads_dir):
            file_path = os.path.join(downloads_dir, f)
            if os.path.isfile(file_path):
                all_files.append(file_path)
        
        # Sort by modification time (newest first)
        all_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Apply limit and filter for pattern
        latest_files = all_files[:limit]
        matched_files = [f for f in latest_files 
                       if os.path.basename(f).startswith('df_OHLCV_')]
        
        # Display search status with dark-mode friendly color
        msg = f"<span style='color:#00ffff;font-weight:500'>[Downloads] Scanned latest {len(latest_files)} files • Found {len(matched_files)} matches</span>"
        display(Markdown(msg))

        return matched_files
    
    except Exception as e:
        display(Markdown(f"<span style='color:red'>Error accessing Downloads: {str(e)}</span>"))
        return []

def display_file_selector(files_full_path):
    """Show interactive file selection interface with file metadata"""
    display(Markdown("**Available OHLCV files:**"))
    
    for idx, f in enumerate(files_full_path, 1):
        # Get file metadata
        name = os.path.basename(f)
        size = os.path.getsize(f)
        timestamp = os.path.getmtime(f)
        
        # Format metadata
        size_mb = size / (1024 * 1024)
        formatted_date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
        
        # Create markdown with metadata
        file_info = (
            f"- ({idx}) `{name}` "
            f"<span style='color:#00ffff'>"
            f"({size_mb:.2f} MB, {formatted_date})"
            f"</span>"
        )
        display(Markdown(file_info))
    
    print(f'\nInput a number into the prompt (top of the screen) to select file to process')

def get_user_choice(files_full_path):
    """Handle user input with validation"""
    while True:
        try:
            prompt = f"Select file (1-{len(files_full_path)}):"
            choice = int(input(prompt))
            if 1 <= choice <= len(files_full_path):
                return files_full_path[choice-1]
            display(Markdown(f"<span style='color:red'>Enter 1-{len(files_full_path)}</span>"))
        except ValueError:
            display(Markdown("<span style='color:red'>Numbers only!</span>"))

def generate_clean_filename(source_file):
    """Create cleaned filename with _clean suffix"""
    base, ext = os.path.splitext(source_file)
    return f"{base}_clean{ext}"


def main_processor(data_dir='../data', downloads_dir=None, downloads_limit=20, clean_name_override=None):
    """Orchestrate the file selection process with Downloads limiting"""
    # Set default downloads directory
    if downloads_dir is None:
        downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
    # Get data directory files
    data_files = [os.path.join(data_dir, f) for f in get_ohlcv_files(data_dir, create_dir=True)]
    
    # Get downloads directory files with limiting
    downloads_files = []
    if os.path.exists(downloads_dir):
        downloads_files = process_downloads_dir(downloads_dir, downloads_limit)
    
    # Combine file lists
    ohlcv_files = data_files + downloads_files
    
    if not ohlcv_files:
        display(Markdown("**Error:** No OHLCV files found!"))
        return None, None
    
    # User interaction
    display_file_selector(ohlcv_files)  # Existing function
    selected_file = get_user_choice(ohlcv_files)  # Existing function
    
    # Generate clean path (always in data directory)
    clean_name = generate_clean_filename(os.path.basename(selected_file))
    if clean_name_override is not None:  # Override if provided
        clean_name = clean_name_override
    dest_path = os.path.join(data_dir, clean_name)
    
    display(Markdown(f"""
    **Selected paths:**
    - Source: `{selected_file}`  
    - Destination: `{dest_path}`
    """))
    return selected_file, dest_path


# def main_processor(data_dir='../data', downloads_dir=None, downloads_limit=20):
#     """Orchestrate the file selection process with Downloads limiting"""
#     # Set default downloads directory
#     if downloads_dir is None:
#         downloads_dir = os.path.join(os.path.expanduser('~'), 'Downloads')
    
#     # Get data directory files
#     data_files = [os.path.join(data_dir, f) for f in get_ohlcv_files(data_dir, create_dir=True)]
    
#     # Get downloads directory files with limiting
#     downloads_files = []
#     if os.path.exists(downloads_dir):
#         downloads_files = process_downloads_dir(downloads_dir, downloads_limit)
    
#     # Combine file lists
#     ohlcv_files = data_files + downloads_files
    
#     if not ohlcv_files:
#         display(Markdown("**Error:** No OHLCV files found!"))
#         return None, None
    
#     # User interaction
#     display_file_selector(ohlcv_files)  # Existing function
#     selected_file = get_user_choice(ohlcv_files)  # Existing function
    
#     # Generate clean path (always in data directory)
#     clean_name = generate_clean_filename(os.path.basename(selected_file))
#     dest_path = os.path.join(data_dir, clean_name)
    
#     display(Markdown(f"""
#     **Selected paths:**
#     - Source: `{selected_file}`  
#     - Destination: `{dest_path}`
#     """))
#     return selected_file, dest_path

# ====================

