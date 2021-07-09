from flask import request, Response
import traceback
import dbstatements

# Creating a function that logs out a user
def logout_user():
    # Trying to get the user's login token
    try:
        login_token = request.json['loginToken']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid login token.", mimetype="text/plain", status=400)

    # Checking to see if the user's token is deleted
    row_count = dbstatements.run_delete_statement("DELETE FROM user_session WHERE token = ?", [login_token,])
    # If the user's token is deleted, send a client success response
    if(row_count == 1):
        return Response(status=204)
    # If the user's token is not deleted, send a server error response
    else:
        return Response("Failed to log out.", mimetype="text/plain", status=500)