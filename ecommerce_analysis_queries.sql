-- =====================================
-- E-COMMERCE SALES ANALYSIS PROJECT
-- SQL Database Setup and Analysis Queries
-- =====================================

-- 1. DATABASE SETUP
-- Create the database and tables structure
CREATE DATABASE IF NOT EXISTS ecommerce_analysis;
USE ecommerce_analysis;

-- Create main tables based on Olist Brazilian E-commerce dataset structure
CREATE TABLE customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_unique_id VARCHAR(50),
    customer_zip_code_prefix INT,
    customer_city VARCHAR(50),
    customer_state VARCHAR(2)
);

CREATE TABLE orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_status VARCHAR(20),
    order_purchase_timestamp DATETIME,
    order_approved_at DATETIME,
    order_delivered_carrier_date DATETIME,
    order_delivered_customer_date DATETIME,
    order_estimated_delivery_date DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_id VARCHAR(50),
    order_item_id INT,
    product_id VARCHAR(50),
    seller_id VARCHAR(50),
    shipping_limit_date DATETIME,
    price DECIMAL(10,2),
    freight_value DECIMAL(10,2),
    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE products (
    product_id VARCHAR(50) PRIMARY KEY,
    product_category_name VARCHAR(50),
    product_name_lenght INT,
    product_description_lenght INT,
    product_photos_qty INT,
    product_weight_g INT,
    product_length_cm INT,
    product_height_cm INT,
    product_width_cm INT
);

CREATE TABLE sellers (
    seller_id VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(50),
    seller_state VARCHAR(2)
);

CREATE TABLE order_payments (
    order_id VARCHAR(50),
    payment_sequential INT,
    payment_type VARCHAR(20),
    payment_installments INT,
    payment_value DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_reviews (
    review_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date DATETIME,
    review_answer_timestamp DATETIME,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- =====================================
-- 2. BUSINESS ANALYSIS QUERIES
-- =====================================

-- QUERY 1: Revenue Analysis by Month
SELECT 
    DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m') as order_month,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT o.customer_id) as unique_customers,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
    AND o.order_purchase_timestamp >= '2017-01-01'
GROUP BY DATE_FORMAT(o.order_purchase_timestamp, '%Y-%m')
ORDER BY order_month;

-- QUERY 2: Top Product Categories by Revenue
SELECT 
    p.product_category_name,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_price,
    SUM(oi.freight_value) as total_shipping,
    SUM(oi.price + oi.freight_value) as total_revenue_with_shipping
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.product_category_name
ORDER BY total_revenue DESC
LIMIT 15;

-- QUERY 3: Geographic Sales Analysis
SELECT 
    c.customer_state,
    COUNT(DISTINCT o.order_id) as total_orders,
    COUNT(DISTINCT c.customer_id) as total_customers,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(oi.price + oi.freight_value) as avg_order_value,
    SUM(oi.price + oi.freight_value) / COUNT(DISTINCT c.customer_id) as revenue_per_customer
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;

-- QUERY 4: Payment Methods Analysis
SELECT 
    op.payment_type,
    COUNT(DISTINCT op.order_id) as total_orders,
    AVG(op.payment_installments) as avg_installments,
    SUM(op.payment_value) as total_payment_value,
    AVG(op.payment_value) as avg_payment_value
FROM order_payments op
JOIN orders o ON op.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY op.payment_type
ORDER BY total_payment_value DESC;

-- QUERY 5: Customer Satisfaction Analysis
SELECT 
    r.review_score,
    COUNT(*) as review_count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM order_reviews) as percentage,
    AVG(oi.price + oi.freight_value) as avg_order_value
FROM order_reviews r
JOIN orders o ON r.order_id = o.order_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.order_status = 'delivered'
GROUP BY r.review_score
ORDER BY r.review_score;

-- QUERY 6: Delivery Performance Analysis
SELECT 
    CASE 
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) <= 0 
        THEN 'On Time/Early'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) BETWEEN 1 AND 7
        THEN 'Late (1-7 days)'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) > 7
        THEN 'Very Late (>7 days)'
    END as delivery_performance,
    COUNT(*) as order_count,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM orders WHERE order_status = 'delivered') as percentage,
    AVG(r.review_score) as avg_review_score
