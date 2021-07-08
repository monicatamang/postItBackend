from flask import request, Response
import traceback
import dbstatements
import json

# Creating a function that updates a comment
def update_comment():
    # Trying to get the user's login token, comment id and comment content
    try:
        login_token = request.json['loginToken']
        comment_id = int(request.json['commentId'])
        content = request.json['content']
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
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
        return Response("Invalid tweet id.", mimetype="text/plain", status=400)

    # Trying to update the user's comment with the given data
    row_count = dbstatements.run_update_statement("UPDATE user_session us INNER JOIN comment c ON c.user_id = us.user_id SET c.content = ? WHERE us.token = ? AND c.id = ?", [content, login_token, comment_id])

    # If the user's content was updated, try to get the updated comment from the database
    if(row_count == 1):
        updated_comment = dbstatements.run_select_statement("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM users u INNER JOIN comment c ON c.user_id = u.id WHERE c.id = ?", [comment_id,])
        # If the update comment was retrieved from the database, send the updated comment to the user
        if(len(updated_comment) == 1):
            user_comment = {
                'commentId': updated_comment[0][0],
                'tweetId': updated_comment[0][1],
                'userId': updated_comment[0][2],
                'username': updated_comment[0][3],
                'content': updated_comment[0][4],
                'createdAt': updated_comment[0][5]
            }
            # Convert data into JSON
            user_comment_json = json.dumps(user_comment, default=str)
            # Send a client success response with the updated comment
            return Response(user_comment_json, mimetype="application/json", status=200)
        # If the updated comment was not retrieved from the database, send a server error response
        else:
            return Response("Failed to update comment.", mimetype="text/plain", status=500)
    # If the user's comment was not updated, send a server error response
    else:
        return Response("Failed to update comment.", mimetype="text/plain", status=500)