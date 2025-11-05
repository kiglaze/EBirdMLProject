from typing import Optional
import pandas as pd

class DataSummarizationHelper:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.max_date: Optional[pd.Timestamp] = None
        self.min_date: Optional[pd.Timestamp] = None
        self.max_latitude: Optional[float] = None
        self.min_latitude: Optional[float] = None
        self.max_longitude: Optional[float] = None
        self.min_longitude: Optional[float] = None

        self.define_dataframe_bounds()

    def define_dataframe_bounds(self):
        """
        Coerce relevant columns and return min/max values:
        - 'OBSERVATION DATE' -> pandas.Timestamp (min_date, max_date)
        - 'LATITUDE' and 'LONGITUDE' -> float (min/max)
        Returns a dict with keys:
        'min_date', 'max_date', 'min_latitude', 'max_latitude', 'min_longitude', 'max_longitude'
        """
        df = self.dataframe
        if df is not None:
            # ensure columns exist to avoid KeyError
            if 'OBSERVATION DATE' in df.columns:
                self.min_date = pd.to_datetime(df['OBSERVATION DATE']).min()
                self.max_date = pd.to_datetime(df['OBSERVATION DATE']).max()
            else:
                self.min_date = None
                self.max_date = None

            if 'LATITUDE' in df.columns:
                df.loc[:, ('LATITUDE')] = pd.to_numeric(df['LATITUDE'])
                self.min_latitude = df['LATITUDE'].min()
                self.max_latitude = df['LATITUDE'].max()
            else:
                self.min_latitude = None
                self.max_latitude = None

            if 'LONGITUDE' in df.columns:
                # Convert LONGITUDE to numeric
                df.loc[:, ('LONGITUDE')] = pd.to_numeric(df['LONGITUDE'])
                self.min_longitude = df['LONGITUDE'].min()
                self.max_longitude = df['LONGITUDE'].max()
            else:
                self.min_longitude = None
                self.max_longitude = None

    def print_geo_range_date_range(self):
        print("==================")
        print("latitude range:")
        print(self.min_latitude)
        print(self.max_latitude)
        print("longitude range:")
        print(self.min_longitude)
        print(self.max_longitude)
        print("date range:")
        print(self.max_date)
        print(self.min_date)
        print("==================")
