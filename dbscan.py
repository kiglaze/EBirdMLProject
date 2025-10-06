import pandas as pd
import folium
import plotly.express as px
import imageio
import datetime
import os
import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import DBSCAN
import numpy as np

def main():
    # Load csv file into pandas dataframe: output_filtered_species_consolidated/osprey_ca_condor_output.csv
    df = pd.read_csv(
        'output_filtered_species_consolidated/osprey_ca_condor_output.csv',
        usecols=['LATITUDE', 'LONGITUDE', 'COMMON NAME', 'COUNTRY', 'OBSERVATION DATE', 'BEHAVIOR CODE', 'OBSERVER ID', 'OBSERVATION TYPE'],
        dtype={'LATITUDE': float, 'LONGITUDE': float, 'COMMON NAME': str, 'COUNTRY': str, 'BEHAVIOR CODE': str, 'OBSERVER ID': str, 'OBSERVATION TYPE': str},
        parse_dates=['OBSERVATION DATE']
    )

    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])]
    #df = df[df['COMMON NAME'] == "California Condor"]
    df = df[df['COMMON NAME'] == "Osprey"]

    df = find_clusters_by_geo_loc_no_noise(df, '2025-08-31')

def find_clusters_by_geo_loc_no_noise(df, observation_date):
    df = find_clusters_by_geo_loc(df, observation_date)
    print(len(df))
    df_no_noise = df[df['CLUSTER'] != -1]
    print(len(df_no_noise))
    return df_no_noise

# observation_date in format '2025-08-31'
def find_clusters_by_geo_loc(df, observation_date):
    df['LATITUDE_RADIANS'] = np.radians(df['LATITUDE'])
    df['LONGITUDE_RADIANS'] = np.radians(df['LONGITUDE'])

    # limit observation date to 8/31/2025
    df = df[df['OBSERVATION DATE'] == pd.Timestamp(observation_date)]

    coords_radians = df[["LATITUDE_RADIANS", "LONGITUDE_RADIANS"]].to_numpy()

    # Define eps in km and convert to radians
    earth_radius_km = 6371.0088
    eps_km = 50.0  # 50 km neighborhood
    eps_rad = eps_km / earth_radius_km

    # Run DBSCAN with haversine distance, which works with latitude and longitude in radians
    db = DBSCAN(
        eps=eps_rad,
        min_samples=2,
        metric="haversine",
        algorithm="ball_tree"
    ).fit(coords_radians)

    df["CLUSTER"] = db.labels_
    return df

if __name__ == "__main__":
    main()
