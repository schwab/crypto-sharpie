#!/usr/bin/python
import sys
import unittest
from sqlalchemy import *
from sqlite3 import OperationalError
import random
import argparse
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from coin_data_models import DimDate
from date_repo import DateRepo 



class TestDateRepo(unittest.TestCase):
    """
    DateRepo Unit Tests
    """
    CONNECTION = "mysql+pymysql://root:cryptoquant@%s/%s"
    mariadb_virtual_host = "mariadb.cryptoquant.org"
    mysql_database = "quant"
    d_date = None
    date_repo = None
    d_base = None
    session = None
    db_path = None
    def setUp(self):
        connection = self.CONNECTION % (self.mariadb_virtual_host, self.mysql_database)
        print "Connection %s" % (connection)
        try:
            # Verify the required database exists before running any tests
            self.d_base = create_engine(connection.replace(self.mysql_database, ""))
            self.d_base.connect()
            query_result = self.d_base.execute("SHOW DATABASES;")
            databases = [row[0] for row in query_result]
            
            if self.mysql_database not in databases:
                print "Existing databases %s" % (",".join(databases))
                raise OperationalError()
        except OperationalError as e:
            # Switch database component of the uri
            print "%s database DNE, run ./coin_data_models.py -c <mdb_url> first" % (self.mysql_database)
            raise e
        self.d_date = DimDate()
        self.d_base = create_engine(connection)
        self.session = sessionmaker(bind=self.d_base)
        print self.session
        self.date_repo = DateRepo(connection=connection)
    def tearDown(self):
        self.session.close_all()
    def test_date_add(self):
        """
        Verify repo can create a date.
        """
        # Arrange
        session = self.session()
        test_date = datetime(year=2017, month=4, day=7)
        query = session.query(DimDate)\
            .filter_by(year=test_date.year, month=test_date.month, \
                day=test_date.day)
        existing = query.first()
        if existing and existing.date_id > 0:
            print "Delete existing date %s" % (existing.date_id)
            session.delete(existing)
            session.commit()
        self.assertEqual(query.count(), 0)
        # Act
        saved = self.date_repo.add_get(test_date)
        session.commit()
        # Assert
        print saved
        # self.assertGreater(saved.date_id, 0)
        self.assertEqual(2017, saved.year)
        self.assertEqual(4, saved.month)
        self.assertEqual(7, saved.day)
        self.assertEqual(2, saved.qtr)
        self.assertEqual("april", str.lower(saved.month_name))
        self.assertEqual(14, saved.week_number)
    def test_date_delete(self):
        """
        Verify the repo.delete method removes the provided date
        """
        # Arrange.
        test_date = datetime(year=2017, month=3, day=1)
        item = self.date_repo.add_get(test_date)
        self.assertIsNotNone(item)
        self.assertGreaterEqual(item.date_id, 0)
        # Act
        self.date_repo.delete(item)
        # Assert
        test = self.date_repo.get(test_date)
        self.assertIsNone(test)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("Date repo tests.")
    PARSER.add_argument("-c", "--connection", dest="connection",\
        help="Use alternative connection string instead of the default %s"\
             % (TestDateRepo.CONNECTION),\
        required=False)

    ARGUMENTS = PARSER.parse_args()
    print ARGUMENTS.connection
    if not ARGUMENTS.connection is None:
        print "Using %s" % (ARGUMENTS.connection)
        TestDateRepo.CONNECTION = ARGUMENTS.connection
        print sys.argv.pop()
        print "After %s" % (TestDateRepo.CONNECTION)
    unittest.main()
