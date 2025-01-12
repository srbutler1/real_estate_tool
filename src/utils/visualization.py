"""Visualization utilities for the dashboard."""

import plotly.express as px
from openai import OpenAI
from typing import Optional, Tuple, Union
import pandas as pd
from src.config import (
    OPENAI_API_KEY, 
    OPENAI_MODEL, 
    MAP_STYLE, 
    DEFAULT_MAP_CENTER, 
    DEFAULT_MAP_ZOOM
)

client = OpenAI(api_key=OPENAI_API_KEY)

def create_map_visualization(data: pd.DataFrame) -> Union[px.scatter_mapbox, px.scatter]:
    """Create the main map visualization."""
    return px.scatter_mapbox(
        data,
        lat='latitude',
        lon='longitude',
        hover_name='RegionName',
        hover_data={
            'StateName': True,
            'Metro_market_temp_index': ':.2f',
            'Metro_invt_fs': ':.2f',
            'Metro_mean_doz_pending': ':.2f',
            'Metro_mean_sale_to_list': ':.2f',
            'Metro_median_sale_price': ':.2f',
            'Metro_mlp': ':.2f',
            'Metro_new_con_median_sale_price': ':.2f',
            'Metro_new_con_sales_count_raw': ':.0f',
            'Metro_new_listings': ':.0f',
            'Metro_pct_sold_above_list': ':.2f',
            'Metro_perc_listings_price_cut': ':.2f',
            'Metro_sales_count_now': ':.0f',
            'Metro_total_transaction_value': ':.2f',
            'Metro_zhvi': ':.2f',
            'Metro_zordi': ':.2f',
            'Metro_zori': ':.2f'
        },
        color='Metro_market_temp_index',
        color_continuous_scale='Viridis',
        title='Interactive Map of Metro Metrics',
        mapbox_style=MAP_STYLE,
        zoom=DEFAULT_MAP_ZOOM,
        center=DEFAULT_MAP_CENTER
    )

def generate_custom_visualization(
    query: str,
    data: pd.DataFrame,
    second_latest_data: pd.DataFrame
) -> Tuple[Optional[Union[px.scatter_mapbox, px.scatter]], str]:
    """Generate a custom visualization based on natural language query."""
    try:
        # Get visualization code from OpenAI
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a data visualization assistant."},
                {"role": "user", "content": _generate_visualization_prompt(query)}
            ]
        )
        
        code = response.choices[0].message.content.strip()
        
        # Clean the code
        code = _clean_code(code)
        
        # Execute the code
        local_vars = {'px': px, 'pd': pd, 'data': data, 'second_latest_data': second_latest_data}
        exec(code, {}, local_vars)
        
        return local_vars.get('fig'), code
    
    except Exception as e:
        return None, f"Error: {str(e)}"

def _clean_code(code: str) -> str:
    """Clean the AI-generated code."""
    code = code.strip()
    if code.startswith("```python"):
        code = code[8:]
    if code.endswith("```"):
        code = code[:-3]
    return code.strip()

def _generate_visualization_prompt(query: str) -> str:
    """Generate the prompt for the visualization request."""
    return f"""
    Create a visualization using Plotly Express for the following query: {query}
    
    Return only valid Python code that creates a figure named 'fig'.
    The code should import plotly.express as px and use the provided dataset.
    """