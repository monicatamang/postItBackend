import dbcreds
import mariadb
import traceback

# Creating a function that opens that database connection
def open_db_connection():
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password, host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection.")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("Error detected in the database and resulted in a connection failure.")
        traceback.print_exc()
    except:
        print("An error has occured. Failed to connect to the database.")
        traceback.print_exc()

# Creating a function that returns a cursor object using the current connection
def create_db_cursor(conn):
    try:
        return conn.cursor()
    except mariadb.InternalError:
        print("Internal errors detected in the database. Failed to create a cursor.")
        traceback.print_exc()
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection. Failed to create a cursor.")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("Errors detected in database. Failed to create a cursor.")
        traceback.print_exc()
    except:
        print("An error has occured. Failed to create a cursor.")
        traceback.print_exc()

# Creating a function that closes the cursor
def close_cursor(cursor):
    # Checking to see if the cursor was initially created and if it wasn't, don't attempt to close the cursor
    if(cursor == None):
        return True
    try:
        cursor.close()
        return True
    except mariadb.InternalError:
        print("Internal errors detected in the database. Failed to create a cursor.")
        traceback.print_exc()
    except mariadb.OperationalError:
        print("Operational errors detected in the database connection. Failed to create a cursor.")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("Errors detected with the current connection. Failed to close cursor.")
        traceback.print_exc()
    except:
        print("An error has occured. Failed to close cursor.")
        traceback.print_exc()
        return False

# Creating a function that closes the database connection
def close_db_connection(conn):
    # If the database connect was not initially opened, don't attempt to close it
    if(conn == None):
        return True
    try:
        conn.close()
        return True
    except mariadb.OperationalError:
        print("Optional errors detected in the database. Failed to close the connection.")
        traceback.print_exc()
    except mariadb.DatabaseError:
        print("Errored detected in the database. Failed to close the connection.")
        traceback.print_exc()
    except:
        print("An error has occured. Failed to close database connection.")
        traceback.print_exc()
        return False