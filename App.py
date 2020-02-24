from flask_pymongo import PyMongo
from flask import Flask, jsonify, request, render_template, json

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'usermanagement'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/usermanagement'

mongo = PyMongo(app)
@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    # read the posted values from the UI
    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    # validate the received values
    if _name and _email and _password:
        return json.dumps({'html': '<span>All fields good !!</span>'})
    else:
        return json.dumps({'html': '<span>Enter the required fields</span>'})

@app.route('/users', methods = ['GET'])
def get_all_users():
    users = mongo.db.users
    output = []
    for user in users.find():
        output.append({'name': user['name'], 'phone': user['phone']})
    return jsonify({'result': output})

@app.route('/user', methods=['GET'])
def get_one_user():
    users = mongo.db.users
    name = request.json['name']
    user = users.find_one({'name': name})
    if user:
        output = {'name': user['name'], 'phone': user['phone']}
    else:
        output = 'No such name'
    return jsonify({'result': output})

@app.route('/user', methods = ['POST'])
def add_user():
    users = mongo.db.users
    name = request.json['name']
    phone = request.json['phone']
    user_id = users.insert({'name': name, 'phone': phone})
    new_user = users.find_one({'_id': user_id})
    output = {'name': new_user['name'], 'phone': new_user['phone']}
    return jsonify({'result': output})

if __name__ == '__main__':
    app.run(debug=True)