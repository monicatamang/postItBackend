from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function to get a list of all follows
def get_all_follows():
    # Trying to get the user's id
    try:
        user_id = int(request.args['userId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
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
        return Response("Failed to follow user.", mimetype="text/plain", status=400)

    # Checking to see if the user exists
    db_user_id = dbstatements.run_select_statement("SELECT id FROM users WHERE id = ?", [user_id,])

    # If the user exists in the database, get the user's follows
    if(len(db_user_id) == 1):
        # Getting all the user's follows
        follows = dbstatements.run_select_statement("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url FROM users u INNER JOIN follow f ON u.id = f.follow_id WHERE f.follower_id = ?", [user_id,])
        
        # If the list of follows is not found in the database, send a server error response
        if(follows == None):
            return Response("Failed to get all follows.", mimetype="text/plain", status=500)
        # If the list of follows is found in the database, send the data for each follow as list of dictionaries
        else:
            user_follows = []
            for follow in follows:
                each_follow = {
                    'userId': follow[0],
                    'email': follow[1],
                    'username': follow[2],
                    'bio': follow[3],
                    'birthdate': follow[4],
                    'imageUrl': follow[5]
                }
                user_follows.append(each_follow)
            # Convert data into JSON
            user_follows_json = json.dumps(user_follows, default=str)
            # Send JSON data and a client success response
            return Response(user_follows_json, mimetype="application/json", status=200)
    # If the user does not exist in the database, send a client error response
    else:
        return Response("User does not exist.", mimetype="text/plain", status=400)