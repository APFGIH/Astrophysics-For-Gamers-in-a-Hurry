from firebase_admin import credentials, firestore, auth
import firebase_admin
import hashlib

# Very super secure authentication library
# Jk this is very insecure
# For one, anyone can pull the entire database and mess with things
# This project was for english. So... yeah.

cred = credentials.Certificate('../fb.json')
firebase_admin.initialize_app(cred)

master_user = None
username = None

def hash(password, salt):
    return hashlib.sha512(str.encode(password + salt)).hexdigest()

def register(username, password):
    user = firebase_admin.firestore.client(app=None).collection('users').document(username).get().to_dict()

    if user:
        return 'Username already taken!'
    elif len(password) < 8:
        return 'Password must be at least 8 characters'
    elif password.lower() == 'password123':
        return 'Boi that\'s a really crappy password...'
    else:
        firebase_admin.firestore.client(app=None).collection('users').document(username).set(
                        {'password': hash(password, username),
                         'master_user': {}})

        return authenticate(username, password)


def authenticate(username, password):
    global master_user

    user = firebase_admin.firestore.client(app=None).collection('users').document(username).get().to_dict()

    if user and 'password' in user and hash(password, username) == user['password']:
        print('Successfully authenticated.')

        master_user = user['master_user']
        master_user['username'] = username

        return True
    else:
        print('Rejected.')
        return False

#def save():

if __name__ == '__main__':
    print(authenticate('test', 'asdassds'))
    print(master_user)