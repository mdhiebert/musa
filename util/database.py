from datetime import datetime
import sqlite3
import os

import logging
from uuid import uuid4

import util.config as config

db_logger = logging.getLogger(__name__)
db_logger.setLevel(logging.DEBUG)

class DatabaseHandler:
    def __init__(self, database_url):
        self.database_url = database_url

    def _connection(self):
        db_logger.debug('Connecting to SQLite Database...')
        return sqlite3.connect(self.database_url)

    def _execute_query(self, query):
        with self._connection() as c:
            c.execute(query)

    def initialize_database(self):
        db_logger.debug('Initializing Tables...')
        with self._connection() as c:
            self._init_source_table(c)
            self._init_frame_table(c)
            self._init_detection_table(c)
            self._init_identities_table(c)
            self._init_edges_table(c)
            self._init_tracks_table(c)
            self._init_idmap_table(c)
            self._init_detimage_table(c)
            self._init_notifications_table(c)
            self._init_reliability_table(c)
            self._init_phone_table(c)


    #================================================
    #                TABLE INITIALIZATIONS
    #================================================

    def _init_stock_table(self, c: sqlite3.Connection):
        c.execute(f'''CREATE TABLE IF NOT EXISTS stock (
                date TEXT,
                market TEXT,
                ticker TEXT,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adjusted_close REAL,
                volume INTEGER,
                UNIQUE (date, market, ticker)
            );''')
        db_logger.debug('Table stock initialized.')

    #================================================
    #                META FUNCTIONS
    #================================================

    def _get_table_names(self):
        query = """SELECT name FROM sqlite_master WHERE type='table';"""

        with self._connection() as c:
            return c.execute(query).fetchall()

    def delete_database(self, delete_file = False):
        if delete_file:
            try:
                os.remove(self.database_url)
                db_logger.warning(f'Database located at {self.database_url} removed.')
            except FileNotFoundError as e:
                db_logger.warn(e)
        else:
            table_names = self._get_table_names()

            query = """DELETE from """

            with self._connection() as c:
                for table_name in table_names:
                    table_name = table_name[0]
    
                    c.execute(query + table_name)
                
            with self._connection() as c:
                c.execute('VACUUM')

    #================================================
    #                    PUTTERS
    #================================================

    def put_stock(self,
        date: datetime.date,
        market: str,
        ticker: str,
        open: float,
        high: float,
        low: float,
        close: float,
        adjusted_close: float,
        volume: int
    ):

        with self._connection() as c:
            c.execute('''INSERT into frame VALUES (?,?,?,?,?,?,?,?,?)''', 
                (
                    date.strftime('%Y-%m-%d'), 
                    market,
                    ticker,
                    open,
                    high,
                    low,
                    close,
                    adjusted_close,
                    volume
                )
            )

    #================================================
    #                    GETTERS
    #================================================

    def get_stock_data(self, date: datetime.date, market: str, ticker: str):
        date = date.strftime('%Y-%m-%d')
        with self._connection() as c:
            stock_data = c.execute('''SELECT * from stock WHERE date = ? AND market = ? AND ticker = ?''', (date, market, ticker)).fetchone()

        return stock_data

DATABASE = DatabaseHandler(config.DATABASE_URL)