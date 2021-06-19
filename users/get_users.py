from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Getting all users or one user from the database
def get_users():
    try:
        user_id = request.args.get('userId')
        if(user_id != None):
            user_id = int(user_id)
    except IndexError:
        traceback.print_exc()
        print("User does not exist in the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid id.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid id.", mimetype="text/plain", status=400)

    # If a user id is not sent, send all users back
    if(user_id == None):
        all_users = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users", [])

        # If the database does not return all users, send a server error response
        if(all_users == None):
            return Response("Failed to retrieve all users.", mimetype="application/json", status=500)
        # If the database returns all users, send all users as a list of dictionaries
        else:
            users = []
            for user in all_users:
                each_user = {
                    'userId': user[0],
                    'email': user[1],
                    'username': user[2],
                    'bio': user[3],
                    'birthdate': user[4],
                    'imageUrl': user[5],
                }
                users.append(each_user)
            # Convert data to JSON
            users_json = json.dumps(users, default=str)
            # Send a client success response
            return Response(users_json, mimetype="application/json", status=200)
    # If a user id is sent, send back the user with the user id
    else:
        one_user = dbstatements.run_select_statement("SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [user_id,])

        # If the database does not return a user, send a server error response
        if(one_user == None):
            return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
        # If the database returns a user, send the user as a dictionary
        else:
            try:
                user = [
                    {
                        'userId': one_user[0][0],
                        'email': one_user[0][1],
                        'username': one_user[0][2],
                        'bio': one_user[0][3],
                        'birthdate': one_user[0][4],
                        'imageUrl': one_user[0][5],
                    }
                ]
                # Convert data to JSON
                user_json = json.dumps(user, default=str)
                # Send a client success response
                return Response(user_json, mimetype="application/json", status=200)
            except IndexError:
                traceback.print_exc()
                print("User does not exist in the database.")
                return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
            except UnboundLocalError:
                traceback.print_exc()
                print("Data Error. Referencing variables that are not declared.")
                return Response("Invalid id.", mimetype="text/plain", status=500)
            except TypeError:
                traceback.print_exc()
                print("Data Error. Invalid data type sent to the database.")
                return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
            except ValueError:
                traceback.print_exc()
                print("Invalid data was sent to the database.")
                return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
            except:
                traceback.print_exc()
                print("An error has occured.")