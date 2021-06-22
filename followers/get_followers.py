from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function to get a list of all followers
def get_all_followers():
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

    # Getting all the user's followers
    followers = dbstatements.run_select_statement("SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url FROM users u INNER JOIN follow f on u.id = f.follower_id WHERE f.follow_id = ?", [user_id,])
    
    # If the list of followers is not found in the database, send a server error response
    if(followers == None):
        return Response("Failed to get all follows.", mimetype="text/plain", status=500)
    # If the list of followers is found in the database, send the data for each follower as a list of dictionaries
    else:
        user_followers = []
        for follower in followers:
            each_follower = {
                'userId': follower[0],
                'email': follower[1],
                'username': follower[2],
                'bio': follower[3],
                'birthdate': follower[4],
                'imageUrl': follower[5]
            }
            user_followers.append(each_follower)
        # Convert data into JSON
        user_followers_json = json.dumps(user_followers, default=str)
        # Send JSON data and a client success response
        return Response(user_followers_json, mimetype="application/json", status=200)