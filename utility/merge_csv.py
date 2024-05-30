import os
import pandas as pd

root_folder = 'data'
subfolders = ['no_scaling', 'multithreading', 'multithreading_nogil', 'multiprocessing', 'ray']

# initialize an empty DataFrame to hold all data
merged_df = pd.DataFrame()

# loop through each subfolder
for subfolder in subfolders:
    # get the list of CSV files in the current subfolder
    folder_path = os.path.join(root_folder, subfolder)
    csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # read each CSV file and append it to the merged DataFrame
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)
        df = pd.read_csv(file_path)
        
        # add a column for the technique
        df['Technique'] = subfolder.replace('_', ' ')
        
        # append the data to the merged DataFrame
        merged_df = pd.concat([merged_df, df], ignore_index=True)

# reorder columns to have 'Technique' as the first column
cols = ['Technique'] + [col for col in merged_df.columns if col != 'Technique']
merged_df = merged_df[cols]

# save the merged DataFrame to a new CSV file
merged_file_path = os.path.join(root_folder, 'merged_benchmark_stats.csv')
merged_df.to_csv(merged_file_path, index=False)

print(f"Merged CSV file created at {merged_file_path}")
