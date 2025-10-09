import pandas as pd
import os
import glob
# Combines multiple CSV files from a directory into a single CSV file

def combine_filtered_bird_data(input_directory, output_directory, output_csv_filename):
    csv_files = glob.glob(f"../{input_directory}/*.csv")
    df_list = [pd.read_csv(f, dtype="string") for f in csv_files]
    combined_df = pd.concat(df_list, ignore_index=True)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    combined_df.to_csv(f"../{output_directory}/{output_csv_filename}", index=False)

def main():
    # combine_filtered_bird_data("output_osprey_ca_condor", "output_filtered_species_consolidated", "osprey_ca_condor_output.csv")
    combine_filtered_bird_data("output_puffins", "output_filtered_species_consolidated", "puffins_output.csv")

if __name__ == "__main__":
    main()