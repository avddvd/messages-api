from pymongo import MongoClient

s = 'mongodb+srv://todos:6CQxC4E4baqD7Cxm@backend-pesjv.mongodb.net'
client = MongoClient(s)
db = client.voicemail
users = db.users
messages = db.messages
connections = db.connections


def insertUser(user):
    try:
        existingUser = users.find_one({'name': user['name']})
        if not existingUser:
            users.insert_one(user)
            connections.insert_one({'name': user['name']})
            return {'success': 'user created'}
        else:
            return {'error': 'user already exists'}
    except Exception as e:
        print(e)
        return {'error': 'Internal server error'}


def fetchUser(userName):
    try:
        user = users.find_one({'name': userName})
        if not user:
            return {'error': 'user not found'}
        return user
    except Exception as e:
        print(e)
        return {'error': 'Internal server error'}


def insertMessage(message):
    try:
        messages.insert_one(message)
        return {'success': 'sent message'}
    except Exception as e:
        print(e)
        return {'error': 'Internal server error'}


def readMessages(user):
    try:
        c = messages.find({'receiver': user},
                          projection={'_id': False})
        return [m for m in c]
    except Exception as e:
        print(e)
        return {'error': 'Internal server error'}


def upsertConnections(user, friend):
    try:
        updates = {
            user: 'connections.' + friend,
            friend: 'connections.' + user
        }
        connections.update_one({'name': user},
                               {'$set': {updates[user]: True}})
        connections.update_one({'name': friend},
                               {'$set': {updates[friend]: True}})
        return {'success': 'connections added'}
    except Exception as e:
        print(e)
        return {'error': 'Internal server error'}
