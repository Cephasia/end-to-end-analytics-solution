"""
End-to-End Analytics Solution
A comprehensive BI and analytics platform for sales data analysis
"""

__version__ = "1.0.0"
__author__ = "Cephasia"

from .data_loader import DataLoader
from .data_processor import DataProcessor
from .data_analyzer import DataAnalyzer

__all__ = ["DataLoader", "DataProcessor", "DataAnalyzer"]
