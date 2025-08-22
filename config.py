# E-Commerce Sales Analysis Project Configuration

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
