import pandas as pd
from numpy.ma.extras import atleast_1d
from pathlib import Path
from tqdm import tqdm  # optional, just for progress bar

RESTRICTED_GEO_LOC_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output_by_species/restricted_by_geo_time"

from geopy.geocoders import Nominatim

def get_zipcode_from_coords(latitude, longitude):
    """
    Retrieves the zip code for given latitude and longitude using Nominatim.
    """
    geolocator = Nominatim(user_agent="my_geocoder_app") # Replace with a unique user agent
    try:
        location = geolocator.reverse(f"{latitude}, {longitude}")
        if location and 'address' in location.raw and 'postcode' in location.raw['address']:
            return location.raw['address']['postcode']
        else:
            return None
    except Exception as e:
        print(f"Error during reverse geocoding: {e}")
        return None


def reverse_geocode_zip(species_geo_filtered_df):
    # Ensure lat/lon columns exist (replace with your actual column names)
    if 'LATITUDE' in species_geo_filtered_df.columns and 'LONGITUDE' in species_geo_filtered_df.columns:
        tqdm.pandas(desc="Fetching zip codes")  # optional
        species_geo_filtered_df["ZIP_CODE"] = species_geo_filtered_df.progress_apply(
            lambda row: get_zipcode_from_coords(row["LATITUDE"], row["LONGITUDE"]), axis=1
        )
    else:
        print("Missing LATITUDE or LONGITUDE columns in CSV.")
    return species_geo_filtered_df


if __name__ == "__main__":
    # osprey_geo_filtered_df = pd.read_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "osprey_glacier_bay_15_25_restricted.csv")
    # osprey_geo_filtered_df = reverse_geocode_zip(osprey_geo_filtered_df)
    # osprey_geo_filtered_df.to_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "osprey_glacier_bay_15_25_restricted_with_zip.csv", index=False)

    # atl_puffin_geo_filtered_df = pd.read_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "atl_puffin_ma_coastal_15_25_restricted.csv")
    # atl_puffin_geo_filtered_df = reverse_geocode_zip(atl_puffin_geo_filtered_df)
    # atl_puffin_geo_filtered_df.to_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "atl_puffin_ma_coastal_15_25_restricted_with_zip.csv", index=False)

    ca_condor_geo_filtered_df = pd.read_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "ca_condor_grand_canyon_15_25_restricted.csv")
    ca_condor_geo_filtered_df = reverse_geocode_zip(ca_condor_geo_filtered_df)
    ca_condor_geo_filtered_df.to_csv(RESTRICTED_GEO_LOC_OUTPUT_DIR / "ca_condor_grand_canyon_15_25_restricted_with_zip.csv", index=False)

