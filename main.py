import gzip
import shutil
import pandas as pd
import os

file_path = "/Volumes/LaCie/CSC522-2025/project/ebd_relAug-2025/ebd_relAug-2025.txt.gz"
preview_file_path = "ebd_preview.txt"
n_lines = 10000     # how many lines to copy
rows_per_chunk = 1000000  # how many rows to read at a time

def print_preview():
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f):
            print(line.rstrip())
            if i >= 9:  # print first 10 lines
                break
def write_preview():
    with gzip.open(file_path, "rt", encoding="utf-8", errors="ignore") as fin, \
        open(preview_file_path, "w", encoding="utf-8") as fout:
        for i, line in enumerate(fin):
            fout.write(line)
            if i + 1 >= n_lines:
                break

    print(f"Wrote first {n_lines} lines to {preview_file_path}")

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
    with open("unique_bird_species.txt", "w", encoding="utf-8") as f:
        for species in unique_bird_species:
            f.write(f"{species}\n")

def main():
    chunks_count_limit = 10
    # Possible additional species: "Atlantic Puffin", "Horned Puffin", "Tufted Puffin", "puffin sp."
    filter_species_list = ["California Condor", "Osprey"]
    filtered_df_concatenated = pd.DataFrame()
    reader = pd.read_csv(file_path,
                         sep="\t",
                         dtype="string",
                         chunksize=rows_per_chunk)
    batch_num = 0
    # Make directory named output if it doesn't exist

    if not os.path.exists("output"):
        os.makedirs("output")

    for i, chunk_df in enumerate(reader):
        unique_bird_species = chunk_df["COMMON NAME"].unique()
        # Write unique species to a file (appending)
        with open("unique_bird_species.txt", "a", encoding="utf-8") as f:
            for species in unique_bird_species:
                f.write(f"{species}\n")
        print(f"Processing chunk {i+1} (shape: {chunk_df.shape})")
        print(chunk_df.head())
        filtered_df = chunk_df[chunk_df['COMMON NAME'].isin(filter_species_list)]
        filtered_df_concatenated = pd.concat([filtered_df_concatenated, filtered_df], ignore_index=True)
        if (i + 1) % chunks_count_limit == 0:
            output_file = f"output/filtered_bird_data_{batch_num}.csv"
            filtered_df_concatenated.to_csv(output_file, index=False)
            filtered_df_concatenated = pd.DataFrame()
            batch_num += 1
            print(f"Wrote filtered data to {output_file} and reset DataFrame.")

            # Make all values in unique_bird_species.txt unique
            with open("unique_bird_species.txt", "r", encoding="utf-8") as f:
                unique_species = set(f.read().splitlines())
            with open("unique_bird_species.txt", "w", encoding="utf-8") as f:
                for species in unique_species:
                    f.write(f"{species}\n")
    # Write filtered_df_concatenated to a CSV file
    filtered_df_concatenated.to_csv("filtered_bird_data.csv", index=False)

if __name__ == "__main__":
    main()


