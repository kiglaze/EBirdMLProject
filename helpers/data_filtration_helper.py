from models.RegionClass import RegionClass

def filter_df_by_region(df, region: RegionClass):
    """
    Filters the given DataFrame to only include rows within the specified geographic region.

    Parameters:
    - df: pandas.DataFrame with 'LATITUDE' and 'LONGITUDE' columns
    - region: Region object with lat_range and lon_range tuples

    Returns:
    - Filtered pandas.DataFrame
    """
    lat_min, lat_max = region.lat_range
    lon_min, lon_max = region.lon_range
    filtered_df = df[
        (df['LATITUDE'] >= lat_min) & (df['LATITUDE'] <= lat_max) &
        (df['LONGITUDE'] >= lon_min) & (df['LONGITUDE'] <= lon_max)
    ]
    return filtered_df

def getOspreyGlacierBayRegion():
    """
    Returns a RegionClass object
    """
    # lat/lon ranges for Osprey habitat, Glacier Bay, Alaska
    lat_range = (58.0, 60.0)
    lon_range = (-137.0, -135.0)
    return RegionClass(lat_range, lon_range)

def getCondorGrandCanyonRegion():
    """
    Returns a RegionClass object
    """
    # Example lat/lon ranges for Condor habitat, Grand Canyon, Arizona
    lat_range = (35.0, 37.0)
    lon_range = (-113.0, -111.0)
    return RegionClass(lat_range, lon_range)

def getAtlPuffinMACoastalRegion():
    """
    Returns a RegionClass object
    """
    # Example lat/lon ranges for Atlantic Puffin habitat, Massachusetts coastal area
    lat_range = (41.0, 42.8)
    lon_range = (-73.7, -69.8)
    return RegionClass(lat_range, lon_range)
