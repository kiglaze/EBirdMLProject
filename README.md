# Bird Species ML Project
## Installation
```bash
pip install -r requirements.txt
```

## Files
- `data_preprocessing.py`: Script for data cleaning and preprocessing.
- `data_interpretation.py`: ML

Generates the map images that become map animations, showing bird sightings over time.
- `data_preprocessing/maps_generation.py`
    - Start date (maps): datetime.date(2023, 3, 1)
    - End date (maps): datetime.date(2025, 8, 31)

Makes animations from images of bird GPS locations. (in North America: US, Canada, Mexico, Cuba)
- `combine_maps_video.py`


Prepares input files to make logistic regressions. (restricted to certain geographic regions)
- `data_preprocessing/restricted_geo_loc_appearance_weekly.py`
    - Start date (logistic regression): datetime.date(2015, 3, 1)
    - End date (logistic regression): datetime.date(2025, 8, 31)

Makes logistic regression graphs. (restricted to certain geographic regions)
- `analysis/logistic_regression.py`


Getting data ready for decision tree models.
- `data_preprocessing/add_environmental_data.py`


## GPS regions by species (for boolean appearance variables in logistic regression)
Osprey
Glacier Bay Region
58.0, -137.0
58.0, -135.0
60.0, -137.0
60.0, -135.0
glacier_bay_region = Region((58.0, 60.0), (-137.0, -135.0))

California Condors
Grand Canyon -- Latitude: 35.0°N to 37.0°N; Longitude: −113.0°W to −111.0°W
35, -113
35, -111
37, -113
37, -111
grand_canyon_region = Region((35.0, 37.0), (-113.0, -111.0))

Atlantic Puffins
41.724641, -70.255132
ma_coastal_region = Region((41.0, 42.8), (-73.7, -69.8))
MA Coastal Region
41.0, -73.7
41.0, -69.8
42.8, -73.7
42.8, -69.8
