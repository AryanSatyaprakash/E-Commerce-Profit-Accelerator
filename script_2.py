# Create requirements.txt file for Python dependencies
requirements_content = """# E-Commerce Sales Analysis - Python Requirements
# Data Analysis and Manipulation
pandas>=1.3.0
numpy>=1.21.0

# Data Visualization
matplotlib>=3.4.0
seaborn>=0.11.0
plotly>=5.0.0

# Database Connectivity
SQLAlchemy>=1.4.0
sqlite3

# Jupyter and Interactive Analysis
jupyter>=1.0.0
ipython>=7.0.0

# Additional Utilities
python-dateutil>=2.8.0
scipy>=1.7.0
scikit-learn>=1.0.0

# Development and Testing
pytest>=6.0.0
black>=21.0.0
flake8>=3.9.0

# Optional: For advanced visualizations
bokeh>=2.3.0
dash>=2.0.0
streamlit>=1.0.0
"""

with open('requirements.txt', 'w') as f:
    f.write(requirements_content)

print("✅ Requirements file created: requirements.txt")

# Create setup script for database initialization
setup_script = """#!/usr/bin/env python3
\"\"\"
Database Setup Script for E-Commerce Analysis Project
\"\"\"

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_database_schema():
    \"\"\"Create database schema for e-commerce analysis\"\"\"
    
    conn = sqlite3.connect('ecommerce_analysis.db')
    cursor = conn.cursor()
    
    # Create tables
    schema_sql = \"\"\"
    -- Customers table
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        customer_unique_id TEXT,
        customer_zip_code_prefix INTEGER,
        customer_city TEXT,
        customer_state TEXT
    );
    
    -- Orders table
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_status TEXT,
        order_purchase_timestamp DATETIME,
        order_approved_at DATETIME,
        order_delivered_carrier_date DATETIME,
        order_delivered_customer_date DATETIME,
        order_estimated_delivery_date DATETIME,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
    );
    
    -- Order items table
    CREATE TABLE IF NOT EXISTS order_items (
        order_id TEXT,
        order_item_id INTEGER,
        product_id TEXT,
        seller_id TEXT,
        shipping_limit_date DATETIME,
        price REAL,
        freight_value REAL,
        PRIMARY KEY (order_id, order_item_id),
        FOREIGN KEY (order_id) REFERENCES orders(order_id)
    );
    
    -- Products table
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_category_name TEXT,
        product_name_length INTEGER,
        product_description_length INTEGER,
        product_photos_qty INTEGER,
        product_weight_g INTEGER,
        product_length_cm INTEGER,
        product_height_cm INTEGER,
        product_width_cm INTEGER
    );
    
    -- Create indexes for better performance
    CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
    CREATE INDEX IF NOT EXISTS idx_orders_date ON orders(order_purchase_timestamp);
    CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);
    CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
    \"\"\"
    
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print("✅ Database schema created successfully")

def generate_sample_data():
    \"\"\"Generate sample data for testing purposes\"\"\"
    
    np.random.seed(42)
    
    # Generate sample data
    n_customers = 5000
    n_orders = 15000
    n_products = 1000
    
    # Sample customers
    customers_data = {
        'customer_id': [f'CUST_{i:06d}' for i in range(n_customers)],
        'customer_unique_id': [f'UNIQUE_{i:06d}' for i in range(n_customers)],
        'customer_zip_code_prefix': np.random.randint(10000, 99999, n_customers),
        'customer_city': np.random.choice(['São Paulo', 'Rio de Janeiro', 'Brasília', 
                                         'Salvador', 'Fortaleza'], n_customers),
        'customer_state': np.random.choice(['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA'], 
                                         n_customers, p=[0.4, 0.15, 0.12, 0.1, 0.08, 0.08, 0.07])
    }
    
    customers_df = pd.DataFrame(customers_data)
    
    # Sample products
    categories = ['Electronics', 'Home & Garden', 'Fashion', 'Sports', 'Health & Beauty', 
                 'Auto', 'Books', 'Toys', 'Food & Beverages']
    
    products_data = {
        'product_id': [f'PROD_{i:06d}' for i in range(n_products)],
        'product_category_name': np.random.choice(categories, n_products),
        'product_name_length': np.random.randint(10, 100, n_products),
        'product_description_length': np.random.randint(50, 500, n_products),
        'product_photos_qty': np.random.randint(1, 10, n_products),
        'product_weight_g': np.random.randint(50, 5000, n_products),
        'product_length_cm': np.random.randint(5, 50, n_products),
        'product_height_cm': np.random.randint(5, 50, n_products),
        'product_width_cm': np.random.randint(5, 50, n_products)
    }
    
    products_df = pd.DataFrame(products_data)
    
    # Sample orders
    start_date = datetime(2017, 1, 1)
    end_date = datetime(2018, 12, 31)
    date_range = (end_date - start_date).days
    
    orders_data = {
        'order_id': [f'ORDER_{i:08d}' for i in range(n_orders)],
        'customer_id': np.random.choice(customers_df['customer_id'], n_orders),
        'order_status': np.random.choice(['delivered', 'shipped', 'processing', 'cancelled'], 
                                       n_orders, p=[0.85, 0.08, 0.04, 0.03]),
        'order_purchase_timestamp': [
            start_date + timedelta(days=np.random.randint(0, date_range))
            for _ in range(n_orders)
        ]
    }
    
    orders_df = pd.DataFrame(orders_data)
    
    # Add delivery dates
    orders_df['order_approved_at'] = orders_df['order_purchase_timestamp'] + pd.Timedelta(days=1)
    orders_df['order_delivered_carrier_date'] = orders_df['order_approved_at'] + pd.Timedelta(days=2)
    orders_df['order_delivered_customer_date'] = orders_df['order_delivered_carrier_date'] + pd.Timedelta(days=5)
    orders_df['order_estimated_delivery_date'] = orders_df['order_delivered_carrier_date'] + pd.Timedelta(days=7)
    
    # Sample order items
    order_items_data = []
    for order_id in orders_df['order_id']:
        n_items = np.random.choice([1, 2, 3, 4], p=[0.7, 0.2, 0.08, 0.02])
        for item_id in range(1, n_items + 1):
            order_items_data.append({
                'order_id': order_id,
                'order_item_id': item_id,
                'product_id': np.random.choice(products_df['product_id']),
                'seller_id': f'SELLER_{np.random.randint(1, 1000):04d}',
                'shipping_limit_date': datetime.now() + timedelta(days=np.random.randint(1, 30)),
                'price': round(np.random.lognormal(3.5, 0.8), 2),
                'freight_value': round(np.random.uniform(5, 50), 2)
            })
    
    order_items_df = pd.DataFrame(order_items_data)
    
    # Save to database
    conn = sqlite3.connect('ecommerce_analysis.db')
    
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    products_df.to_sql('products', conn, if_exists='replace', index=False)
    orders_df.to_sql('orders', conn, if_exists='replace', index=False)
    order_items_df.to_sql('order_items', conn, if_exists='replace', index=False)
    
    conn.close()
    
    print(f"✅ Sample data generated:")
    print(f"   • {len(customers_df):,} customers")
    print(f"   • {len(products_df):,} products")
    print(f"   • {len(orders_df):,} orders")
    print(f"   • {len(order_items_df):,} order items")

if __name__ == "__main__":
    print("🚀 Setting up E-Commerce Analysis Database...")
    print("=" * 50)
    
    # Create database schema
    create_database_schema()
    
    # Generate sample data
    generate_sample_data()
    
    print("\\n✅ Database setup complete!")
    print("📊 Ready to run analysis scripts")
"""

