from flask import Flask, request, Response
import dbstatements
import string
import random

# Creating a function that will generate a salt
def create_salt():
    # Creating a salt as 10 random characters
    letters_and_digits = string.ascii_letters + string.digits
    salt = ''.join((random.choice(letters_and_digits) for i in range(10)))
    # Return salt
    return salt

# Creating a function that will get the user's salt from the database given the user's email
def get_salt(email):
    # Trying to get the salt from the database
    user = dbstatements.run_select_statement("SELECT salt FROM users WHERE email = ?", [email,])
    # If the user's salt is retrieved from the database, return the salt
    if(len(user) == 1):
        return user[0][0]
    # if the user's salt is not retrieved from the database, send a server error response
    else:
        return Response("Failed to log in.", mimetype="text/plain", status=500)