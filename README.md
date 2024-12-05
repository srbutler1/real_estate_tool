# real_estate_tool
(All data is available on Zillow: https://www.zillow.com/research/data/)

Overview
The Real Estate Data Visualization Tool is an interactive dashboard and AI-powered assistant designed to help users explore, analyze, and visualize real estate market trends. This tool uses a combination of Dash (for web-based interactivity) and OpenAI's GPT (to process natural language queries) to generate data visualizations dynamically based on user input.

Features
Interactive Dashboard:

Map Visualization: Displays geographical real estate trends using an interactive map.
Historical Data Search: Allows users to search for specific metro areas and retrieve historical data for analysis.
Data Dictionary: Provides descriptions of all dataset columns for better understanding of available data.
AI-Powered Query Handling:

Users can ask questions or describe the visualizations they want, and the AI generates Python Plotly code to create those visualizations dynamically.
The tool supports both specific queries (e.g., "Show trends in Fayetteville, AR") and broad regional analyses (e.g., "What are the trends in the Northeast?").
Data Insights:

Analyze key real estate metrics, such as median sale prices, market temperatures, inventory, and transaction values.
Filter data based on time, location, and user-defined criteria.
Dynamic Aggregation:

Automatically aggregates and summarizes data when broader queries (e.g., regional trends) are made.
Technology Stack
Frontend:

Dash by Plotly: For interactive web-based visualizations.
Plotly: For creating visually appealing charts and graphs.
Backend:

OpenAI GPT Model: Powers the natural language processing and code generation.
Python: Core language for the tool's logic and integration.
Data Handling:

Pandas: For efficient data processing and manipulation.
How It Works
Data Loading:

The tool reads a preprocessed CSV file containing real estate metrics across different metro areas, states, and regions.
AI Query Processing:

Users input queries in natural language (e.g., "Generate a graph of Fayetteville, AR home prices").
The AI parses the query and generates Plotly Python code to produce the desired visualization.
Dynamic Visualization:

The AI-generated Python code is executed in a sandboxed environment, producing the requested chart.
Charts are displayed on the dashboard in real-time.
Interactivity:

Users can filter and interact with the data through the dashboard's components, such as dropdowns, text inputs, and clickable map elements.
