from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import safe_str_cmp

atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left brank")
atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left brank")


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário not found.'}, 404  # not found

    @jwt_required
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurrend trying to delete Usuário.'}, 500  # Internal server error
            return {'message': 'Usuário deletado'}
        return {'message': 'Usuário not found.'}, 404  # not found


class UserRegister(Resource):
    # Cadastro de Usuário

    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' alread exists.".format(dados['login'])}, 409
        try:
            UserModel(**dados).save_user()
            return {'message': 'User Created with success '}, 201
        except:
            return {'message': 'An internal error ocurrend trying to save Usuário.'}, 500  # Internal server error


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acess = create_access_token(identity=user.user_id)
            return {'access_token': token_de_acess}, 200
        return {'message': 'The username or password is incorrect.'}, 401  # Unauthorized

