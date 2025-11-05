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
from dbscan import find_clusters_by_geo_loc_no_noise
import plotly.graph_objects as go

MAP_OUTPUT_DIR = "map_output"
MAP_OUTPUT_DBSCAN_DIR = "map_output/dbscan"
MAP_OUTPUT_RAW_DIR = "map_output/raw"
WEEKLY_FOLDER = "weekly"
SEASONAL_FOLDER = "seasonal"

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

    input_filename_by_species = "atlantic_puffin_data.csv"
    #input_filename_by_species = "california_condor_data.csv"
    # Load csv file into pandas dataframe: output_filtered_species_consolidated/osprey_ca_condor_output.csv
    df = pd.read_csv(
        f"data_preprocessing/output_by_species/with_added_cols/{input_filename_by_species}",
        usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE', 'OBSERVER ID', 'OBSERVATION TYPE', 'MONTH', 'YEAR', 'WEEK_IN_YEAR', 'SEASON', 'SEASON_INDEX', 'SEASON_START_YEAR', 'LATITUDE_RADIANS', 'LONGITUDE_RADIANS'],
        dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str, 'OBSERVER ID': str, 'OBSERVATION TYPE': str, 'MONTH': int, 'YEAR': int, 'WEEK_IN_YEAR': int, 'SEASON': str, 'SEASON_INDEX': int, 'SEASON_START_YEAR': int, 'LATITUDE_RADIANS': float, 'LONGITUDE_RADIANS': float},
        parse_dates=['OBSERVATION DATE']
    )

    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])].copy()

    # Osprey
    # generate_raw_maps(df, "Osprey", f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}/map_output_osprey_raw_weekly", False, False, 1)
    # generate_raw_maps(df, "Osprey", f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}/map_output_osprey_dbscan_weekly", False, True, 1)
    # generate_raw_maps(df, "Osprey", f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}/map_output_osprey_raw_seasonal", True, False, 0.1)
    # generate_raw_maps(df, "Osprey", f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}/map_output_osprey_dbscan_seasonal", True, True, 0.1)

    # Atlantic Puffins
    #generate_raw_maps(df, "Atlantic Puffin", f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}/map_output_puffin_raw_weekly", False, False, 1)
    #generate_raw_maps(df, "Atlantic Puffin", f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}/map_output_puffin_dbscan_weekly", False, True, 1)
    #generate_raw_maps(df, "Atlantic Puffin", f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}/map_output_puffin_raw_seasonal", True, False, 0.4)
    #generate_raw_maps(df, "Atlantic Puffin", f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}/map_output_puffin_dbscan_seasonal", True, True, 0.4)

    # California Condors
    #generate_raw_maps(df, "California Condor", f"{MAP_OUTPUT_RAW_DIR}/{WEEKLY_FOLDER}/map_output_ca_condor_raw_weekly", False, False, 1)
    #generate_raw_maps(df, "California Condor", f"{MAP_OUTPUT_DBSCAN_DIR}/{WEEKLY_FOLDER}/map_output_ca_condor_dbscan_weekly", False, True, 1)
    #generate_raw_maps(df, "California Condor", f"{MAP_OUTPUT_RAW_DIR}/{SEASONAL_FOLDER}/map_output_ca_condor_raw_seasonal", True, False, 1)
    #generate_raw_maps(df, "California Condor", f"{MAP_OUTPUT_DBSCAN_DIR}/{SEASONAL_FOLDER}/map_output_ca_condor_dbscan_seasonal", True, True, 1)

