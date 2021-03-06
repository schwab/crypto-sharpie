import os
import time
import hashlib
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from coin_data_models import DimDate
from sqlalchemy import create_engine

class DateRepo(object):
    """
    Repo for Date
    """
    db_url = ""
    session = None
    active_session = None
    def __init__(self, connection=None):
        self.db_engine = create_engine(connection)
        self.session = sessionmaker(bind=self.db_engine)
        self.active_session = self.session()
    def hash(self, to_hash):
        return hashlib.sha224(to_hash).hexdigest()[:50]
    
    def create_instance(self, date):
        instance = DimDate(year=date.year, \
                month=date.month,\
                day=date.day, \
                qtr=self.get_qtr(date), \
                hour=date.hour, \
                week_number=date.isocalendar()[1], \
                weekday=date.weekday(), \
                month_name=date.strftime("%B"), 
                timestamp=time.mktime(date.timetuple()))  
        instance.hash_value = self.hash(instance.__repr__())
        return instance
    def add_get(self, date):
        """
        Add the provided date to the database if it DNE
        """

        query = self.active_session.query(DimDate).filter_by(\
            year=date.year, month=date.month, day=date.day)
        if query.count() > 0:
            return query.first()
        else:
            insert_date = self.create_instance(date)
            self.active_session.add(insert_date)
            self.active_session.commit()
            return insert_date
    
    def get(self, date):
        """
        Get the matching date entry from the database, None if it DNE
        """
        query = self.active_session.query(DimDate).filter_by(\
            year=date.year, month=date.month, day=date.day)
        if query.count() > 0:
            return query.first()
        else:
            return None

    def get_by_ut(self, date_ut):
        query = self.active_session.query(DimDate).filter(\
        DimDate.timestamp == date_ut)
        return query.first()

    def delete(self, date):
        """
        Delete the date entry from the table
        """
        item = self.active_session.query(DimDate).filter_by(\
        year=date.year, month=date.month, day=date.day).first()
        self.active_session.delete(item)
    
    def get_between(self, start_ut, end_ut):
        items = self.active_session.query(DimDate).filter(\
            and_(DimDate.timestamp <= start_ut, DimDate.timestamp >= end_ut))
        return items.all()

    def get_qtr(self, date):
        if date.month in [1, 2, 3]: return 1
        if date.month in [4, 5, 6]: return 2
        if date.month in [7, 8, 9]: return 3
        if date.month in [10, 11, 12]: return 4
