import pandas as pd
import plotly.express as px
from dash import Dash,html, dcc, Input, Output, State, dash_table
import dash
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from accelerate import init_empty_weights
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv(r'X:\openapi.env')

# Access the API key
api_key = os.getenv("OPENAI_API_KEY")


# Load the dataset
dataset_path = r"C:\Users\srb019\Real Estate App\Zillow Data\geocoded_msa_data.csv"
try:
    data = pd.read_csv(dataset_path)
except FileNotFoundError:
    raise FileNotFoundError(f"Dataset not found at {dataset_path}")

# Sort data by RegionID and Date in descending order
data = data.sort_values(['RegionID', 'Date'], ascending=[True, False])

# Select the second most recent data point
second_latest_data = data.groupby('RegionID').nth(1).reset_index()

# Prepare hottest and coldest markets
hottest_markets = second_latest_data.nlargest(10, 'Metro_market_temp_index')
coldest_markets = second_latest_data.nsmallest(10, 'Metro_market_temp_index')
import openai

# Set your OpenAI API key
client = OpenAI(api_key)

def generate_visualization_prompt_openai(query):
    """
    Use OpenAI model to interpret user query and suggest visualization parameters.
    """
    prompt = f"""
    You are a data visualization assistant specializing in real estate market data. Your task is to interpret the user's query and generate valid Python code using the Plotly library to create the requested visualization.

    ### Instructions:
    1. Return only valid Python code. Do not include explanations or comments.
    2. The code should start with `import plotly.express as px` and include `fig = ...` to define the figure object.
    3. Use the provided dataset `data` for generating visualizations.
    4. Ensure all column names are used exactly as provided in the dataset.
    5. The dataset contains monthly data occurring on the last day of each month. Aggregate or filter data appropriately based on the query.
    6. Return the Python code as a single, valid code block.
    7. Include filtering logic to match the query using the correct column names: 
        - Use `RegionName` to filter by metro areas (e.g., "Fayetteville, AR").
        - Use `StateName` to filter by U.S. states (e.g., "AR").
    8. Include a check for whether the filtered dataset is empty and handle it gracefully (e.g., return an empty chart with an appropriate message).
    9. Handle regional queries by grouping states as follows:
        - **Northeast:** ['CT', 'ME', 'MA', 'NH', 'NJ', 'NY', 'PA', 'RI', 'VT']
        - **South:** ['AL', 'AR', 'FL', 'GA', 'KY', 'LA', 'MS', 'NC', 'SC', 'TN', 'VA', 'WV']
        - **Midwest:** ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI']
        - **West:** ['AK', 'AZ', 'CA', 'CO', 'HI', 'ID', 'MT', 'NV', 'NM', 'OR', 'UT', 'WA', 'WY']
    10. Handle aggregation queries:
        - For trends, aggregate data by time (e.g., months or years).
        - Use functions like `pandas.groupby()` to calculate averages, medians, or totals.

    ### Dataset Description:
 The dataset contains the following columns:
    - **StateName**: The name of the U.S. state where the metro area is located.
    - **Metro_market_temp_index**: The market temperature index reflects the balance of supply and demand in a metro area. A higher value indicates a hotter (seller's) market.
    - **Metro_invt_fs**: The total number of active for-sale inventory (e.g., homes listed on the market) in the metro area.
    - **Metro_mean_doz_pending**: The mean number of days homes spend pending (time between offer acceptance and final closing).
    - **Metro_mean_sale_to_list**: The mean ratio of sale price to list price for homes sold in the metro area. A value above 1.0 indicates homes are selling above the list price on average.
    - **Metro_median_sale_price**: The median sale price of homes in the metro area.
    - **Metro_mlp**: The median listing price of homes in the metro area.
    - **Metro_new_con_median_sale_price**: The median sale price for newly constructed homes in the metro area.
    - **Metro_new_con_sales_count_raw**: The raw count of newly constructed homes sold in the metro area.
    - **Metro_new_listings**: The total number of new home listings in the metro area during the specified period.
    - **Metro_pct_sold_above_list**: The percentage of homes sold above the list price.
    - **Metro_perc_listings_price_cut**: The percentage of active listings with price reductions during the specified period.
    - **Metro_sales_count_now**: The total number of homes sold in the metro area during the specified period.
    - **Metro_total_transaction_value**: The total dollar value of all transactions in the metro area during the specified period.
    - **Metro_zhvi**: The Zillow Home Value Index (ZHVI), a measure of typical home values in the metro area.
    - **Metro_zordi**: The Zillow Renter Demand Index (ZORDI), which reflects the level of demand for rental housing in the metro area.
    - **Metro_zori**: The Zillow Observed Rent Index (ZORI), a measure of market-rate rents in the metro area.
    - **Date**: The date of the data.

    Example input: "Show a bar chart of the top 10 hottest markets by Metro_market_temp_index."
    Example output:
    ```python
    import plotly.express as px
    filtered_data = data.nlargest(10, "Metro_market_temp_index")
    fig = px.bar(filtered_data, x="RegionName", y="Metro_market_temp_index", title="Top 10 Hottest Markets")
    ```

    ### User Query:
    {query}

    ### Expected Output:
    Provide only valid Python code to create the visualization.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # Adjust to the correct model
            messages=[
                {"role": "system", "content": "You are a data visualization assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error querying OpenAI API: {e}")
        return f"Error: {e}"

# Initialize dash.Dash app
app = Dash(__name__)

# Define app layout
fig = px.scatter_mapbox(
    second_latest_data,
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
    mapbox_style='carto-positron',
    zoom=4,
    center={"lat": 37.0902, "lon": -95.7129}
)

data_definitions = {
    "StateName": "The name of the U.S. state where the metro area is located.",
    "Metro_market_temp_index": "Reflects the balance of supply and demand in a metro area. A higher value indicates a hotter (seller's) market.",
    "Metro_invt_fs": "The total number of active for-sale inventory in the metro area.",
    "Metro_mean_doz_pending": "The mean number of days homes spend pending (time between offer acceptance and final closing).",
    "Metro_mean_sale_to_list": "The mean ratio of sale price to list price for homes sold in the metro area. A value above 1.0 indicates homes are selling above the list price on average.",
    "Metro_median_sale_price": "The median sale price of homes in the metro area.",
    "Metro_mlp": "The median listing price of homes in the metro area.",
    "Metro_new_con_median_sale_price": "The median sale price for newly constructed homes in the metro area.",
    "Metro_new_con_sales_count_raw": "The raw count of newly constructed homes sold in the metro area.",
    "Metro_new_listings": "The total number of new home listings in the metro area during the specified period.",
    "Metro_pct_sold_above_list": "The percentage of homes sold above the list price.",
    "Metro_perc_listings_price_cut": "The percentage of active listings with price reductions during the specified period.",
    "Metro_sales_count_now": "The total number of homes sold in the metro area during the specified period.",
    "Metro_total_transaction_value": "The total dollar value of all transactions in the metro area during the specified period.",
    "Metro_zhvi": "The Zillow Home Value Index (ZHVI), a measure of typical home values in the metro area.",
    "Metro_zordi": "The Zillow Renter Demand Index (ZORDI), which reflects the level of demand for rental housing in the metro area.",
    "Metro_zori": "The Zillow Observed Rent Index (ZORI), a measure of market-rate rents in the metro area.",
    "Date": "The date of the data."
}
# Create a data dictionary table
data_dictionary_table = html.Table(
    # Create table headers
    [html.Tr([html.Th("Column Name"), html.Th("Description")])] +
    # Populate rows with data definitions
    [
        html.Tr([html.Td(column), html.Td(description)])
        for column, description in data_definitions.items()
    ],
    style={"width": "100%", "border": "1px solid black", "borderCollapse": "collapse"}
)
# Define the layout for the app
app.layout = html.Div([
    html.H1("Metro Metrics Dashboard", style={'textAlign': 'center'}),

    # Tabs for different functionalities
    dcc.Tabs([

        # Tab for Map Visualization
        dcc.Tab(label='Map Visualization', children=[
            html.H2("Map Visualization", style={'textAlign': 'center'}),
            dcc.Graph(figure=fig, id='main-map')
        ]),

        # Tab for Searching Historical Data
        dcc.Tab(label='Search Historical Data', children=[
            html.H2("Search for a Metro's Historical Data", style={'textAlign': 'center'}),
            dcc.Input(
                id='search-input',
                type='text',
                placeholder='Enter a Metro name...',
                style={'width': '50%', 'margin': '10px auto', 'display': 'block'}
            ),
            html.Button(
                'Search',
                id='search-button',
                n_clicks=0,
                style={'margin': '10px'}
            ),
            dash_table.DataTable(
                id='search-results',
                columns=[{'name': col, 'id': col} for col in data.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
                page_size=10
            )
        ]),

        # Tab for Custom Visualization using NLP
        dcc.Tab(label='Ask AI for Custom Visualization', children=[
            html.H2("Ask the AI for a Custom Visualization", style={'textAlign': 'center'}),
            dcc.Textarea(
                id='query-input',
                placeholder="Describe the visualization you'd like to see...",
                style={'width': '100%', 'height': '100px', 'margin-bottom': '10px'}
            ),
            html.Button('Generate Visualization', id='submit-query', n_clicks=0, style={'margin': '10px'}),
            dcc.Graph(id='custom-visualization'),
            html.Div(id='query-response', style={'whiteSpace': 'pre-wrap', 'margin': '20px'})
        ]),

        # Tab for Data Dictionary
        dcc.Tab(label='Data Dictionary', children=[
            html.H2("Data Dictionary", style={'textAlign': 'center'}),
            data_dictionary_table
        ])
    ])
])
# Callbacks Section

import re

@app.callback(
    [Output("custom-visualization", "figure"), Output("query-response", "children")],
    [Input("submit-query", "n_clicks")],
    [State("query-input", "value")]
)
def handle_query(n_clicks, query):
    if not query or n_clicks == 0:
        return px.scatter(), "Enter a query to generate a visualization."

    # Query OpenAI
    ai_response = generate_visualization_prompt_openai(query)

    if not ai_response:
        return px.scatter(), "Error: AI did not return a valid response."

    try:
        # Clean the AI response by removing the "python" keyword and any code fences
        cleaned_response = ai_response.strip()
        if cleaned_response.startswith("```python"):
            cleaned_response = cleaned_response[9:]  # Remove the leading "```python"
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]  # Remove the trailing "```"

        # Debugging: Print the cleaned response
        print(f"Cleaned AI Response:\n{cleaned_response}")

        # Include all necessary variables in the execution environment
        exec_globals = {
            "data": data,  # Full dataset
            "second_latest_data": second_latest_data,  # The processed dataset
            "px": px,  # Plotly Express
            "pd": pd,  # Pandas
            # Add other relevant variables here as needed
        }

        # Execute the cleaned Python code
        exec(cleaned_response, exec_globals)

        # Retrieve the 'fig' object from the executed code
        fig = exec_globals.get("fig", px.scatter())
        if not fig:
            raise ValueError("No figure generated by AI code.")
    except Exception as e:
        # Handle errors in AI-generated code execution
        return px.scatter(), f"Error executing AI-generated code: {str(e)}"

    return fig, f"AI Response:\n{ai_response}"


# Callback for Historical Data Search
@app.callback(
    Output('search-results', 'data'),
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')]
)
def update_search_results(n_clicks, search_value):
    if not search_value or n_clicks == 0:
        return []

    # Filter the data based on the search value
    filtered_data = data[data['RegionName'].str.contains(search_value, case=False, na=False)]
    return filtered_data.sort_values(by='Date', ascending=False).to_dict('records')


# Callback for Map Click-to-Search
@app.callback(
    Output('search-input', 'value'),
    [Input('main-map', 'clickData')]
)
def map_click_to_search(click_data):
    if click_data and 'points' in click_data:
        return click_data['points'][0]['hovertext']
    return ""


# Optional: Add additional interactivity to tabs or other UI components if needed.

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
