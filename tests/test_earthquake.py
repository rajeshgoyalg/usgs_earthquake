from unittest.mock import Mock, patch
from nose.tools import assert_is_none, assert_is_not_none, assert_equal, assert_list_equal
from earthquake import USGSService


class TestUSGSService(object):
    """
    `TestUSGSService` Unit Test Object. 
    """

    @classmethod
    def setup_class(cls):
        cls.earthquake = USGSService()
        cls.mock_get_patcher = patch('earthquake.urllib3.request')
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_get_version_ok(self):
        """
        Mock earthquake.urllib3.request and test API version
        """
        self.mock_get.return_value.ok = True
        version = '1.5.8'
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.return_value = version
        response = self.earthquake.make_request('version')
        assert_equal(response.data.decode('utf-8'), version)

    def test_get_version_not_ok(self):
        self.mock_get.return_value.ok = False
        response = self.earthquake.make_request('version')
        assert_is_not_none(response)

    def test_service_api(self):
        response = self.earthquake.make_request('version')
        actual = response.data.decode('utf-8')

        with patch('earthquake.urllib3.request') as mock_get:
            mock_get.return_value.ok = True
            version = '1.5.8'
            mock_get.return_value.return_value = version

            response = self.earthquake.make_request('version')
            mocked = response.data.decode('utf-8')

        assert_equal(actual, mocked)

