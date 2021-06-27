from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that will return all search results or specific search results based on the username
def search_by_username():
    # Trying to get the username from the user
    try:
        search_input = request.args.get('searchInput')
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid login token and/or tweet id.", mimetype="text/plain", status=400)

    # If the user doesn't send any data, i.e., if the user doesn't type anything into the search bar, send all users
    if(search_input == None):
        results = dbstatements.run_select_statement("SELECT id, username, bio, image_url FROM users", [])
    # If the user does send data, i.e., they type in a username into the search bar, try to find all records that matches or closely matches that username
    else:
        results = dbstatements.run_select_statement("SELECT id, username, bio, image_url FROM users WHERE username LIKE CONCAT('%', ?, '%')", [search_input,])

    # If something goes wrong in the database, ex. database connection failure, send a server error response
    if(results == None):
        return Response(f"Failed to find '{search_input}'.", mimetype="text/plain", status=500)
    # If a match is found, send all matches as a list of dictionaries
    # If no matches are found, an empty list will be returned
    else:
        search_results = []
        for result in results:
            each_result = {
                'userId': result[0],
                'username': result[1],
                'bio': result[2],
                'imageUrl': result[3]
            }
            search_results.append(each_result)
        # Convert data into JSON
        search_results_json = json.dumps(search_results, default=str)
        # Send a client success response with the JSON data
        return Response(search_results_json, mimetype="application/json", status=200)