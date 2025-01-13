"""Main application file for the Real Estate Analytics Dashboard."""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import dash
from dash import Dash, Input, Output, State, html, dcc, callback_context
import plotly.express as px
import pandas as pd

from src.data.data_loader import DataLoader
from src.layouts.dashboard import create_dashboard_layout
from src.utils.visualization import generate_custom_visualization

# Initialize the Dash app
app = Dash(__name__, suppress_callback_exceptions=True)

# Initialize data loader and load data
data_loader = DataLoader("data/processed/geocoded_msa_data.csv")
data = data_loader.load_data()

# Set the app layout
app.layout = create_dashboard_layout(
    data_loader.second_latest_data)

# --------------------- Callbacks --------------------- #

# 1. Callback for Search Functionality
@app.callback(
    [Output('search-results', 'data'),
     Output('search-results', 'columns')],
    [Input('search-button', 'n_clicks')],
    [State('search-input', 'value')],
    prevent_initial_call=True
)
def update_search_results(n_clicks, search_value):
    if not search_value or n_clicks == 0:
        return [], []
    
    filtered_data = data_loader.search_metro(search_value)
    columns = [{"name": col, "id": col} for col in filtered_data.columns]
    
    return filtered_data.to_dict('records'), columns

# 2. Callback for Map Click-to-Search
@app.callback(
    Output('search-input', 'value'),
    [Input('main-map', 'clickData')],
    prevent_initial_call=True
)
def map_click_to_search(click_data):
    if click_data and 'points' in click_data:
        return click_data['points'][0]['hovertext']
    return ""

# 3. Combined callback for visualization and status
@app.callback(
    [Output("custom-visualization", "figure"),
     Output("query-response", "children"),
     Output("agent-status", "children"),
     Output("agent-interval", "disabled")],
    [Input("submit-query", "n_clicks"),
     Input("agent-interval", "n_intervals")],
    [State("query-input", "value")],
    prevent_initial_call=True
)
def handle_visualization_and_status(n_clicks, n_intervals, query):
    """Combined callback for visualization generation and status updates."""
    ctx = callback_context
    triggered_id = ctx.triggered[0]["prop_id"].split(".")[0] if ctx.triggered else None

    if triggered_id == "agent-interval":
        # Handle interval updates - cycle through messages
        messages = [
            {"icon": "🤖", "text": "Analyzing your request...", "color": "#007bff"},
            {"icon": "📊", "text": "Generating visualization code...", "color": "#28a745"},
            {"icon": "✨", "text": "Creating the perfect visualization...", "color": "#17a2b8"}
        ]
        current_msg = messages[n_intervals % len(messages)]
        
        status_div = html.Div([
            html.H4(f"{current_msg['icon']} Working on it...", style={"color": current_msg['color']}),
            html.P(current_msg['text'])
        ])
        
        # Return current figure and response (unchanged) with new status
        return dash.no_update, dash.no_update, status_div, False

    elif triggered_id == "submit-query":
        if not query or n_clicks == 0:
            return px.scatter(), "Enter a query to generate a visualization.", "", True

        try:
            # Generate visualization
            fig, code, explanation = generate_custom_visualization(
                query,
                data_loader.data,
                data_loader.second_latest_data
            )
            
            if fig is None:
                return (px.scatter(), 
                       html.Div([
                           html.H4("Error", style={'color': 'red'}),
                           html.P(f"Failed to generate visualization: {code}")
                       ]), 
                       "", 
                       True)
            
            return (fig,
                   html.Div([
                       html.H4("✅ Analysis Complete", style={'color': '#28a745', 'marginBottom': '20px'}),
                       html.H4("Visualization Explanation"),
                       html.P(explanation),
                       html.H4("Generated Python Code"),
                       dcc.Markdown(f"```python\n{code}\n```")
                   ]),
                   "",  # Clear status when complete
                   True)  # Disable interval
        
        except Exception as e:
            return (px.scatter(),
                   html.Div([
                       html.H4("Error", style={'color': 'red'}),
                       html.P(f"An error occurred: {str(e)}")
                   ]),
                   "",
                   True)
    
    # Initial load - return defaults
    return px.scatter(), "", "", True

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)