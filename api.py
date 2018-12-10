#!flask/bin/python
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import json_util
from bson.objectid import ObjectId
import json
import os

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = os.environ['MONGO_URL']
mongo = PyMongo(app)

@app.route('/comments/all', methods=['GET'])
def get_all():
    # here we get all comments
    data = mongo.db.comments.find()
    l=[]
    for d in data :
        l.append(d)
    return json.dumps(l,default=json_util.default),200

@app.route('/comments/<string:_id>', methods=['GET'])
def get_comment(_id):
    # here we get comment based on its mongo id
    query = {"_id" : ObjectId(_id)}
    print(query)
    data = mongo.db.comments.find_one(query)
    return json.dumps(data,default=json_util.default), 200

@app.route('/comments', methods=['GET'])
def comment():
    # here we want to get a specific comment based on a query (i.e. ?user=some-value)
    query = request.args
    data = mongo.db.comments.find(query)
    l=[]
    for d in data:
        l.append(d)
    return json.dumps(l,default=json_util.default), 200

@app.route('/comments/', methods=['POST'])
def post_comment():
    # post one comment
    data = request.get_json()
    print(data)
    if data.get('user', None) is not None and data.get('item', None) is not None and data.get('comment', None) is not None and data.get('date', None) is not None:
        
        mongo.db.comments.insert_one(data)
        return jsonify({'ok': True, 'message': 'Comment created succesfully!'}), 200
    
    else:
        return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


@app.route('/comments/<string:_id>', methods=['DELETE'])
def delete_comment(_id):
    # delete one comment
    query = {"_id" : ObjectId(_id)}
    print(query)
    mongo.db.comments.delete_one(query)
    return {"ok" : True}, 200

@app.route('/comments/<string:_id>', methods=['POST'])
def update_comment(_id):
    # update one comment
    query = {"_id" : ObjectId(_id)}
    data = request.get_json()
    newvalues = { "$set": data}
    mongo.db.comments.update_one(query,newvalues)
    newdata = mongo.db.comments.find_one(query)
    return json.dumps(newdata,default=json_util.default), 200 


if __name__ == '__main__':
    app.run(debug=True)