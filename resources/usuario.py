from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from secrets import compare_digest

    
atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left blank")
class User (Resource):
    # /usuarios/{user_id}
    def get (self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message' : 'User not found.'}, 404
    
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user()
            return {"message" : "User deleted."}
        return {'message' : 'User not found.'}, 404 
    
class UserRegister(Resource):
    # cadastro
    def post (self):
        dados = atributos.parse_args()
        if UserModel.find_by_login(dados ['login']):
            return {'messege' : "The login '{}' already exists.".format(dados ['login'])}
        
        user = UserModel(**dados)
        user.save_user()
        return {'message' : 'User created successfully!'}, 201 # created
    

    
