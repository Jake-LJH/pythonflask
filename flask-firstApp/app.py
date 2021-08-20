from flask import Flask,jsonify, render_template, request
from model.User import User
from validation.Validator import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

users = [
    {"userid"   : 1,
     "username" : "John", 
     "email"    : "john@gmailer.com", 
     "role"     : "member",
     "password" : "abc123"}
    ]

@app.route('/users', methods=['GET'])
#@login_required
#@require_admin
def getUsers():
    try:
        
        users = User.getUsers()
        output = {'Users':users}
        return jsonify(output), 200
        
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

@app.route('/users/<int:userid>', methods=['GET'])
# @login_required
# @require_isAdminOrSelf

def getOneUsers(userid):
    try:
        
        users = User.getUserByUserid(userid)
        
        if len(users)>0:
            output = {'Users':users}
            return jsonify(output), 200
        else:
            output={'Users':''}
            return jsonify(output), 404
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#POST 1 new user - Insert
@app.route('/users', methods=['POST'])
@validateNum
def insertUser():
    try:
        #extract the incoming request data from user
        userData = request.json
        username = userData['username']
        email = userData['email']
        role = userData['role']
        password = userData['password']

        count = User.insertUser(username, email, role, password)
        output = {'Rows Inserted': count}
        return jsonify(output), 201
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#retrieve users using query string

@app.route('/usersQuery', methods=['GET'])
@login_required
@require_admin
def getUsersByRole():
    try:
        queryString = request.args
        print(queryString)
        role = queryString['role']
        found = False
        userData = []
        for user in users:
            role0 = user['role']
            if role == role0:
                found = True
                userData.append(user)
                
        if found:
            output = {'Users':users}
            return jsonify(output), 200
        else:
            output={'Users':''}
            return jsonify(output), 404
        output = {'Users':users}
        return jsonify(output), 200
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#Delete Request    
@app.route('/users/<int:userid>', methods=['DELETE'])
@login_required
@require_isAdminOrSelf
def deleteUser(userid):
    try: 
        count = User.deleteUser(userid)
        
        if count == 1:
            output = {'message': 'User with '+str(userid)+' has been successfully deleted!'}
            return jsonify(output), 200
        else:
            output={'message': 'User with '+str(userid)+' does not exist!'}
            return jsonify(output), 404
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#Update Request    
@app.route('/users/<int:userid>', methods=['PUT'])
#@login_required
#@require_isAdminOrSelf
@validateNum
def updateUser(userid):
    try: 
        userData = request.json
        email = userData['email']
        password = userData['password']
        count = User.updateUser(userid, email, password)
        
        if count ==1:
            output = {'message': 'User with '+str(userid)+' has been successfully updated!'}
            return jsonify(output), 200
        else:
            output={'message': 'User with '+str(userid)+' does not exist!'}
            return jsonify(output), 404
    except Exception as err:
        print(err)
        output={'Message':'Error Occurrence'}
        return jsonify(output),500

#generating a resource, JWT - use POST method instead of GET
@app.route('/users/login', methods=['POST'])
def loginUsers():
    try:
        
        userJson=request.json
        output=User.loginUser(userJson)
        print(output)
        return jsonify(output)
    except Exception as err:
        print(err)
        return {},500


if __name__ == '__main__':
    app.run(debug=True)