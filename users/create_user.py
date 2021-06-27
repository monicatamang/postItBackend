from flask import Flask, request, Response
import traceback
import dbstatements
import json
import user_token
import hashlib
import dbsalt

# Creating a function to create a new user
def create_user():
    # Receiving the data from the user
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        bio = request.json.get("bio")
        birthdate = request.json["birthdate"]
        image_url = request.json.get("imageUrl")
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Failed to create user.", mimetype="text/plain", status=400)

    # If the username, email, password or birthdate is not received, send a client error response
    if(username == None or email == None or password == None or birthdate == None):
        return Response("Invalid Data.", mimetype="text/plain", status=400)

    # Hashing and salting the user's password
    salt = dbsalt.create_salt()
    password = salt + password
    password = hashlib.sha512(password.encode()).hexdigest()

    # Inserting the user's data into the database and getting the new user's id
    user_id = dbstatements.run_insert_statement("INSERT INTO users(username, email, password, bio, birthdate, image_url, salt) VALUES(?, ?, ?, ?, ?, ?, ?)", [username, email, password, bio, birthdate, image_url, salt])

    # If user's id is not created, send a server error response
    if(user_id == None):
        return Response("Database Error. Failed to create a user.", mimetype="text/plain", status=500)
    # If the user's id is created, create a token 
    else:
        token = user_token.get_user_token(user_id)
        # If the token is created, send the user their data as a dictionary
        if(token != None):
            user_data = {
                'userId': user_id,
                'loginToken': token,
                'email': email,
                'username': username,
                'bio': bio,
                'birthdate': birthdate,
                'imageUrl': image_url,
            }
            # Convert data to JSON
            user_data_json = json.dumps(user_data, default=str)
            # Send a client success response
            return Response(user_data_json, mimetype="application/json", status=201)
        # If the token is not created, send a server error response
        else:
            return Response("Invalid Data.", mimetype="text/plain", status=500)