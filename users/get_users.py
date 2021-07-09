from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function to get all users or one user from the database
def get_users():
    # Trying to get the user's id
    try:
        user_id = request.args.get('userId')
        # If the user id is valid, convert it into an integer
        if(user_id != None):
            user_id = int(user_id)
            # Checking to see if the user exists
            db_user_id = dbstatements.run_select_statement("SELECT id FROM users WHERE id = ?", [user_id,])
            # If the user does not exist in the database, send a client error response
            if(len(db_user_id) != 1):
                return Response("User does not exist.", mimetype="text/plain", status=401)
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
        print("An error has occurred.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)

    # If the user does not send a user id, return all users
    if(user_id == None):
        users = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users", [])
    # If the user does send a user id, return one user with that user id
    else:
        users = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [user_id,])

    # If the database does not return users, send a server error response
    if(users == None):
        return Response("Failed to return data.", mimetype="application/json", status=500)
    # If the database returns users, send users as a list of dictionaries
    else:
        users_list = []
        for user in users:
            each_user = {
                'userId': user[0],
                'email': user[1],
                'username': user[2],
                'bio': user[3],
                'birthdate': user[4],
                'imageUrl': user[5],
            }
            users_list.append(each_user)
        # Convert data to JSON
        users_list_json = json.dumps(users_list, default=str)
        # Send a client success response with the JSON data
        return Response(users_list_json, mimetype="application/json", status=200)