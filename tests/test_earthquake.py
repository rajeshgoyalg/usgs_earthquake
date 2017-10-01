from unittest.mock import patch
from unittest import skipIf
from nose.tools import assert_is_none, assert_is_not_none, assert_equal, assert_list_equal
from earthquake import USGSService
from constants import SKIP_ACTUAL_SERVICE


class TestUSGSService(object):
    """
    `TestUSGSService` Unit Test Object. 
    """

    @classmethod
    def setup_class(cls):
        cls.earthquake = USGSService()
        cls.mock_get_patcher = patch('earthquake.requests.get')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_request_ok(self):
        self.mock_get.return_value.ok = True

        response = self.earthquake.make_request('version')

        assert_is_not_none(response)

    def test_request_none(self):
        self.mock_get.return_value.ok = False

        response = self.earthquake.make_request('version')

        assert_is_none(response)


class TestUSGSServiceIntegration(object):
    """
    `TestUSGSServiceIntegration` Unit Test Object. 
    """

    @classmethod
    def setup_class(cls):
        cls.earthquake = USGSService()

    @classmethod
    def teardown_class(cls):
        pass

    @skipIf(SKIP_ACTUAL_SERVICE, 'Skipping tests that hit real service.')
    def test_query(self):
        self.earthquake.ServiceParams = {'format': 'geojson', 'limit': 1, 'offset': 1}
        actual = self.earthquake.make_request('query')
        actual_keys = actual.json().keys()

        with patch('earthquake.requests.get') as mock_get:

            mock_get.return_value.ok = True
            mock_get.return_value.json.return_value = {
                "type": "FeatureCollection",
                "metadata": {
                    "generated": 1506827476000,
                    "url": "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&limit=1&offset=1",
                    "title": "USGS Earthquakes",
                    "status": 200,
                    "api": "1.5.8",
                    "limit": 1,
                    "offset": 1,
                    "count": 1
                },
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "mag": 1.16,
                            "place": "6km ESE of Tehachapi, CA",
                            "time": 1506827015220,
                            "updated": 1506827220492,
                            "tz": -480,
                            "url": "https://earthquake.usgs.gov/earthquakes/eventpage/ci38015992",
                            "detail": "https://earthquake.usgs.gov/fdsnws/event/1/query?eventid=ci38015992&format=geojson",
                            "felt": "",
                            "cdi": "",
                            "mmi": "",
                            "alert": "",
                            "status": "automatic",
                            "tsunami": 0,
                            "sig": 21,
                            "net": "ci",
                            "code": "38015992",
                            "ids": ",ci38015992,",
                            "sources": ",ci,",
                            "types": ",geoserve,nearby-cities,origin,phase-data,scitech-link,",
                            "nst": 18,
                            "dmin": 0.1273,
                            "rms": 0.17,
                            "gap": 67,
                            "magType": "ml",
                            "type": "earthquake",
                            "title": "M 1.2 - 6km ESE of Tehachapi, CA"
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [
                                -118.3846667,
                                35.1131667,
                                2.44
                            ]
                        },
                        "id": "ci38015992"
                    }
                ]
            }
            mocked = self.earthquake.make_request('query')
            mocked_keys = mocked.json().keys()

        assert_list_equal(list(actual_keys), list(mocked_keys))