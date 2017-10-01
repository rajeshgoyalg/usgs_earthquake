import os

SERVICE_URL = 'https://earthquake.usgs.gov/fdsnws/event/1/'
SERVICE_API_VERSION = '1.5.8'
SERVICE_LIMIT = 20000
SKIP_ACTUAL_SERVICE = os.getenv('SKIP_ACTUAL_SERVICE', True)