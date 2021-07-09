from flask import request, Response
import traceback
import dbstatements

# Creating a function that unlikes a comment
def unlike_comment():
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

    # Trying to unlike a comment with the given comment id
    row_count = dbstatements.run_delete_statement("DELETE cl FROM user_session us INNER JOIN comment_like cl ON cl.user_id = us.user_id WHERE us.token = ? AND cl.comment_id = ?", [login_token, comment_id])

    # If the comment like is deleted from the database, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the comment like is not deleted from the database, send a server error response
    else:
        return Response("Failed to unlike comment.", mimetype="text/plain", status=500)