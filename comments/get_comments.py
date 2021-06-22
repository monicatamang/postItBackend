from flask import Flask, request, Response
import traceback
import dbstatements
import json

# Creating a function that will get comments from a tweet
def get_comments():
    # Trying to get the user's tweet id
    try:
        tweet_id = int(request.args['tweetId'])
    except KeyError:
        traceback.print_exc()
        print("Key Error. Incorrect or missing key.")
        return Response("Incorrect or missing key.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occured.")
        return Response("Invalid tweet id.", mimetype="text/plain", status=400)

    # Trying to get the comments from the databse based on the tweet id
    comments = dbstatements.run_select_statement("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM users u INNER JOIN comment c ON c.user_id = u.id WHERE c.tweet_id = ?", [tweet_id,])

    # If the comments are not retrieved from the datbase, send a server error response
    if(comments == None):
        return Response("Failed to retrieve comments.", mimetype="text/plain", status=500)
    else:
        # If the comments are retrieved from the datbase, try sending the comments
        try:
            for comment in comments:
                each_comment = [
                    {
                        'commentId': comment[0],
                        'tweetId': comment[1],
                        'userId': comment[2],
                        'username': comment[3],
                        'content': comment[4],
                        'createdAt': comment[5]
                    }
                ]
            # Convert data into JSON
            each_comment_json = json.dumps(each_comment, default=str)
            # Send a client success response with the comments
            return Response(each_comment_json, mimetype="application/json", status=200)
        except UnboundLocalError:
            traceback.print_exc()
            print("each_comment is referenced before assignment.")
            return Response(f"Tweet with an id of {tweet_id} does not exist.", mimetype="text/plain", status=500)
        except:
            traceback.print_exc()
            print("An error has occured.")
            return Response("Invalid user id and/or tweet id.", mimetype="text/plain", status=400)