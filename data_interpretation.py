import pandas as pd
import folium
import plotly.express as px
import imageio
import datetime
import os

def main():
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
    generate_raw_maps(df, "Osprey", "map_output_osprey_raw")
    generate_raw_maps(df, "California Condor", "map_output_ca_condor_raw")

def generate_raw_maps(df, species_name, output_directory_name):
    df = df[df['COMMON NAME'] == species_name]
    most_recent_date = df['OBSERVATION DATE'].max()

    #df_most_recent = df[df['OBSERVATION DATE'] == most_recent_date]

    print(list(df.columns))

    start_date = datetime.date(2025, 6, 1)
    end_date = datetime.date(2025, 8, 31)
    df = df[(df['OBSERVATION DATE'] >= pd.Timestamp(start_date)) & (df['OBSERVATION DATE'] <= pd.Timestamp(end_date))]

    frames = sorted(df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d').unique())
    images = []

    # Create directory "map_output" if it doesn't exist
    if not os.path.exists(output_directory_name):
        os.makedirs(output_directory_name)

    for frame in frames:
        print(frame)
        dfi = df[df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d') == frame]
        fig = px.scatter_geo(
            dfi, lat='LATITUDE', lon='LONGITUDE',
            color='COMMON NAME', scope='north america',
            projection='natural earth'
        )
        fig.update_geos(showcountries=True)
        img_path = f"{output_directory_name}/frame_{frame}.png"
        fig.write_image(img_path)

if __name__ == "__main__":
    main()
