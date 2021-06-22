from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function to get all users or one user from the database
def get_users():
    try:
        user_id = request.args.get('userId')
        # If the user id is valid, convert it into an integer
        if(user_id != None):
            user_id = int(user_id)
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
        return Response("Failed to get users.", mimetype="text/plain", status=400)

    # If a user id is not sent, send all users back
    if(user_id == None):
        users = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users", [])
    # If a user id is send, send one user back
    else:
        users = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [user_id])

    # If the database does not return all users, send a server error response
    if(get_users == None):
        return Response("Failed to retrieve all users.", mimetype="application/json", status=500)
    # If the database returns all users, send all users as a list of dictionaries
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
        users_list_json = json.dumps(users, default=str)
        # Send a client success response
        return Response(users_list_json, mimetype="application/json", status=200)