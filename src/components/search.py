"""Search component for historical data."""

from dash import html, dcc, dash_table

def create_search_tab():
    """Create the search tab for historical data."""
    return dcc.Tab(
        label='Search Historical Data',
        children=[
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
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'whiteSpace': 'normal'},
                page_size=10
            )
        ]
    )