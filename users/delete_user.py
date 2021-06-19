from flask import Flask, request, Response
import traceback
import dbstatements

# Deleting a user
def delete_user():
    # Receiving the token and password from the user
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