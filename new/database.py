import sqlite3
import datetime
from typing import Dict, Any


class MarketDatabase:
    def __init__(self, db_path: str = "market_data.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Create historical data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS historical_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date TIMESTAMP NOT NULL,
                    open REAL NOT NULL,
                    high REAL NOT NULL,
                    low REAL NOT NULL,
                    close REAL NOT NULL,
                    volume INTEGER NOT NULL,
                    timeframe TEXT NOT NULL,
                    UNIQUE(symbol, date, timeframe)
                )
            """)

            # Create scanner data table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS scanner_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    sec_type TEXT,
                    sec_id TEXT,
                    exchange TEXT,
                    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, scan_time)
                )
            """)

            # Create order status table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS order_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    filled INTEGER NOT NULL,
                    remaining INTEGER NOT NULL,
                    avg_fill_price REAL,
                    last_fill_price REAL,
                    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.commit()

    def insert_historical_data(self, symbol: str, timeframe: str, data: Dict[str, Any]):
        """Insert historical bar data into database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO historical_data 
                (symbol, date, open, high, low, close, volume, timeframe)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    symbol,
                    data["date"],
                    data["open"],
                    data["high"],
                    data["low"],
                    data["close"],
                    data["volume"],
                    timeframe,
                ),
            )
            conn.commit()

    def insert_scanner_data(self, data: Dict[str, Any]):
        """Insert scanner data into database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO scanner_data 
                (symbol, sec_type, sec_id, exchange)
                VALUES (?, ?, ?, ?)
            """,
                (data["symbol"], data["secType"], data["secId"], data["exchange"]),
            )
            conn.commit()

    def insert_order_status(
        self,
        order_id: int,
        status: str,
        filled: int,
        remaining: int,
        avg_fill_price: float,
        last_fill_price: float,
    ):
        """Insert order status into database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO order_status 
                (order_id, status, filled, remaining, avg_fill_price, last_fill_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (order_id, status, filled, remaining, avg_fill_price, last_fill_price),
            )
            conn.commit()
