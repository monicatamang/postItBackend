from flask import Flask, request, Response
import mariadb
import traceback
import dbconnect
import dbcheck
import secrets

def get_user_token(user_id):
    # Open database and create a cursor
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)
    # Initalize the result to None and create a token
    result = None
    token = secrets.token_urlsafe(60)

    # Check if the database connection is still open
    check_database = dbcheck.check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    # Try to to insert the new token into the database
    try:
        cursor.execute("INSERT INTO user_session(user_id, token) VALUES(?, ?)", [user_id, token])
        conn.commit()
        result = cursor.rowcount
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Unique key constraint failure. Username or Email already exists in the database.")
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An operational error has occured when creating the user.")
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured. Failed to create user.")
    except:
        traceback.print_exc()
        print("An error has occured.")

    # Closing the cursor and database connection
    dbcheck.close_db_connection_and_cursor(conn, cursor)
    # If a new row is created in the 'user_session' table, return the token
    if(result == 1):
        return token
    # If a new row is not created, return None
    else:
        return None