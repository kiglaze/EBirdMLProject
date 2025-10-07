import pandas as pd
import folium
import plotly.express as px
import imageio
import datetime
import os
import numpy as np
import gc
import time
import plotly.io as pio
import json, urllib.request, shutil

TOPO_DIR = os.path.abspath("plotly_topojson")
FILES = [
    ("world_110m.json", "https://cdn.plot.ly/world_110m.json"),
]

def ensure_topojson():
    # Make dirs
    os.makedirs(TOPO_DIR, exist_ok=True)
    os.makedirs(os.path.join(TOPO_DIR, "un"), exist_ok=True)

    for fname, url in FILES:
        dst = os.path.join(TOPO_DIR, fname)

        # Download if missing
        if not os.path.isfile(dst):
            try:
                print(f"Downloading {fname} …")
                with urllib.request.urlopen(url) as r, open(dst, "wb") as f:
                    shutil.copyfileobj(r, f)
            except Exception as e:
                raise RuntimeError(f"Could not fetch {url}. Download it manually and save as {dst}. Error: {e}")

        # Validate JSON (not HTML or gz)
        with open(dst, "rb") as f:
            if f.read(2) == b"\x1f\x8b":
                raise RuntimeError(f"{dst} is gzipped; ungzip it first.")
        with open(dst, "r", encoding="utf-8") as f:
            json.load(f)

        # Place a copy under TOPO_DIR/un/
        un_dst = os.path.join(TOPO_DIR, "un", fname)
        if not os.path.isfile(un_dst):
            shutil.copyfile(dst, un_dst)

    # New, non-deprecated API:
    pio.defaults.topojson = TOPO_DIR

def main():
    ensure_topojson()

    # Load csv file into pandas dataframe: output_filtered_species_consolidated/osprey_ca_condor_output.csv
    df = pd.read_csv(
        'output_filtered_species_consolidated/osprey_ca_condor_output.csv',
        usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE', 'OBSERVER ID', 'OBSERVATION TYPE'],
        dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str, 'OBSERVER ID': str, 'OBSERVATION TYPE': str},
        parse_dates=['OBSERVATION DATE']
    )
    print(df.head())
    print(df.dtypes)
    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])]
    #generate_raw_maps(df, "California Condor", "map_output_ca_condor_raw")
    #generate_raw_maps(df, "Osprey", "map_output_osprey_raw_seasonal", True)
    generate_raw_maps(df, "Osprey", "map_output_osprey_raw_weekly", False)


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

def get_season_start_year(date, season):
    if season == 'Winter' and date.month in [1, 2]:
        return date.year - 1
    else:
        return date.year

def generate_raw_maps(df, species_name, output_directory_name, is_seasonal=True):
    df = df[df['COMMON NAME'] == species_name]
    #most_recent_date = df['OBSERVATION DATE'].max()

    #df_most_recent = df[df['OBSERVATION DATE'] == most_recent_date]

    print(list(df.columns))

    start_date = datetime.date(2023, 3, 1)
    end_date = datetime.date(2025, 8, 31)
    df = df[(df['OBSERVATION DATE'] >= pd.Timestamp(start_date)) & (df['OBSERVATION DATE'] <= pd.Timestamp(end_date))]

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

    # Sort and get unique years
    sorted_years = np.sort(df['YEAR'].unique())

    sorted_season_start_years = np.sort(df['SEASON_START_YEAR'].unique())

    sorted_weeks = np.sort(df['WEEK_IN_YEAR'].unique())
    max_sorted_week = np.max(sorted_weeks)

    frames = sorted(df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d').unique())
    images = []

    # Create directory "map_output" if it doesn't exist
    if not os.path.exists(output_directory_name):
        os.makedirs(output_directory_name)

    if is_seasonal:
        for season_year in sorted_season_start_years:
            for season_index in [1, 2, 3, 4]:
                dfi = df[(df['SEASON_START_YEAR'] == season_year) & (df['SEASON_INDEX'] == season_index)]
                # Sample 10% of dfi if more than 100 rows
                if len(dfi) > 100:
                    dfi = dfi.sample(frac=0.1, random_state=1)
                if dfi.empty:
                    continue
                print(f"Generating map for {season_index} {season_year} with {len(dfi)} points")
                generate_season_plot_map(dfi, species_name, output_directory_name, season_index, season_year)
            time.sleep(0.5)
    else:
        for year in sorted_years:
            for week_idx in range(1, max_sorted_week+1):
                dfi = df[(df['YEAR'] == year) & (df['WEEK_IN_YEAR'] == week_idx)]
                if dfi.empty:
                    continue
                print(f"Generating map for week {week_idx} {year} with {len(dfi)} points")
                generate_weekly_plot_map(dfi, species_name, output_directory_name, week_idx, year)
                time.sleep(0.5)
            time.sleep(0.5)

    # frame = frames[0]
    # dfi = df[df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d') == frame]
    # fig = px.scatter_geo(
    #     dfi, lat='LATITUDE', lon='LONGITUDE',
    #     color='COMMON NAME', scope='north america',
    #     projection='natural earth'
    # )
    # fig.update_geos(showcountries=True)
    # img_path = f"{output_directory_name}/frame_{frame}.png"
    # fig.write_image(img_path)


def generate_season_plot_map(dfi, species_name, output_directory_name, season_index: int, season_year):
    if not os.path.exists(output_directory_name):
        os.makedirs(output_directory_name)
    season_mapping = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    season = season_mapping[season_index]
    plot_title = f"{species_name} Observations - {season} {season_year}"
    img_path = f"{output_directory_name}/frame_{season_year}_{season_index}.png"
    generate_plot_map(dfi, img_path, plot_title, season_index, season_year)

def generate_weekly_plot_map(dfi, species_name, output_directory_name, week_index: int, year):
    if not os.path.exists(output_directory_name):
        os.makedirs(output_directory_name)
    plot_title = f"{species_name} Observations - Week {week_index} {year}"
    img_path = f"{output_directory_name}/frame_{year}_week_{week_index:02d}.png"
    generate_plot_map(dfi, img_path, plot_title, week_index, year)

def generate_plot_map(dfi, img_path: str, plot_title: str, time_increment_indicator: int, year):
    fig = px.scatter_geo(
        dfi, lat='LATITUDE', lon='LONGITUDE',
        color='COMMON NAME',
        projection='natural earth',
        title=f"{plot_title}"
    )

    fig.update_geos(
        showcountries=True,
        lataxis_range=[14.0, 72.0],  # latitude range for North America (continental US/Canada)
        lonaxis_range=[-170.0, -52.0]  # longitude range for North America (continental US/Canada)
    )

    try:
        fig.write_image(img_path)
    except Exception as e:
        print(f"Failed to write image for {time_increment_indicator} {year}: {e}")
    finally:
        del fig
        gc.collect()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
