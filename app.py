from flask import Flask, request, Response
from users import get_users, create_user, update_user, delete_user
from login import create_login, delete_login
from follows import create_follow, get_follows, delete_follow
from followers import get_followers
from tweets import get_tweets, create_tweet
import sys

app = Flask(__name__)

# Calling the function to get all users or one user
@app.get("/api/users")
def call_get_users():
    return get_users.get_users()

# Calling the function to create a user
@app.post("/api/users")
def call_create_user():
    return create_user.create_user()

# Calling the function to update a user
@app.patch("/api/users")
def call_update_user():
    return update_user.update_user()

# Calling the function to delete a user
@app.delete("/api/users")
def call_delete_users():
    return delete_user.delete_user()

# Calling the function to log in a user
@app.post("/api/login")
def call_create_login():
    return create_login.login_user()

# Calling the function to log out a user
@app.delete("/api/login")
def call_delete_login():
    return delete_login.logout_user()

# Calling the function to get all follows
@app.get("/api/follows")
def call_get_follows():
    return get_follows.get_all_follows()

# Calling the function to follow a user
@app.post("/api/follows")
def call_follow_user():
    return create_follow.follow_user()

# Calling the function to unfollow a user
@app.delete("/api/follows")
def call_unfollow_user():
    return delete_follow.unfollow_user()

# Calling the function to get all followers
@app.get("/api/followers")
def call_get_followers():
    return get_followers.get_all_followers()

# Calling the function to get tweets
@app.get("/api/tweets")
def call_get_tweets():
    return get_tweets.get_tweets()

# Calling the function to create a tweet
@app.post("/api/tweets")
def call_create_tweets():
    return create_tweet.post_tweet()

# Creating a mode
if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

# Checking which mode is used
if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5001)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()