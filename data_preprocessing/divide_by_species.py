# input files:
# output_filtered_species_consolidated/osprey_ca_condor_output.csv

import pandas as pd
import os

def main():
    # input_file_path = '../output_filtered_species_consolidated/osprey_ca_condor_output.csv'
    input_file_path = '../output_filtered_species_consolidated/puffins_output.csv'

    # species_list_osprey_condor = ["California Condor", "Osprey"]
    # species_list_puffins = ["Atlantic Puffin", "Horned Puffin", "Tufted Puffin", "puffin sp."]
    df = pd.read_csv(
        input_file_path,
        usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE',
                 'OBSERVER ID', 'OBSERVATION TYPE'],
        dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str,
               'OBSERVER ID': str, 'OBSERVATION TYPE': str},
        parse_dates=['OBSERVATION DATE']
    )
    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])].copy()

    unique_species = df['COMMON NAME'].unique()
    for species in unique_species:
        print(species)
        output_filepath = f"output_by_species/originals/{species.replace(' ', '_').lower()}_data.csv"
        os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
        df[df['COMMON NAME'] == species].to_csv(output_filepath, index=False)


if __name__ == "__main__":
    main()