import pandas as pd
import matplotlib.pyplot as plt
import os

# Constants
N_INTERSECTIONS = '# Intersections'
SETUP_TIME = 'Setup time'
SIM_TIME = 'Simulation time'
TOT_TIME = 'Total execution time'
CPU_USAGE = 'CPU usage'
MEM_USAGE = 'Memory usage'

def read_csv_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filepath = os.path.join(directory, filename)
            df = pd.read_csv(filepath)
            data.append(df)
    return pd.concat(data, ignore_index=True)

def plot_time_measures(df, output_file):
    df_sorted = df.sort_values(by=N_INTERSECTIONS)
    intersections = df_sorted[N_INTERSECTIONS].unique()
    setup_time = df_sorted.groupby(N_INTERSECTIONS)[SETUP_TIME].mean()
    simulation_time = df_sorted.groupby(N_INTERSECTIONS)[SIM_TIME].mean()
    
    fig, ax = plt.subplots()
    
    bar_width = 0.20
    bar_positions = range(len(intersections))
    
    ax.bar(bar_positions, setup_time, bar_width, label='Setup Time')
    ax.bar(bar_positions, simulation_time, bar_width, bottom=setup_time, label='Simulation Time')
    
    ax.set_xlabel(N_INTERSECTIONS)
    ax.set_ylabel('Time (seconds)')
    ax.set_title('Setup and Simulation Time by Number of Intersections')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(intersections)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def plot_resource_usage(df, output_file):
    df_sorted = df.sort_values(by=N_INTERSECTIONS)
    intersections = df_sorted[N_INTERSECTIONS].unique()
    cpu_usage = df_sorted.groupby(N_INTERSECTIONS)[CPU_USAGE].mean()
    memory_usage = df_sorted.groupby(N_INTERSECTIONS)[MEM_USAGE].mean()
    
    fig, ax = plt.subplots()
    
    bar_width = 0.35
    bar_positions = range(len(intersections))
    
    ax.bar([p - bar_width/2 for p in bar_positions], cpu_usage, bar_width, label='CPU Usage (%)')
    ax.bar([p + bar_width/2 for p in bar_positions], memory_usage, bar_width, label='Memory Usage (%)')
    
    ax.set_xlabel(N_INTERSECTIONS)
    ax.set_ylabel('Resource Usage (%)')
    ax.set_title('CPU and Memory Usage by Number of Intersections')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(intersections)
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()


def main():
    directory = "data"
    df = read_csv_files(directory)
    
    # Generate plots
    plot_time_measures(df, os.path.join(directory, "combined_times.png"))
    plot_resource_usage(df, os.path.join(directory, "combined_resources.png"))


if __name__ == "__main__":
    main()
