import pandas as pd
import folium

#def main():

if __name__ == "__main__":
    # Load csv file into pandas dataframe: output_filtered_species_consolidated/osprey_ca_condor_output.csv
    df = pd.read_csv("output_filtered_species_consolidated/osprey_ca_condor_output.csv", dtype="string")
    print(df.head())
    df = df[df['COUNTRY'].isin(['United States', 'Mexico', 'Canada', 'Cuba'])]
    df = df[df['COMMON NAME'] == "Osprey"]
    most_recent_date = df['OBSERVATION DATE'].max()
    df_most_recent = df[df['OBSERVATION DATE'] == most_recent_date]
    df = df_most_recent

    print(list(df.columns))

    # Create a map centered at the mean location
    center_lat = df['LATITUDE'].astype(float).mean()
    center_lon = df['LONGITUDE'].astype(float).mean()
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Add points
    for _, row in df.iterrows():
        folium.Marker(
            location=[float(row['LATITUDE']), float(row['LONGITUDE'])],
            popup=row.get('COMMON NAME', '')
        ).add_to(m)

    # Save to HTML
    m.save('map.html')

    #main()
