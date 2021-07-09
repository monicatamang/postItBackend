from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a new tweet
def post_tweet():
    # Trying to get the user's login token and tweet content
    try:
        login_token = request.json['loginToken']
        content = request.json['content']

        # If the user creates a tweet without content, send a client error response
        if(login_token == "" or content == ""):
            return Response("Invalid tweet.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)
    
    # Getting the user's id from the database
    user_id = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user's id is retrieved from the database, create a new tweet
    if(len(user_id) == 1):
        tweet_id = dbstatements.run_insert_statement("INSERT INTO tweet(content, user_id) VALUES(?, ?)", [content, user_id[0][0]])
        # If a new tweet id is not created, send a server error response
        if(tweet_id == None):
            return Response("Failed to create tweet.", mimetype="text/plain", status=500)
        # If a new tweet id is created, get the new tweet from the database
        else:
            get_new_tweet = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, u.image_url, t.content, t.created_at FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE t.id = ?", [tweet_id,])
            # If the new tweet is retrieved from the database, return the new tweet as a dictionary
            if(len(get_new_tweet) == 1):
                new_tweet = {
                    'tweetId': get_new_tweet[0][0],
                    'userId': get_new_tweet[0][1],
                    'username': get_new_tweet[0][2],
                    'imageUrl': get_new_tweet[0][3],
                    'content': get_new_tweet[0][4],
                    'createdAt': get_new_tweet[0][5]
                }
                # Convert data to JSON
                new_tweet_json = json.dumps(new_tweet, default=str)
                # Send a client success response with the new tweet
                return Response(new_tweet_json, mimetype="application/json", status=201)
            # If the new tweet is not retrieved from the database, send a server error response
            else:
                return Response("Failed to create tweet.", mimetype="text/plain", status=500)
    # If the user's id is not retrieved from the database, send a server error response
    else:
        return Response("User not logged in.", mimetype="text/plain", status=403)