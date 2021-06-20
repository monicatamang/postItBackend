from flask import Flask, request, Response
import traceback
import dbstatements

# Creating a function to follow other users
def follow_user():
    # Receiving data from the user
    try:
        login_token = request.json['loginToken']
        follow_id = int(request.json['followId'])
    except IndexError:
        traceback.print_exc()
        print("User or login token does not exist in the database.")
        return Response("User or login token does not exist.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
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
        return Response("Failed to follow user.", mimetype="text/plain", status=400)

    # Getting the user id of the user who is currently logged in
    user_id = dbstatements.run_select_statement("SELECT user_id FROM user_session WHERE token = ?", [login_token,])
    
    # If the user id is able to be retrieved from the database, insert the user id and follow id into the database
    if(len(user_id) == 1):
        is_id_created = dbstatements.run_insert_statement("INSERT INTO follow(follower_id, follow_id) VALUES(?, ?)", [user_id[0][0], follow_id])
        # If a new id in the 'follow' table is not created, send a server error response
        if(is_id_created == None):
            return Response(f"Failed to follow user with an id of {follow_id}.", mimetype="text/plain", status=500)
        # If a new id is created, send a client success response
        else:
            return Response(f"Successfully followed user with an of {follow_id}.", mimetype="text/plain", status=204)
    # If the user id was not able to be retrieved from the database, send a server error response
    else:
        return Response("User not logged in.", mimetype="text/plain", status=500)