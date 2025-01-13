"""Visualization utilities for the dashboard."""

import ast
import plotly.express as px
from openai import OpenAI
import plotly.graph_objects as go
from typing import Optional, Tuple, Union
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from prophet import Prophet 
import pandas as pd
import matplotlib
matplotlib.use("Agg")
from src.config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MAP_STYLE,
    DEFAULT_MAP_CENTER,
    DEFAULT_MAP_ZOOM,
)

client = OpenAI(api_key=OPENAI_API_KEY)


def create_map_visualization(
    data: pd.DataFrame,
) -> Union[px.scatter_mapbox, px.scatter]:
    """Create the main map visualization."""
    return px.scatter_mapbox(
        data,
        lat="latitude",
        lon="longitude",
        hover_name="RegionName",
        hover_data={
            "StateName": True,
            "Metro_market_temp_index": ":.2f",
            "Metro_invt_fs": ":.2f",
            "Metro_mean_doz_pending": ":.2f",
            "Metro_mean_sale_to_list": ":.2f",
            "Metro_median_sale_price": ":.2f",
            "Metro_mlp": ":.2f",
            "Metro_new_con_median_sale_price": ":.2f",
            "Metro_new_con_sales_count_raw": ":.0f",
            "Metro_new_listings": ":.0f",
            "Metro_pct_sold_above_list": ":.2f",
            "Metro_perc_listings_price_cut": ":.2f",
            "Metro_sales_count_now": ":.0f",
            "Metro_total_transaction_value": ":.2f",
            "Metro_zhvi": ":.2f",
            "Metro_zordi": ":.2f",
            "Metro_zori": ":.2f",
        },
        color="Metro_market_temp_index",
        color_continuous_scale="Viridis",
        title="Interactive Map of Metro Metrics",
        mapbox_style=MAP_STYLE,
        zoom=DEFAULT_MAP_ZOOM,
        center=DEFAULT_MAP_CENTER,
    )


def _get_data_context() -> str:
    """Generate the common data context for both agents."""
    return """
    Dataset Structure and Column Names:
    1. Location Identifiers:
        - RegionName: Metro area name (use for city filtering)
        - RegionID: Unique identifier
        - StateName: State location
        - latitude: Geographic coordinate
        - longitude: Geographic coordinate

    2. Price Metrics (in USD):
        - Metro_median_sale_price: Median home sale price
        - Metro_mlp: Median listing price
        - Metro_new_con_median_sale_price: New construction median sale price
        - Metro_total_transaction_value: Total value of transactions

    3. Market Activity Metrics:
        - Metro_market_temp_index: Market temperature (supply/demand balance)
        - Metro_invt_fs: Active for-sale inventory count
        - Metro_mean_doz_pending: Average days homes spend pending
        - Metro_mean_sale_to_list: Sale to list price ratio
        - Metro_new_listings: Count of new listings
        - Metro_new_con_sales_count_raw: New construction sales count
        - Metro_sales_count_now: Total homes sold

    4. Market Performance Indicators:
        - Metro_pct_sold_above_list: Percentage sold above list price
        - Metro_perc_listings_price_cut: Percentage of listings with price cuts
        - Metro_zhvi: Zillow Home Value Index
        - Metro_zordi: Zillow Renter Demand Index
        - Metro_zori: Zillow Observed Rent Index

    5. Time Information:
        - Date: Time period of data (YYYY-MM-DD format)

    Data Characteristics:
        - Monthly frequency
        - Monetary values in USD
        - Percentages in decimal form (0.15 = 15%)
        - Some metrics may have missing values
    """