with open('setup_database.py', 'w') as f:
    f.write(setup_script)

print("✅ Database setup script created: setup_database.py")

# Create a simple data preprocessing utility
preprocessing_script = """#!/usr/bin/env python3
\"\"\"
Data Preprocessing Utilities for E-Commerce Analysis
\"\"\"

import pandas as pd
import numpy as np
from datetime import datetime
import sqlite3

class DataPreprocessor:
    \"\"\"
    Utility class for data preprocessing and cleaning operations
    \"\"\"
    
    def __init__(self, db_path='ecommerce_analysis.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def clean_orders_data(self, df):
        \"\"\"Clean and validate orders data\"\"\"
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
        \"\"\"Clean and validate order items data\"\"\"
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
        \"\"\"Add calculated fields for analysis\"\"\"
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
        \"\"\"Validate data quality and report issues\"\"\"
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
        \"\"\"Export cleaned data to CSV files\"\"\"
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
        \"\"\"Close database connection\"\"\"
        self.conn.close()

if __name__ == "__main__":
    print("🧹 Data Preprocessing Pipeline")
    print("=" * 40)
    
    preprocessor = DataPreprocessor()
    preprocessor.export_clean_data()
    preprocessor.close_connection()
    
    print("\\n✅ Data preprocessing complete!")
"""

with open('data_preprocessing.py', 'w') as f:
    f.write(preprocessing_script)

print("✅ Data preprocessing script created: data_preprocessing.py")

# Create a project configuration file
config_content = """# E-Commerce Sales Analysis Project Configuration

# Database Settings
DATABASE_PATH = 'ecommerce_analysis.db'
BACKUP_PATH = 'backups/'

# Analysis Parameters
ANALYSIS_START_DATE = '2017-01-01'
ANALYSIS_END_DATE = '2018-12-31'
MIN_ORDER_VALUE = 0.01
MAX_ORDER_VALUE = 10000

# Visualization Settings
FIGURE_SIZE = (12, 8)
DPI = 300
COLOR_PALETTE = 'husl'
EXPORT_FORMAT = 'png'

# File Paths
DATA_DIR = 'data/'
RAW_DATA_DIR = 'data/raw/'
PROCESSED_DATA_DIR = 'data/processed/'
RESULTS_DIR = 'results/'
VISUALIZATIONS_DIR = 'visualizations/'

# Business Logic
TOP_N_CATEGORIES = 10
TOP_N_STATES = 15
RFM_PERCENTILES = [0.2, 0.4, 0.6, 0.8]

# Report Settings
REPORT_TITLE = "E-Commerce Sales Analysis Report"
REPORT_AUTHOR = "Data Analytics Team"
EXECUTIVE_SUMMARY_LENGTH = 500
"""

with open('config.py', 'w') as f:
    f.write(config_content)

print("✅ Configuration file created: config.py")

print("\\n🎉 PROJECT FILES CREATED SUCCESSFULLY!")
print("=" * 50)
print("📋 Files created:")
print("   ✅ ecommerce_analysis_queries.sql - Comprehensive SQL queries")
print("   ✅ ecommerce_data_analysis.py - Main Python analysis script")
print("   ✅ README.md - Detailed project documentation")
print("   ✅ requirements.txt - Python dependencies")
print("   ✅ setup_database.py - Database initialization")
print("   ✅ data_preprocessing.py - Data cleaning utilities")
print("   ✅ config.py - Project configuration")
print("\\n🚀 READY FOR GITHUB DEPLOYMENT!")