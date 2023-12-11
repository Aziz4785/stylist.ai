## Install a virtual environment

You will need [Python3](https://www.python.org/downloads/) on your machine.

```bash
# Install pip3 and virtualenv
sudo apt-get install python3-pip
sudo pip3 install virtualenv

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