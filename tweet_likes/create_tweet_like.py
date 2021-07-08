from flask import request, Response
import traceback
import dbstatements

# Creating a function that creates a like on a tweet
def like_tweet():
    # Trying to the get the user's login token and tweet id
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid login token and/or tweet id.", mimetype="text/plain", status=400)

    # Trying to get the user's id
    user_id = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])
    
    # If the user's id is retrieved from the database, try to create a tweet like
    if(len(user_id) == 1):
        tweet_like_id = dbstatements.run_update_statement("INSERT INTO tweet_like(user_id, tweet_id) VALUES(?, ?)", [user_id[0][0], tweet_id])
        # If a new row is not created in the database, send a server error response
        if(tweet_like_id == None):
            return Response("Failed to like tweet.", mimetype="text/plain", status=500)
        # If a new row is created, send a client success response
        else:
            return Response(status=201)
    # If the user's id is not retrieved from the database, send a server error response
    else:
        return Response("Failed to like tweet.", mimetype="text/plain", status=500)