from flask import request, Response
import traceback
import dbstatements
import dbsalt
import hashlib

# Creating a function to delete an existing user
def delete_user():
    # Trying to get the user's token and password
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

    # Trying to get the user's email from the database given the login token
    email = dbstatements.run_select_statement("SELECT email FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ?", [token,])
    # If the email is retrieved from the database, get the user's salt from the database and hash the password
    if(len(email) == 1):
        salt = dbsalt.get_salt(email[0][0])
        # If the user's salt is not retrieved from the database, send a server error response
        if(salt == None):
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        # If the user's salt is retrieved from the database, hash and salt the user's password
        else:
            password = salt + password
            password = hashlib.sha512(password.encode()).hexdigest()
    # If the email is not retrieved from the database, send a server error response
    else:
        return Response("User not logged in.", mimetype="text/plain", status=500)

    # If the user was deleted, send a client success response
    row_count = dbstatements.run_delete_statement("DELETE u FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ? AND u.password = ?", [token, password])
    if(row_count == 1):
        return Response(status=204)
    # If the user was not deleted, send a server error response
    else:
        return Response("Failed to delete user.", mimetype="text/plain", status=500)