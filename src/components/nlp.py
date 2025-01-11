"""NLP-powered visualization component."""

from dash import html, dcc

def create_nlp_tab():
    """Create the NLP-powered visualization tab."""
    return dcc.Tab(
        label='Ask AI for Custom Visualization',
        children=[
            html.H2("Ask the AI for a Custom Visualization", style={'textAlign': 'center'}),
            dcc.Textarea(
                id='query-input',
                placeholder="Describe the visualization you'd like to see...",
                style={'width': '100%', 'height': '100px', 'margin-bottom': '10px'}
            ),
            html.Button(
                'Generate Visualization',
                id='submit-query',
                n_clicks=0,
                style={'margin': '10px'}
            ),
            dcc.Graph(id='custom-visualization'),
            html.Div(id='query-response', style={'whiteSpace': 'pre-wrap', 'margin': '20px'})
        ]
    )