from flask import request, Response
import traceback
import dbsalt
import dbstatements
import json
import hashlib

# Creating a function to update a user
def update_user():
    # Trying to get the user's data
    try:
        token = request.json['loginToken']
        username = request.json.get('username')
        email = request.json.get('email')
        password = request.json.get('password')
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        image_url = request.json.get('imageUrl')
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occurred.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)
    
    # Updating the user based on the data sent
    # Initializing the UPDATE query and an empty list to store the values
    sql = "UPDATE users u INNER JOIN user_session us ON u.id = us.user_id SET"
    data = []
    # The following if statements have the same comments applied to them:
    # If the user changes one of their information, add their information to the UPDATE query as a column and append the column value to the list
    if(email != None and username != ''):
        sql += " u.email = ?,"
        data.append(email)
    if(username != None and username != ''):
        sql += " u.username = ?,"
        data.append(username)
    if(password != None and password != ''):
        # If the user wants to change their password, replace the user's existing salt with a new generated salt in the database
        salt = dbsalt.create_salt()
        # Salt and hash the new password
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
        sql += " u.password = ?, u.salt = ?,"
        data.append(password)
        data.append(salt)
    if(bio != None and password != ''):
        sql += " u.bio = ?,"
        data.append(bio)
    if(birthdate != None and password != ''):
        sql += " u.birthdate = ?,"
        data.append(birthdate)
    if(image_url != None and password != ''):
        sql += " u.image_url = ?,"
        data.append(image_url)

    # Removing the comma at the end of the query
    sql = sql[:-1]
    # Adding the where clause to the query
    sql += " WHERE us.token = ?"
    # Appending the token to the list
    data.append(token)

    # Checking to see if the user's data has been udpated in the database
    row_count = dbstatements.run_update_statement(sql, data)
    
    # If the user is updated, get the updated data from the database
    if(row_count == 1):
        db_updated_records = dbstatements.run_select_statement("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ?", [token,])
        # If the updated data is not retrieved from the database, send a server error response
        if(db_updated_records == None):
            return Response("Database Error. Please refresh the page.", mimetype="application/json", status=500)
        # If the updated data is retreived from the database, return the updated data as a dictionary
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
            # Send client success response with the JSON data
            return Response(updated_data_json, mimetype="application/json", status=200)
    # If the user is not updated, send a server error response
    else:
        return Response("Failed to update user.", mimetype="text/plain", status=500)