def generate_raw_maps(df, species_name, output_directory_name, is_seasonal=True, running_dbscan=False, sample_frac=1.0):
    df = df[df['COMMON NAME'] == species_name]

    print(list(df.columns))

    start_date = datetime.date(2023, 3, 1)
    end_date = datetime.date(2025, 8, 31)
    df = df[(df['OBSERVATION DATE'] >= pd.Timestamp(start_date)) & (df['OBSERVATION DATE'] <= pd.Timestamp(end_date))]

    # Sort and get unique years
    sorted_years = np.sort(df['YEAR'].unique())

    sorted_season_start_years = np.sort(df['SEASON_START_YEAR'].unique())

    sorted_weeks = np.sort(df['WEEK_IN_YEAR'].unique())

    if len(sorted_weeks) == 0:
        max_sorted_week = 52
    else:
        max_sorted_week = max(52, np.max(sorted_weeks))

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
                if sample_frac < 1:
                    dfi = dfi.sample(frac=sample_frac, random_state=1)
                if dfi.empty:
                    continue
                if running_dbscan == True:
                    dfi = find_clusters_by_geo_loc_no_noise(dfi)
                print(f"Generating map for {season_index} {season_year} with {len(dfi)} points")
                generate_season_plot_map(dfi, species_name, output_directory_name, season_index, season_year)
            time.sleep(0.5)
    else:
        for year in sorted_years:
            for week_idx in range(1, max_sorted_week+1):
                dfi = df[(df['YEAR'] == year) & (df['WEEK_IN_YEAR'] == week_idx)]
                if sample_frac < 1:
                    dfi = dfi.sample(frac=sample_frac, random_state=1)
                if dfi.empty:
                    continue
                if running_dbscan == True:
                    dfi = find_clusters_by_geo_loc_no_noise(dfi)
                print(f"Generating map for week {week_idx} {year} with {len(dfi)} points")
                generate_weekly_plot_map(dfi, species_name, output_directory_name, week_idx, year)
                time.sleep(0.5)
            time.sleep(0.5)



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
    print(f"Image path: {img_path}")
    generate_plot_map(dfi, img_path, plot_title, week_index, year)

def generate_plot_map(dfi, img_path: str, plot_title: str, time_increment_indicator: int, year):
    if not dfi.empty:
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

        fig.update_layout(
            width=750,
            height=500,
            margin=dict(l=60, r=180, t=70, b=0)
        )
    else:
        # Create a real GEO figure even with no points
        fig = go.Figure(
            data=[go.Scattergeo(lon=[], lat=[], mode="markers", showlegend=False, hoverinfo="skip")]
        )
        fig.update_layout(
            title=f"{plot_title} (No data available)",
            geo=dict(
                projection=dict(type="natural earth"),
                showcountries=True,
                lonaxis=dict(range=[-170.0, -52.0]),
                lataxis=dict(range=[14.0, 72.0]),
            ),
        )
        fig.update_layout(
            width=750,
            height=500,
            margin=dict(l=60, r=180, t=70, b=0)
        )
        # Optional: a centered “No data” label on the map
        fig.add_annotation(
            text="No data for this period",
            x=0.5, y=0.5, xref="paper", yref="paper",
            showarrow=False
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
    # ensure_topojson()
    # input_filename_by_species = "california_condor_data.csv"
    # df = pd.read_csv(
    #     f"data_preprocessing/output_by_species/with_added_cols/{input_filename_by_species}",
    #     usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE', 'OBSERVER ID', 'OBSERVATION TYPE', 'MONTH', 'YEAR', 'WEEK_IN_YEAR', 'SEASON', 'SEASON_INDEX', 'SEASON_START_YEAR', 'LATITUDE_RADIANS', 'LONGITUDE_RADIANS'],
    #     dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str, 'OBSERVER ID': str, 'OBSERVATION TYPE': str, 'MONTH': int, 'YEAR': int, 'WEEK_IN_YEAR': int, 'SEASON': str, 'SEASON_INDEX': int, 'SEASON_START_YEAR': int, 'LATITUDE_RADIANS': float, 'LONGITUDE_RADIANS': float},
    #     parse_dates=['OBSERVATION DATE']
    # )
    # # Filter df so that no rows are selected
    # # Select only first row of dataframe df
    # df = df[0:1]
    #
    #
    # #df = df[df['COMMON NAME'] != "California Condor"]
    # print(f"Number of rows after filtering: {len(df)}")
    # generate_plot_map(df, "example1.png", "Testing No Data Points", 11, 2024)
