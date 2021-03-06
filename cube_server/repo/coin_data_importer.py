#!/usr/bin/python
from __future__ import print_function
import argparse
import ast
import datetime as datetime
import pandas as pd
import sys
import json
from datetime import datetime  
from datetime import timedelta 
import time
from decimal import *
import coin_data_models as models
from coin_data_models import DimDate as date
from coin_data_models import DimExchange as Exchange
from coin_data_models import DimCoin as coin 
from coin_data_models import FactCoinExchangePrice as fact_coin
from coin_data_models import drop_recreate_db
from date_repo import DateRepo
from exchange_repo import ExchangeRepo
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import exc


class CoinDataImporter(object):
    '''
    '''
    exchange_file_name = None
    connection = None

    def __init__(self, connection, data_dir="./data"):
        '''
        Object init
        '''
        self.exchange_file_name = "%s/exchange.json" % (data_dir)
        self.connection = connection
        self.dt_repo = DateRepo(connection=self.connection)
        # Create tables
        print ("Creating table if they do not exist on database %s" % (self.connection), file=sys.stderr)
        connection_made = False
        while not connection_made:
            try:
                ENGINE = models.create_engine(self.connection)
                connection_made = True
                
            except exc.SQLAlchemyError, e:
                print ("Caught SQLAlchemyError %s " % (str(e)))
                print ("Waiting for database server to start...", file=sys.stderr)
                time.sleep(5)
        
        models.Base.metadata.drop_all(ENGINE)
        models.Base.metadata.create_all(ENGINE)
    def import_exchanges(self):
        """
        import exchange data
        """
        erepo = ExchangeRepo(connection=self.connection)
        print ("importing exchanges from %s" % (self.exchange_file_name), file=sys.stderr)
        with open(self.exchange_file_name, 'r') as file:
            data = json.load(file)
            for item in data:
                data_item = erepo.add_get(Exchange(exchange_nm=item["name"], exchange_url=item["url"],exchange_api_url=item["api_url"]))
                print ("Inserted or found %s" % (data_item), file=sys.stderr)
    
    def import_dates_daily(self):
        date_start = datetime(2015, 1,1)
        date_ptr = date_start
        date_list_all = []
        date_repo = DateRepo(connection=self.connection)
        while date_ptr < datetime.now():
            item = date_repo.add_get(date_ptr)
            date_list_all.append(item)
            date_ptr = date_ptr + timedelta(1)
        print ("Dates from %s to %s added or verified." % (date_start, date_ptr), file=sys.stderr)
        return date_list_all
    
    def import_coins(self):
        
    def generate_days_in_range(self, dt_start, dt_end):
        if not isinstance(dt_start, datetime) or not isinstance(dt_end, datetime):
            raise Exception("dt_start and dt_end must be datettime.")
        if dt_end <= dt_start:
            raise Exception("dt_end must be after dt_start")
        dt_current = dt_start
        dt_current.replace(hour=0, minute=0, second=0)
        
        ts = timedelta(days=1)
        result = []
        while dt_current < dt_end:
            result.append(time.mktime(dt_current.timetuple()))
            dt_current = dt_current + ts
        return result

    def clean_datatables(self):
        '''
        Until we get a system in place where we import deltas, clean out the existing data
        '''
        drop_recreate_db(self.connection)
    
    def create_missing_dates(self, start, end):
        """
        Create all dates missing from the datable
        """
        dt_range = self.generate_days_in_range(start, \
            end)
        range_items = []
        for dt in dt_range:
            range_items.append(self.dt_repo.add_get(datetime.fromtimestamp(dt)))
        
        return range_items
        
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