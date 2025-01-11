"""Data loading and processing utilities."""

import pandas as pd
from typing import Optional, Dict, Any

class DataLoader:
    def __init__(self, data_path: str):
        """Initialize the DataLoader with a path to the data file."""
        self.data_path = data_path
        self.data = None
        self.second_latest_data = None
    
    def load_data(self) -> pd.DataFrame:
        """Load and preprocess the dataset."""
        try:
            self.data = pd.read_csv(self.data_path)
            self._preprocess_data()
            return self.data
        except FileNotFoundError:
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")
    
    def _preprocess_data(self):
        """Preprocess the loaded data."""
        # Sort data by RegionID and Date in descending order
        self.data = self.data.sort_values(['RegionID', 'Date'], ascending=[True, False])
        
        # Select the second most recent data point for each region
        self.second_latest_data = self.data.groupby('RegionID').nth(1).reset_index()
    
    def get_hottest_markets(self, n: int = 10) -> pd.DataFrame:
        """Get the n hottest markets based on market temperature index."""
        return self.second_latest_data.nlargest(n, 'Metro_market_temp_index')
    
    def get_coldest_markets(self, n: int = 10) -> pd.DataFrame:
        """Get the n coldest markets based on market temperature index."""
        return self.second_latest_data.nsmallest(n, 'Metro_market_temp_index')
    
    def search_metro(self, query: str) -> pd.DataFrame:
        """Search for a metro area in the dataset."""
        return self.data[
            self.data['RegionName'].str.contains(query, case=False, na=False)
        ].sort_values(by='Date', ascending=False)
    
    def get_latest_metrics(self, metro_name: str) -> Dict[str, Any]:
        """Get the latest metrics for a specific metro area."""
        metro_data = self.search_metro(metro_name)
        if metro_data.empty:
            return {}
        return metro_data.iloc[0].to_dict()