from flask import Flask, request, Response
import traceback
import dbstatements

# Logging out user
def logout_user():
    # Receiving the login token from the user
    try:
        login_token = request.json['loginToken']
    except IndexError:
            traceback.print_exc()
            print("User does not exist in the database.")
            return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect key.")
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
        return Response("Invalid id.", mimetype="text/plain", status=400)

    # Check if the user's token was deleted
    row_count = dbstatements.run_delete_statement("DELETE FROM user_session WHERE token = ?", [login_token,])
    # If the user's token was deleted, send a client success response
    if(row_count == 1):
        return Response("Succesfully logged out.", mimetype="text/plain", status=204)
    # If the user's token was not deleted, send a server error response
    else:
        return Response("Failed to log out.", mimetype="text/plain", status=500)