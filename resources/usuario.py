from flask_restful import Resource, reqparse
from models.usuario import UserModel


class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'Hotel not found.'}, 404  # not found

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An error ocurrend trying to delete hotel.'}, 500  # Internal server error
            return {'message': 'hotel deletado'}
        return {'message': 'hotel not found.'}, 404  # not found
