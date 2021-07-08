from flask import request, Response
import traceback
import dbstatements

# Creating a function that deletes a tweet
def delete_tweet():
    # Trying to get the user's login token and tweet id
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
        return Response("Invalid user id and/or tweet id.", mimetype="text/plain", status=400)

    # Trying to delete the user's tweet with the login token and tweet id
    row_count = dbstatements.run_delete_statement("DELETE t FROM user_session us INNER JOIN tweet t ON t.user_id = us.user_id WHERE us.token = ? AND t.id = ?", [login_token, tweet_id])
    # If the tweet was deleted, send a client success response
    if(row_count == 1):
        return Response (status=204)
    # If the tweet was not deleted, send a server error response
    else:
        return Response(f"Failed to delete tweet with an id of {tweet_id}.", mimetype="application/json", status=500)