def _generate_visualization_prompt(query: str) -> str:
    """Generate the prompt for the code generation agent."""
    return f"""
    You are a data visualization expert with creative freedom to make beautiful, informative visualizations.
    Your goal is to tell the best possible data story while maintaining precise Python syntax. NO comments, NO explanations, NO fig.show(), and NO additional text of any kind.
    
    NEVER use the latest date for analysis. Always use the second latest date. 

    AVAILABLE PACKAGES: pandas (pd), plotly.express (px), plotly.graph_objects (go), scikit-learn (sklearn), and zprophet.

    DATA COLUMN NAMES (Use Exactly):
    1. For Metro Areas:
       - Use 'RegionName' (not 'Market' or 'City')
       - Example: data['RegionName']
       - when looking up a city or region use wildcard search. For example: data[data['RegionName'].str.contains('City', case=False)]
       - if two cities have the same name, use the region name to differentiate them. For exampmple: Query contains Fayeteville. See if the query contains the state name as well to differentiate between the two cities.
    
    2. For Metrics:
       - 'Metro_market_temp_index' for market temperature
       - 'Metro_median_sale_price' for prices
       - 'Metro_invt_fs' for inventory
       - 'Metro_mean_doz_pending' for days pending
       
    3. Time Data:
       - Use 'Date' for time series
       - Example: data.sort_values('Date')
       -REQUIRED CODE STRUCTURE:
        -ALWAYS start with date conversion:
        - data['Date'] = pd.to_datetime(data['Date'])
       
    4. For State Level:
       - Use 'StateName' for state filtering
       
    5. Common Operations:
       - Grouping: data.groupby('RegionName')
       - Filtering: data[data['RegionName'].str.contains('City')]
       - Time series: sort_values('Date')
       - Top N: nlargest(10, 'Metro_market_temp_index')

    Remember: ALWAYS use these exact column names - the code will fail if using 'Market', 'City', or other variations.

    The dataset is already loaded into a DataFrame called `data`.

    If no date is specified, assume the latest date that has data available.

    only use these packages: pandas, plotly.express (as px), and plotly.graph_objects (as go), sklearn (as )
    
    IMPORTANT PROPHET GUIDELINES:
    When using Prophet for forecasting:
    1. NEVER use model.plot() - it creates matplotlib figures which are not compatible
    2. Instead, create Plotly figures from Prophet predictions like this. Remember to disregard latest dates from all sklearn and prophet models, the latest date should be the second latest date.
    3. ensure that all data that is necessary is present before running the model.
    4. Ensure that the data is sorted by date before running the model but remember the latest date should be the second latest date.

    ALWAYS verify the data that will be used for the analysis. Here are few ideas for doing so: 
    - Checking the first few rows: data.head()
    - Checking the data types: data.info()
    - Checking for missing values: data.isnull().sum()
      # Get unique dates and verify
        available_dates = sorted(data['Date'].unique())
        print(f"Available dates: available_dates[-5:]")  
    
    DATA VALIDATION RULES (Required) (*code* is placeholder for actual code):
    1. Always check if filtered data exists:
        city_data = data[data['RegionName'] == 'Boston']
        if len(city_data) == 0:
            raise ValueError(f"No data found for selected city")
    
    2. For finding max values and dates:
        if len(city_data) > 0:
            max_price = city_data['Metro_median_sale_price'].max()
            max_price_date = city_data.loc[city_data['Metro_median_sale_price'] == max_price, 'Date'].iloc[0]
    
    3. Print data checks (for debugging):
        print(f"Total records: *code*")
        print(f"Filtered records: *code*")
        print(f"Available cities: *code*)
    
    4. Safe data access example:
        city_data = data[data['RegionName'].str.contains('Boston', case=False)]
        if len(city_data) > 0:
            # proceed with visualization
        else:
            fig = go.Figure()
            fig.add_annotation(text="No data available", xref="paper", yref="paper", x=0.5, y=0.5)")
        print(f"Available cities: *code*")


    If it is cross-sectional, be sure there are no duplicate RegionName's. 

    If using percent changes or growth rates, ensure that the data is sorted by date. But the latest date can only be the second latest date.
    
    If it is time series, be sure that there are no duplicate RegionName's for the same date.

    When I say constructing the most homes, use Metro_new_con_sales_count_raw

    CREATIVE OPTIONS (All Available):
    1. Visual Elements:
        - Any figure dimensions
        - Custom color schemes
        - Multiple traces/lines
        - Statistical overlays (moving averages, trends)
        - Annotations and reference lines
        - Subplots and secondary axes
        - Customized hover information
        - Interactive range selectors
    
    2. Data Analysis:
        - Rolling averages
        - Growth rates
        - Seasonality
        - Year-over-year comparisons
        - Price acceleration
        - Market cycle indicators
        - Correlations and regressions
        - Outlier detection and analysis

    3. Geographic Visualization:
        - Choropleth maps
        - Bubble maps
        - Heatmaps
        - Custom map markers
        - Mapbox customization
        - Geographic overlays

    4. Chart Types:
        - Line charts
        - Bar charts
        - Scatter plots
        - Area charts
        - Histograms
        - Box plots
        - Pie charts
        - Radar charts
        - Sankey diagrams

    5. Advanced Techniques:
        - Dimensionality reduction
        - Clustering and segmentation
        - Time series decomposition
        - Forecasting and prediction
        - Machine learning integration
        - Custom visual encoding
        - Storytelling and narrative flow
    
    Syntax Reminder:
    - Use 'px' as the Plotly Express alias
    - Use 'data' as the DataFrame name
    - Use 'fig' as the final figure object
    - Do NOT include 'fig.show()' - the figure will be displayed automatically
    - Ensure all code is self-contained and error-free

    Remember: The goal is to create a visually appealing and informative data visualization.
    Now create the most insightful visualization for this query: {query}
    Be creative while maintaining exact syntax. The visualization should reveal key insights about the data. ONLY return valid, executable Python code.
    """

