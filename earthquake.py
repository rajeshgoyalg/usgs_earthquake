import json
import math
import asyncio
import concurrent.futures
import requests
import datetime
import matplotlib.pyplot as plot
import pandas as pd
from constants import SERVICE_URL, SERVICE_LIMIT


class USGSService:
    """
    Create a new `USGSService` object. `USGSService` takes start and end date    
    that specify the behaviour of the `USGSService` object:
    * `start_date`: accepts date in 'YYYY-MM-DD' format
    * `end_date`: accepts date in 'YYYY-MM-DD' format    
    """

    Offset = 1
    ServiceParams = {}

    def __init__(self, start_date='', end_date=''):
        if start_date != "":
            self.StartDate = start_date
        if end_date != "":
            self.EndDate = end_date

    def check_api_version(self):
        """
        Check USGS API Version. Current version of API is '1.5.8'
        :return: Exception if USGS API Version is different than '1.5.8'
        """
        self.ServiceParams['format'] = 'quakeml'
        result = self.make_request('version')
        return result.text

    def get_record_count(self):
        """
        Query API for `count` endpoint.
        :return:
         Long: Result Count for query 
        """
        self.ServiceParams['format'] = 'quakeml'
        self.ServiceParams['starttime'] = self.StartDate
        self.ServiceParams['endtime'] = self.EndDate
        result = self.make_request('count')
        return result.text

    def request_count(self):
        """
        Get result count for API and determines the number of requests 
        by dividing total count by limit
        :return: 
        int: Returns total number of requests
        """
        record_count = self.get_record_count()
        print('Total records found for your search: %s' % record_count)
        return math.ceil(float(record_count) / SERVICE_LIMIT)

    def make_request(self, method):
        """
        Make API query request to USGS Service and return response
        :param method: String: API Method / endpoint
        :return: 
        Object: Object of response
        """
        result = requests.get(SERVICE_URL + method, self.ServiceParams)
        return result if result.ok else None

    def create_request_params(self):
        """
        Create a list of URLs params for building request 
        :return: dictionary of params
        """
        params = []
        param = {
            'format': 'geojson',
            'starttime': self.StartDate,
            'endtime': self.EndDate,
            'limit': SERVICE_LIMIT
        }
        total_requests = self.request_count()
        for x in range(total_requests):
            param['offset'] = self.Offset
            params.append(param)
            # increase offset to fetch next set of records
            self.Offset = self.Offset + SERVICE_LIMIT

        return params

    async def make_async_request(self):
        """
        Make Async request to USGS Service and return response. 
        :return: 
        List: List of magnitude
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            loop = asyncio.get_event_loop()
            params = self.create_request_params()
            futures = [loop.run_in_executor(executor, requests.get, SERVICE_URL + 'query', params[i]) for i in range(len(params))]

            responses = []
            magnitudes = []
            for response in await asyncio.gather(*futures):
                if response:
                    response = json.loads(response.text)
                    responses.append(response)
                    for result in responses:
                        for row in result['features']:
                            row["properties"].get("mag") and magnitudes.append(row['properties']['mag'])

        return magnitudes


def validate_date(date_text):
    """
    Validate user input whether it is valid date format
    :param date_text: Date string
    :return: 
    date: Date if valid date
    Exception: ValueError - Incorrect date format
    """
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")


def visualize_earthquake(magnitudes):
    """
    Visualize earthquake magnitude data.
    It generates pandas data frame and plot histogram
    :param magnitudes: 
    :return: 
    """

    # Plot a histogram.
    n, bins, patch = plot.hist(magnitudes, histtype='step', range=(0, 10), bins=10)

    # Draw histogram of the DataFrame’s series
    histogram = pd.DataFrame()
    for i in range(0, len(n)):
        magnitude_range = str(bins[i]) + " - " + str(bins[i + 1])
        frequency = n[i]
        percentage = round((n[i] / len(magnitudes)) * 100, 4) if magnitudes else 0
        histogram = histogram.append(pd.Series([magnitude_range, frequency, percentage]), ignore_index=True)

    histogram.columns = ['Range of Magnitude', 'Frequency', 'Percentage']
    print(histogram)

    # Plot magnitude Histogram
    plot.xlabel("Earthquake Magnitudes")
    plot.ylabel("Frequency")
    plot.title("Frequency by Magnitude")
    plot.show()
    plot.clf()


def main():
    print('Welcome to Earthquake visualisation. Please provide date range for your search.')
    date_entry = input('Enter start date in YYYY-MM-DD format: ')
    start_date = validate_date(date_entry)

    date_entry = input('Enter end date in YYYY-MM-DD format: ')
    end_date = validate_date(date_entry)

    # Create an object of class USGSService to consume the USGS API
    service = USGSService(start_date, end_date)
    # collect all magnitude data for data visualization
    loop = asyncio.get_event_loop()
    magnitudes = loop.run_until_complete(service.make_async_request())

    visualize_earthquake(magnitudes)

if __name__ == '__main__':
    main()