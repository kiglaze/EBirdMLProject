import gzip
import shutil
import pandas as pd
import os
import glob

#file_path = "/Volumes/LaCie/CSC522-2025/project/ebd_relAug-2025/redownloads0/ebd_relAug-2025.txt.gz"
file_path = "/Volumes/Extreme SSD/CSC522-25/project/ebd_relAug-2025/ebd_relAug-2025.txt.gz"
preview_file_path = "ebd_preview.txt"
n_lines = 10000     # how many lines to copy
rows_per_chunk = 1000000  # how many rows to read at a time

def process_preview():
    # Read only the one column; pandas will decompress on the fly.
    preview_df = pd.read_csv(
        preview_file_path,
        sep="\t",
        dtype="string",
    )
    print(preview_df)

    filter_species_list = ["California Condor", "Osprey"]
    filter_country_list = ["United States", "Canada", "Mexico", "Cuba"]
    filtered_df = preview_df[
        preview_df['COMMON NAME'].isin(filter_species_list) &
        preview_df['COUNTRY'].isin(filter_country_list)
        ]
    print("\nFiltered DataFrame:")
    print(filtered_df)

    unique_bird_species = preview_df["COMMON NAME"].unique()
    with open("../unique_bird_species.txt", "w", encoding="utf-8") as f:
        for species in unique_bird_species:
            f.write(f"{species}\n")

def filter_original_data_by_species_loc(output_dir_name, filter_species_list):
    chunks_count_limit = 10
    # Possible additional species: "Atlantic Puffin", "Horned Puffin", "Tufted Puffin", "puffin sp."
    #filter_species_list = ["California Condor", "Osprey"]
    filtered_df_concatenated = pd.DataFrame()
    reader = pd.read_csv(file_path,
                         sep="\t",
                         dtype="string",
                         chunksize=rows_per_chunk)
    batch_num = 0
    # Make directory named output if it doesn't exist

    if not os.path.exists("output"):
        os.makedirs("output")

    if not os.path.exists(output_dir_name):
        os.makedirs(output_dir_name)

    for i, chunk_df in enumerate(reader):
        unique_bird_species = chunk_df["COMMON NAME"].unique()
        # Write unique species to a file (appending)
        with open("../unique_bird_species.txt", "a", encoding="utf-8") as f:
            for species in unique_bird_species:
                f.write(f"{species}\n")
        print(f"Processing chunk {i+1} (shape: {chunk_df.shape})")
        print(chunk_df.head())
        filtered_df = chunk_df[chunk_df['COMMON NAME'].isin(filter_species_list)]
        filtered_df_concatenated = pd.concat([filtered_df_concatenated, filtered_df], ignore_index=True)
        if (i + 1) % chunks_count_limit == 0:
            output_file = f"{output_dir_name}/filtered_bird_data_{batch_num}.csv"
            filtered_df_concatenated.to_csv(output_file, index=False)
            filtered_df_concatenated = pd.DataFrame()
            batch_num += 1
            print(f"Wrote filtered data to {output_file} and reset DataFrame.")

            # Make all values in unique_bird_species.txt unique
            with open("../unique_bird_species.txt", "r", encoding="utf-8") as f:
                unique_species = set(f.read().splitlines())
            with open("../unique_bird_species.txt", "w", encoding="utf-8") as f:
                for species in unique_species:
                    f.write(f"{species}\n")
    # Write filtered_df_concatenated to a CSV file
    filtered_df_concatenated.to_csv("filtered_bird_data.csv", index=False)

def main():
    #if not os.path.exists("output_filtered_species_consolidated"):
    #    os.makedirs("output_filtered_species_consolidated")
    #df = pd.read_csv('output_filtered_species_consolidated/osprey_ca_condor_output.csv', dtype="string")
    #print(df['COMMON NAME'].value_counts())

    #filter_original_data_by_species_loc("output_osprey_ca_condor", ["California Condor", "Osprey"])

    filter_original_data_by_species_loc("output_puffins", ["Atlantic Puffin", "Horned Puffin", "Tufted Puffin", "puffin sp."])

if __name__ == "__main__":
    main()


