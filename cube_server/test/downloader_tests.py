"""
Testsfor downloaders
"""
__author__ = 'mcstar'
from datetime import datetime
import time
import unittest
from service.poloniex_downloader import PoloniexDownloader
from service.poloniex_downloader import poloniex

class TestDownloader(unittest.TestCase):
    """
    Downloader tests
    """
    def test_get_order_book(self):
        """
        Verify get_order_book
        """
        pdown = PoloniexDownloader()
        result = pdown.get_order_book("BTC_ETH")
        print type(result)
        self.assertTrue(isinstance(result, object))
    def test_daily_data(self):
        """
        Verify daily data pull
        """
        start = datetime(2016, 1, 1)
        unix_start = time.mktime(start.timetuple())
        self.assertTrue(unix_start > 0)

    def poloniex_lib_ticker(self):
        """
        Verify ticker.
        """
        polon_lib = poloniex("", "")
        print polon_lib.returnTicker()
        self.assertTrue(True)

    #poloniex_lib_ticker()
    #test_get_order_book()

if __name__ == '__main__':
    unittest.main()
    