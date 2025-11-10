from typing import Any

import pandas as pd
import datetime
import os
from datetime import datetime, timedelta, date

from helpers.data_filtration_helper import getOspreyGlacierBayRegion, getCondorGrandCanyonRegion, getAtlPuffinMACoastalRegion, filter_df_by_region
from models.RegionClass import RegionClass

def main():
    start_date = date(2015, 3, 1)
    end_date = date(2025, 8, 31)

    osprey_df = prepare_species_data_by_country_time_range('osprey_data.csv', start_date, end_date)

    # Glacier Bay, Alaska -- 58°N to 60°N, 137°W to 135°W
    glacier_bay_region = getOspreyGlacierBayRegion()
    get_weekly_presence_by_loc_data(osprey_df, glacier_bay_region, "osprey_glacier_bay_weekly.csv")

    # Grand Canyon -- Latitude: 35.7°N to 36.5°N; Longitude: −113.5°W to −111.8°W
    grand_canyon_region = getCondorGrandCanyonRegion()

    ca_condor_df = prepare_species_data_by_country_time_range('california_condor_data.csv', start_date, end_date)
    get_weekly_presence_by_loc_data(ca_condor_df, grand_canyon_region, "ca_condor_grand_canyon_weekly.csv")

    # 41.724641, -70.255132
    ma_coastal_region = getAtlPuffinMACoastalRegion()
    atlantic_puffin_df = prepare_species_data_by_country_time_range('atlantic_puffin_data.csv', start_date, end_date)
    get_weekly_presence_by_loc_data(atlantic_puffin_df, ma_coastal_region, "atlantic_puffin_ma_coastal_weekly.csv")


def prepare_species_data_by_country_time_range(input_species_filename: str, start_date, end_date) -> Any:
    df = pd.read_csv(
        f"output_by_species/with_added_cols/{input_species_filename}",
        usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE', 'OBSERVER ID',
                 'OBSERVATION TYPE', 'MONTH', 'YEAR', 'WEEK_IN_YEAR', 'SEASON', 'SEASON_INDEX', 'SEASON_START_YEAR',
                 'LATITUDE_RADIANS', 'LONGITUDE_RADIANS'],
        dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str,
               'OBSERVER ID': str, 'OBSERVATION TYPE': str, 'MONTH': int, 'YEAR': int, 'WEEK_IN_YEAR': int,
               'SEASON': str, 'SEASON_INDEX': int, 'SEASON_START_YEAR': int, 'LATITUDE_RADIANS': float,
               'LONGITUDE_RADIANS': float},
        parse_dates=['OBSERVATION DATE']
    )
    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])].copy()
    df = df[(df['OBSERVATION DATE'] >= pd.Timestamp(start_date)) & (df['OBSERVATION DATE'] <= pd.Timestamp(end_date))]
    return df


def get_weekly_presence_by_loc_data(df, glacier_bay_region: RegionClass, output_filename):
    first_obs_date = df['OBSERVATION DATE'].min()
    last_obs_date = df['OBSERVATION DATE'].max()

    week_year_combinations = get_week_year_combs_betw_dates(first_obs_date, last_obs_date)

    # Create a DataFrame from the week_year_combinations list
    df_week_year = pd.DataFrame(week_year_combinations, columns=['YEAR', 'WEEK_IN_YEAR'])
    df_week_year['OBSERVATION_COUNT'] = 0  # Initialize observation count to 0
    df_week_year = df_week_year.sort_values(['YEAR', 'WEEK_IN_YEAR']).reset_index(drop=True)
    print(df_week_year)

    df_gb = filter_df_by_region(df, glacier_bay_region)

    # Group by YEAR and WEEK_IN_YEAR
    grouped = df_gb.groupby(['YEAR', 'WEEK_IN_YEAR'])
    print(f"Number of groups (year, week): {len(grouped)}")
    for (year, week), group in grouped:
        print(f"YEAR: {year}, WEEK: {week}, Records: {len(group)}")
        # Find row in df_week_year with matchin YEAR and WEEK_IN_YEAR, then update OBSERVATION_COUNT with len(group)
        df_week_year.loc[
            (df_week_year['YEAR'] == year) & (df_week_year['WEEK_IN_YEAR'] == week), 'OBSERVATION_COUNT'] = len(group)

    # Add a column to df_week_year that is 1 if OBSERVATION_COUNT > 0 else 0
    df_week_year['OBSERVATION_PRESENT'] = 0
    df_week_year.loc[df_week_year['OBSERVATION_COUNT'] > 0, 'OBSERVATION_PRESENT'] = 1

    export_directory = "restricted_geo_loc_sighting_weekly"
    # Create directory if it doesn't exist
    if not os.path.exists(export_directory):
        os.makedirs(export_directory)
    # You can now proceed with further analysis or export
    df_week_year.to_csv(f"{export_directory}/{output_filename}", index=False)

# Get all week number and year value combinations between two dates.
def get_week_year_combs_betw_dates(first_obs_date, last_obs_date):
    dates = get_dates_between_timestamps(first_obs_date, last_obs_date)

    week_year_combinations = []
    for date in dates:
        week = date.isocalendar().week
        year = date.isocalendar().year
        week_year_combinations.append((year, week))

    week_year_combinations = sorted(set(week_year_combinations))
    return week_year_combinations


def get_dates_between_timestamps(first_obs_date, last_obs_date):
    # Get all dates between first and last observation date
    first_obs_datetime = first_obs_date.to_pydatetime()
    last_obs_datetime = last_obs_date.to_pydatetime()

    delta = last_obs_datetime - first_obs_datetime
    dates = [first_obs_datetime + timedelta(days=i) for i in range(delta.days + 1)]
    print(dates)
    return dates


if __name__ == "__main__":
    main()
