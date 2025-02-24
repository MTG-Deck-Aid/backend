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

    def execute_query(self, query, params = None):
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

            if(params == None):
                cursor.execute(query)
            else:
                cursor.execute(query, params)
            
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            # Close the cursor and connection if they were created
            if connection:
                cursor.close()
                connection.close()
                print("Connection closed")


    def test_connection(self):
        """
        params: self
        returns: boolean
        
        attempts to establish connection to the Mystic_Tuner_Application database server
        main purpose is for troubleshooting.  Returns true if the connection was successful
        """

        result = self.execute_query("SELECT version();")

        if(result != False):
            print(F"Connection successfully established: {result}")
            return True
        else:
            print("Failled to connect to database")
            return False


        
    def get_deck(self, deckid):

        query = "SELECT * FROM public.\"Card\" WHERE \"deckid\" = %s ORDER BY id ASC;"
        params = (deckid,)
        return self.execute_query(query, params)

    def get_card(self, cardName):

        query = "SELECT * FROM public.\"Card\" WHERE \"cardname\" = %s ORDER BY id ASC;"
        params = (cardName,)
        return self.execute_query(query, params)
    
    def get_user_decks(self, userid):

        query = "SELECT * FROM public.\"Deck\" WHERE \"userId\" = %s ORDER BY \"DID\" ASC;"
        params = (userid,)
        return self.execute_query(query, params)

    