import pandas as pd
import os
import numpy as np

def get_season(date):
    month = date.month
    if month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    elif month in [9, 10, 11]:
        return 'Fall'
    else:
        return 'Winter'

def add_date_columns_to_species_files(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith("_data.csv"):
            filepath = os.path.join(input_directory, filename)
            df = pd.read_csv(filepath, parse_dates=['OBSERVATION DATE'])

            df['MONTH'] = df['OBSERVATION DATE'].dt.month
            df['YEAR'] = df['OBSERVATION DATE'].dt.year
            # Add a column named 'WEEK_IN_YEAR' that extracts the week in year from 'OBSERVATION DATE'
            df['WEEK_IN_YEAR'] = df['OBSERVATION DATE'].dt.isocalendar().week
            # Add a column named 'SEASON' that converts 'OBSERVATION DATE' to season (Spring, Summer, Fall, Winter)
            df['SEASON'] = df['OBSERVATION DATE'].apply(get_season)
            # Add column for 'SEASON_INDEX' that is 1 for Spring, 2 for Summer, 3 for Fall, 4 for Winter
            season_mapping = {'Spring': 1, 'Summer': 2, 'Fall': 3, 'Winter': 4}
            df['SEASON_INDEX'] = df['SEASON'].map(season_mapping)
            # Add a column named 'SEASON_START_YEAR' that sets the year when the season starts. Uses function get_season_start_year()
            df['SEASON_START_YEAR'] = df['YEAR']

            df['SEASON_START_YEAR'] = np.where(
                (df['SEASON'] == 'Winter') & (df['MONTH'].isin([1, 2])),
                df['YEAR'] - 1,
                df['YEAR']
            )

            df['LATITUDE_RADIANS'] = np.radians(df['LATITUDE'])
            df['LONGITUDE_RADIANS'] = np.radians(df['LONGITUDE'])

            output_filepath = os.path.join(output_directory, filename)
            df.to_csv(output_filepath, index=False)
            print(f"Processed and saved: {output_filepath}")



def main():
    add_date_columns_to_species_files("output_by_species/originals", "output_by_species/with_added_cols")

if __name__ == "__main__":
    main()
