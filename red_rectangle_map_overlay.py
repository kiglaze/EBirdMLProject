import folium
from helpers.data_filtration_helper import getOspreyGlacierBayRegion, getCondorGrandCanyonRegion, getAtlPuffinMACoastalRegion
import os

def create_map_with_rectangle(min_lat, max_lat, min_lon, max_lon, output_file_name="rectangle_map.html"):
    # Create map centered roughly in the middle
    center_lat = (min_lat + max_lat) / 2
    center_lon = (min_lon + max_lon) / 2
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7)

    # Draw rectangle
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]
    folium.Rectangle(
        bounds=bounds,
        color="red",
        fill=True,
        fill_opacity=0.2,
        tooltip=f"Lat: {min_lat}-{max_lat}, Lon: {min_lon}-{max_lon}"
    ).add_to(m)

    m.save(output_file_name)

if __name__ == "__main__":
    output_dir = "rectangle_map_overlays"
    # If the output directory does not exist, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    osprey_glacier_bay_region = getOspreyGlacierBayRegion()
    # Define bounding box coordinates
    min_lat, max_lat = osprey_glacier_bay_region.get_min_lat(), osprey_glacier_bay_region.get_max_lat()
    min_lon, max_lon = osprey_glacier_bay_region.get_min_lon(), osprey_glacier_bay_region.get_max_lon()
    create_map_with_rectangle(min_lat, max_lat, min_lon, max_lon, f"{output_dir}/osprey_rectangle_map.html")

    atl_puffin_ma_coastal_region = getAtlPuffinMACoastalRegion()
    # Define bounding box coordinates
    min_lat, max_lat = atl_puffin_ma_coastal_region.get_min_lat(), atl_puffin_ma_coastal_region.get_max_lat()
    min_lon, max_lon = atl_puffin_ma_coastal_region.get_min_lon(), atl_puffin_ma_coastal_region.get_max_lon()
    create_map_with_rectangle(min_lat, max_lat, min_lon, max_lon, f"{output_dir}/atl_puffin_rectangle_map.html")

    ca_condor_grand_canyon_region = getCondorGrandCanyonRegion()
    # Define bounding box coordinates
    min_lat, max_lat = ca_condor_grand_canyon_region.get_min_lat(), ca_condor_grand_canyon_region.get_max_lat()
    min_lon, max_lon = ca_condor_grand_canyon_region.get_min_lon(), ca_condor_grand_canyon_region.get_max_lon()
    create_map_with_rectangle(min_lat, max_lat, min_lon, max_lon, f"{output_dir}/ca_condor_rectangle_map.html")