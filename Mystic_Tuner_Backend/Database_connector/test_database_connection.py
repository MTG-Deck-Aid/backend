from database_connector import DatabaseConnector 
def main():
    instance = DatabaseConnector()

    result = instance.test_connection()

    if(result):
        print("Database is running, successfully connected to it")
    else:
        print("Error with connection")

    instance.get_deck()

if __name__ == "__main__":
    main()