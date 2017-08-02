"""
Tests for downloaders
"""
__author__ = 'mcstar'
import time
import unittest
from datetime import datetime
from service.poloniex_downloader import PoloniexDownloader, poloniex

class TestDownloader(unittest.TestCase):
    """
    Downloader tests
    """
    #def setUp(self):
    #    pass
    def test_get_order_book(self):
        """
        Verify get_order_book
        """
        pdown = PoloniexDownloader()
        result = pdown.get_order_book("BTC_ETH")
        print "result type: %s value: %s" % (type(result),result)
        self.assertTrue(isinstance(result, object))
    def test_daily_data(self):
        """
        Verify daily data pull
        """
        start = datetime(2016, 1, 1)
        unix_start = time.mktime(start.timetuple())
        self.assertTrue(unix_start > 0)
#
    #def test_poloniex_lib_ticker(self):
    #    """
    #    Verify ticker.
    #    """
    #    polon_lib = poloniex("", "")
    #    print polon_lib.returnTicker()
    #    self.assertTrue(True)
#
    ##poloniex_lib_ticker()
    ##test_get_order_book()

if __name__ == '__main__':
    unittest.main()
