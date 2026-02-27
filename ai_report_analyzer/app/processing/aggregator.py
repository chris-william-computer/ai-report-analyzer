def aggregate_data(df):
    """
    Calculate comprehensive statistical summaries for numeric columns in a DataFrame.

    This function analyzes a pandas DataFrame and computes essential statistical measures
    for all numeric columns (both integers and floating-point numbers). It generates
    mean, sum, minimum, and maximum values for each numeric column, providing a quick
    overview of the data distribution and range. The aggregated statistics serve as
    foundational insights for data analysis, reporting, and AI-driven interpretation
    of the dataset characteristics.

    The function automatically identifies numeric columns using pandas' type selection
    capabilities, focusing only on columns with float64 and int64 data types. This
    selective approach ensures that calculations are performed only on appropriate
    numerical data while ignoring text, categorical, or other non-numeric columns.
    The resulting dictionary structure makes it easy to access specific statistics
    for individual columns or iterate through all computed measures.

    Args:
        df (pandas.DataFrame): Input DataFrame containing the data to analyze. Must
                    contain at least one numeric column (float64 or int64)
                    for meaningful aggregation results. The DataFrame can
                    include mixed data types, but only numeric columns
                    will be processed.

    Returns:
        dict: A nested dictionary where keys are column names of numeric columns
                and values are dictionaries containing statistical measures. Each
                inner dictionary contains 'mean', 'sum', 'min', and 'max' keys
                with their corresponding calculated values for that specific column.

                Example return format:
                {
                    'sales_amount': {
                    'mean': 1250.50,
                    'sum': 25000.0,
                    'min': 100.0,
                    'max': 5000.0
                },
                'quantity': {
                        'mean': 25.3,
                        'sum': 500,
                        'min': 1,
                        'max': 100
                    }
                }

    Example:
        # Sample DataFrame
        df = pd.DataFrame({
            'sales': [1000, 1500, 2000, 1200],
            'quantity': [10, 15, 20, 12],
            'name': ['A', 'B', 'C', 'D']  # Non-numeric, will be ignored
        })
        
        stats = aggregate_data(df)
        print(stats['sales']['mean'])  # Output: 1425.0
        print(stats['quantity']['max'])  # Output: 20
    """
    summary_stats = {}
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    
    for col in numeric_cols:
        summary_stats[col] = {
            "mean": df[col].mean(),
            "sum": df[col].sum(),
            "min": df[col].min(),
            "max": df[col].max()
        }
    
    return summary_stats

def prepare_context_for_ai(df, stats):
    """
    Format DataFrame content and statistics into a structured text context for AI processing.

    This function combines the initial rows of a DataFrame with computed statistical
    summaries to create a comprehensive text representation suitable for AI analysis.
    The resulting context string provides both sample data (first 5 rows) and
    statistical insights, giving AI systems sufficient information to understand
    data patterns, relationships, and characteristics. This preparation step is
    crucial for effective AI-driven data interpretation and insight generation.

    The function creates a human-readable format that preserves the structure of
    the original data while highlighting key statistical properties. The sample
    data shows actual values and column relationships, while the statistics reveal
    overall data distribution, ranges, and central tendencies. This dual approach
    enables AI systems to perform both granular analysis and high-level pattern
    recognition on the provided dataset.

    Args:
        df (pandas.DataFrame): The original DataFrame containing the data to be
            analyzed. This DataFrame provides the sample data
            (first 5 rows) that will be included in the context.

        stats (dict): Dictionary containing statistical summaries as returned by
                the aggregate_data function. This dictionary provides the
                numerical insights that complement the sample data.

    Returns:
        str: Formatted string containing both the first 5 rows of the DataFrame
            and the statistical summaries in a structured format. The returned
            string follows the pattern:
            "Data Head:
                [first 5 rows of DataFrame as formatted string]
            
                Statistics:
                [string representation of stats dictionary]"

            This format is optimized for AI consumption, providing both sample
                data and statistical context in a clear, readable structure.

    Example:
        df = pd.DataFrame({
            'revenue': [1000, 1500, 2000, 1200, 1800],
            'users': [100, 150, 200, 120, 180]
        })
        
        stats = {'revenue': {'mean': 1500, 'sum': 7500}, 'users': {'mean': 150, 'sum': 750}}
        
        context = prepare_context_for_ai(df, stats)
        print(context)
        # Output will contain both the first 5 rows and the statistical summary
    """
    head_data = df.head(5).to_string()
    stats_string = str(stats)
    context = f"Data Head:\n{head_data}\n\nStatistics:\n{stats_string}"
    return context