import os
import psycopg2
from psycopg2.extras import execute_values
from urllib.parse import urlparse
class DatabaseConnector():
    """
    Singleton connector class that excutes queries passed to it
    """
    _instance = None #instance variable to ensure singleton restriction

    def __new__(cls, *args, **kwargs):
        if (cls._instance is None):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, host = "localhost", database_name = "Mystic_Tuner_Application", user = "MT_Admin", password = "admin", port = 5433):
        """
        args:
            host (String) - host IP 
            database_name (String) - name of database
            user (String) - database user username
            password (String) - database user password
            port (int) - port of the database
        return:
            nothing
        """
        self._establish_connection()

    def _establish_connection(self, host = "localhost", database_name = "Mystic_Tuner_Application", user = "MT_Admin", password = "admin", port = 5433):
        """
        args:
            host (String) - host IP 
            database_name (String) - name of database
            user (String) - database user username
            password (String) - database user password
            port (int) - port of the database
        return:
            success of connection (boolean)
        """
        try:
            # If the DATABASE_URL environment variable is set, use that to connect to the database
            # DATABASE_URL provides a Heroku Postgres Login for application purposes
            # Parse the DATABASE_URL environment variable into it's components
            if 'DATABASE_URL' in os.environ:
                parsed_url = urlparse(os.environ['DATABASE_URL'])
                self.connection = psycopg2.connect(
                    dbname = parsed_url.path[1:],
                    user = parsed_url.username,
                    password = parsed_url.password,
                    host = parsed_url.hostname,
                    port = parsed_url.port
                )
            else:
                self.connection = psycopg2.connect(
                    host = host,
                    dbname = database_name,
                    user = user,
                    password = password,
                    port = port
                )
            print("Connection successfully established with database")

        except Exception as e:
            print(f"Could not establish connection to database: {e}")
            return False
        return True

    @staticmethod
    def get_instance():
        """
        args:
            Nothing
        return:
            (DatabaseConnector) - singleton instance of the database connector
        """
        if DatabaseConnector._instance == None:
            DatabaseConnector._instance = DatabaseConnector()
        return DatabaseConnector._instance

    def change_connection(self, host = "localhost", database_name = "Mystic_Tuner_Application", user = "MT_Admin", password = "admin", port = 5433):
        """
        args:
            host (String) - host IP 
            database_name (String) - name of database
            user (String) - database user username
            password (String) - database user password
            port (int) - port of the database
        return:
            success of connection (boolean)
        """
        self.connection.close()
        return self._establish_connection()

    def execute_query(self, query, params = None, is_select = True):
        """
        args:
            query (String) - base SQL query
            params (tuple) - tuple of values for the query
            is_select (boolean) - true if the query is a select query
        return:
            results of query
                - list of rows for select queries (List)
                - number of rows affected for all other (int)
        
        designed for majority of possible SQL queries
        """
        try:

            cursor = self.connection.cursor()

            if(params == None):
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            
            row_count = cursor.rowcount

            print(f"Rows affected: {row_count}")
            if(is_select):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return row_count
        except Exception as e:
            print(f"With query: {query}\nWith params: {params}\nHas error: {e}")
            self.connection.rollback()
            return False

    def execute_long_query(self, query, params):
        """
        args:
            query (String) - base SQL query
            params (tuple) - tuple of values for the query
            is_select (boolean) - true if the query is a select query
        return:
            (int) number of rows affected 
        
        designed for the few more complex SQL queries; typically queries involving inserting 
        a bulk of rows at once
        """
        try:
            cursor = self.connection.cursor()
            execute_values(cursor, query, params)
            self.connection.commit()

            row_count = cursor.rowcount
            print(f"Rows affected: {row_count}")
            return row_count

        except Exception as e:
            print(f"With query: {query}\nWith params: {params}\nHas error: {e}")
            self.connection.rollback()
            return False