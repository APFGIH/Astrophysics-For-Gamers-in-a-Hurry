from firebase_admin import credentials, firestore, auth
import firebase_admin
import hashlib
import pickle
import os

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

        jar()

        return True
    else:
        print('Rejected.')
        return False

def jar():
    global master_user

    with open('s00pers3cuuret0k3n', 'wb') as file:
        pickle.dump(master_user, file)

def cucumber():
    global master_user

    try:
        with open('s00pers3cuuret0k3n', 'rb') as file:
            master_user = pickle.load(file)
            return True
    except:
        return False

def authenticated():
    return master_user

def save():
    if authenticated():
        firebase_admin.firestore.client(app=None).collection('users').document(master_user['username']).update(
                        {'master_user': master_user})

        jar()

        return True
    return False

def update():
    global master_user

    if authenticated():
        user = firebase_admin.firestore.client(app=None).collection('users').document(master_user['username']).get().to_dict()

        master_user = user['master_user']

        jar()

        return True
    return False

def logout():
    global master_user

    try:
        os.remove('s00pers3cuuret0k3n')
    except:
        pass

    master_user = {}

if __name__ == '__main__':
    #register('henry', hash('password', 'henry'))
    print(authenticate('henry', hash('password', 'henry')))
    print(master_user)

    master_user['pineapple'] = 'pineappleasdsdasasd'
    save()