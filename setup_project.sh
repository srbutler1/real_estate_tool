#!/bin/bash

# Create main project directory
mkdir -p real_estate_tool

# Navigate into project directory
cd real_estate_tool

# Create initial files
touch README.md
touch requirements.txt
touch .env.example
touch .gitignore

# Create directory structure with __init__.py files
mkdir -p src/{data,utils,components,layouts}
touch src/__init__.py
touch src/app.py
touch src/config.py

# Create __init__.py files in each subdirectory
touch src/data/__init__.py
touch src/data/data_loader.py
touch src/utils/__init__.py
touch src/utils/visualization.py
touch src/components/__init__.py
touch src/components/{map,search,nlp}.py
touch src/layouts/__init__.py
touch src/layouts/dashboard.py

# Create tests directory
mkdir -p tests
touch tests/__init__.py
touch tests/test_data_loader.py
touch tests/test_visualization.py

# Set execute permissions for the project
chmod -R 755 .

echo "Project structure created successfully!"
ls -R
