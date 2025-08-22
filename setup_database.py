#!/usr/bin/env python3
"""
Database Setup Script for E-Commerce Analysis Project
"""

import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_database_schema():
    """Create database schema for e-commerce analysis"""

    conn = sqlite3.connect('ecommerce_analysis.db')
    cursor = conn.cursor()

    # Create tables
    schema_sql = """
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
    """

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    print("✅ Database schema created successfully")

def generate_sample_data():
    """Generate sample data for testing purposes"""

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

    print("\n✅ Database setup complete!")
    print("📊 Ready to run analysis scripts")
