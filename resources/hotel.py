from flask_restful import Resource

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
    def get (self, hotel_id):
        for hotel in hoteis:
            if hotel ['hotel_id'] == hotel_id:
                return hotel
        return {'message' : 'Hotel not found.'}, 404
        