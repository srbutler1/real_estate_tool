# Real Estate Analytics Dashboard

An interactive dashboard powered by AI agents for analyzing real estate market data. This tool allows users to explore real estate metrics through natural language queries, creating custom visualizations and providing insightful analysis.
## System Architecture

The system uses three AI agents working together to process natural language queries and generate insights:

```mermaid
flowchart TD
    subgraph User["User Input"]
        Query["'Analyze real estate market trends and provide visualization instructions'"]
    end

    subgraph Data["Data"]
        DataFrame["Real Estate Dataset (DataFrame)"]
    end

    subgraph Agents["AI Agents"]
        Agent1["🧠 Data Analysis Agent
        Analyzes data and provides visualization instructions"]
        Agent2["🎨 Visualization Agent
        Creates Python code for the visualization based on instructions"]
        Agent3["🔍 Code Refinement Agent
        Enhances and validates the generated code using AST"]
        Agent4["📊 Explanation Agent
        Explains insights in business terms"]
    end

    subgraph Output["Dashboard Output"]
        Chart["Interactive Chart"]
        Text["Business Insights"]
    end

    Query --> Agent1
    DataFrame --> Agent1
    Agent1 --> Agent2
    Agent2 --> Agent3
    Agent3 --> Agent4
    DataFrame --> Agent3
    Agent3 --> Chart
    Agent4 --> Text

    classDef queryClass fill:#e6f3ff,stroke:#333,stroke-width:2px,color:#000
    classDef dataClass fill:#f2f2f2,stroke:#333,stroke-width:2px,color:#000
    classDef agentClass fill:#fff7e6,stroke:#333,stroke-width:2px,color:#000
    classDef outputClass fill:#e6ffe6,stroke:#333,stroke-width:2px,color:#000
    
    class Query queryClass
    class DataFrame dataClass
    class Agent1,Agent2,Agent3,Agent4 agentClass
    class Chart,Text outputClass
```
```

## Data Sources 
This dashboard uses Zillow's Metro-level real estate data. To get the required data:
Download Required Files from Zillow Research
Visit Zillow Research Data and download these files:

Metro_market_temp_index_uc_sfrcondo_month.csv
Metro_invt_fs_uc_sfrcondo_sm_month.csv
Metro_mean_doz_pending_uc_sfrcondo_sm_month.csv
Metro_mean_sale_to_list_uc_sfrcondo_sm_month.csv
Metro_median_sale_price_uc_sfrcondo_sm_sa_month.csv
Metro_mlp_uc_sfrcondo_sm_month.csv
Metro_new_con_median_sale_price_uc_sfrcondo_month.csv
Metro_new_con_sales_count_raw_uc_sfrcondo_month.csv
Metro_new_listings_uc_sfrcondo_sm_month.csv
Metro_pct_sold_above_list_uc_sfrcondo_sm_month.csv
Metro_perc_listings_price_cut_uc_sfrcondo_sm_month.csv
Metro_sales_count_now_uc_sfrcondo_month.csv
Metro_total_transaction_value_uc_sfrcondo_sm_sa_month.csv
Metro_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv
Metro_zordi_uc_sfrcondomfr_month.csv
Metro_zori_uc_sfrcondomfr_sm_month.csv

Place files in structure (Geocoded_msa_data will have to be created. Reach out for directions to do so as I haven't added the logic in here)
real-estate-analytics/

```plaintext
real-estate-analytics/
├── data/
│   ├── processed/           # For processed data files
│   │   ├── geocoded_msa_data.csv
│   │   └── custom_msa_geojson.geojson
│   └── zillow/             # Place downloaded files here
│       ├── Metro_market_temp_index_uc_sfrcondo_month.csv
│       ├── Metro_invt_fs_uc_sfrcondo_sm_month.csv
│       └── ... [other Zillow files]
```
The data includes key metrics such as:

Home Values (ZHVI)
Inventory Levels
Price Changes
Market Temperature Index
Days on Market
Sales Volume
Rental Data (ZORI)
And more


## Features

- **Natural Language Interface**: Ask questions about real estate data in plain English
- **Interactive Map**: Explore geographic data visualization
- **Custom Visualizations**: Generate tailored charts and graphs
- **Automated Analysis**: Get AI-powered insights and explanations
- **Historical Data**: Access and analyze historical real estate trends
- **Safe Code Execution**: Secure handling of generated visualization code

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/real-estate-analytics.git
cd real-estate-analytics
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and other settings
```

## Usage

1. Start the dashboard:
```bash
python src/app.py
```

2. Open your browser and navigate to:
```
http://localhost:8050
```

3. Enter your query in the "Ask AI" tab to generate visualizations

## Example Queries

- "Show me the hottest real estate markets right now"
- "Compare home prices in Boston over the last 5 years"
- "Which cities have the highest price growth rate?"
- "Forecast housing prices in San Francisco"
- "Show inventory levels across major cities"

## Data Sources

The dashboard uses Zillow's real estate data, including:
- Home Values
- Inventory Levels
- Price Changes
- Market Temperature Index
- Days on Market
- Sales Volume

## Requirements

- Python 3.8+
- OpenAI API key
- Dependencies listed in requirements.txt

## License

MIT License - see LICENSE file for details

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For support, please open an issue in the GitHub repository.
