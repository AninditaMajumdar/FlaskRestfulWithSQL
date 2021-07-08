from user import User

def authenticate(username,password):       #  to generate jwt token
    user = User.find_by_username(username)
    if user and user.password == password:
        return user

def identity(payload):                      #when api request made
    user_id = payload['identity']   #content of jwt
    return User.find_by_id(user_id)