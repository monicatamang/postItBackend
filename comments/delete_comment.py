from flask import Flask, request, Response
import traceback
import dbstatements

# Creating a function that deletes a comment
def delete_comment():
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
        return Response("Invalid login token and/or tweet content.", mimetype="text/plain", status=400)

    # Trying to delete the comment with the given login token and comment id
    row_count = dbstatements.run_delete_statement("DELETE c FROM user_session us INNER JOIN comment c ON us.user_id = c.user_id WHERE us.token = ? AND c.id = ?", [login_token, comment_id])

    # If the comment was deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the comment was not deleted, send a server error response
    else:
        return Response("Failed to delete comment.", mimetype="text/plain", status=500)