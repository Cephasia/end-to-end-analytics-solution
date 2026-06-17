"""
Main execution script for End-to-End Analytics Solution
"""

import logging
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.data_analyzer import DataAnalyzer
from src.config import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting End-to-End Analytics Solution")
    try:
        loader = DataLoader(config.database)
        csv_path = "data/sample_data.csv"

        # Create sample data if it doesn't exist
        if not Path(csv_path).exists():
            import pandas as pd
            dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')
            sample_data = pd.DataFrame({
                'date': dates,
                'product': ['Product A', 'Product B', 'Product C', 'Product D'] * (len(dates) // 4 + 1),
                'region': ['North', 'South', 'East', 'West'] * (len(dates) // 4 + 1),
                'quantity': list(range(1, len(dates)+1))[:len(dates)],
                'revenue': list(range(100, 100 + len(dates)))[:len(dates)],
                'customer_id': list(range(1, len(dates)+1))[:len(dates)]
            })[:len(dates)]
            Path("data").mkdir(exist_ok=True)
            sample_data.to_csv(csv_path, index=False)
            logger.info(f"Sample data created at {csv_path}")

        df = loader.load_csv(csv_path)

        processor = DataProcessor(df)
        processor.clean_data(remove_duplicates=True, handle_missing='drop')
        if 'date' in df.columns:
            processor.parse_dates(['date'])
        processed_df = processor.get_data()

        analyzer = DataAnalyzer(processed_df)
        stats = analyzer.get_descriptive_stats()
        print("Descriptive statistics:")
        print(stats.head())

        output_path = "data/processed/processed_sales_data.csv"
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        processed_df.to_csv(output_path, index=False)
        logger.info(f"Processed data saved to {output_path}")

        print("\nDATA SUMMARY")
        print("="*50)
        print(f"Total Records: {len(processed_df)}")
        print(f"Total Columns: {len(processed_df.columns)}")
        print(f"Columns: {list(processed_df.columns)}")
        print(processed_df.head())

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()
