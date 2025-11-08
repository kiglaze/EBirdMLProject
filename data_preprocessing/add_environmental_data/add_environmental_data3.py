from meteostat import Stations, Point, Daily
from datetime import datetime
import pandas as pd
import os

from helpers.data_filtration_helper import getOspreyGlacierBayRegion, getCondorGrandCanyonRegion, getAtlPuffinMACoastalRegion
from models.RegionClass import RegionClass


def get_region_weather_data_df(region: RegionClass, start_date, end_date):
    stations_osprey_glacier_bay_region = Stations().bounds(region.get_top_left(), region.get_bottom_right())

    # Stations.bounds expects two corner coordinates: top-left and bottom-right.
    # Top-left should be (max_lat, min_lon), bottom-right should be (min_lat, max_lon). This defines the rectangular bbox correctly for the API.

    # Fetch all matching stations as a DataFrame
    stations_osprey_glacier_bay_region_df = stations_osprey_glacier_bay_region.fetch()
    print(stations_osprey_glacier_bay_region_df.head())
    print(f"Total stations found: {len(stations_osprey_glacier_bay_region_df)}")

    stations_dfs = []
    for index, row in stations_osprey_glacier_bay_region_df.iterrows():
        station_id = index
        daily_df = Daily(station_id, start_date, end_date).fetch()
        # print(daily_df.head())
        daily_df['station_id'] = station_id
        stations_dfs.append(daily_df)

    combined_station_dfs = pd.concat(stations_dfs)
    cols_to_average = ['tavg', 'prcp', 'snow', 'wspd', 'pres']
    regional_avg = combined_station_dfs[cols_to_average].groupby(combined_station_dfs[cols_to_average].index).mean(
        numeric_only=True)
    regional_min = combined_station_dfs[['tmin']].groupby(combined_station_dfs[['tmin']].index).min()
    regional_max = combined_station_dfs[['tmax']].groupby(combined_station_dfs[['tmax']].index).max()
    regional_df = pd.concat([regional_avg, regional_min, regional_max], axis=1)

    regional_df['week_number'] = pd.to_datetime(regional_df.index).isocalendar().week
    regional_df['year'] = pd.to_datetime(regional_df.index).isocalendar().year

    print(regional_avg.head())
    return regional_df


if __name__ == '__main__':
    # Define bounding box (min_lat, max_lat, min_lon, max_lon)

    osprey_glacier_bay_region = getOspreyGlacierBayRegion()
    condor_grand_canyon_region = getCondorGrandCanyonRegion()
    atl_puffin_ma_coastal_region = getAtlPuffinMACoastalRegion()

    start_date = datetime(2015, 3, 1)
    end_date = datetime(2025, 8, 31)

    # Make directory ../weather_data/ if it doesn't exist
    if not os.path.exists("../weather_data_daily/"):
        os.makedirs("../weather_data_daily/")

    osprey_glacier_bay_region_weather_df = get_region_weather_data_df(osprey_glacier_bay_region, start_date, end_date)
    print(osprey_glacier_bay_region_weather_df.head())
    osprey_glacier_bay_region_weather_df.to_csv("../weather_data_daily/osprey_glacier_bay_region_weather_data.csv")

    condor_grand_canyon_region_weather_df = get_region_weather_data_df(condor_grand_canyon_region, start_date, end_date)
    print(condor_grand_canyon_region_weather_df.head())
    condor_grand_canyon_region_weather_df.to_csv("../weather_data_daily/condor_grand_canyon_region_weather_data.csv")

    atl_puffin_ma_coastal_region_weather_df = get_region_weather_data_df(atl_puffin_ma_coastal_region, start_date, end_date)
    print(atl_puffin_ma_coastal_region_weather_df.head())
    atl_puffin_ma_coastal_region_weather_df.to_csv("../weather_data_daily/atl_puffin_ma_coastal_region_weather_data.csv")
