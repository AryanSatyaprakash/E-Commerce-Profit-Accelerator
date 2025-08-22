# =====================================
# E-COMMERCE SALES ANALYSIS PROJECT
# Python Data Analysis & Visualization
# =====================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class EcommerceAnalyzer:
    '''
    A comprehensive e-commerce data analysis class that combines SQL querying
    with Python data analysis and visualization capabilities.
    '''

    def __init__(self, db_path='ecommerce_data.db'):
        '''Initialize the analyzer with database connection'''
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        print(f"Connected to database: {db_path}")

    def load_sample_data(self):
        '''
        Create sample data for demonstration purposes
        In real implementation, you would load actual Olist dataset
        '''
        np.random.seed(42)

        # Generate sample orders data
        n_orders = 10000
        start_date = datetime(2017, 1, 1)
        end_date = datetime(2018, 12, 31)

        # Sample data generation
        order_dates = pd.date_range(start_date, end_date, periods=n_orders)

        orders_data = {
            'order_id': [f'ORD_{i:06d}' for i in range(n_orders)],
            'customer_id': [f'CUST_{np.random.randint(1, 5000):06d}' for _ in range(n_orders)],
            'order_date': np.random.choice(order_dates, n_orders),
            'product_category': np.random.choice([
                'Electronics', 'Home & Garden', 'Fashion', 'Sports & Leisure',
                'Health & Beauty', 'Auto', 'Books', 'Toys', 'Food & Beverages'
            ], n_orders, p=[0.15, 0.12, 0.18, 0.08, 0.10, 0.07, 0.05, 0.08, 0.17]),
            'price': np.random.lognormal(3.5, 0.8, n_orders).round(2),
            'quantity': np.random.choice([1, 2, 3, 4], n_orders, p=[0.7, 0.2, 0.08, 0.02]),
            'customer_state': np.random.choice([
                'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'DF', 'GO', 'PE'
            ], n_orders, p=[0.4, 0.15, 0.12, 0.08, 0.07, 0.05, 0.04, 0.03, 0.03, 0.03]),
            'payment_type': np.random.choice([
                'credit_card', 'boleto', 'debit_card', 'voucher'
            ], n_orders, p=[0.75, 0.15, 0.08, 0.02]),
            'review_score': np.random.choice([1, 2, 3, 4, 5], n_orders, p=[0.05, 0.05, 0.15, 0.25, 0.5])
        }

        self.df = pd.DataFrame(orders_data)
        self.df['total_amount'] = self.df['price'] * self.df['quantity']
        self.df['order_date'] = pd.to_datetime(self.df['order_date'])

        # Save to database
        self.df.to_sql('orders_analysis', self.conn, if_exists='replace', index=False)

        print(f"✅ Sample dataset created with {len(self.df):,} orders")
        print(f"📊 Dataset shape: {self.df.shape}")
        return self.df

    def revenue_trend_analysis(self):
        '''Analyze revenue trends over time'''
        print("\n📈 REVENUE TREND ANALYSIS")
        print("=" * 50)

        # Monthly revenue analysis
        monthly_revenue = self.df.groupby(self.df['order_date'].dt.to_period('M')).agg({
            'total_amount': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique'
        }).reset_index()

        monthly_revenue.columns = ['Month', 'Total_Revenue', 'Total_Orders', 'Unique_Customers']
        monthly_revenue['Avg_Order_Value'] = monthly_revenue['Total_Revenue'] / monthly_revenue['Total_Orders']

        # Display summary
        print(f"📊 Total Revenue: ${monthly_revenue['Total_Revenue'].sum():,.2f}")
        print(f"📦 Total Orders: {monthly_revenue['Total_Orders'].sum():,}")
        print(f"👥 Unique Customers: {self.df['customer_id'].nunique():,}")
        print(f"💰 Average Order Value: ${monthly_revenue['Avg_Order_Value'].mean():.2f}")

        # Create visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('E-Commerce Business Performance Dashboard', fontsize=16, fontweight='bold')

        # Monthly revenue trend
        ax1.plot(monthly_revenue.index, monthly_revenue['Total_Revenue'], marker='o', linewidth=2)
        ax1.set_title('Monthly Revenue Trend')
        ax1.set_ylabel('Revenue ($)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # Monthly order count
        ax2.bar(monthly_revenue.index, monthly_revenue['Total_Orders'], alpha=0.7)
        ax2.set_title('Monthly Order Count')
        ax2.set_ylabel('Number of Orders')
        ax2.grid(True, alpha=0.3)

        # Average order value trend
        ax3.plot(monthly_revenue.index, monthly_revenue['Avg_Order_Value'], 
                marker='s', color='green', linewidth=2)
        ax3.set_title('Average Order Value Trend')
        ax3.set_ylabel('AOV ($)')
        ax3.grid(True, alpha=0.3)

        # Customer acquisition trend
        ax4.plot(monthly_revenue.index, monthly_revenue['Unique_Customers'], 
                marker='^', color='orange', linewidth=2)
        ax4.set_title('Monthly Unique Customers')
        ax4.set_ylabel('Unique Customers')
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('revenue_trend_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return monthly_revenue

    def product_category_analysis(self):
        '''Analyze performance by product category'''
        print("\n🛍️ PRODUCT CATEGORY ANALYSIS")
        print("=" * 50)

        category_stats = self.df.groupby('product_category').agg({
            'total_amount': ['sum', 'mean'],
            'order_id': 'count',
            'review_score': 'mean',
            'quantity': 'sum'
        }).round(2)

        category_stats.columns = ['Total_Revenue', 'Avg_Order_Value', 'Order_Count', 
                                'Avg_Rating', 'Total_Quantity']
        category_stats = category_stats.sort_values('Total_Revenue', ascending=False)

        print("\n🏆 Top Product Categories by Revenue:")
        print(category_stats.head(10).to_string())

        # Visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Product Category Performance Analysis', fontsize=16, fontweight='bold')

        # Top categories by revenue
        top_categories = category_stats.head(8)
        ax1.barh(top_categories.index, top_categories['Total_Revenue'])
        ax1.set_title('Top Categories by Revenue')
        ax1.set_xlabel('Total Revenue ($)')

        # Average order value by category
        ax2.bar(top_categories.index, top_categories['Avg_Order_Value'], alpha=0.7)
        ax2.set_title('Average Order Value by Category')
        ax2.set_ylabel('AOV ($)')
        ax2.tick_params(axis='x', rotation=45)

        # Customer satisfaction by category
        ax3.bar(top_categories.index, top_categories['Avg_Rating'], 
                color='green', alpha=0.7)
        ax3.set_title('Average Rating by Category')
        ax3.set_ylabel('Average Rating (1-5)')
        ax3.set_ylim(0, 5)
        ax3.tick_params(axis='x', rotation=45)

        # Order volume by category
        ax4.pie(top_categories['Order_Count'], labels=top_categories.index, autopct='%1.1f%%')
        ax4.set_title('Order Distribution by Category')

        plt.tight_layout()
        plt.savefig('category_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return category_stats

    def geographic_analysis(self):
        '''Analyze performance by geographic region'''
        print("\n🗺️ GEOGRAPHIC ANALYSIS")
        print("=" * 50)

        geo_stats = self.df.groupby('customer_state').agg({
            'total_amount': ['sum', 'mean'],
            'order_id': 'count',
            'customer_id': 'nunique',
            'review_score': 'mean'
        }).round(2)

        geo_stats.columns = ['Total_Revenue', 'AOV', 'Total_Orders', 
                           'Unique_Customers', 'Avg_Rating']
        geo_stats['Revenue_per_Customer'] = (geo_stats['Total_Revenue'] / 
                                           geo_stats['Unique_Customers']).round(2)
        geo_stats = geo_stats.sort_values('Total_Revenue', ascending=False)

        print("\n🌟 Top States by Revenue:")
        print(geo_stats.head(10).to_string())

        # Visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Geographic Performance Analysis', fontsize=16, fontweight='bold')

        top_states = geo_stats.head(10)

        # Revenue by state
        ax1.bar(top_states.index, top_states['Total_Revenue'])
        ax1.set_title('Revenue by State')
        ax1.set_ylabel('Total Revenue ($)')
        ax1.tick_params(axis='x', rotation=45)

        # Customer distribution
        ax2.pie(top_states['Unique_Customers'], labels=top_states.index, autopct='%1.1f%%')
        ax2.set_title('Customer Distribution by State')

        # Revenue per customer
        ax3.bar(top_states.index, top_states['Revenue_per_Customer'], color='green')
        ax3.set_title('Revenue per Customer by State')
        ax3.set_ylabel('Revenue per Customer ($)')
        ax3.tick_params(axis='x', rotation=45)

        # Average rating by state
        ax4.bar(top_states.index, top_states['Avg_Rating'], color='orange', alpha=0.7)
        ax4.set_title('Average Rating by State')
        ax4.set_ylabel('Average Rating (1-5)')
        ax4.set_ylim(0, 5)
        ax4.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('geographic_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return geo_stats

    def customer_segmentation_analysis(self):
        '''Perform RFM-like customer segmentation'''
        print("\n👥 CUSTOMER SEGMENTATION ANALYSIS")
        print("=" * 50)

        # Calculate RFM metrics
        current_date = self.df['order_date'].max()

        rfm = self.df.groupby('customer_id').agg({
            'order_date': lambda x: (current_date - x.max()).days,  # Recency
            'order_id': 'count',  # Frequency
            'total_amount': 'sum'  # Monetary
        }).reset_index()

        rfm.columns = ['customer_id', 'Recency', 'Frequency', 'Monetary']

        # Create RFM segments
        def assign_rfm_segment(row):
            if row['Frequency'] >= 3 and row['Monetary'] >= 200:
                return 'High Value'
            elif row['Frequency'] >= 2 and row['Monetary'] >= 100:
                return 'Medium Value'
            elif row['Recency'] <= 90:
                return 'Recent Customer'
            else:
                return 'Low Value'

        rfm['Segment'] = rfm.apply(assign_rfm_segment, axis=1)

        segment_stats = rfm.groupby('Segment').agg({
            'customer_id': 'count',
            'Recency': 'mean',
            'Frequency': 'mean',
            'Monetary': ['mean', 'sum']
        }).round(2)

        print("\n📊 Customer Segment Analysis:")
        print(segment_stats.to_string())

        # Visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Customer Segmentation Analysis', fontsize=16, fontweight='bold')

        segment_summary = rfm.groupby('Segment').agg({
            'customer_id': 'count',
            'Monetary': 'sum'
        }).reset_index()

        # Customer distribution by segment
        ax1.pie(segment_summary['customer_id'], labels=segment_summary['Segment'], 
                autopct='%1.1f%%')
        ax1.set_title('Customer Distribution by Segment')

        # Revenue by segment
        ax2.bar(segment_summary['Segment'], segment_summary['Monetary'])
        ax2.set_title('Total Revenue by Segment')
        ax2.set_ylabel('Total Revenue ($)')
        ax2.tick_params(axis='x', rotation=45)

        # RFM scatter plot
        scatter = ax3.scatter(rfm['Frequency'], rfm['Monetary'], 
                            c=rfm['Recency'], cmap='viridis', alpha=0.6)
        ax3.set_xlabel('Frequency')
        ax3.set_ylabel('Monetary ($)')
        ax3.set_title('Customer RFM Analysis')
        plt.colorbar(scatter, ax=ax3, label='Recency (days)')

        # Average metrics by segment
        avg_metrics = rfm.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
        x_pos = range(len(avg_metrics.index))
        width = 0.25

        ax4.bar([x - width for x in x_pos], avg_metrics['Frequency'], 
               width, label='Frequency', alpha=0.7)
        ax4.bar(x_pos, avg_metrics['Monetary']/100, 
               width, label='Monetary/100', alpha=0.7)
        ax4.bar([x + width for x in x_pos], avg_metrics['Recency']/10, 
               width, label='Recency/10', alpha=0.7)

        ax4.set_xlabel('Segment')
        ax4.set_ylabel('Normalized Values')
        ax4.set_title('Average RFM Metrics by Segment')
        ax4.set_xticks(x_pos)
        ax4.set_xticklabels(avg_metrics.index, rotation=45)
        ax4.legend()

        plt.tight_layout()
        plt.savefig('customer_segmentation.png', dpi=300, bbox_inches='tight')
        plt.show()

        return rfm, segment_stats

    def payment_analysis(self):
        '''Analyze payment methods and patterns'''
        print("\n💳 PAYMENT ANALYSIS")
        print("=" * 50)

        payment_stats = self.df.groupby('payment_type').agg({
            'total_amount': ['sum', 'mean', 'count'],
            'review_score': 'mean'
        }).round(2)

        payment_stats.columns = ['Total_Revenue', 'AOV', 'Order_Count', 'Avg_Rating']
        payment_stats['Market_Share'] = (payment_stats['Order_Count'] / 
                                       payment_stats['Order_Count'].sum() * 100).round(1)

        print("\n💰 Payment Method Performance:")
        print(payment_stats.to_string())

        # Visualization
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Payment Method Analysis', fontsize=16, fontweight='bold')

        # Market share
        ax1.pie(payment_stats['Market_Share'], labels=payment_stats.index, 
                autopct='%1.1f%%')
        ax1.set_title('Payment Method Market Share')

        # Revenue by payment type
        ax2.bar(payment_stats.index, payment_stats['Total_Revenue'])
        ax2.set_title('Revenue by Payment Method')
        ax2.set_ylabel('Total Revenue ($)')
        ax2.tick_params(axis='x', rotation=45)

        # AOV by payment type
        ax3.bar(payment_stats.index, payment_stats['AOV'], color='green', alpha=0.7)
        ax3.set_title('Average Order Value by Payment Method')
        ax3.set_ylabel('AOV ($)')
        ax3.tick_params(axis='x', rotation=45)

        # Rating by payment type
        ax4.bar(payment_stats.index, payment_stats['Avg_Rating'], 
                color='orange', alpha=0.7)
        ax4.set_title('Customer Satisfaction by Payment Method')
        ax4.set_ylabel('Average Rating (1-5)')
        ax4.set_ylim(0, 5)
        ax4.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.savefig('payment_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()

        return payment_stats

    def generate_business_insights(self):
        '''Generate comprehensive business insights and recommendations'''
        print("\n🎯 BUSINESS INSIGHTS & RECOMMENDATIONS")
        print("=" * 60)

        insights = []

        # Revenue insights
        total_revenue = self.df['total_amount'].sum()
        avg_order_value = self.df['total_amount'].mean()
        total_orders = len(self.df)
        unique_customers = self.df['customer_id'].nunique()

        insights.append(f"📊 Business Performance Summary:")
        insights.append(f"   • Total Revenue: ${total_revenue:,.2f}")
        insights.append(f"   • Average Order Value: ${avg_order_value:.2f}")
        insights.append(f"   • Total Orders: {total_orders:,}")
        insights.append(f"   • Unique Customers: {unique_customers:,}")
        insights.append(f"   • Customer Lifetime Value: ${total_revenue/unique_customers:.2f}")

        # Top category insight
        top_category = self.df.groupby('product_category')['total_amount'].sum().idxmax()
        top_category_revenue = self.df.groupby('product_category')['total_amount'].sum().max()

        insights.append(f"\n🏆 Product Insights:")
        insights.append(f"   • Top Category: {top_category} (${top_category_revenue:,.2f})")
        insights.append(f"   • Category contributes {top_category_revenue/total_revenue*100:.1f}% of total revenue")

        # Geographic insights
        top_state = self.df.groupby('customer_state')['total_amount'].sum().idxmax()
        top_state_revenue = self.df.groupby('customer_state')['total_amount'].sum().max()

        insights.append(f"\n🗺️ Geographic Insights:")
        insights.append(f"   • Top State: {top_state} (${top_state_revenue:,.2f})")
        insights.append(f"   • State contributes {top_state_revenue/total_revenue*100:.1f}% of total revenue")

        # Customer satisfaction
        avg_rating = self.df['review_score'].mean()
        high_rating_orders = len(self.df[self.df['review_score'] >= 4])

        insights.append(f"\n😊 Customer Satisfaction:")
        insights.append(f"   • Average Rating: {avg_rating:.2f}/5.0")
        insights.append(f"   • High Satisfaction Rate: {high_rating_orders/total_orders*100:.1f}%")

        # Recommendations
        insights.append(f"\n💡 Strategic Recommendations:")
        insights.append(f"   1. Focus marketing spend on {top_category} category")
        insights.append(f"   2. Expand operations in {top_state} and similar high-performing states")
        insights.append(f"   3. Investigate low-performing categories for improvement opportunities")
        insights.append(f"   4. Implement customer retention programs for high-value segments")
        insights.append(f"   5. Optimize inventory based on geographic and seasonal patterns")

        for insight in insights:
            print(insight)

        return insights

    def export_results_to_csv(self):
        '''Export all analysis results to CSV files'''
        print("\n📁 EXPORTING RESULTS")
        print("=" * 50)

        # Monthly revenue
        monthly_revenue = self.df.groupby(self.df['order_date'].dt.to_period('M')).agg({
            'total_amount': 'sum',
            'order_id': 'count',
            'customer_id': 'nunique'
        })
        monthly_revenue.to_csv('monthly_revenue_analysis.csv')

        # Category performance
        category_stats = self.df.groupby('product_category').agg({
            'total_amount': ['sum', 'mean'],
            'order_id': 'count',
            'review_score': 'mean'
        })
        category_stats.to_csv('category_performance.csv')

        # Geographic analysis
        geo_stats = self.df.groupby('customer_state').agg({
            'total_amount': ['sum', 'mean'],
            'order_id': 'count',
            'customer_id': 'nunique'
        })
        geo_stats.to_csv('geographic_analysis.csv')

        # Customer data
        customer_summary = self.df.groupby('customer_id').agg({
            'total_amount': 'sum',
            'order_id': 'count',
            'order_date': 'max'
        })
        customer_summary.to_csv('customer_summary.csv')

        print("✅ Results exported to CSV files:")
        print("   • monthly_revenue_analysis.csv")
        print("   • category_performance.csv")
        print("   • geographic_analysis.csv")
        print("   • customer_summary.csv")

    def close_connection(self):
        '''Close database connection'''
        self.conn.close()
        print("\n🔐 Database connection closed")

# =====================================
# MAIN EXECUTION SCRIPT
# =====================================

if __name__ == "__main__":
    print("🚀 E-COMMERCE SALES ANALYSIS PROJECT")
    print("=" * 60)
    print("📊 Comprehensive Business Intelligence Dashboard")
    print("🔧 Technologies: Python, SQL, Pandas, Matplotlib, Seaborn")
    print("=" * 60)

    # Initialize analyzer
    analyzer = EcommerceAnalyzer()

    # Load sample data (replace with real data loading in production)
    df = analyzer.load_sample_data()

    # Perform comprehensive analysis
    print("\n🔄 Starting comprehensive analysis...")

    # 1. Revenue trend analysis
    monthly_revenue = analyzer.revenue_trend_analysis()

    # 2. Product category analysis
    category_performance = analyzer.product_category_analysis()

    # 3. Geographic analysis
    geographic_performance = analyzer.geographic_analysis()

    # 4. Customer segmentation
    rfm_data, segment_stats = analyzer.customer_segmentation_analysis()

    # 5. Payment analysis
    payment_performance = analyzer.payment_analysis()

    # 6. Generate business insights
    business_insights = analyzer.generate_business_insights()

    # 7. Export results
    analyzer.export_results_to_csv()

    # Close connection
    analyzer.close_connection()

    print("\n✅ ANALYSIS COMPLETE!")
    print("🎯 Check generated visualizations and CSV files for detailed insights")
    print("📊 Ready for presentation to stakeholders!")
