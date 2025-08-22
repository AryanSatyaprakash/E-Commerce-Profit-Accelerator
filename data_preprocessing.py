#!/usr/bin/env python3
"""
Data Preprocessing Utilities for E-Commerce Analysis
"""

import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

class DataPreprocessor:
    """
    Utility class for data preprocessing and cleaning operations
    """

    def __init__(self, db_path='ecommerce_analysis.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)

    def clean_orders_data(self, df):
        """Clean and validate orders data"""
        print("🧹 Cleaning orders data...")

        # Convert datetime columns
        datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                        'order_delivered_carrier_date', 'order_delivered_customer_date']

        for col in datetime_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')

        # Remove invalid orders
        initial_rows = len(df)
        df = df.dropna(subset=['order_id', 'customer_id'])
        df = df[df['order_status'].notna()]

        print(f"   • Removed {initial_rows - len(df)} invalid records")
        return df

    def clean_order_items_data(self, df):
        """Clean and validate order items data"""
        print("🧹 Cleaning order items data...")

        # Remove negative prices
        initial_rows = len(df)
        df = df[df['price'] > 0]
        df = df[df['freight_value'] >= 0]

        # Remove duplicates
        df = df.drop_duplicates(subset=['order_id', 'order_item_id'])

        print(f"   • Removed {initial_rows - len(df)} invalid/duplicate records")
        return df

    def add_calculated_fields(self, df):
        """Add calculated fields for analysis"""
        print("➕ Adding calculated fields...")

        # Add total amount
        if 'price' in df.columns and 'freight_value' in df.columns:
            df['total_amount'] = df['price'] + df['freight_value']

        # Add date components
        if 'order_purchase_timestamp' in df.columns:
            df['order_year'] = df['order_purchase_timestamp'].dt.year
            df['order_month'] = df['order_purchase_timestamp'].dt.month
            df['order_quarter'] = df['order_purchase_timestamp'].dt.quarter
            df['order_day_of_week'] = df['order_purchase_timestamp'].dt.dayofweek

        return df

    def validate_data_quality(self, df, table_name):
        """Validate data quality and report issues"""
        print(f"✅ Validating {table_name} data quality...")

        # Check for missing values
        missing_data = df.isnull().sum()
        if missing_data.any():
            print(f"   • Missing values found:")
            for col, count in missing_data[missing_data > 0].items():
                print(f"     - {col}: {count} ({count/len(df)*100:.1f}%)")

        # Check for duplicates
        duplicates = df.duplicated().sum()
        if duplicates > 0:
            print(f"   • Duplicate rows: {duplicates}")

        # Data type validation
        print(f"   • Data types:")
        for col, dtype in df.dtypes.items():
            print(f"     - {col}: {dtype}")

        return True

    def export_clean_data(self):
        """Export cleaned data to CSV files"""
        print("💾 Exporting cleaned data...")

        # Read and clean each table
        tables = ['customers', 'orders', 'order_items', 'products']

        for table in tables:
            try:
                df = pd.read_sql(f"SELECT * FROM {table}", self.conn)

                if table == 'orders':
                    df = self.clean_orders_data(df)
                    df = self.add_calculated_fields(df)
                elif table == 'order_items':
                    df = self.clean_order_items_data(df)

                self.validate_data_quality(df, table)

                # Export to CSV
                df.to_csv(f'data/processed/{table}_clean.csv', index=False)
                print(f"   • Exported {table}: {len(df):,} records")

            except Exception as e:
                print(f"   • Error processing {table}: {str(e)}")

    def close_connection(self):
        """Close database connection"""
        self.conn.close()

if __name__ == "__main__":
    print("🧹 Data Preprocessing Pipeline")
    print("=" * 40)

    preprocessor = DataPreprocessor()
    preprocessor.export_clean_data()
    preprocessor.close_connection()

    print("\n✅ Data preprocessing complete!")
