from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a new tweet
def post_tweet():
    # Trying to get the user's login token and tweet content
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
    except IndexError:
        traceback.print_exc()
        print("Login token and/or tweet content does not exist in the database.")
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
        return Response("Invalid login token and/or tweet content.", mimetype="text/plain", status=400)
    
    # Validating the user's login token
    check_user_login = dbstatements.run_select_statement("SELECT user_id, token FROM user_session WHERE token = ?", [login_token,])

    # If the user's login token is valid, create a new tweet
    if(len(check_user_login) == 1):
        tweet_id = dbstatements.run_insert_statement("INSERT INTO tweet(content, user_id) VALUES(?, ?)", [content, check_user_login[0][0]])
        # If a new tweet id is not created, send a server error response
        if(tweet_id == None):
            return Response("Failed to create tweet.", mimetype="text/plain", status=500)
        # If a new tweet id is created, get the new tweet from the database
        else:
            get_new_tweet = dbstatements.run_select_statement("SELECT t.id, u.id, u.username, u.image_url, t.content, t.created_at FROM users u INNER JOIN tweet t ON t.user_id = u.id WHERE t.id = ?", [tweet_id,])
            # If the new tweet is retrieved from the database, send the new tweet to the user
            if(len(get_new_tweet) == 1):
                new_tweet = {
                    'tweetId': get_new_tweet[0][0],
                    'userId': get_new_tweet[0][1],
                    'username': get_new_tweet[0][2],
                    'userImageUrl': get_new_tweet[0][3],
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
    # If the user's login token is not valid, send a server error response
    else:
        return Response("User not logged in.", mimetype="text/plain", status=500)