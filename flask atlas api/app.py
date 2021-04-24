from flask import Flask
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId  # bson is in pymongo
from flask import jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mongoengine import MongoEngine


app = Flask(__name__)

db_name = "user"
db_password = str(input())

app.secret_key = "secret_key"


app.config['MONGO_URI'] = "mongodb+srv://vaishnav:{}@test.5ycd1.mongodb.net/{}?retryWrites=true&w=majority".format(
    db_password, db_name)

mongo = PyMongo(app)


@app.route('/add', methods=['POST'])
def add_user():
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']

    if _name and _email and _password and request.method == 'POST':
        _hashed_password = generate_password_hash(_password)
        id = mongo.db.user.insert(
            {'name': _name, 'email': _email, 'pwd': _hashed_password})

        resp = jsonify("User added successfully")

        resp.status_code = 200

        return resp

    else:
        return not_found()


@app.route('/users')
def users():
    users = mongo.db.user.find()
    resp = dumps(users)
    return resp


@app.route('/user/<id>')
def user(id):
    user = mongo.db.user.find_one({'_id': ObjectId(id)})
    resp = dumps(user)
    return resp


@app.route('/delete/<id>', methods=['DELETE'])
def delete_user(id):
    mongo.db.user.delete_one({'_id': ObjectId(id)})
    resp = jsonify("user deleted")
    resp.status_code = 200
    return resp


@app.route('/update/<id>', methods=['PUT'])
def update_user(id):
    _id = id
    _json = request.json
    _name = _json['name']
    _email = _json['email']
    _password = _json['pwd']
    if _name and _email and _password and _id and request.method == 'PUT':
        _hashed_password = generate_password_hash(_password)
        mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '%oid' in _id else ObjectId(
            _id)}, {'$set': {'name': _name, 'email': _email, 'pwd': _hashed_password}})

        resp = jsonify("User updated")
        resp.status_code = 200
        return resp

    else:
        return not_found()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not found' + request.url
    }

    resp = jsonify(message)

    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=True)
