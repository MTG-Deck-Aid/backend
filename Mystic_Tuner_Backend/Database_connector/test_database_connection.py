from database_connector import DatabaseConnector 
def main():
    instance = DatabaseConnector()

    result = instance.test_connection()

    if(result):
        print("Database is running, successfully connected to it")
    else:
        print("Error with connection")

    response = instance.get_user_decks(1)
    for item in response:
        print(item)

if __name__ == "__main__":
    main()