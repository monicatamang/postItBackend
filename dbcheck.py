import dbconnect

# Creating a function that closes the database connection and the cursor
def close_db_connection_and_cursor(conn, cursor):
    closing_cursor = dbconnect.close_cursor(cursor)
    closing_db = dbconnect.close_db_connection(conn)
    # If the cursor or database connection failed to close, print an error message
    if(closing_cursor == False or closing_db == False):
        print("Failed to close cursor and database connection.")

# Check if the database connection and cursor is opened
def check_db_connection_and_cursor(conn, cursor):
    # If the database connection is still open, close all resources
    if(conn == None or cursor == None):
        print("An error has occured in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return False
    return True