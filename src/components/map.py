"""Map visualization component for the dashboard."""

from dash import html, dcc
import plotly.express as px
from src.utils.visualization import create_map_visualization

def create_map_tab(data):
    """Create the map visualization tab."""
    return dcc.Tab(
        label='Map Visualization',
        children=[
            html.H2("Map Visualization", style={'textAlign': 'center'}),
            dcc.Graph(
                figure=create_map_visualization(data),
                id='main-map'
            )
        ]
    )