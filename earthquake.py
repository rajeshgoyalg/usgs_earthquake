import json
import math
import urllib3
import datetime
import matplotlib.pyplot as plot


class USGSService:
    """
    Create a new `USGSService` object. `USGSService` takes optional arguments    
    that specify the behaviour of the `USGSService` object:
    * `start_date`: Optional argument and accepts date in 'YYYY-MM-DD' format
    * `end_date`: Optional argument and accepts date in 'YYYY-MM-DD' format    
    """

    SERVICE_API_VERSION = '1.5.8'
    SERVICE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/"
    StartDate = '2016-01-01'
    EndDate = '2016-01-02'
    LIMIT = 20000
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
        result = result.data.decode('utf-8')
        if result != self.SERVICE_API_VERSION:
            raise Exception('Current USGS API Version : ' + result + ' Expected : ' + self.SERVICE_API_VERSION)

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
        return result.data.decode('utf-8')

    def request_count(self):
        """
        Get result count for API and determines the number of requests 
        by dividing total count by limit
        :return: 
        int: Returns total number of requests
        """
        record_count = self.get_record_count()
        return math.ceil(float(record_count) / self.LIMIT)

    def fetch_service(self):
        """
        Fetches all the results for API query
        :return: 
        List: List of response objects 
        """
        total_requests = self.request_count()
        self.ServiceParams['format'] = 'geojson'
        self.ServiceParams['starttime'] = self.StartDate
        self.ServiceParams['endtime'] = self.EndDate
        self.ServiceParams['limit'] = self.LIMIT
        results = []
        for x in range(total_requests):
            self.ServiceParams['offset'] = self.Offset
            result = self.make_request('query')
            result = json.loads(result.data.decode('utf-8'))
            results.append(result)
            self.Offset = self.Offset + self.LIMIT

        return results

    def fetch_magnitude_data(self):
        """
        Fetches all the results for API query and collects magnitude data
        :return: 
        List: List of magnitudes data 
        """
        self.check_api_version()
        results = self.fetch_service()
        magnitudes = []
        for result in results:
            for row in result['features']:
                if row["properties"].get("mag"):
                    magnitudes.append(row['properties']['mag'])

        return magnitudes

    def make_request(self, method):
        """
        Make API query request to USGS Service and return response
        :param method: String: API Method / endpoint
        :return: 
        Object: Object of response
        """
        http = urllib3.PoolManager()
        return http.request('GET', self.SERVICE_URL + method, self.ServiceParams)


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


def main():
    date_entry = input('Enter start date in YYYY-MM-DD format: ')
    start_date = validate_date(date_entry)

    date_entry = input('Enter end date in YYYY-MM-DD format: ')
    end_date = validate_date(date_entry)

    # Create an object of class USGSService to consume the USGS API
    service = USGSService(start_date, end_date)
    # collect all magnitide data for data visualization
    magnitudes = service.fetch_magnitude_data()

    # Plot Histogram of magnitude data
    colors = ['skyblue']
    plot.hist(magnitudes, bins=[0, 1, 2, 3, 4, 5, 6, 7], normed=0, histtype='bar', color=colors, label=colors)
    plot.xlabel('Magnitudes')
    plot.ylabel('Frequency')
    plot.title('Histogram')
    plot.show()
    plot.clf()

if __name__ == '__main__':
    main()