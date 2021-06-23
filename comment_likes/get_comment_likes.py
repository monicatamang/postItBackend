from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that gets comment likes
def get_comment_likes():
    # Trying to get the user's comment id
    try:
        comment_id = request.args.get('commentId')
        # If the user sends a comment id, convert into an integer
        if(comment_id != None):
            comment_id = int(comment_id)
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
        return Response("Invalid comment id.", mimetype="text/plain", status=400)

    # If the user doesn't send a comment id, get all comment likes
    if(comment_id == None):
        comment_likes = dbstatements.run_select_statement("SELECT cl.id, cl.user_id, u.username FROM users u INNER JOIN comment_likes cl ON cl.user_id = u.id", [])
    # If the user does send a comment id, check if the commend id exist in the database
    else:
        db_comment_id = dbstatements.run_select_statement("SELECT id FROM comment WHERE id = ?", [comment_id,])
        # If the comment id does exist in the database, get the comment likes based on the comment id
        if(len(db_comment_id) == 1):
            comment_likes = dbstatements.run_select_statement("SELECT cl.id, cl.user_id, u.username FROM users u INNER JOIN comment_likes cl ON cl.user_id = u.id WHERE cl.comment_id = ?", [comment_id,])
        # If the comment id doesn't exist in the database, send a client error response
        else:
            return Response(f"Failed to get comment likes from comment with an id of {comment_id}.", mimetype="text/plain", status=400)

    # If the comment likes are not retrieved from the database, send a server error response
    if(comment_likes == None):
        return Response(f"Failed to retrieve comment likes on comment {comment_id}.", mimetype="text/plain", status=500)
    # If the comment likes are retrieved from the database, send the comment likes as a list of dictionaries
    else:
        comment_likes_list = []
        for like in comment_likes:
            each_comment_like = {
                'commentId': like[0],
                'userId': like[1],
                'username': like[2]
            }
            comment_likes_list.append(each_comment_like)
        # Convert data to JSON
        comment_likes_json = json.dumps(comment_likes_list, default=str)
        # Send a client success response with the comment likes
        return Response(comment_likes_json, mimetype="application/json", status=200)