"""
database/connection.py
PostgreSQL Connection Handler for AMAS Project
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()


class DatabaseConnection:
    """Handle PostgreSQL connections and basic operations"""
    
    def __init__(self):
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish PostgreSQL connection"""
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
                database=os.getenv("DB_NAME", "AMAS_DB"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", "password")
            )
            print("✅ PostgreSQL Connected Successfully!")
        except psycopg2.Error as e:
            print(f"❌ Database Connection Error: {e}")
            raise
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            self.conn.commit()
            
            # If SELECT query, fetch results
            if query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                cursor.close()
                return True
                
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"❌ Query Error: {e}")
            raise
    
    def execute_insert(self, query, params=None):
        """Execute INSERT and return the inserted ID"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(query, params)
            self.conn.commit()
            
            # Get last inserted ID
            last_id = cursor.lastrowid if hasattr(cursor, 'lastrowid') else None
            cursor.close()
            return last_id
            
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"❌ Insert Error: {e}")
            raise
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("✅ Database Connection Closed")
    
    def __del__(self):
        """Cleanup on object destruction"""
        self.close()


# Global instance
db = DatabaseConnection()