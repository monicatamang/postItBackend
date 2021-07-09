from flask import Response
import mariadb
import dbconnect
import traceback
import dbcheck

def run_select_statement(sql, params):
    # Opening database and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None
    result = None

    # Checking to see if the database connection is still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    # Trying to run the SELECT statement with the sql and params passed in
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    except IndexError:
        traceback.print_exc()
        print("Data does not exist in the database.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Error in the database.")
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Errors detected in the database and resulted in a connection failure.")
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)
    # Returning the result
    return result

def run_insert_statement(sql, data):
    # Opening database and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None
    result = None

    # Checking to see if the database connection is still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    # Trying to run the INSERT statement with the sql and data passed in
    try:
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.lastrowid
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Constraint failure. Failed to insert data into the database.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Error in the database.")
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured.")
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)
    # Returning the result
    return result

def run_update_statement(sql, data):
    # Opening database and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None
    result = None

    # Checking to see if the database connection is still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    # Trying to run the UPDATE statement with the sql and data passed in
    try:
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.rowcount
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Constraint failure. Failed to update.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Error in the database. Failed to update.")
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured.")
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)
    # Returning the result
    return result

def run_delete_statement(sql, data):
    # Opening database and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalizing the result to None
    result = None

    # Checking if the database connection is still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    # Trying to run the DELETE statment with the sql and data passed in
    try:
        cursor.execute(sql, data)
        conn.commit()
        result = cursor.rowcount
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Constraint failure. Failed to delete.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Error in the database. Failed to delete.")
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured. Failed to delete.")
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)
    # Returning the result
    return result