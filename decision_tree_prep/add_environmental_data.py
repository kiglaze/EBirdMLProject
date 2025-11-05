import pandas as pd
from helpers.data_retrieval_helper import DataRetrievalHelper
from helpers.data_summarization_helper import DataSummarizationHelper
from helpers.data_filtration_helper import filter_df_by_region, getOspreyGlacierBayRegion, getCondorGrandCanyonRegion, getAtlPuffinMACoastalRegion

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

    osprey_df = data_retrieval_helper.osprey_df
    #condor_df = data_retrieval_helper.condor_df
    #alt_puffin_df = data_retrieval_helper.atl_puffin_df

    data_summarization_osprey_helper = DataSummarizationHelper(osprey_df)
    data_summarization_osprey_helper.define_dataframe_bounds()
    data_summarization_osprey_helper.print_geo_range_date_range()

    osprey_glacier_bay_region = getOspreyGlacierBayRegion()
    osprey_glacier_bay_df = filter_df_by_region(osprey_df, osprey_glacier_bay_region)

    osprey_glacier_bay_df_data_summary = DataSummarizationHelper(osprey_glacier_bay_df)
    osprey_glacier_bay_df_data_summary.print_geo_range_date_range()

    #condor_grand_canyon_region = getCondorGrandCanyonRegion()
    #condor_grand_canyon_df = filter_df_by_region(condor_df, condor_grand_canyon_region)

    #atl_puffin_ma_coastal_region = getAtlPuffinMACoastalRegion()
    #atl_puffin_ma_coastal_df = filter_df_by_region(alt_puffin_df, atl_puffin_ma_coastal_region)

