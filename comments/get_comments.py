from flask import request, Response
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
    except ValueError:
        traceback.print_exc()
        print("Invalid data was sent to the database.")
        return Response("Invalid data.", mimetype="text/plain", status=400)
    except:
        traceback.print_exc()
        print("An error has occurred.")
        return Response("An error has occurred.", mimetype="text/plain", status=400)

    # Checking to see if the tweet id exists in the database
    db_tweet_id = dbstatements.run_select_statement("SELECT id FROM tweet WHERE id = ?", [tweet_id,])

    # If the tweet id exists in the database, get the comments for that tweet
    if(len(db_tweet_id) == 1):
        # Getting the comments from the databse based on the tweet id
        comments = dbstatements.run_select_statement("SELECT c.id, c.tweet_id, c.user_id, u.username, c.content, c.created_at FROM users u INNER JOIN comment c ON c.user_id = u.id WHERE c.tweet_id = ? ORDER BY c.created_at DESC", [tweet_id,])
        # If the comments are not retrieved from the database, send a server error response
        if(comments == None):
            return Response("Failed to retrieve comments.", mimetype="text/plain", status=500)
        # If the comments are retrieved from the database, return comments as a list of dictionaries
        else:
            user_comments = []
            for comment in comments:
                each_comment = {
                    'commentId': comment[0],
                    'tweetId': comment[1],
                    'userId': comment[2],
                    'username': comment[3],
                    'content': comment[4],
                    'createdAt': comment[5]
                }
                user_comments.append(each_comment)
            # Convert data into JSON
            user_comments_json = json.dumps(user_comments, default=str)
            # Send a client success response with the JSON data
            return Response(user_comments_json, mimetype="application/json", status=200)
    # If the tweet id does not exist in the database, send a client error response
    else:
        return Response(f"Failed to retrieve comments.", mimetype="text/plain", status=400)