from flask import Flask, request, Response
import traceback
import dbstatements

# Creating a function to delete an existing user
def delete_user():
    # Receiving the token and password from the user
    try:
        token = request.json['loginToken']
        password = request.json['password']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)

    # If the user was deleted, send a client success response
    row_count = dbstatements.run_delete_statement("DELETE u FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ? AND u.password = ?", [token, password])
    if(row_count == 1):
        return Response(status=204)
    # If the user was not deleted, send a server error response
    else:
        return Response("Failed to delete user.", mimetype="text/plain", status=500)