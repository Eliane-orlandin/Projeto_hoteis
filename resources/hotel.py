from flask_restful import Resource, reqparse
from models.hotel import HotelModel

class Hoteis (Resource):
    def get (self):
        return {"hoteis" : hoteis}
    
class Hotel (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome')
    argumentos.add_argument('estrelas')
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get (self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404

    def post (self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"messege" : "Hotel id '{}' alredy exists.".format(hotel_id)}, 400 # Bad request
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json()
    
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # ok
        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201  # create 
    
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {"message" : "Hotel deleted."}
        return {'message' : 'Hotel not found.'}, 404 

    

        