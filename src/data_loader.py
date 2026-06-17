"""
Data Loader Module
Handles loading data from CSV files and SQL databases
"""

import pandas as pd
import logging
from typing import Optional
from sqlalchemy import create_engine, inspect

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataLoader:
    """Load data from various sources"""
    
    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self.engine = None
    
    def load_csv(self, file_path: str, **kwargs) -> pd.DataFrame:
        try:
            logger.info(f"Loading CSV file: {file_path}")
            df = pd.read_csv(file_path, **kwargs)
            logger.info(f"Successfully loaded {len(df)} rows from {file_path}")
            return df
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error loading CSV file: {str(e)}")
            raise
    
    def load_from_sql(self, query: str, db_type: str = "sqlite", db_config: Optional[dict] = None) -> pd.DataFrame:
        try:
            logger.info(f"Connecting to {db_type} database...")
            engine = self._create_engine(db_type, db_config)
            logger.info("Executing SQL query...")
            df = pd.read_sql(query, engine)
            logger.info(f"Successfully loaded {len(df)} rows from database")
            return df
        except Exception as e:
            logger.error(f"Error loading data from SQL: {str(e)}")
            raise
    
    def load_from_table(self, table_name: str, db_type: str = "sqlite", db_config: Optional[dict] = None) -> pd.DataFrame:
        query = f"SELECT * FROM {table_name}"
        return self.load_from_sql(query, db_type, db_config)
    
    def _create_engine(self, db_type: str, db_config: Optional[dict] = None):
        if db_config is None:
            db_config = self.config
        if db_type == "sqlite":
            db_path = db_config.get('sqlite_path', 'data/sales_database.db')
            connection_string = f"sqlite:///{db_path}"
        elif db_type == "mysql":
            user = db_config.get('user', 'root')
            password = db_config.get('password', '')
            host = db_config.get('host', 'localhost')
            port = db_config.get('port', 3306)
            database = db_config.get('database', '')
            connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == "postgresql":
            user = db_config.get('user', 'postgres')
            password = db_config.get('password', '')
            host = db_config.get('host', 'localhost')
            port = db_config.get('port', 5432)
            database = db_config.get('database', '')
            connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        return create_engine(connection_string)
    
    def list_tables(self, db_type: str = "sqlite", db_config: Optional[dict] = None) -> list:
        try:
            engine = self._create_engine(db_type, db_config)
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            logger.info(f"Found {len(tables)} tables: {tables}")
            return tables
        except Exception as e:
            logger.error(f"Error listing tables: {str(e)}")
            raise
