from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that gets tweets from the database
def get_tweets():
    # Trying to get the user id and tweet id
    try:
        user_id = request.args.get('userId')
        tweet_id = request.args.get('tweetId')
        # If the user sends a user id, convert it into an integer
        if(user_id != None):
            user_id = int(user_id)
            # Checking to see if the user exists
            db_user_id = dbstatements.run_select_statement("SELECT id FROM users WHERE id = ?", [user_id,])
            # If the user does not exist in the database, send a client error response
            if(len(db_user_id) != 1):
                return Response("User does not exist.", mimetype="text/plain", status=401)
        # If the user sends a tweet id, convert it into an integer
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
        return Response("An error has occurred.", mimetype="text/plain", status=400)

    # If the user does not send a user id or tweet id, get all tweets from the database
    if(user_id == None and tweet_id == None):
        tweets = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id ORDER BY t.created_at DESC", [])
    # If the user sends only the user id, get tweets that are owned by the user id
    elif(user_id != None):
        tweets = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE u.id = ? ORDER BY t.created_at DESC", [user_id,])
    # If the user sends only the tweet id, get tweet with that tweet id
    elif(tweet_id != None):
        tweets = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE t.id = ?", [tweet_id,])

    # If tweets are not retrieved from the database, send a server error response
    if(tweets == None):
        return Response("Failed to retrieve tweets.", mimetype="text/plain", status=500)
    # If tweets are retrieved from the database, return tweets as a list of dictionaries
    else:
        tweets_list = []
        for tweet in tweets:
            each_tweet = {
                'tweetId': tweet[0],
                'userId': tweet[1],
                'username': tweet[2],
                'content': tweet[3],
                'createdAt': tweet[4],
                'imageUrl': tweet[5]
            }
            tweets_list.append(each_tweet)
        # Convert data to JSON
        all_tweets_json = json.dumps(tweets_list, default=str)
        # Send a client success response with the JSON data
        return Response(all_tweets_json, mimetype="application/json", status=200)