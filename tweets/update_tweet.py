from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a tweet
def update_tweet():
    # Trying to get the user's data
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
        content = request.json['content']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid user id and/or tweet id.", mimetype="text/plain", status=400)

    # Trying to update the user's tweet with the login token, tweet id and content
    row_count = dbstatements.run_update_statement("UPDATE user_session us INNER JOIN tweet t ON t.user_id = us.user_id SET t.content = ? WHERE us.token = ? AND t.id = ?", [content, login_token, tweet_id])

    # If the user's tweet got updated, send the updated tweet
    if(row_count == 1):
        tweet = {
            'tweetId': tweet_id,
            'content': content
        }
        # Convert data to JSON
        tweet_json = json.dumps(tweet, default=str)
        # Send a client success response
        return Response(tweet_json, mimetype="application/json", status=200)
    # If the user's tweet did not get updated, send a server error response
    else:
        return Response("Failed to update tweet.", mimetype="text/plain", status=500)