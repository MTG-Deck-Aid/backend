import psycopg2
from psycopg2.extras import execute_values

class database_connector():
    """
    Singleton connector class that excutes queries passed to it
    """

    _instance = None

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

        #TODO implement environment variables to get connection details
        try:
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

    @staticmethod
    def get_instance():
        """
        args:
            Nothing
        return:
            (DatabaseConnector) - singleton instance of the database connector
        """
        if database_connector._instance == None:
            database_connector._instance = database_connector()
        return database_connector._instance

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