FROM orders o
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered' 
    AND o.order_delivered_customer_date IS NOT NULL 
    AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY 
    CASE 
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) <= 0 
        THEN 'On Time/Early'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) BETWEEN 1 AND 7
        THEN 'Late (1-7 days)'
        WHEN DATEDIFF(o.order_delivered_customer_date, o.order_estimated_delivery_date) > 7
        THEN 'Very Late (>7 days)'
    END;

-- QUERY 7: Seller Performance Analysis
SELECT 
    s.seller_state,
    COUNT(DISTINCT s.seller_id) as total_sellers,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_product_price,
    SUM(oi.price) / COUNT(DISTINCT s.seller_id) as revenue_per_seller
FROM sellers s
JOIN order_items oi ON s.seller_id = oi.seller_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'delivered'
GROUP BY s.seller_state
HAVING COUNT(DISTINCT s.seller_id) >= 10  -- States with at least 10 sellers
ORDER BY total_revenue DESC;

-- QUERY 8: Customer Retention Analysis (RFM-like approach)
WITH customer_metrics AS (
    SELECT 
        c.customer_unique_id,
        COUNT(DISTINCT o.order_id) as frequency,
        SUM(oi.price + oi.freight_value) as monetary_value,
        MAX(o.order_purchase_timestamp) as last_purchase_date,
        DATEDIFF('2018-12-31', MAX(o.order_purchase_timestamp)) as recency_days
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.order_status = 'delivered'
    GROUP BY c.customer_unique_id
)
SELECT 
    CASE 
        WHEN frequency = 1 THEN 'One-time Customer'
        WHEN frequency BETWEEN 2 AND 3 THEN 'Returning Customer'
        WHEN frequency > 3 THEN 'Loyal Customer'
    END as customer_segment,
    COUNT(*) as customer_count,
    AVG(monetary_value) as avg_total_spent,
    AVG(recency_days) as avg_days_since_last_purchase
FROM customer_metrics
GROUP BY 
    CASE 
        WHEN frequency = 1 THEN 'One-time Customer'
        WHEN frequency BETWEEN 2 AND 3 THEN 'Returning Customer'
        WHEN frequency > 3 THEN 'Loyal Customer'
    END
ORDER BY avg_total_spent DESC;

-- QUERY 9: Seasonal Trends Analysis
SELECT 
    QUARTER(o.order_purchase_timestamp) as quarter,
    MONTHNAME(o.order_purchase_timestamp) as month_name,
    COUNT(DISTINCT o.order_id) as total_orders,
    SUM(oi.price + oi.freight_value) as total_revenue,
    AVG(r.review_score) as avg_customer_satisfaction
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
    AND YEAR(o.order_purchase_timestamp) IN (2017, 2018)
GROUP BY QUARTER(o.order_purchase_timestamp), MONTH(o.order_purchase_timestamp), MONTHNAME(o.order_purchase_timestamp)
ORDER BY QUARTER(o.order_purchase_timestamp), MONTH(o.order_purchase_timestamp);

-- QUERY 10: Product Performance Analysis
SELECT 
    p.product_category_name,
    COUNT(DISTINCT oi.product_id) as unique_products,
    COUNT(DISTINCT oi.order_id) as total_orders,
    SUM(oi.price) as total_revenue,
    AVG(oi.price) as avg_price,
    AVG(r.review_score) as avg_rating,
    SUM(oi.price) / COUNT(DISTINCT oi.order_id) as revenue_per_order
FROM products p
JOIN order_items oi ON p.product_id = oi.product_id
JOIN orders o ON oi.order_id = o.order_id
LEFT JOIN order_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
    AND p.product_category_name IS NOT NULL
GROUP BY p.product_category_name
HAVING COUNT(DISTINCT oi.order_id) >= 100  -- Categories with at least 100 orders
ORDER BY total_revenue DESC;
