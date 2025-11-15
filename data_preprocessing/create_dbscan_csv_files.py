from dbscan import find_clusters_by_geo_loc_no_noise
import pandas as pd
import glob
import numpy as np
import time
import datetime
from helpers.time_helper import get_week_year_combs_betw_dates

if __name__ == "__main__":
    input_csv_dir = 'output_by_species/with_added_cols'
    output_csv_dir = 'output_by_species/with_added_cols_dbscan'

    # iterate through all csv files in input_csv_dir
    for fname in glob.glob(input_csv_dir + '/*.csv'):
        input_csv_file = fname
        print(input_csv_file)
        #if input_csv_file in [input_csv_dir + '/osprey_data.csv']:
        if input_csv_file in [input_csv_dir + '/california_condor_data.csv', input_csv_dir + '/atlantic_puffin_data.csv']:
            df = pd.read_csv(input_csv_file)
            # Filter rows in db by OBSERVATION DATE in year 2000 or later
            df = df[pd.to_datetime(df['OBSERVATION DATE']) >= pd.Timestamp('2000-01-01')].copy()
            df['OBSERVATION DATE'] = df['OBSERVATION DATE'].astype(str)

            unique_dates = sorted(df['OBSERVATION DATE'].unique())
            week_year_combinations = []
            for date_str in unique_dates:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                week = date.isocalendar().week
                year = date.isocalendar().year
                week_year_combinations.append((year, week))

            week_year_combinations = sorted(set(week_year_combinations))

            df_with_clusters = pd.DataFrame()
            for year, week in week_year_combinations:
                dfi = df[(df['YEAR'] == year) & (df['WEEK_IN_YEAR'] == week)]
                print(f"YEAR: {year}, WEEK: {week}, Records: {len(dfi)}")

                if dfi.empty:
                    continue
                dfi = find_clusters_by_geo_loc_no_noise(dfi)
                df_with_clusters = pd.concat([df_with_clusters, dfi], ignore_index=True)
                time.sleep(0.5)

            output_csv_file = output_csv_dir + '/' + input_csv_file.split('/')[-1]
            df_with_clusters.to_csv(output_csv_file, index=False)

            print(f"DBSCAN clustering completed. Results saved to {output_csv_file}.")