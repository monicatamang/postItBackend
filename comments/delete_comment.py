from flask import request, Response
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
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occurred.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)

    # Checking to see if the comment is deleted given the given login token and comment id
    row_count = dbstatements.run_delete_statement("DELETE c FROM user_session us INNER JOIN comment c ON us.user_id = c.user_id WHERE us.token = ? AND c.id = ?", [login_token, comment_id])

    # If the comment is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the comment is not deleted, send a server error response
    else:
        return Response("Failed to delete comment.", mimetype="text/plain", status=500)