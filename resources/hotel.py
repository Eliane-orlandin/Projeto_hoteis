from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade = None,
                          estrelas_min = 0,
                          estrelas_max = 5,
                          diaria_min = 0,
                          diaria_max = 10000,
                          limit = 5,
                          offset = 0, **dados):
    if cidade: 
        return {
        'estrelas_min' : estrelas_min,
        'estrelas_max' : estrelas_max,
        'diaria_min' : diaria_min,
        'diaria_max' : diaria_max,
        'cidade' : cidade,
        'limit' : limit,
        'offset' : offset
        }
    return {
        'estrelas_min' : estrelas_min,
        'estrelas_max' : estrelas_max,
        'diaria_min' : diaria_min,
        'diaria_max' : diaria_max,
        'cidade' : cidade,
        'limit' : limit,
        'offset' : offset
    }

path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type = str)
path_params.add_argument('estrelas_min', type = float)
path_params.add_argument('estrelas_max', type = float)
path_params.add_argument('diaria_min', type = float)
path_params.add_argument('diaria_max', type = float)
path_params.add_argument('limit', type = float)
path_params.add_argument('offset', type = float)

class Hoteis(Resource):
    query_params = reqparse.RequestParser()
    query_params.add_argument("cidade", type=str, default="", location="args")
    query_params.add_argument("estrelas_min", type=float, default=0, location="args")
    query_params.add_argument("estrelas_max", type=float, default=0, location="args")
    query_params.add_argument("diaria_min", type=float, default=0, location="args")
    query_params.add_argument("diaria_max", type=float, default=0, location="args")

    def get(self):
        filters = Hoteis.query_params.parse_args()

        query = HotelModel.query

        if filters["cidade"]:
            query = query.filter(HotelModel.cidade == filters["cidade"])
        if filters["estrelas_min"]:
            query = query.filter(HotelModel.estrelas >= filters["estrelas_min"])
        if filters["estrelas_max"]:
            query = query.filter(HotelModel.estrelas <= filters["estrelas_max"])
        if filters["diaria_min"]:
            query = query.filter(HotelModel.diaria >= filters["diaria_min"])
        if filters["diaria_max"]:
            query = query.filter(HotelModel.diaria <= filters["diaria_max"])

        return {"hoteis": [hotel.json() for hotel in query]}
    
class Hotel (Resource):

    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be left blank")
    argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' cannot be left blank")
    argumentos.add_argument('diaria')
    argumentos.add_argument('cidade')

    def get (self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message' : 'Hotel not found.'}, 404
    
    @jwt_required()
    def post (self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"messege" : "Hotel id '{}' alredy exists.".format(hotel_id)}, 400 # Bad request
        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return { 'message' : 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json()
    
    @jwt_required()
    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200 # ok
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return { 'message' : 'An internal error ocurred trying to save hotel.'}, 500
        return hotel.json(), 201  # create 
    
    @jwt_required()
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'messege' : 'An error ocurred trying to delete hotel.'}, 500
            return {"message" : "Hotel deleted."}
        return {'message' : 'Hotel not found.'}, 404 

    

        