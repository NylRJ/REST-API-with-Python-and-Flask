from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [{
    'hotel_id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.5,
    'diaria': 420.34,
    'cidade': 'Rio de Janeiro'
}, {
    'hotel_id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 4.4,
    'diaria': 420.34,
    'cidade': 'Santa Catarina'
}, {
    'hotel_id': 'charlie',
    'nome': 'Charlie Hotel',
    'estrelas': 3.9,
    'diaria': 420.34,
    'cidade': 'Santa Catarina'
}

]


class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found.'}, 404  # not found

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "hotel_id '{}' already exists.".format(hotel_id)}, 400  # Bad request

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201 # create

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200  # success
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

        return {'message': 'Hotel not found.'}, 404  # not found


        novo_hotel = hotel_objeto.json()
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200  # ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201  # created criado

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'hotel deletado'}
