from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that get tweet likes
def get_tweet_likes():
    # Trying to get the user's tweet id
    try:
        tweet_id = request.args.get('tweetId')
        # If the user sends a valid tweet id, convert it into a integer
        if(tweet_id != None):
            tweet_id = int(tweet_id)
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
        return Response("Invalid user id and/or tweet id.", mimetype="text/plain", status=400)

    # If the tweet id is not given, send all tweet likes on all tweets
    if(tweet_id == None):
        tweet_likes = dbstatements.run_select_statement("SELECT tl.tweet_id, u.id, u.username FROM users u INNER JOIN tweet_likes tl ON tl.user_id = u.id", [])
    # If the tweet id is given, send all tweet likes with the tweet id
    else:
        tweet_likes = dbstatements.run_select_statement("SELECT tl.tweet_id, u.id, u.username FROM users u INNER JOIN tweet_likes tl ON tl.user_id = u.id WHERE tl.tweet_id = ?", [tweet_id,])

    # If the tweet likes are not retrieved from the database, send a server error response
    if(tweet_likes == None):
        return Response(f"Failed to get tweet likes for tweet {tweet_id}.", mimetype="text/plain", status=500)
    # If the tweet likes are retrieved from the database, send the tweet likes
    else:
        tweet_likes_list = []
        for like in tweet_likes:
            each_tweet_like = {
                'tweetId': like[0],
                'userId': like[1],
                'username': like[2]
            }
            tweet_likes_list.append(each_tweet_like)
        # Convert data into JSON
        tweet_likes_json = json.dumps(tweet_likes_list, default=str)
        # Send a client success response with the tweet likes
        return Response(tweet_likes_json, mimetype="application/json", status=200)