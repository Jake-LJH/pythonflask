from flask import Flask,jsonify, render_template, request,g
from config.Settings import Settings
import functools
import jwt
import re


def login_required(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        token = request.headers.get('Authorization')
        print(token)
        auth = True
        if token and token.index('Bearer')==0:
            token = token.split(' ')[1]
        else:
            auth = False
        if auth:
            try:
                payload = jwt.decode(token,Settings.secretKey,"HS256")
                g.role = payload['role']
                g.userid = payload['userid']
            except jwt.exceptions.InvalidSignatureError as err:
                print(err)
                auth = False
        if auth == False:
            output = {'Message': 'Error JWT'}
            return jsonify(output), 500


        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def require_admin(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if g.role == 'Admin':
            try:
                print('Approved')

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)       
        else:    
            output = {'Message': 'Not Authorised'}
            return jsonify(output), 500


        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def require_isAdminOrSelf(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):

        
        if g.role == 'Admin' or g.userid == kwargs['userid']:
            try:
                print(kwargs['userid'])

            except jwt.exceptions.InvalidSignatureError as err:
                print(err)       
        else:    
            output = {'Message': 'Not Authorised'}
            return jsonify(output), 500


        value = func(*args, **kwargs)
        return value
    return wrapper_decorator

def validateNum(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        password = request.json['password']
        pattern=re.compile('^[a-zA-Z0-9]{8,}$')
        
        try:
            if(pattern.match(password)): # match will return None if there is no match
                print('Input Match')
                value = func(*args, **kwargs)
                return value

            else:
                print('Input Not Match')
                output = {'Message': 'Input does not match pattern!'}
                return jsonify(output), 500
        except jwt.exceptions.InvalidSignatureError as err:
                print(err)

        
    return wrapper_decorator


