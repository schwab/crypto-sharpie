import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from coin_data_models import FactCoinExchangePrice, DimDate, DimCoin

class FactCoinExchangeRepo(object):
    """
    Repo for Anesthesia Encounter
    """
    db_file = ""
    active_session = None
    def __init__(self, connection="mysql://root:qiadvisor@localhost/qiadvisor"):
        self.db_engine = create_engine(connection)
        
        self.active_session = sessionmaker(bind=self.db_engine)()
    def add(self, fact):
        """
        Add the provided fact (FactCoinExchangePrice) to the database
        """
        self.active_session.add(fact)
        self.active_session.commit()
        return encounter
    def add_batch(self, facts):
        """
        Add a batch of encounters
        """
        cnt = 0
        for item in facts:
            self.active_session.add(item)
            cnt += 1
        self.active_session.commit()
        return cnt

    def get_by_date(self, exchange, symbol, date):
        """
        Get the fact entry by the exchange, symbol,date specified
        """
        date = self.active_session.query(DimDate).filter(and_(DimDate.year == date.year, DimDate.month  == date.month, DimDate.day == date.day))
        #items = self.active_session.query(FactCoinExchangePrice)\
        #    .filter(and_(FactCoinExchangePrice.date_id == start,\
        #     FactPatientEncounterAnesthesia.admission_date <= end))
        return date
    def delete(self, encounter):
        """
        Delete the encounter provided.
        """
        if encounter.id > 0:
            encounter.drugs[:] = []
            self.active_session.delete(encounter)
            self.active_session.commit()
            print "Deleted Encounter %s" % (encounter)
        else:
            raise ValueError("encounter.encounter_id is required.")

    def truncate(self):
        """
        TODO: The sqlalchemy docs say not to do bulk delete this way, but it seems
        most expedient
        """
        self.db_engine.execute("DELETE FROM encounter_anesthesia_drug_association;")
        self.db_engine.execute("DELETE FROM fact_patient_encounter_anesthesia;")
