from flask import Flask, request, Response
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
        # If the user sends a tweet id, convert it into an integer
        if(tweet_id != None):
            tweet_id = int(tweet_id)
    except IndexError:
        traceback.print_exc()
        print("User and/or tweet does not exist in the database.")
        return Response("User and/or tweet does not exist.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
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

    # If the user does not send a user id or tweet id, get all tweets from the database
    if(user_id == None and tweet_id == None):
        tweets = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id", [])
        # If the tweets are unable to be retrieved from the database, send a server error response
        if(tweets == None):
            return Response("Failed to retrieve all tweets.", mimetype="text/plain", status=500)
        # If the tweets are retrieved from the database, send all tweets as a list of dictionaries
        else:
            all_tweets = []
            for tweet in tweets:
                each_tweet = {
                    'tweetId': tweet[0],
                    'userId': tweet[1],
                    'username': tweet[2],
                    'content': tweet[3],
                    'createdAt': tweet[4],
                    'imageUrl': tweet[5]
                }
                all_tweets.append(each_tweet)
            # Convert data to JSON
            all_tweets_json = json.dumps(all_tweets, default=str)
            # Send a client success response with the JSON data
            return Response(all_tweets_json, mimetype="application/json", status=200)
    # If the user sends just the user id, get all tweets that belongs to that user id
    elif(user_id != None):
        user_tweets = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE u.id = ?", [user_id,])
        # If the tweets owned by the user id are not retrieved from the database, send a server error response
        if(user_tweets == None):
            return Response(f"Failed to retrieve tweet(s) by user {user_id}.", mimetype="text/plain", status=500)
        # If the tweets owned by the user id are retrieved from the database, send all the user's tweets as a list of dictionaries
        else:
            all_user_tweets = []
            for tweet in user_tweets:
                each_tweet = {
                    'tweetId': tweet[0],
                    'userId': tweet[1],
                    'username': tweet[2],
                    'content': tweet[3],
                    'createdAt': tweet[4],
                    'imageUrl': tweet[5]
                }
                all_user_tweets.append(each_tweet)
            # Convert data to JSON
            all_tweets_json = json.dumps(all_user_tweets, default=str)
            # Send a client success response with the JSON data
            return Response(all_tweets_json, mimetype="application/json", status=200)
    # If the user just sends the tweet id, get the tweet with that tweet id
    elif(tweet_id != None):
        tweet = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, t.content, t.created_at, u.image_url FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE t.id = ? AND u.id", [tweet_id, user_id])
        # If the tweet exists in the database, send the tweet as a dictionary inside a list
        if(len(tweet) == 1):
            one_tweet = [
                {
                    'tweetId': tweet[0][0],
                    'userId': tweet[0][1],
                    'username': tweet[0][2],
                    'content': tweet[0][3],
                    'createdAt': tweet[0][4],
                    'imageUrl': tweet[0][5]
                }
            ]
            # Convert data to JSON
            one_tweet_json = json.dumps(one_tweet, default=str)
            # Send a client success response with the JSON data
            return Response(one_tweet_json, mimetype="application/json", status=200)
        # If the tweet does not exist in the datbase, send a server error response
        else:
            return Response(f"Failed to retrieve tweet with an id of {tweet_id}.", mimetype="text/plain", status=500)