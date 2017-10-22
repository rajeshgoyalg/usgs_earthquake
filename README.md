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
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/Earthquake_Magnitude_DataFrame_2016.PNG)
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/Earthquake_Magnitude_Histogram_2016.PNG)
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/Earthquake_2016_Magnitude_Depth.png)
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/Earthquake_2016_Corelation_Lat_Long.png)

# Running Unit Test Cases:
- nosetests tests/test_earthquake.py
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/unit_and_integration_test.PNG)

# Code Coverage
- coverage report -m

# Static Analysis
- pylint constants.py earthquake.py tests/test_earthquake.py
- ![Screenshot](https://github.com/rajeshgoyalg/usgs_earthquake/blob/master/screenshots/static_analysis_pylint.png)

