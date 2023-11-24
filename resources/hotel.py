from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
        {
        'hotel_id' : 'alpha',
        'nome' : 'Alpha Hotel',
        'estrelas' : 4.3,
        'diaria' : 521.30,
        'cidade' : 'São Paulo'
        },
        {
        'hotel_id' : 'barra',
        'nome' : 'Barra Hotel',
        'estrelas' : 4.8,
        'diaria' : 620.80,
        'cidade' : 'Salvador'
        },
        {
        'hotel_id' : 'copacabana',
        'nome' : 'Copacabana Hotel',
        'estrelas' : 4.9,
        'diaria' : 980.25,
        'cidade' : 'Rio de Janeiro'
        },
        {
        'hotel_id' : 'prainha',
        'nome' : 'Prainha Hotel',
        'estrelas' : 4.1,
        'diaria' : 285.30,
        'cidade' : 'Bertioga'
        },
        {
        'hotel_id' : 'bao',
        'nome' : 'Bão Hotel',
        'estrelas' : 4.6,
        'diaria' : 752.20,
        'cidade' : 'Belo Horizonte'
        },
        {
        'hotel_id' : 'galeria',
        'nome' : 'Galeria Hotel',
        'estrelas' : 4.6,
        'diaria' : 620.87,
        'cidade' : 'São Paulo'
        }
    
    ]
class Hoteis (Resource):
    def get (self):
        return {"hoteis" : hoteis}
    
class Hotel (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def find_hotel(self, hotel_id):
        for hotel in hoteis:
            if hotel ['hotel_id'] == hotel_id:
                return hotel
        return None

    def get (self, hotel_id):
        hotel = Hotel.find_hotel(self, hotel_id)
        if hotel:
            return hotel
        return {'message' : 'Hotel not found.'}, 404

    def post (self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'messege' : 'Hotel id "{}" alredy exists.'.format(hotel_id)}, 400 # Bad request
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        hoteis.append(novo_hotel)
        return novo_hotel, 201
    
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_ojeto = HotelModel (hotel_id, **dados)
        novo_hotel = hotel_ojeto.json()
        hotel = Hotel.find_hotel(self, hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200 # ok
        hoteis.append(novo_hotel)
        return novo_hotel, 201  # create 
    
    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel ["hotel_id"] != hotel_id]
        return {"message" : "Hotel deleted."}

    

        