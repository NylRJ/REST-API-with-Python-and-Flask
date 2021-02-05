from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Usuário not found.'}, 404  # not found

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

    def post(self):
        atributos = reqparse.RequestParser()
        atributos.add_argument('login', type=str, required=True, help="The field 'login' cannot be left brank")
        atributos.add_argument('senha', type=str, required=True, help="The field 'senha' cannot be left brank")
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' alread exists.".format(dados['login'])}
        try:
            UserModel(**dados).save_user()
            return {'message': 'User Created with success '}, 201
        except:
            return {'message': 'An internal error ocurrend trying to save Usuário.'}, 500  # Internal server error

