import psycopg2
from psycopg2 import sql

class DatabaseConnector():
    __instance = None

    def __new__(cls, *args, **kwargs):
        if (cls.__instance is None):
            cls.__instance = super().__new__(cls)
        return cls.__instance



    def __init__(self):
        # Database connection parameters
        self.host = "localhost"  # Example: localhost or an IP address
        self.dbname = "Mystic_Tuner_Application"  # Your database name
        self.user = "MT_Admin"  # Your database username
        self.password = "admin"  # Your database password
        self.port = "5433"  # Default PostgreSQL port

    def test_connection(self):
        """
        params: self
        returns: boolean
        
        attempts to establish connection to the Mystic_Tuner_Application database server
        main purpose is for troubleshooting.  Returns true if the connection was successful
        """
        try:
            connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection successful")

            cursor = connection.cursor()

            cursor.execute("SELECT version();")
            
            db_version = cursor.fetchone()
            print(f"Database version: {db_version}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            # Close the cursor and connection if they were created
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")
        
    def get_deck(self, deckid):
        try:
            connection = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("Connection opened")
            cursor = connection.cursor()

            query = "SELECT * FROM public.\"Card\" WHERE \"deckid\" = %d ORDER BY id ASC;"

            cursor.execute(query)

            response = cursor.fetchall()

            print(response)
        except Exception as e:
            print(f"Error: {e}")

        finally:
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")