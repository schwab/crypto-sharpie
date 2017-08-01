#!/usr/bin/python
from __future__ import print_function
import argparse
import ast
import datetime as datetime
import pandas as pd
import sys
import json
from decimal import *
import coin_data_models as models
from coin_data_models import DimDate as date
from coin_data_models import DimExchange as Exchange
from coin_data_models import DimCoin as coin 
from coin_data_models import FactCoinExchangePrice as fact_coin
from date_repo import DateRepo
from exchange_repo import ExchangeRepo
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

class CoinDataImporter(object):
    '''
    '''
    exchange_file_name = "./data/exchange.json"
    def __init__(self, connection, experimental=False ):
        '''
        Object init
        '''
        self.connection = connection
        self.dt_repo = DateRepo(self.connection)
        # Create tables
        print ("Creating tables on database %s" % (self.connection), file=sys.stderr)
       
        ENGINE = models.create_engine(self.connection)
        models.Base.metadata.drop_all(ENGINE)
        models.Base.metadata.create_all(ENGINE)
    def import_exchanges(self):
        """
        import exchange data
        """
        erepo = ExchangeRepo(self.connection)
        print ("importing exchanges from %s" % (self.exchange_file_name), file=sys.stderr)
        with open(self.exchange_file_name, 'r') as file:
            data = json.load(file)
            for item in data:
                data_item = erepo.add_get(Exchange(exchange_nm=item["name"], exchange_url=item["url"],exchange_api_url=item["api_url"]))
                print ("Inserted or found %s" % (data_item), file=sys.stderr)
    def import_dates_daily(self):
        date_start = datetime.datetime(2015, 1,1)
        date_ptr = date_start
        date_list_all = []
        date_repo = DateRepo(connection=self.connection)
        while date_ptr < datetime.datetime.now():

            item = date_repo.add_get(date_ptr)
            date_list_all.append(item)
            date_ptr = date_ptr + datetime.timedelta(1)
        print ("Dates from %s to %s added or verified." % (date_start, date_ptr), file=sys.stderr)
        return date_list_all


    def clean_datatables(self):
        '''
        Until we get a system in place where we import deltas, clean out the existing data
        '''
        #models.
    
def main(connection, init):
    '''
    Main method for running from command line
    '''
    #if init:
        #STATEMENT = "create database IF NOT EXISTS quant;"
        #INIT_CONN = connection.replace("/quant", "")
        #print "%s using connection %s" % (STATEMENT, INIT_CONN)
        #ENGINE = create_engine(INIT_CONN)
        #ENGINE.execute(STATEMENT)
        #print STATEMENT
    cdi = CoinDataImporter(connection=connection)

    cdi.import_exchanges()
    cdi.import_dates_daily()
    print ('import completed', file=sys.stderr)

    erepo = ExchangeRepo(connection)
    exchanges = erepo.get_all()
    print ("all exchanges : %s" % (exchanges), file=sys.stderr)

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(\
    "Import the data files")
    PARSER.add_argument("-c", "--connection", dest="connection", \
        help="DB Connection.", required=False)
    ARGUMENTS = PARSER.parse_args()

    
    main(connection=ARGUMENTS.connection, init=True)