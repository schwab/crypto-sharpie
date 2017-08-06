""" Unit tests for the CoinDataImporter
"""
__author__ = 'mcstar'
import time
import unittest
from datetime import datetime
from cube_server.repo.coin_data_importer import CoinDataImporter
from cube_server.provider.config_provider import ConfigProvider

class TestDownloader(unittest.TestCase):
    """
    Downloader tests
    """
    config_provider = None
    def setUp(self):
        self.config_provider = ConfigProvider(required_settings=["connection"])
        print self.config_provider.data
    def test_generate_days_in_range(self):
        dt_start = datetime(2016,1,1)
        dt_end = datetime(2016,2,1)
        cdi = CoinDataImporter(self.config_provider.data["connection"])
        result = cdi.generate_days_in_range(dt_start, dt_end)
        print "dates in result : %s" % (len(result))
        self.assertTrue(len(result) == 31)
        
