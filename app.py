from flask import Flask, request, Response
import mariadb
import dbconnect
import json
import traceback
import secrets
import sys

app = Flask(__name__)

# Creating a function that closes the database connection and the cursor
def close_db_connection_and_cursor(conn, cursor):
    closing_cursor = dbconnect.close_cursor(cursor)
    closing_db = dbconnect.close_db_connection(conn)
    # If the cursor or database connection failed to close, print an error message
    if(closing_cursor == False or closing_db == False):
        print("Failed to close cursor and database connection.")

# If the connection is still open, close the cursor and connection
def check_db_connection_and_cursor(conn, cursor):
    if(conn == None or cursor == None):
        print("An error has occured in the database.")
        dbconnect.close_cursor(cursor)
        dbconnect.close_db_connection(conn)
        return False
    return True

# Getting all users or one user
@app.get("/api/users")
def get_users():
    try:
        user_id = request.args.get('userId')
        if(user_id != None):
            user_id = int(user_id)
    except IndexError:
        traceback.print_exc()
        print("User does not exist in the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    
    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created. If the database connection failed, send a server error response
    check_database = check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    all_users = None
    one_user = None

    try:
        # If no user id is sent, get all users from the database
        if(user_id == None):
            cursor.execute("SELECT id, name, username, email, major, school, bio, birthdate, profile_image_url, banner_url FROM users")
            all_users = cursor.fetchall()
        # If a user id is sent, get the user with that user id
        else:
            cursor.execute("SELECT id, name, username, email, major, school, bio, birthdate, profile_image_url, banner_url FROM users WHERE id = ?", [user_id])
            one_user = cursor.fetchall()
    except IndexError:
        traceback.print_exc()
        print("User does not exist in the database.")
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

    close_db_connection_and_cursor(conn, cursor)

    if(all_users != None):
        users = []
        for user in all_users:
            each_user = {
                'userId': user[0],
                'name': user[1],
                'username': user[2],
                'email': user[3],
                'major': user[4],
                'school': user[5],
                'bio': user[6],
                'birthdate': user[7],
                'profileImageUrl': user[8],
                'bannerUrl': user[9],
            }
            users.append(each_user)
        users_json = json.dumps(users, default=str)
        return Response(users_json, mimetype="application/json", status=200)
    elif(one_user != None):
        try:
            user = [
                {
                    'userId': one_user[0][0],
                    'name': one_user[0][1],
                    'username': one_user[0][2],
                    'email': one_user[0][3],
                    'major': one_user[0][4],
                    'school': one_user[0][5],
                    'bio': one_user[0][6],
                    'birthdate': one_user[0][7],
                    'profileImageUrl': one_user[0][8],
                    'bannerUrl': one_user[0][9],
                }
            ]
            print(user)
            user_json = json.dumps(user, default=str)
            return Response(user_json, mimetype="application/json", status=200)
        except IndexError:
            traceback.print_exc()
            print("User does not exist in the database.")
            return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
        except TypeError:
            traceback.print_exc()
            print("Data Error. Invalid data type sent to the database.")
            return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
        except ValueError:
            traceback.print_exc()
            print("Invalid data was sent to the database.")
            return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
        except:
            traceback.print_exc()
            print("An error has occured.")
    else:
        return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)

# Creating a user
@app.post("/api/users")
def create_user():
    try:
        # try:
        name = request.json.get("name")
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        major = request.json.get("major")
        school = request.json.get("school")
        bio = request.json.get("bio")
        birthdate = request.json["birthdate"]
        profile_image_url = request.json.get("profileImageUrl")
        banner_url = request.json.get("bannerUrl")
        
        if(username == None or email == None or password == None or birthdate == None):
            return Response("Invalid Data.", mimetype="text/plain", status=400)
    except mariadb.DataError:
        traceback.print_exc()
        print("Data Error. Invalid data was sent to the database.")
        return Response("Invalid data. Failed to create user.", mimetype="text/plain", status=400)
    except mariadb.IntegrityError:
        traceback.print_exc()
        print("Unique key constraint failure. Username or Email already exists in the database.")
        return Response("Username or Email already exists in the database.", mimetype="text/plain", status=400)
    except mariadb.OperationalError:
        traceback.print_exc()
        print("An operational error has occured when creating the user.")
        return Response("Failed to create user.", mimetype="text/plain", status=400)
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Invalid SQL syntax.")
        return Response("Failed to create user.", mimetype="text/plain", status=400)
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("An error in the database has occured. Failed to create user.")
        return Response("Failed to create user.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Failed to create user.", mimetype="text/plain", status=400)

    conn = dbconnect.open_db_connection()
    cursor = dbconnect.create_db_cursor(conn)

    # Checking to see if the database connection is opened and whether the cursor is created. If the database connection failed, send a server error response
    check_database = check_db_connection_and_cursor(conn, cursor)
    if(check_database == False):
        return Response("Database connection failed.", mimetype="text/plain", status=500)

    user_id = None
    rows_inserted = None

    try:
        # Run INSERT statement
        cursor.execute("INSERT INTO users(name, username, email, password, major, school, bio, birthdate, profile_image_url, banner_url) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", [name, username, email, password, major, school, bio, birthdate, profile_image_url, banner_url])
        conn.commit()
        user_id = cursor.lastrowid
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

    close_db_connection_and_cursor(conn, cursor)

    if(user_id == None):
        return Response("Database Error. Failed to create a user.", mimetype="text/plain", status=500)
    else:
        try:
            # Getting the user's token
            conn = dbconnect.open_db_connection()
            cursor = dbconnect.create_db_cursor(conn)
            token = secrets.token_urlsafe(60)
            cursor.execute("INSERT INTO user_session(user_id, token) VALUES(?, ?)", [user_id, token])
            conn.commit()
            rows_inserted = cursor.rowcount
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

        close_db_connection_and_cursor(conn, cursor)

        if(rows_inserted == 1):
            user_data = {
                'userId': user_id,
                'token': token,
                'name': name,
                'username': username,
                'email': email,
                'password': password,
                'major': major,
                'school': school,
                'bio': bio,
                'birthDate': birthdate,
                'bannerUrl': banner_url,
            }
            user_data_json = json.dumps(user_data, default=str)
            return Response(user_data_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid Data.", mimetype="text/plain", status=500)

# Creating a mode
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

# Checking which mode is used
if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5001)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()