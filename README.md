## Local Development Golden Path
```
# Create venv enviroment
python3 -m venv .venv

# Active local environment
source .venv/bin/activate

# Install deveoplment only dependencies
pip install black, isort, pylint

# Install dependencies
pip install beautifulsoup4 requests 

# Run script
python3 main.py --category humor