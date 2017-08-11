import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from coin_data_models import DimExchange
from coin_data_models import *
from sqlalchemy import create_engine

class ExchangeRepo(object):
    def __init__(self, connection=None):
        self.db_engine = create_engine(connection)
        self.session = sessionmaker(bind=self.db_engine)
        self.active_session = self.session()
    def add_get(self, exchange):
        """
        get the exchange object from the db or add it and return with id
        """
        query = self.active_session.query(DimExchange).filter_by(\
            exchange_nm=exchange.exchange_nm)
        if query.count() > 0:
            return query.first()
        else:
            insert_exchange = DimExchange(\
                exchange_nm=exchange.exchange_nm,\
                exchange_url=exchange.exchange_url,\
                exchange_api_url=exchange.exchange_api_url,\
                exchange_api_user=exchange.exchange_api_user,\
                exchange_api_secret=exchange.exchange_api_secret)
            self.active_session.add(insert_exchange)
            self.active_session.commit()
            return insert_exchange
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
