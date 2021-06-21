from flask import Flask, request, Response
import traceback
import dbstatements
import json

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
    except IndexError:
        traceback.print_exc()
        print("User does not exist in the database.")
        return Response("Failed to update user with the given data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
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

    # Checking to see if the token is stored in the database
    db_records = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [token,])
    # If the token does not match, send a server error response
    if(db_records == None):
        return Response("Failed to update user.", mimetype="text/plain", status=500)
    # If the token matches with the database records, get the user id
    else:
        user_id = db_records[0][0]

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
        sql += " password = ?,"
        data.append(password)
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