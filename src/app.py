"""Main application file for the Real Estate Analytics Dashboard."""

import pandas as pd
from dash import Dash, Input, Output, State
import plotly.express as px

from .data.data_loader import DataLoader
from .layouts.dashboard import create_dashboard_layout
from .utils.visualization import generate_custom_visualization

# Initialize the Dash app
app = Dash(__name__)

# Initialize data loader and load data
data_loader = DataLoader("path/to/your/geocoded_msa_data.csv")  # Update with your data path
data = data_loader.load_data()

# Set up the app layout
app.layout = create_dashboard_layout(data_loader.second_latest_data)

# Callback for Search functionality
@app.callback(
    Output('search-results', 'data'),
    Output('search-results', 'columns'),
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')]
)
def update_search_results(n_clicks, search_value):
    if not search_value or n_clicks == 0:
        return [], []
    
    # Filter the data based on the search value
    filtered_data = data_loader.search_metro(search_value)
    
    # Prepare columns configuration
    columns = [{"name": col, "id": col} for col in filtered_data.columns]
    
    return filtered_data.to_dict('records'), columns

# Callback for Map Click-to-Search
@app.callback(
    Output('search-input', 'value'),
    [Input('main-map', 'clickData')]
)
def map_click_to_search(click_data):
    if click_data and 'points' in click_data:
        return click_data['points'][0]['hovertext']
    return ""

# Callback for NLP Visualization
@app.callback(
    [Output("custom-visualization", "figure"), 
     Output("query-response", "children")],
    [Input("submit-query", "n_clicks")],
    [State("query-input", "value")]
)
def handle_visualization_query(n_clicks, query):
    if not query or n_clicks == 0:
        return px.scatter(), "Enter a query to generate a visualization."
    
    # Generate visualization using OpenAI
    fig, response = generate_custom_visualization(
        query,
        data_loader.data,
        data_loader.second_latest_data
    )
    
    if fig is None:
        return px.scatter(), f"Error: {response}"
    
    return fig, f"Generated visualization based on your query"

if __name__ == '__main__':
    app.run_server(debug=True)