"""Configuration settings for the Real Estate Analytics Dashboard."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"  # or your preferred model

# Map Configuration
DEFAULT_MAP_CENTER = {"lat": 37.0902, "lon": -95.7129}
DEFAULT_MAP_ZOOM = 4
MAP_STYLE = "carto-positron"

# Regional Definitions
REGIONS = {
    "Northeast": ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT'],
    "South": ['AL', 'AR', 'FL', 'GA', 'KY', 'LA', 'MS', 'NC', 'SC', 'TN', 'VA', 'WV'],
    "Midwest": ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI'],
    "West": ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WY']
}

# Data Dictionary
METRIC_DEFINITIONS = {
    "StateName": "The name of the U.S. state where the metro area is located.",
    "Metro_market_temp_index": "Reflects the balance of supply and demand in a metro area. A higher value indicates a hotter (seller's) market.",
    "Metro_invt_fs": "The total number of active for-sale inventory in the metro area.",
    "Metro_mean_doz_pending": "The mean number of days homes spend pending.",
    "Metro_mean_sale_to_list": "The mean ratio of sale price to list price.",
    "Metro_median_sale_price": "The median sale price of homes in the metro area.",
    "Metro_mlp": "The median listing price of homes in the metro area.",
    "Metro_new_con_median_sale_price": "The median sale price for newly constructed homes.",
    "Metro_new_con_sales_count_raw": "The raw count of newly constructed homes sold.",
    "Metro_new_listings": "The total number of new home listings.",
    "Metro_pct_sold_above_list": "The percentage of homes sold above list price.",
    "Metro_perc_listings_price_cut": "The percentage of listings with price reductions.",
    "Metro_sales_count_now": "The total number of homes sold.",
    "Metro_total_transaction_value": "The total dollar value of all transactions.",
    "Metro_zhvi": "The Zillow Home Value Index.",
    "Metro_zordi": "The Zillow Renter Demand Index.",
    "Metro_zori": "The Zillow Observed Rent Index.",
    "Date": "The date of the data."
}