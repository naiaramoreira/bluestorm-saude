import datetime

from flask_restful import Resource, reqparse
from models.pharmacies import PharmaciesModel
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument('name', type=str)
path_params.add_argument('city', type=str)

class Pharmacies(Resource):

    @staticmethod
    def get():
        return {'patient': [patient.json() for patient in PharmaciesModel.query.all()]}

class Pharmacie(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank.")
    atributos.add_argument('city', type=str, required=True, help="The field 'city' cannot be left blank.")

    @staticmethod
    def get(pharmacie_id=None, name=None, city=None):

        if pharmacie_id is None and name is None and city is None:
            return {'message': 'Pharmacie not found.'}, 404

        pharmacie = PharmaciesModel.find_pharmacie(pharmacie_id, name, city)
        if pharmacie:
            return pharmacie.json()
        return {'message': 'Pharmacie not found.'}, 404 # not found

    @staticmethod
    @jwt_required
    def post(pharmacie_id):

        if PharmaciesModel.find_pharmacie(pharmacie_id):
            return {"message": "Pharmacie is exist."}, 400

        dados = Pharmacie.atributos.parse_args()
        pharmacie = PharmaciesModel(**dados)
        try:
            pharmacie.save_pharmacie()
        except:
            return {'message': 'An error ocurred trying to create pharmacie.'}, 500
        return pharmacie.json()

    @staticmethod
    @jwt_required
    def put(pharmacie_id=None, name=None, city=None):
        dados = Pharmacie.atributos.parse_args()
        pharmacie = PharmaciesModel(**dados)

        if pharmacie_id is None and name is None and city is None:
            return {'message': 'Pharmacie not found.'}, 404

        pharmacie_found = PharmaciesModel.find_pharmacie(pharmacie_id, name, city)

        if pharmacie_found:
            pharmacie_found.update_pharmacie(**dados)
            pharmacie_found.save_pharmacie()
            return pharmacie_found.json(), 200
        pharmacie.save_pharmacie()
        return pharmacie.json(), 201

    @staticmethod
    @jwt_required
    def delete(pharmacie_id):
        pharmacie = PharmaciesModel.find_pharmacie(pharmacie_id)
        if pharmacie:
            pharmacie.delete_pharmacie()
            return {'message': 'Pharmacie deleted.'}
        return {'message': 'Pharmacie not found.'}, 404
