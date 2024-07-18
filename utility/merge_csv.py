import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import ( 
    DATA_FOLDER,
    DATA_SUBFOLDERS_LOW,
    DATA_SUBFOLDERS_HIGH,
    MERGED_STATS_FILE_LOW,
    MERGED_STATS_FILE_HIGH,
    IMAGE_EXECUTION_TIME_LOW,
    IMAGE_EXECUTION_TIME_HIGH,
    IMAGE_CPU_USAGE_LOW,
    IMAGE_CPU_USAGE_HIGH,
    IMAGE_MEM_USAGE_LOW,
    IMAGE_MEM_USAGE_HIGH,
    ORDER_LOW,
    ORDER_HIGH
)

def load_and_merge_data(root_folder, subfolders):
    """
    Load and merge CSV data from multiple subfolders.
    
    Parameters:
    - root_folder (str): The root directory containing subfolders.
    - subfolders (list of str): List of subfolder names.

    Returns:
    - merged_df (DataFrame): The merged DataFrame containing all data.
    """
    merged_df = pd.DataFrame()

    for subfolder in subfolders:
        folder_path = os.path.join(root_folder, subfolder)
        csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
        
        for csv_file in csv_files:
            file_path = os.path.join(folder_path, csv_file)
            df = pd.read_csv(file_path)
            df["Technique"] = subfolder.replace("_", " ")
            merged_df = pd.concat([merged_df, df], ignore_index=True)
    
    return merged_df

def save_merged_data(merged_df, output_file):
    """
    Save the merged DataFrame to a CSV file.

    Parameters:
    - merged_df (DataFrame): The merged DataFrame.
    - output_file (str): The path to the output CSV file.
    """
    cols = ["Technique"] + [col for col in merged_df.columns if col != "Technique"]
    merged_df = merged_df[cols]
    merged_df.to_csv(output_file, index=False)

def plot_data(data, desired_order, output_image):
    """
    Plot the data as a bar chart.

    Parameters:
    - data (DataFrame): The data to plot.
    - desired_order (list of str): The order of techniques for plotting.
    - output_image (str): The path to the output image file.
    """
    data_filtered = data[["Technique", "# Intersections", "Total execution time"]]
    pivot_table = data_filtered.pivot(index="# Intersections", columns="Technique", values="Total execution time")
    pivot_table = pivot_table[desired_order]

    x_labels = pivot_table.index.tolist()
    num_techniques = len(pivot_table.columns)
    x = np.arange(len(x_labels))
    bar_width = 0.1

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, technique in enumerate(pivot_table.columns):
        ax.bar(x + i * bar_width, pivot_table[technique], width=bar_width, label=technique)

    ax.set_xticks(x + bar_width * (num_techniques - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel("# Intersections")
    ax.set_ylabel("Total execution time (seconds)")
    ax.legend()
    ax.set_title("Total Execution Time by Scaling Technique")

    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()

def plot_cpu_usage(data, desired_order, output_image):
    """
    Plot the CPU usage as a bar chart.

    Parameters:
    - data (DataFrame): The data to plot.
    - desired_order (list of str): The order of techniques for plotting.
    - output_image (str): The path to the output image file.
    """
    data_filtered = data[["Technique", "# Intersections", "CPU usage"]]
    pivot_table = data_filtered.pivot(index="# Intersections", columns="Technique", values="CPU usage")
    pivot_table = pivot_table[desired_order]

    x_labels = pivot_table.index.tolist()
    num_techniques = len(pivot_table.columns)
    x = np.arange(len(x_labels))
    bar_width = 0.1

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, technique in enumerate(pivot_table.columns):
        ax.bar(x + i * bar_width, pivot_table[technique], width=bar_width, label=technique)

    ax.set_xticks(x + bar_width * (num_techniques - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel("# Intersections")
    ax.set_ylabel("CPU usage (%)")
    ax.legend()
    ax.set_title("CPU Usage by Scaling Technique")

    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()
    
def plot_memory_usage(data, desired_order, output_image):
    """
    Plot the memory usage as a bar chart.

    Parameters:
    - data (DataFrame): The data to plot.
    - desired_order (list of str): The order of techniques for plotting.
    - output_image (str): The path to the output image file.
    """
    data_filtered = data[["Technique", "# Intersections", "Memory usage"]]
    pivot_table = data_filtered.pivot(index="# Intersections", columns="Technique", values="Memory usage")
    pivot_table = pivot_table[desired_order]

    x_labels = pivot_table.index.tolist()
    num_techniques = len(pivot_table.columns)
    x = np.arange(len(x_labels))
    bar_width = 0.1

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, technique in enumerate(pivot_table.columns):
        ax.bar(x + i * bar_width, pivot_table[technique], width=bar_width, label=technique)

    ax.set_xticks(x + bar_width * (num_techniques - 1) / 2)
    ax.set_xticklabels(x_labels)
    ax.set_xlabel("# Intersections")
    ax.set_ylabel("Memory usage (%)")
    ax.legend()
    ax.set_title("Memory Usage by Scaling Technique")

    plt.tight_layout()
    plt.savefig(output_image)
    plt.close()

def main():
    if len(sys.argv) != 2:
        raise ValueError("Usage: python merge_csv.py <mode>")
    
    mode = sys.argv[1]
    root_folder = DATA_FOLDER
    
    if mode == "low":
        subfolders = DATA_SUBFOLDERS_LOW
        output_file = os.path.join(root_folder, MERGED_STATS_FILE_LOW)
        output_image_execution_time = os.path.join(root_folder, IMAGE_EXECUTION_TIME_LOW)
        output_image_cpu_usage = os.path.join(root_folder, IMAGE_CPU_USAGE_LOW)
        output_image_memory_usage = os.path.join(root_folder, IMAGE_MEM_USAGE_LOW)
        desired_order = ORDER_LOW
    
    elif mode == "high":
        subfolders = DATA_SUBFOLDERS_HIGH
        output_file = os.path.join(root_folder, MERGED_STATS_FILE_HIGH)
        output_image_execution_time = os.path.join(root_folder, IMAGE_EXECUTION_TIME_HIGH)
        output_image_cpu_usage = os.path.join(root_folder, IMAGE_CPU_USAGE_HIGH)
        output_image_memory_usage = os.path.join(root_folder, IMAGE_MEM_USAGE_HIGH)
        desired_order = ORDER_HIGH
    
    else:
        raise ValueError("Invalid mode. Use 'low' or 'high'.")

    merged_df = load_and_merge_data(root_folder, subfolders)
    save_merged_data(merged_df, output_file)
    
    data = pd.read_csv(output_file)
    plot_data(data, desired_order, output_image_execution_time)
    plot_cpu_usage(data, desired_order, output_image_cpu_usage)
    plot_memory_usage(data, desired_order, output_image_memory_usage)


if __name__ == "__main__":
    main()
