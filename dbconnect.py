import dbcreds
import mariadb
import traceback

# Creating a function that opens that database connection
def open_db_connection():
    # Try to return the connection to the database
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational errors detected in the database connection.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Error detected in the database and resulted in a connection failure.")
    except:
        traceback.print_exc()
        print("An error has occured. Failed to connect to the database.")

# Creating a function that returns a cursor object using the current connection
def create_db_cursor(conn):
    # Trying to return the database cursor
    try:
        return conn.cursor()
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal errors detected in the database. Failed to create a cursor.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational errors detected in the database connection. Failed to create a cursor.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Errors detected in database. Failed to create a cursor.")
    except:
        traceback.print_exc()
        print("An error has occured. Failed to create a cursor.")

# Creating a function that closes the cursor
def close_cursor(cursor):
    # Checking to see if the cursor was initially created and if it wasn't, don't attempt to close the cursor
    if(cursor == None):
        return True
    # Trying to close the database cursor
    try:
        cursor.close()
        # If the cursor closes, return True
        return True
    # If the cursor is not able to be closed, catch errors with exceptions and return False
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal errors detected in the database. Failed to create a cursor.")
        return False
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational errors detected in the database connection. Failed to create a cursor.")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Errors detected with the current connection. Failed to close cursor.")
        return False
    except:
        traceback.print_exc()
        print("An error has occured. Failed to close cursor.")
        return False

# Creating a function that closes the database connection
def close_db_connection(conn):
    # Checking to see if the database connection was initially opened and if it was't, don't attempt to close the connection
    if(conn == None):
        return True
    # Trying to close the database connection
    try:
        conn.close()
        # If the database connection is closed, return True
        return True
    # If the database connection cannot be closed, return False
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Optional errors detected in the database. Failed to close the connection.")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Errored detected in the database. Failed to close the connection.")
        return False
    except:
        print("An error has occured. Failed to close database connection.")
        traceback.print_exc()
        return False