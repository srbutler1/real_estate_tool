# src/layouts/dashboard.py

from dash import html, dcc, dash_table
from src.components.map import create_map_visualization
from src.components.search import create_search_tab
from src.components.nlp import create_nlp_tab  # Import our NLP tab
from src.config import METRIC_DEFINITIONS

def create_dashboard_layout(data):
    """Create the main dashboard layout."""
    
    # Create data dictionary table
    data_dictionary_table = html.Table(
        [html.Tr([html.Th("Column Name"), html.Th("Description")])] +
        [
            html.Tr([html.Td(column), html.Td(description)])
            for column, description in METRIC_DEFINITIONS.items()
        ],
        style={
            "width": "100%", 
            "border": "1px solid black", 
            "borderCollapse": "collapse"
        }
    )

    return html.Div([
        html.H1("Metro Metrics Dashboard", style={'textAlign': 'center'}),

        # Tabs for different functionalities
        dcc.Tabs([
            # Tab for Map Visualization
            dcc.Tab(label='Map Visualization', children=[
                html.H2("Map Visualization", style={'textAlign': 'center'}),
                dcc.Graph(figure=create_map_visualization(data), id='main-map')
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
                    columns=[{"name": col, "id": col} for col in data.columns],
                    style_table={'overflowX': 'auto'},
                    style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
                    page_size=10
                )
            ]),

            # NLP Tab is just inserted here by calling create_nlp_tab()
            create_nlp_tab(),

            # Tab for Data Dictionary
            dcc.Tab(label='Data Dictionary', children=[
                html.H2("Data Dictionary", style={'textAlign': 'center'}),
                data_dictionary_table
            ])
        ])
    ])

