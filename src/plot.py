"""
plot.py:

Contains methods for plotting Faial benchmarks.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import stats

PATH = 'results/'
COLORS = ["#808080", "#556b2f",
          "#8b4513", "#483d8b",
          "#008000", "#3cb371",
          "#b8860b", "#bdb76b",
          "#008b8b", "#4682b4",
          "#000080", "#9acd32",
          "#800080", "#b03060",
          "#ff0000", "#ff8c00",
          "#ffd700", "#7fff00",
          "#8a2be2", "#00ff7f",
          "#dc143c", "#00ffff",
          "#0000ff", "#da70d6",
          "#ff00ff", "#1e90ff",
          "#fa8072", "#add8e6",
          "#ff1493", "#7b68ee",
          "#ffb6c1"]

def load_files_as_df(path=PATH):
    """
    Loads a list of CSV files into a dictionary that maps a logic to a DataFrame.
  
    Parameters:
    path (str): A relative path to a folder containing a list of CSV files.
  
    Returns:
    dict: A dictionary that maps a logic to a DataFrame.
    """
    filenames = os.listdir(path)
    filenames = [file for file in filenames if '.csv' in file]
    dfs = {}

    for _, filename in enumerate(filenames):
        df = pd.read_csv(PATH + filename)
        logic = df['logic'][0]
        dfs[logic] = df
    
    return dfs

def plot_file_id_and_elapsed_time(dfs, k = 5, filter = None):
    """
    Plots a list of (file, elapsed time) pairs from a DataFrame.
  
    Parameters:
    dfs (dict): A dictionary of DataFrames.
    k (int): The number of entries to plot. When k is less than the total
             number of entries, only the k best entries are plotted.
    filter (List[str]): A list of file statuses to exclude from the plot.
  
    Returns:
    (void)
    """
    logics = stats.get_k_best_entries(stats.get_mean_median_std(dfs), k)[0]

    if filter is not None:
        for status in filter:
            dfs = stats.filter_rows_by_values(dfs, "filename", stats.get_file_statuses(dfs, status))

    idx = 0

    for logic, df in dfs.items():
        if logic in logics:
            plt.scatter(df['file no.'], df['elapsed'], label=logic, color=COLORS[idx])
            idx += 1

    plt.xlabel("File ID")
    plt.ylabel("Time to run (ms)")

    plt.legend(title='Logic', loc='center left', bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()

def plot_mean_median_std(dfs, k = 5, filter = None):
    """
    Plots the mean, median, and standard deviation for a logic's
    execution time from a DataFrame.
  
    Parameters:
    dfs (dict): A dictionary of DataFrames.
    k (int): The number of entries to plot. When k is less than the total
             number of entries, only the k best entries are plotted.
    filter (List[str]): A list of file statuses to exclude from the plot.
  
    Returns:
    (void)
    """
    if filter is not None:
        for status in filter:
            dfs = stats.filter_rows_by_values(dfs, "filename", stats.get_file_statuses(dfs, status))

    logics, nums = stats.get_k_best_entries(stats.get_mean_median_std(dfs), k)

    means = []
    medians = []
    stds = []

    for i in range(len(nums)):
        data = nums[i]
        means.append(data[0])
        medians.append(data[1])
        stds.append(data[2])

    r = np.arange(k)
    width = 0.20
    
    plt.bar(r, means, color = 'r', width = width, edgecolor = 'black', label='Mean')
    plt.bar(r + width, medians, color = 'b', width = width, edgecolor = 'black', label='Median')
    plt.bar(r + width * 2, stds, color = 'g', width = width, edgecolor = 'black', label='Standard Deviation')

    plt.xticks(r + width, logics)
    
    plt.xlabel("Logic")
    plt.ylabel("Time to run (ms)")
    
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_status(dfs, k = 5, status = "failed", reverse = False):
    """
    Plots the number of times that a status occured for a logic from a DataFrame. 
  
    Parameters:
    dfs (dict): A dictionary of DataFrames.
    k (int): The number of entries to plot. When k is less than the total
             number of entries, only the k best entries are plotted.
    reverse (bool): False for ascending order.
                    True for descending order.
            
    Returns:
    (void)
    """
    
    dfs = load_files_as_df()
    logics, timeouts = stats.get_k_best_entries(stats.get_status_counts(dfs, status), k, reverse)

    r = np.arange(k)
    width = 0.40

    plt.bar(r, timeouts, color = 'r', width = width, edgecolor = 'black')
    plt.locator_params(axis="both", integer=True, tight=True)

    plt.xticks(r, logics)
    
    plt.xlabel("Logic")
    plt.ylabel(f"Number of statuses: {status}")
    
    plt.show()

def plot_consistency(dfs, k = 5, filter = None):
    """
    Plot the sum of (logic's time) - (best time) for each file from a DataFrame. 
  
    Parameters:
    dfs (dict): A dictionary of DataFrames.
    k (int): The number of entries to plot. When k is less than the total
             number of entries, only the k best entries are plotted.
    filter (List[str]): A list of file statuses to exclude from the plot.
            
    Returns:
    (void)
    """
    if filter is not None:
        for status in filter:
            dfs = stats.filter_rows_by_values(dfs, "filename", stats.get_file_statuses(dfs, status))

    best_times = stats.get_best_times(dfs)
    logics, costs = stats.get_k_best_entries(stats.get_costs(dfs, best_times), k)
    
    r = np.arange(k)
    width = 0.40
    
    plt.bar(r, costs, color = 'r', width = width, edgecolor = 'black')

    plt.xticks(r, logics)
    
    plt.xlabel("Logic")
    plt.ylabel("Sum of Time Minus Best time (ms)")
    
    plt.show()

if __name__ == '__main__':
    dfs = load_files_as_df()
    plot_consistency(dfs)