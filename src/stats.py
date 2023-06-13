"""
stats.py:

Contains methods for counting and filtering Faial benchmarks.
"""
def get_mean_median_std(dfs):
    """
    Gets the mean, median, and standard deviation for each 
    logic's execution time from a DataFrame.
  
    Parameters:
    dfs (DataFrame): A DataFrame containing a list of execution times.
  
    Returns:
    dict: A dictionary that maps a logic to a list of the mean, median, and standard deviation
    for the logic's execution time.
    """
    stats = {}

    for logic, df in dfs.items():
        data = []
        
        data.append(df['elapsed'].mean())
        data.append(df['elapsed'].median())
        data.append(df['elapsed'].std())

        stats[logic] = data
    
    return stats

def get_status_counts(dfs, target_status):
    """
    Gets the number of occurrences for a target status from a DataFrame.
  
    Parameters:
    dfs (DataFrame): A DataFrame containing a list statuses.
    target_status (str): A target status to count.

    Returns:
    dict: A dictionary that maps a logic to the number of times that it had a target status.
    """
    counts = {}

    for logic, df in dfs.items():
        status = df['status']
        count = 0
        for current_status in status:
            if current_status == target_status:
                count += 1
        
        counts[logic] = count
    
    return counts

def get_file_statuses(dfs, target_status = "timeout"):
    """
    Gets a set of files that match a target status from a DataFrame.
  
    Parameters:
    dfs (DataFrame): A DataFrame containing a list of statuses.
    target_status (str): A target status to match.
    
    Returns:
    set: A set of files that match a target status.
    """
    files = set()

    for _, df in dfs.items():
        for file, status in zip(df['filename'], df['status']):
            if status == target_status:
                files.add(file)
                
    return files

def get_best_times(dfs):
    """
    Gets the best execution time for each file from a DataFrame.
  
    Parameters:
    dfs (DataFrame): A DataFrame containing a list of execution times.
    
    Returns:
    dict: A dictionary that maps a file to the best execution time for that file.
    """
    best_times = {}

    for _, df in dfs.items():
        for file, time in zip(df['filename'], df['elapsed']):
            if file in best_times:
                best_times[file] = min(best_times[file], time)
            else:
                best_times[file] = time

    return best_times

def get_costs(dfs, best_times):
    """
    Gets the sum of (logic's time) - (best time) for each file from a DataFrame. 
  
    Parameters:
    dfs (DataFrame): A DataFrame containing a list of execution times.
    best_times (dict): A dictionary that maps a file to the file's best execution time.
    
    Returns:
    dict: A dictionary that maps a logic to the sum of
    (logic's time) - (best time) for each file.
    """
    costs = {}

    for logic, df in dfs.items():
        total_cost = 0

        for file, time in zip(df['filename'], df['elapsed']):
            total_cost += max(time - best_times[file], 0)

        costs[logic] = total_cost
    
    return costs

def get_k_best_entries(dict, k, reverse = False):
    """
    Gets the k best entries for a dictionary.
  
    Parameters:
    dict (dict): A dictionary to filter.
    k (int): The number of best entries to get.
    reverse (bool): False for ascending order.
                    True for descending order.
    
    Returns:
    tup: A tuple containing a list of the k best (key, value) pairs. 
    """
    dict = {k: v for k, v in sorted(dict.items(), key=lambda item: item[1], reverse = reverse)}
    logics = []
    data = []
    idx = 0

    for logic in dict:
        if idx == k:
            break
        idx += 1
        logics.append(logic)
    
    logics.sort()

    for logic in logics:
        data.append(dict[logic])
    
    return logics, data

def get_query(dfs, status, begin, end):
    """
    Queries a dictionary of DataFrames for a status with an execution time in the range of [start, end].
  
    Parameters:
    dfs (dict): A dictionary of DataFrames.
    status (str): The status to query.
    begin (int): The start of the range for the status's execution time.
    end (int): The end of the range for status's execution time.
    
    Returns:
    dict: A dictionary that maps a logic to a list of files that matches the search criteria.
    """
    file_lookup = {}

    for logic in dfs.keys():
        dfs[logic] = dfs[logic].query(f'status == "{status}"').query(f'{begin} <= elapsed <= {end}')
        
        l = len(dfs[logic].index)

        files = set()
        for file in dfs[logic]['filename']:
            files.add(file)
        file_lookup[logic] = files
    
    return file_lookup

def filter_rows_by_values(dfs, col, values):
    """
    Filters a dictionary of DataFrames by dropping rows that have specific column values.

    Parameters:
    dfs (dict): A dictionary of DataFrames.
    col (str): The column to filter.
    values (set): A set of column values to drop from the DataFrames.
    
    Returns:
    dict: A dictionary that maps a logic to the filtered DataFrame.
    """
    new_dfs = {}

    for logic, df in dfs.items():
        new_df = df[~df[col].isin(values)]
        new_dfs[logic] = new_df

    return new_dfs