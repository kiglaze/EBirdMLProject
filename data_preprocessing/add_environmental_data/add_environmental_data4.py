import pandas as pd
import os

# Join files in data_preprocessing/weather_data_weekly with files in data_preprocessing/restricted_geo_loc_sighting_weekly by species and week/year

def join_weekly_weather_and_observation_data(weather_data_filepath, observation_data_filepath, output_filepath):
    # Load weather data
    weather_df = pd.read_csv(weather_data_filepath)

    # Load observation data
    observation_df = pd.read_csv(observation_data_filepath)

    # Merge datasets on species, week, and year
    merged_df = pd.merge(weather_df, observation_df, left_on=['year', 'week_number'], right_on=['YEAR', 'WEEK_IN_YEAR'], how='left')

    # Save the merged dataset
    merged_df.to_csv(output_filepath, index=False)
    print(f'Merged data saved to {output_filepath}')

if __name__ == '__main__':
    if not os.path.exists("../environmental_data_joined/"):
        os.makedirs("../environmental_data_joined/")

    weather_data_filepath = '../weather_data_weekly/osprey_glacier_bay_region_weekly_weather_data.csv'
    observation_data_filepath = '../restricted_geo_loc_sighting_weekly/osprey_glacier_bay_weekly.csv'
    output_filepath = '../environmental_data_joined/osprey_glacier_bay_weekly_weather_observation_data.csv'
    join_weekly_weather_and_observation_data(weather_data_filepath, observation_data_filepath, output_filepath)

    weather_data_filepath = '../weather_data_weekly/condor_grand_canyon_region_weekly_weather_data.csv'
    observation_data_filepath = '../restricted_geo_loc_sighting_weekly/ca_condor_grand_canyon_weekly.csv'
    output_filepath = '../environmental_data_joined/ca_condor_grand_canyon_weekly_weather_observation_data.csv'
    join_weekly_weather_and_observation_data(weather_data_filepath, observation_data_filepath, output_filepath)

    weather_data_filepath = '../weather_data_weekly/atl_puffin_ma_coastal_region_weekly_weather_data.csv'
    observation_data_filepath = '../restricted_geo_loc_sighting_weekly/atlantic_puffin_ma_coastal_weekly.csv'
    output_filepath = '../environmental_data_joined/atlantic_puffin_ma_coastal_weekly_weather_observation_data.csv'
    join_weekly_weather_and_observation_data(weather_data_filepath, observation_data_filepath, output_filepath)
