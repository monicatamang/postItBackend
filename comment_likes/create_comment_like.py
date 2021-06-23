from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that likes a comment
def like_comment():
    # Trying to get the user's login token and comment id
    try:
        login_token = request.json['loginToken']
        comment_id = int(request.json['commentId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid comment id.", mimetype="text/plain", status=400)

    # Trying to get the user's id based on the login token
    user_id = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])

    # If the user is logged in, create a comment like based on the user id and comment id
    if(len(user_id) == 1):
        comment_like_id = dbstatements.run_insert_statement("INSERT INTO comment_likes(user_id, comment_id) VALUES(?, ?)", [user_id[0][0], comment_id])

        # If a new row is not created in the database, send a server error response
        if(comment_like_id == None):
            return Response(f"Failed to like commment with an id of {comment_id}.", mimetype="text/plain", status=500)
        # If a new row is created in the database, get the users who liked the comment
        else:
            comment_like_info = dbstatements.run_select_statement("SELECT cl.comment_id, cl.user_id, u.username FROM users u INNER JOIN comment_likes cl ON cl.user_id = u.id WHERE cl.id = ?", [comment_like_id,])
            
            # If the users who liked the comment are retrieved from the database, send the data
            if(len(comment_like_info) == 1):
                comment_like_users = {
                    'commentId': comment_like_info[0][0],
                    'userId': comment_like_info[0][1],
                    'username': comment_like_info[0][2],
                }
                # Convert data into JSON
                comment_like_users_json = json.dumps(comment_like_users, default=str)
                # Send a client success response with the JSON data
                return Response(comment_like_users_json, mimetype="application/json", status=201)
            # If the users who liked the comment are not retrieved from the database, send a server error response
            else:
                return Response("Failed to like comment.", mimetype="text/plain", status=500)
    # If the user is not logged in, send a server error response
    else:
        return Response("Failed to like comment.", mimetype="text/plain", status=500)