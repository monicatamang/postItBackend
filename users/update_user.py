from flask import Flask, request, Response
import traceback
import dbsalt
import dbstatements
import json
import hashlib

# Creating a function to update a user
def update_user():
    # Receiving user data
    try:
        token = request.json['loginToken']
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        image_url = request.json.get('imageUrl')

        # If the user does not send the token, username, email, password or birthdate, send a client error response
        if(token == None and username == None and email == None and password == None and birthdate == None):
            return Response("Invalid data. Failed to update user.", mimetype="application/json", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Failed to update user.", mimetype="text/plain", status=400)

    # Getting the user's token, bio, birthdate and image from the database
    db_records = dbstatements.run_select_statement("SELECT us.user_id, u.bio, u.birthdate, u.image_url FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE token = ?", [token,])

    # If the token matches with the database records, get the user's data
    if(len(db_records) == 1):
        user_id = db_records[0][0]
        # If the user's bio, birthdate or image url are not updated, set it as the user's initial bio, birthdate or image url
        if(bio == None or bio == ""):
            bio = db_records[0][1]
        if(birthdate == None or birthdate == ""):
            birthdate = db_records[0][2]
        if(image_url == None or image_url == ""):
            image_url = db_records[0][3]
    # If the token does not match, send a server error response
    else:
        return Response("Failed to update user.", mimetype="text/plain", status=500)
    
    # Updating the user based on the data sent
    data = []
    sql = "UPDATE users SET"
    if(email != None):
        sql += " email = ?,"
        data.append(email)
    if(username != None):
        sql += " username = ?,"
        data.append(username)
    if(password != None):
        # If the user wants to change their password, replace the user's existing salt with a new generated salt
        salt = dbsalt.create_salt()
        row_count = dbstatements.run_update_statement("UPDATE users u INNER JOIN user_session us ON us.user_id = u.id SET u.salt = ? WHERE us.token = ?", [salt, token])
        # If the user's salt is updated, hash and salt the new password
        if(row_count == 1):
            password = salt + password
            password = hashlib.sha512(password.encode()).hexdigest()
            sql += " password = ?,"
            data.append(password)
        # If the user's salt is not updated, send a server error response
        else:
            return Response("Failed to update user.", mimetype="text/plain", status=500)
    if(bio != None):
        sql += " bio = ?,"
        data.append(bio)
    if(birthdate != None):
        sql += " birthdate = ?,"
        data.append(birthdate)
    if(image_url != None):
        sql += " image_url = ?,"
        data.append(image_url)

    # Removing the comma at the end of the list
    sql = sql[:-1]
    # Adding the where clause
    sql += " WHERE id = ?"
    # Appending the user id
    data.append(user_id)

    # Checking to see if the user's data has been udpated in the database
    row_count = dbstatements.run_update_statement(sql, data)
    
    # If the user is updated, get the update data from the database
    if(row_count == 1):
        db_updated_records = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [user_id,])
        # If the updated data is not retrieved from the database, send a server error response
        if(db_updated_records == None):
            return Response("Failed to update user.", mimetype="application/json", status=500)
        # If the updated data is retreived from the database, send the updated data as a dictionary
        else:
            updated_data = {
                'userId': db_updated_records[0][0],
                'email': db_updated_records[0][1],
                'username': db_updated_records[0][2],
                'bio': db_updated_records[0][3],
                'birthdate': db_updated_records[0][4],
                'imageUrl': db_updated_records[0][5]
            }
            # Convert updated data into JSON
            updated_data_json = json.dumps(updated_data, default=str)
            # Send client success response
            return Response(updated_data_json, mimetype="application/json", status=200)
    # If the user is not updated, send a server error response
    else:
        return Response("Failed to update user.", mimetype="text/plain", status=500)