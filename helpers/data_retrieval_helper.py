import os
from typing import Optional
import pandas as pd

INPUT_BY_SPECIES_DIR = "../data_preprocessing/output_by_species/originals"

class DataRetrievalHelper:
    def __init__(self):
        self.base_dir = INPUT_BY_SPECIES_DIR
        self.osprey_filename = "osprey_data.csv"                 # fixed typo from original
        self.condor_filename = "california_condor_data.csv"
        self.atl_puffin_filename = "atlantic_puffin_data.csv"
        self.osprey_filepath = os.path.join(self.base_dir, self.osprey_filename)
        self.condor_filepath = os.path.join(self.base_dir, self.condor_filename)
        self.atl_puffin_filepath = os.path.join(self.base_dir, self.atl_puffin_filename)
        self._osprey_df: Optional[pd.DataFrame] = None
        self._condor_df: Optional[pd.DataFrame] = None
        self._atl_puffin_df: Optional[pd.DataFrame] = None

    def open_csv_file(self, filepath: str, **read_csv_kwargs) -> pd.DataFrame:
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        return pd.read_csv(filepath, **read_csv_kwargs)

    @property
    def osprey_df(self) -> pd.DataFrame:
        if self._osprey_df is None:
            self._osprey_df = self.open_csv_file(self.osprey_filepath)
        return self._osprey_df

    @property
    def condor_df(self) -> pd.DataFrame:
        if self._condor_df is None:
            self._condor_df = self.open_csv_file(self.condor_filepath)
        return self._condor_df

    @property
    def atl_puffin_df(self) -> pd.DataFrame:
        if self._atl_puffin_df is None:
            self._atl_puffin_df = self.open_csv_file(self.atl_puffin_filepath)
        return self._atl_puffin_df

    def reload_all(self, **read_csv_kwargs) -> None:
        self._osprey_df = self.open_csv_file(self.osprey_filepath, **read_csv_kwargs)
        self._condor_df = self.open_csv_file(self.condor_filepath, **read_csv_kwargs)
        self._atl_puffin_df = self.open_csv_file(self.atl_puffin_filepath, **read_csv_kwargs)
