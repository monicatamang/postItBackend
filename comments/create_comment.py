from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that creates a comment
def post_comment():
    # Trying to get the user's login token, tweet id and content
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
        content = request.json['content']

        # If the user sends a login token as an empty string or creates a comment without content, send a client error response
        if(login_token == "" or content == ""):
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occurred.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)

    # Trying to get the user's id based on the login token given
    user_id = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user id is retrieved from the database, insert the comment into the database
    if(len(user_id) == 1):
        comment_id = dbstatements.run_insert_statement("INSERT INTO comment(content, user_id, tweet_id) VALUES(?, ?, ?)", [content, user_id[0][0], tweet_id])
        # If a new id is not created for the comment, send a server error response
        if(comment_id == None):
            return Response("Failed to create comment.", mimetype="text/plain", status=500)
        # If a new id was created for the comment, try to get the new comment from the database
        else:
            new_comment = dbstatements.run_select_statement("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM users u INNER JOIN comment c ON c.user_id = u.id WHERE c.id = ?", [comment_id,])
            # If the new comment is not retrieved from the database, send a server error response
            if(new_comment == None):
                return Response("Failed to create a comment.", mimetype="text/plain", status=500)
            # If the new comment is retrieved from the database, send the new comment to the user as a dictionary
            else:
                user_comment = {
                    'commentId': new_comment[0][0],
                    'tweetId': new_comment[0][1],
                    'userId': new_comment[0][2],
                    'username': new_comment[0][3],
                    'content': new_comment[0][4],
                    'createdAt': new_comment[0][5]
                }
                # Convert data to JSON
                user_comment_json = json.dumps(user_comment, default=str)
                # Send a client success response with the JSON data
                return Response(user_comment_json, mimetype="application/json", status=201)
    # If the user id is not retrieved from the database, send a server error response
    else:
        return Response("User is not logged in.", mimetype="text/plain", status=403)