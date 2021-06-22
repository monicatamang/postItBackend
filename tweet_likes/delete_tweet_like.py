from flask import Flask, request, Response
import traceback
import dbstatements

# Creating a function that creates a like on a tweet
def unlike_tweet():
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

    # Trying to delete a tweet like with the login token and tweet id
    row_count = dbstatements.run_delete_statement("DELETE tl FROM user_session us INNER JOIN tweet_likes tl ON tl.user_id = us.user_id WHERE us.token = ? AND tl.tweet_id = ?", [login_token, tweet_id])

    # If the tweet like is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the tweet like is not deleted, send a server error response
    else:
        return Response("Failed to unlike tweet.", mimetype="text/plain", status=500)