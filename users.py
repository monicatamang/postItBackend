from flask import Flask, request, Response
import traceback
import dbstatements
import json
import user_token

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
        all_users = dbstatements.run_select_statement("SELECT id, username, email, bio, birthdate, image_url FROM users", [])

        # If the database does not return all users, send a server error response
        if(all_users == None):
            return Response("Failed to retrieve all users.", mimetype="application/json", status=500)
        # If the database returns all users, send all users as a list of dictionaries
        else:
            users = []
            for user in all_users:
                each_user = {
                    'userId': user[0],
                    'username': user[1],
                    'email': user[2],
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
        one_user = dbstatements.run_select_statement("SELECT id, username, email, bio, birthdate, image_url FROM users WHERE id = ?", [user_id,])

        # If the database does not return a user, send a server error response
        if(one_user == None):
            return Response(f"Failed to get user with id of {user_id}.", mimetype="text/plain", status=500)
        # If the database returns a user, send the user as a dictionary
        else:
            try:
                user = [
                    {
                        'userId': one_user[0][0],
                        'username': one_user[0][1],
                        'email': one_user[0][2],
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

# Creating a user
def create_user():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        bio = request.json.get("bio")
        birthdate = request.json["birthdate"]
        image_url = request.json.get("imageUrl")
        
        if(username == None or email == None or password == None or birthdate == None):
            return Response("Invalid Data.", mimetype="text/plain", status=400)
    except IndexError:
        traceback.print_exc()
        print("User does not exist in the database.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
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

    user_id = dbstatements.run_insert_statement("INSERT INTO users(username, email, password, bio, birthdate, image_url) VALUES(?, ?, ?, ?, ?, ?)", [username, email, password, bio, birthdate, image_url])

    if(user_id == None):
        return Response("Database Error. Failed to create a user.", mimetype="text/plain", status=500)
    else:
        token = user_token.get_user_token(user_id)
        if(token != None):
            user_data = {
                'userId': user_id,
                'loginToken': token,
                'username': username,
                'email': email,
                'password': password,
                'bio': bio,
                'birthdate': birthdate,
                'imageUrl': image_url,
            }
            user_data_json = json.dumps(user_data, default=str)
            return Response(user_data_json, mimetype="application/json", status=201)
        else:
            return Response("Invalid Data.", mimetype="text/plain", status=500)

def delete_user():
    try:
        token = request.json['loginToken']
        password = request.json['password']
    except IndexError:
        traceback.print_exc()
        print("Token or password does not exist in the database.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect Key name of data.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)
    except UnboundLocalError:
        traceback.print_exc()
        print("Data Error. Referencing variables that are not declared.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)
    except TypeError:
        traceback.print_exc()
        print("Data Error. Invalid data type sent to the database.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid token and/or password.", mimetype="text/plain", status=400)

    # Check if the user's token and password matches with the database records
    db_records = dbstatements.run_select_statement("SELECT us.token, u.password, u.id FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE us.token = ? AND u.password = ?", [token, password])

    # If there wasn't a match, send a server error response
    if(db_records == None):
        return Response("Failed to delete user.", mimetype="text/plain", status=500)
    # If there was a match, delete the user and send a client success response
    else:
        # Catching errors with the database records being out of range
        try:
            user_id = db_records[0][2]
            row_count = dbstatements.run_delete_statement("DELETE FROM users WHERE id = ?", [user_id,])
            if(row_count != None):
                return Response("Successfully deleted user.", mimetype="text/plain", status=204)
        except IndexError:
            traceback.print_exc()
            print("Token or password does not exist in the database.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        except KeyError:
            traceback.print_exc()
            print("Key Error. Incorrect Key name of data.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        except UnboundLocalError:
            traceback.print_exc()
            print("Data Error. Referencing variables that are not declared.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        except TypeError:
            traceback.print_exc()
            print("Data Error. Invalid data type sent to the database.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        except ValueError:
            traceback.print_exc()
            print("Invalid data was sent to the database.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)
        except:
            traceback.print_exc()
            print("An error has occured.")
            return Response("Failed to delete user.", mimetype="text/plain", status=500)