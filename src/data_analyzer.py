"""
Data Analyzer Module
Handles data analysis and statistical calculations
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, Any
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataAnalyzer:
    """Analyze and explore data"""
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_descriptive_stats(self) -> pd.DataFrame:
        return self.df.describe().T
    
    def get_correlation(self, numeric_only: bool = True) -> pd.DataFrame:
        if numeric_only:
            numeric_df = self.df.select_dtypes(include=[np.number])
        else:
            numeric_df = self.df
        return numeric_df.corr()
    
    def get_missing_data_report(self) -> pd.DataFrame:
        missing_counts = self.df.isnull().sum()
        missing_percent = (missing_counts / len(self.df)) * 100
        report = pd.DataFrame({
            'Missing_Count': missing_counts,
            'Percentage': missing_percent
        })
        return report[report['Missing_Count'] > 0].sort_values('Percentage', ascending=False)
    
    def get_value_counts(self, column: str, top_n: int = 10) -> pd.Series:
        if column not in self.df.columns:
            return pd.Series()
        return self.df[column].value_counts().head(top_n)
    
    def get_outliers(self, column: str, method: str = "iqr") -> pd.DataFrame:
        if column not in self.df.columns:
            return pd.DataFrame()
        if method == "iqr":
            Q1 = self.df[column].quantile(0.25)
            Q3 = self.df[column].quantile(0.75)
            IQR = Q3 - Q1
            outliers = self.df[(self.df[column] < Q1 - 1.5 * IQR) | (self.df[column] > Q3 + 1.5 * IQR)]
        elif method == "zscore":
            outliers = self.df[np.abs(stats.zscore(self.df[column].dropna())) > 3]
        else:
            raise ValueError("Unknown method")
        return outliers
    
    def group_analysis(self, groupby_col: str, agg_functions: Dict[str, str]) -> pd.DataFrame:
        if groupby_col not in self.df.columns:
            return pd.DataFrame()
        return self.df.groupby(groupby_col).agg(agg_functions)
    
    def time_series_analysis(self, date_col: str, value_col: str, freq: str = "D") -> pd.DataFrame:
        if date_col not in self.df.columns or value_col not in self.df.columns:
            return pd.DataFrame()
        df_ts = self.df.copy()
        df_ts[date_col] = pd.to_datetime(df_ts[date_col])
        df_ts = df_ts.set_index(date_col)
        return df_ts[value_col].resample(freq).sum()
    
    def get_top_performers(self, group_col: str, value_col: str, top_n: int = 5) -> pd.DataFrame:
        result = self.df.groupby(group_col)[value_col].sum().sort_values(ascending=False).head(top_n)
        return result
    
    def generate_report(self) -> Dict[str, Any]:
        report = {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'data_types': self.df.dtypes.astype(str).to_dict(),
            'descriptive_stats': self.get_descriptive_stats().to_dict(),
            'missing_data': self.get_missing_data_report().to_dict(),
            'duplicates': self.df.duplicated().sum()
        }
        return report
