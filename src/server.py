from bottle import route, run
import time
import mongo


@route('/createUser/<name>')
def createUser(name):
    user = {
        'name': name,
        'timestamp': time.time(),
    }
    return mongo.insertUser(user)


@route('/findUser/<name>')
def findUser(name):
    return mongo.fetchUser(name)


@route('/addConnection/<from_user>/<to_user>')
def addConnection(from_user, to_user):
    if ('error' in mongo.fetchUser(from_user) or
            'error' in mongo.fetchUser(to_user)):
        return {'error': 'users not found'}
    status = mongo.upsertConnections(from_user, to_user)
    return status


@route('/sendMessage/<from_user>/<to_user>/<text>')
def sendMessage(from_user, to_user, text):
    if ('error' in mongo.fetchUser(from_user) or
            'error' in mongo.fetchUser(to_user)):
        return {'error': 'users not found'}
    message = {
        'sender': from_user,
        'receiver': to_user,
        'text': text,
        'timestamp': time.time()
    }
    status = mongo.insertMessage(message)
    return status


@route('/readMessages/<user>')
def readMessages(user):
    if 'error' in mongo.fetchUser(user):
        return {'error': 'users not found'}
    result = mongo.readMessages(user)
    return {'messages': result}


run(host='0.0.0.0', port=80, debug=True)
