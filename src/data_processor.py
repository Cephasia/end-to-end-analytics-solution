"""
Data Processor Module
Handles data cleaning, transformation, and aggregation
"""

import pandas as pd
import numpy as np
import logging
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessor:
    """Process and transform data"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.original_df = df.copy()
    
    def clean_data(self, remove_duplicates: bool = True, handle_missing: str = "drop", remove_outliers: bool = False) -> 'DataProcessor':
        logger.info("Starting data cleaning...")
        if remove_duplicates:
            initial_rows = len(self.df)
            self.df = self.df.drop_duplicates()
            removed = initial_rows - len(self.df)
            logger.info(f"Removed {removed} duplicate rows")
        if handle_missing == "drop":
            initial_rows = len(self.df)
            self.df = self.df.dropna()
            removed = initial_rows - len(self.df)
            logger.info(f"Removed {removed} rows with missing values")
        elif handle_missing == "mean":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].mean())
            logger.info("Filled missing numeric values with mean")
        elif handle_missing == "median":
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns
            self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
            logger.info("Filled missing numeric values with median")
        elif handle_missing == "forward_fill":
            self.df = self.df.fillna(method='ffill')
            logger.info("Filled missing values using forward fill")
        if remove_outliers:
            self.df = self._remove_outliers_iqr()
            logger.info("Removed outliers using IQR method")
        return self
    
    def _remove_outliers_iqr(self) -> pd.DataFrame:
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        df_clean = self.df.copy()
        for col in numeric_cols:
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_clean = df_clean[(df_clean[col] >= lower_bound) & (df_clean[col] <= upper_bound)]
        return df_clean
    
    def convert_data_types(self, type_mapping: Dict[str, str]) -> 'DataProcessor':
        for col, dtype in type_mapping.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                except Exception:
                    pass
        return self
    
    def parse_dates(self, date_columns: List[str], date_format: Optional[str] = None) -> 'DataProcessor':
        for col in date_columns:
            if col in self.df.columns:
                try:
                    self.df[col] = pd.to_datetime(self.df[col], format=date_format)
                except Exception:
                    pass
        return self
    
    def aggregate(self, groupby_cols: List[str], agg_dict: Dict[str, str]) -> pd.DataFrame:
        return self.df.groupby(groupby_cols).agg(agg_dict).reset_index()
    
    def filter_data(self, conditions: Dict[str, Any]) -> 'DataProcessor':
        for col, value in conditions.items():
            if col in self.df.columns:
                if isinstance(value, (list, tuple)):
                    self.df = self.df[self.df[col].isin(value)]
                else:
                    self.df = self.df[self.df[col] == value]
        return self
    
    def create_features(self, feature_dict: Dict[str, str]) -> 'DataProcessor':
        for feature_name, expression in feature_dict.items():
            try:
                self.df[feature_name] = self.df.eval(expression)
            except Exception:
                pass
        return self
    
    def get_data(self) -> pd.DataFrame:
        return self.df.copy()
    
    def reset(self) -> 'DataProcessor':
        self.df = self.original_df.copy()
        return self
    
    def get_summary(self) -> Dict[str, Any]:
        summary = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'memory_usage': self.df.memory_usage(deep=True).sum() / 1024**2,
            'missing_values': self.df.isnull().sum().to_dict(),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'duplicates': self.df.duplicated().sum()
        }
        return summary
