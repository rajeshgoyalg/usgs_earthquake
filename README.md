# USGS Earthquake

Earthquake Visualization

Used The United States Geological Survey (USGS) USGS.gov API for plotting histogram visualization from earthquake magnitude data

*Prerequisite:* Python 3.6.2 Version

*Input:* Earthquake API at https://earthquake.usgs.gov/fdsnws/event/1/

# Installation:

- Clone repo.
- Create Virtual Environment (Not mandatory)
- Run following command from within the main directory:
- pip install -r requirements.txt

# Running Script:
- python earthquake.py

# Running Unit Test Cases:
- nosetests tests/test_earthquake.py

# Code Coverage
- coverage report -m

# Static Analysis
- pylint constants.py earthquake.py tests/test_earthquake.py

