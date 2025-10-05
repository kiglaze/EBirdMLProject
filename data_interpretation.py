import pandas as pd
import folium
import plotly.express as px
import imageio
import datetime
import os

#def main():

if __name__ == "__main__":
    # Load csv file into pandas dataframe: output_filtered_species_consolidated/osprey_ca_condor_output.csv
    df = pd.read_csv("output_filtered_species_consolidated/osprey_ca_condor_output.csv", dtype="string")
    print(df.head())
    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])]
    df = df[df['COMMON NAME'] == "Osprey"]
    most_recent_date = df['OBSERVATION DATE'].max()
    df['OBSERVATION DATE'] = pd.to_datetime(df['OBSERVATION DATE'])
    df['LATITUDE'] = df['LATITUDE'].astype(float)
    df['LONGITUDE'] = df['LONGITUDE'].astype(float)

    #df_most_recent = df[df['OBSERVATION DATE'] == most_recent_date]

    print(list(df.columns))

    # # Create a map centered at the mean location
    # center_lat = df['LATITUDE'].astype(float).mean()
    # center_lon = df['LONGITUDE'].astype(float).mean()
    # m = folium.Map(location=[center_lat, center_lon], zoom_start=4)
    #
    # # Add points
    # for _, row in df.iterrows():
    #     folium.Marker(
    #         location=[float(row['LATITUDE']), float(row['LONGITUDE'])],
    #         popup=row.get('COMMON NAME', '')
    #     ).add_to(m)
    #
    # # Save to HTML
    # m.save('map.html')

    start_date = datetime.date(2025, 6, 1)
    end_date = datetime.date(2025, 8, 31)
    df = df[(df['OBSERVATION DATE'] >= pd.Timestamp(start_date)) & (df['OBSERVATION DATE'] <= pd.Timestamp(end_date))]

    frames = sorted(df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d').unique())
    images = []

    # Create directory "map_output" if it doesn't exist
    if not os.path.exists("map_output_raw"):
        os.makedirs("map_output_raw")

    for frame in frames:
        print(frame)
        dfi = df[df['OBSERVATION DATE'].dt.strftime('%Y-%m-%d') == frame]
        fig = px.scatter_geo(
            dfi, lat='LATITUDE', lon='LONGITUDE',
            color='COMMON NAME', scope='north america',
            projection='natural earth'
        )
        fig.update_geos(showcountries=True)
        img_path = f"map_output_raw/frame_{frame}.png"
        fig.write_image(img_path)

    #main()
