from flask import Flask, request, Response
import sys
import users

app = Flask(__name__)

# Calling the function to get all users or one user
@app.get("/api/users")
def call_get_users():
    return users.get_users()

# Calling the function to create a user
@app.post("/api/users")
def call_create_users():
    return users.create_user()

# Calling the function to delete a user
@app.delete("/api/users")
def call_delete_users():
    return users.delete_user()

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