def _verify_and_execute_code(code: str, data: pd.DataFrame, second_latest_data: pd.DataFrame) -> Tuple[Optional[go.Figure], str]:
    """Verify and execute the visualization code."""
    try:
        # Convert triple backticks if present
        if "```python" in code:
            code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code:
            code = code.split("```")[1].strip()
            
        # Remove any import statements from the code
        cleaned_code = '\n'.join(line for line in code.split('\n') 
                               if not line.strip().startswith('import') 
                               and not line.strip().startswith('from'))
        
        # Create the globals dict with required imports
        globals_dict = {
            "pd": pd,
            "px": px,
            "go": go,
            "Prophet": Prophet,
            "LinearRegression": LinearRegression,
            "train_test_split": train_test_split,
            "mean_squared_error": mean_squared_error,
            "sklearn": __import__('sklearn'),
            "make_pipeline": __import__('sklearn.pipeline').pipeline.make_pipeline,
            "PolynomialFeatures": __import__('sklearn.preprocessing').preprocessing.PolynomialFeatures,
            "np": __import__('numpy'),
            "data": data,  # Make data available in global scope
            "second_latest_data": second_latest_data
        }
        
        # Execute in a clean locals dict
        locals_dict = {}
        exec(cleaned_code, globals_dict, locals_dict)
        
        if "fig" not in locals_dict:
            raise ValueError("Code did not generate a figure. Make sure your code creates a 'fig' variable.")
            
        return locals_dict["fig"], None
        
    except Exception as e:
        return None, f"Error executing code: {str(e)}"

def generate_custom_visualization(
    query: str, data: pd.DataFrame, second_latest_data: pd.DataFrame
) -> Tuple[Optional[Union[px.scatter_mapbox, px.scatter]], str, str]:
    """Generate visualization using OpenAI's code generation and explanation."""
    try:
        # Get code from OpenAI
        code_response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a data visualization expert."},
                {"role": "user", "content": _generate_visualization_prompt(query)}
            ],
            temperature=0.1
        )
        
        # Get the generated code
        code = code_response.choices[0].message.content.strip()
        
        # Execute the code
        fig, error = _verify_and_execute_code(code, data, second_latest_data)
        if error:
            return None, code, f"Error: {error}"
            
        # Get explanation
        explanation_response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a real estate market analyst."},
                {"role": "user", "content": _generate_explanation_prompt(
                    query, code, data.head().to_string()
                )}
            ],
            temperature=0.7
        )
        
        return fig, code, explanation_response.choices[0].message.content.strip()
        
    except Exception as e:
        error_msg = str(e)
        print(f"\nError in visualization generation: {error_msg}")
        return None, code if 'code' in locals() else "", f"Error: {error_msg}"

def _generate_explanation_prompt(query: str, code: str, data_preview: str) -> str:
    """Generate the prompt for the explanation agent."""
    return f"""
    You are a real estate market analyst. Explain this visualization in business terms.

    {_get_data_context()}

    Original Query: {query}

    Refined Visualization Code:
    {code}

    Data Preview:
    {data_preview}

    Provide an explanation that includes:
    1. What the visualization shows (metrics, timeframe, geographic scope)
    2. Key insights and patterns in the data
    3. Business implications for real estate professionals
    4. Notable outliers or trends
    5. Relevant market context

    Focus on insights that would be valuable for:
    - Real estate investors
    - Market analysts
    - Property buyers and sellers
    - Real estate agents

    Remember: The goal is to provide a clear and insightful interpretation of the visualization and extrapaolte the data trends to real-world implications.
    """
