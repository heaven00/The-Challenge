"""Will be adding all the functions that i will be using in the controller here"""
from django.contrib.auth.hashers import check_password
from mongoengine.django.auth import User

def hybrid_authentication(username,password):
    try:
        if '@' in username and '.com' in username:
            user = User.objects(email=username)
        else:
            user = User.objects(username=username)
        if user:
            if password and check_password(password):
                return user
        else:
            return None