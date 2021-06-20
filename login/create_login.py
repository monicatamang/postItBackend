from flask import Flask, request, Response
import traceback
import dbstatements
import json
import user_token

# Creating a function to logs in a user
def login_user():
    # Trying to log the user in with their email and password
    try:
        email = request.json['email']
        password = request.json['password']
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
        return Response("Invalid email and/or password.", mimetype="text/plain", status=400)

    # If the user did not send an eamil or password, send a server error response
    if(email == "" or password == ""):
        return Response("User Data Error.", mimetype="text/plain", status=400)

    # Check if the user's email and password matches with the database records
    db_records = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users WHERE email = ? AND password = ?", [email, password])
    
    # If their email and password matches, create a login token
    if(len(db_records) == 1):
        token = user_token.get_user_token(db_records[0][0])
        # If a login token is made, send the user their data with the login token
        if(token != None):
            user_data = {
                'user_id': db_records[0][0],
                'email': db_records[0][1],
                'username': db_records[0][2],
                'bio': db_records[0][3],
                'birthdate': db_records[0][4],
                'imageUrl': db_records[0][5],
                'loginToken': token
            }
            # Convert data to JSON
            user_data_json = json.dumps(user_data, default=str)
            # Send a client success response
            return Response(user_data_json, mimetype="application/json", status=201)
        # If a login token is not created, send a server error response
        else:
            return Response("Failed to log in.", mimetype="text/plain", status=500)
    # If their email and password does not match, send a server error response
    else:
        return Response("Failed to log in.", mimetype="text/plain", status=500)