import os
import hashlib
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from coin_data_models import DimCoin
from coin_data_models import *
from sqlalchemy import create_engine

class CoinRepo(object):
    def __init__(self, connection=None):
        self.db_engine = create_engine(connection)
        self.session = sessionmaker(bind=self.db_engine)
        self.active_session = self.session()
    
    def hash(self, to_hash):
        return hashlib.sha224(to_hash).hexdigest()[:50]

    def coin_exist(self, coin):
        if not  coin.hash_value is None and len(coin.hash_value) > 0:
            query = self.active_session.query(DimCoin).filter_by(\
                hash_value=coin.hash_value)
            return query.count() > 0

    def add_get(self, coin):
        """
        get the coin object from the db or add it and return with id
        """
        if coin.symbol is None or len(coin.symbol) == 0:
            raise Exception("coin could not be added because it symbol was missing")
        if coin.hash_value is None or len(coin.hash_value) == 0:
            coin.hash_value = self.hash(coin.symbol)
        if not self.coin_exist(coin):
            self.active_session.add(coin)
            self.active_session.commit()
            return coin



    def get_by_name(self, name):
        """
        get an exachange with the exchange.exchange_nm provided
        """
        query = self.active_session.query(DimExchange).filter_by(\
            exchange_nm=name)
        if query.count() > 0:
            return query.first()
        else:
            return None
    def delete(self, exchange):
        """
        Delete the exchange item, fails if there other tables with fk data
        """
        item = self.active_session.query(DimExchange).filter_by(\
            exchange_id=exchange.exchange_id).first()
        self.active_session.delete(exchange)
    def get_all(self):
        return self.active_session.query(DimExchange).all()
