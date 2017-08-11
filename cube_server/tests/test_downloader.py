"""
Tests for downloaders
"""
__author__ = 'mcstar'
import time
import unittest
from datetime import datetime
from cube_server.service.poloniex_downloader import PoloniexDownloader, poloniex


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
        #print "result type: %s value: %s" % (type(result),result)
        self.assertTrue("asks" in result)
        self.assertTrue("bids" in result)
        self.assertTrue(isinstance(result, dict))
        self.assertTrue(len(result["asks"]) > 0)
        self.assertTrue(len(result["bids"]) > 0)
    
    def test_daily_data(self):
        """
        Verify daily data pull
        """
        start = datetime(2016, 1, 1)
        end = datetime(2016, 2, 1)
        unix_start = time.mktime(start.timetuple())
        unix_end = time.mktime(end.timetuple())

        print "test_daily_data start %s : %s, end %s : %s" % (start, unix_start, end, unix_end)
        
        self.assertTrue(unix_start > 0)
        self.assertGreater(unix_end, unix_start)
        

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
