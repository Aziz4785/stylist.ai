## Install a virtual environment

You will need [Python3](https://www.python.org/downloads/) on your machine.

```bash

# Set up a Python virtual environment
python -m venv venv

# Activate  the virtual environment
.\venv\Scripts\activate # Windows
source venv/bin/activate # linux

# Install all dependencies
pip install -r requirements.txt

# Leave the virtual environment
deactivate
```

## Configuration
Before running the server, you need to create a config.py file in the root directory of the project
```bash

# Create a config.py file with this content
OPENAI_API_KEY = 'your-api-key'
```
## Run the server
```bash

py SERVER/server3.py
```
## Run the tests and test report
```bash
cd SERVER
py -m unittest test_app
```
