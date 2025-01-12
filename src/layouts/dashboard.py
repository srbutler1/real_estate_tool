"""Main dashboard layout component."""

from dash import html, dcc
from src.components.map import create_map_tab
from src.components.search import create_search_tab
from src.components.nlp import create_nlp_tab
from src.config import METRIC_DEFINITIONS

def create_dashboard_layout(data):
    """Create the main dashboard layout."""
    
    # Create data dictionary table
    data_dictionary_table = html.Table(
        # Create table headers
        [html.Tr([html.Th("Column Name"), html.Th("Description")])] +
        # Populate rows with data definitions
        [
            html.Tr([html.Td(column), html.Td(description)])
            for column, description in METRIC_DEFINITIONS.items()
        ],
        style={"width": "100%", "border": "1px solid black", "borderCollapse": "collapse"}
    )

    # Main layout
    return html.Div([
        html.H1("Metro Metrics Dashboard", style={'textAlign': 'center'}),

        # Tabs for different functionalities
        dcc.Tabs([
            # Map visualization tab
            create_map_tab(data),

            # Historical data search tab
            create_search_tab(),

            # NLP visualization tab
            create_nlp_tab(),

            # Data dictionary tab
            dcc.Tab(
                label='Data Dictionary',
                children=[
                    html.H2("Data Dictionary", style={'textAlign': 'center'}),
                    data_dictionary_table
                ]
            )
        ])
    ])