from firebase_admin import credentials, firestore, auth
import firebase_admin
import hashlib

# Very super secure authentication library
# Jk this is very insecure
# For one, anyone can pull the entire database and mess with things
# This project was for english. So... yeah.

cred = credentials.Certificate('fb.json')
firebase_admin.initialize_app(cred)

master_user = {}

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
                        {'password': password,
                         'master_user': {}})

        return authenticate(username, password)

def authenticate(username, password):
    global master_user

    user = firebase_admin.firestore.client(app=None).collection('users').document(username).get().to_dict()

    if user and 'password' in user and password == user['password']:
        print('Successfully authenticated.')

        master_user = user['master_user']
        master_user['username'] = username

        return True
    else:
        print('Rejected.')
        return False

def authenticated():
    return master_user

def save():
    if authenticated():
        firebase_admin.firestore.client(app=None).collection('users').document(master_user['username']).update(
                        {'master_user': master_user})

        return True
    return False

def update():
    global master_user

    if authenticated():
        user = firebase_admin.firestore.client(app=None).collection('users').document(master_user['username']).get().to_dict()

        master_user = user['master_user']

        return True
    return False

if __name__ == '__main__':
    #register('henry', hash('password', 'henry'))
    print(authenticate('henry', hash('password', 'henry')))
    print(master_user)

    master_user['pineapple'] = 'pineappleasdsdasasd'
    save()