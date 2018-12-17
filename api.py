#!flask/bin/python
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import requests
import os
import jwt
import datetime

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = os.environ['MONGO_URL']
mongo = PyMongo(app)

# __________________________________________________
#                   FUNCTIONS
# __________________________________________________

def get_token(req):
    auth_header = req.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return ''

def get_Username(auth_token):
# get Username(ID) from token
    try:
        payload = jwt.decode(auth_token, 'HUBLOVESFOUNDBADIEZSALIMALSO19951992ECAMLABO20185MIN')
        return payload['name']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def check_user(Username):
    url = 'http://user.ad5l.ecam.be/api/user/'+Username
    r = requests.get(url)
    return r.status_code 

def check_owner(Username, ItemID):
    url = 'http://order.ad5l.ecam.be/'+Username+ItemID
    r = requests.get(url)
    return r.status_code 

# __________________________________________________
#                   ROUTES
# __________________________________________________

@app.route('/comments/all', methods=['GET'])
# get all saved comments
def get_all():
    data = mongo.db.comments.find()
    l=[]
    for d in data :
        l.append(d)
    return json.dumps(l,default=json_util.default), 200

@app.route('/comments/<string:_id>', methods=['GET'])
# here we get one comment based on its mongo id
def get_comment_byId(_id):
    query = {"_id" : ObjectId(_id)}
    print(query)
    data = mongo.db.comments.find_one(query)
    return json.dumps(data,default=json_util.default), 200

@app.route('/comments', methods=['GET'])
# here we want to get a specific comment based on a query (i.e. ?user=some-value)
def get_comment():
    query = request.args
    data = mongo.db.comments.find(query)
    l=[]
    for d in data:
        l.append(d)
    return json.dumps(l,default=json_util.default), 200

@app.route('/comments/', methods=['POST'])
# create one comment
def post_comment():
    print(get_token(request))
    # Username = get_Username(get_token(request))
    # if check_user(Username)
    data = request.get_json()
    data['user'] = 'Username'
    print(data)
    data['date'] = datetime.datetime.now()
    # if check_owner(Username,itemID)
    if data.get('item', None) is not None and data.get('comment', None) is not None:
        mongo.db.comments.insert_one(data)
        return 'ok', 200
    else:
        return 'nok', 400


@app.route('/comments/<string:_id>', methods=['DELETE'])
# delete one comment
def delete_comment(_id):
    query = {"_id" : ObjectId(_id)}
    print(query)
    mongo.db.comments.delete_one(query)
    return 'ok', 200

@app.route('/comments/<string:_id>', methods=['POST'])
# update one comment
def update_comment(_id):
    print(get_token(request))
    # user = get_Username(get_token(request))
    query = {"_id" : ObjectId(_id)}
    data = request.get_json()
    # if user == data['user']
    newvalues = { "$set": data}

    mongo.db.comments.update_one(query,newvalues)
    newdata = mongo.db.comments.find_one(query)
    return json.dumps(newdata,default=json_util.default), 200 

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,
            host='0.0.0.0',
            port=port)