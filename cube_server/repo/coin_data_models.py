#!/usr/bin/python
import os
import sys
import argparse
import time
from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
#from sqlalchemy import *
from sqlalchemy import exc
from sqlalchemy import create_engine


Base = declarative_base()

class DimExchange(Base):
    """
    Exchanges in this set of data.
    """
    __tablename__ = "dim_exchange"
    hash_value = Column(String(50), primary_key=True)
    exchange_nm = Column(String(200), unique=True)
    exchange_url = Column(String(800), unique=False)
    exchange_api_url = Column(String(800), unique=False)
    exchange_api_user = Column(String(800), unique=False)
    exchange_api_secret = Column(String(800), unique=False)
    downloader = Column(String(800))

    def __repr__(self):
        return "<DimExchange(name='%s', hash='%s', downloader=%s)>" % ( \
                                self.exchange_nm, self.hash_value, self.downloader)

class DimDate(Base):
    """
    Date spans
    """
    __tablename__ = "dim_date"
    __table_args__ = (UniqueConstraint("year", "month", "day","hour", name='_ymd_constraint'),)
    hash_value = Column(String(50), primary_key=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    day = Column(Integer, index=True)
    qtr = Column(Integer, index=True)
    hour = Column(Integer, index=True)
    month_name = Column(String(200), index=True)
    weekday = Column(Integer, index=True)
    week_number = Column(Integer, index=True)
    timestamp = Column(Integer)

class DimCoin(Base):
    """
    Crypto Coin
    """
    __tablename__ = "dim_coin"
    hash_value = Column(String(50), primary_key=True)
    name = Column(String(200), unique=True)
    symbol = Column(String(20), unique=True)
    pre_mined = Column(Integer, index=False)
    ttl_supply = Column(Integer, index=False)
    details_url = Column(String(800), index=False)
    image_url = Column(String(800), index=False)
    algorithm = Column(String(20))
    proof_type = Column(String(20))
    
    def __repr__(self):
        return "<DimCryptoCoin(symbol='%s', exchange='%s')>" % ( \
                                self.symbol, self.exchange_hash)

coin_exchange_association_table = Table("coin_exchange", Base.metadata, \
    Column('coin_hash', String(50), ForeignKey('dim_coin.hash_value')), \
    Column('exchange_hash', String(50), ForeignKey('dim_exchange.hash_value')) \
    )



class FactCoinExchangePrice(Base):
    """
    Details about a Coin Exchange Price .
    """
    __tablename__ = "fact_coin_exchange_price"
    id = Column(Integer, primary_key=True, autoincrement=True)
    coin_id = Column(Integer, index=True)
    exchange_id = Column(Integer, index=True)
    date_hash_value = Column(String(50), index=True)
    price_max = Column(Numeric)
    price_min = Column(Numeric)
    price_open = Column(Numeric)
    price_close = Column(Numeric)


def create_db(connection):
    STATEMENT = "create database IF NOT EXISTS quant;"
    init_conn = connection.replace("/quant", "")
    print "%s using connection %s" % (STATEMENT, init_conn)
    engine = create_engine(init_conn)
    c = engine.connect()
    c.execute(STATEMENT)
    c.close()
    print "%s Complete" % (STATEMENT ) 

def drop_recreate_db(connection):
    create_db(connection)
    print "Dropping schema ..."
    engine = create_engine(connection)
    Base.metadata.drop_all(engine)
    print "Recreate schema ..."
    Base.metadata.create_all(engine)

ENGINE = None
def connect(connection):
    ENGINE = create_engine(connection)
if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("Crypto_sharpie fact and dimension models.")
    PARSER.add_argument("-d", "--drop", dest="drop", \
        help="Drop and replace database tables.", required=False, action="store_true")
    PARSER.add_argument("-i", "--init", dest="init", \
        help="Create the database.", required=False, action="store_true")
    PARSER.add_argument("-c", "--connection", dest="connection", \
        help="Database connection string.", required=False)

    ARGUMENTS = PARSER.parse_args()
    if ARGUMENTS.connection:
        CONNECTION = ARGUMENTS.connection
    else:
        CONNECTION = "mysql+pymysql://root:cryptquant@mariadb/crypto_sharpie"
    print "Crypto_Coin Models (CONNECTION) : " + CONNECTION
    connection_made = False
    while not connection_made:
        try:
            if ARGUMENTS.init:
                STATEMENT = "create database IF NOT EXISTS crypto_sharpie;"
                INIT_CONN = CONNECTION.replace("/crypto_sharpie", "")
                print "%s using connection %s" % (STATEMENT, INIT_CONN)
                ENGINE = create_engine(INIT_CONN)
                ENGINE.execute(STATEMENT)
                print STATEMENT
            ENGINE = create_engine(CONNECTION)
            if ARGUMENTS.drop:
                print "Dropping schema ..."
                Base.metadata.drop_all(ENGINE)
            Base.metadata.create_all(ENGINE)
            connection_made = True
        except exc.SQLAlchemyError:
            print "Waiting for database server to start..."
            time.sleep(5)

