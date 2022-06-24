import jwt
import json
from hmac import compare_digest
from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, unset_jwt_cookies, set_access_cookies
from models.users import UserModel

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
atributos.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")

class User(Resource):
    # /users/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404

class UserRegister(Resource):
    # /register
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' already exists.".format(dados['login'])}, 400 #Bad Request

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User created successfully!'}, 201 # Created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and compare_digest(user.password, dados["password"]):
            response = jsonify({"msg": "login successful"})
            access_token = create_access_token(identity=user.user_id)
            set_access_cookies(response, access_token)
            return {'access_token': access_token}, 200
        return {'message': 'The username or password is incorrect.'}, 401 # Unauthorized


class UserLogout(Resource):

    @jwt_required
    def post(self):
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response
