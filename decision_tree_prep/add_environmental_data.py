import pandas as pd
from helpers.data_retrieval_helper import DataRetrievalHelper

def open_csv_file(filepath):
    df = pd.read_csv(filepath, dtype="string")
    print(f"Opened file: {filepath}")
    print(f"DataFrame shape: {df.shape}")
    print(df.head())
    return df

def get_max_obs_date(df):
    df['OBSERVATION DATE'] = pd.to_datetime(df['OBSERVATION DATE'], errors='coerce')
    max_date = df['OBSERVATION DATE'].max()
    return max_date

def get_min_obs_date(df):
    df['OBSERVATION DATE'] = pd.to_datetime(df['OBSERVATION DATE'], errors='coerce')
    min_date = df['OBSERVATION DATE'].min()
    return min_date

def get_min_latitude(df):
    df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
    min_lat = df['LATITUDE'].min()
    return min_lat
def get_max_latitude(df):
    df['LATITUDE'] = pd.to_numeric(df['LATITUDE'], errors='coerce')
    max_lat = df['LATITUDE'].max()
    return max_lat
def get_min_longitude(df):
    df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')
    min_lon = df['LONGITUDE'].min()
    return min_lon
def get_max_longitude(df):
    df['LONGITUDE'] = pd.to_numeric(df['LONGITUDE'], errors='coerce')
    max_lon = df['LONGITUDE'].max()
    return max_lon

def print_geo_range_date_range(species_df):
    print(get_max_latitude(species_df))
    print(get_min_latitude(species_df))
    print(get_max_longitude(species_df))
    print(get_min_longitude(species_df))

    print(get_max_obs_date(species_df))
    print(get_min_obs_date(species_df))


if __name__ == "__main__":
    # Create DataRetrievalHelper object from helpers/data_retrieval_helper.py
    data_retrieval_helper = DataRetrievalHelper()
    data_retrieval_helper.reload_all()

    osprey_df = data_retrieval_helper.osprey_df
    condor_df = data_retrieval_helper.condor_df
    alt_puffin_df = data_retrieval_helper.atl_puffin_df

    print_geo_range_date_range(osprey_df)

