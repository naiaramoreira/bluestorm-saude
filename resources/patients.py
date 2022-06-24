import datetime

from flask_restful import Resource, reqparse
from models.patients import PatientsModel
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument('name', type=str)
path_params.add_argument('last_name', type=str)
path_params.add_argument('birth_date', type=str)

class Patients(Resource):

    @staticmethod
    def get():
        return {'patient': [patient.json() for patient in PatientsModel.query.all()]}

class Patient(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('name', type=str, required=True, help="The field 'name' cannot be left blank.")
    atributos.add_argument('last_name', type=str, required=True, help="The field 'last name' cannot be left blank.")
    atributos.add_argument('birth_date', type=str, required=True, help="The field 'birth date' cannot be left blank.")

    @staticmethod
    def get(patient_id=None, name=None, last_name=None):
        patient = PatientsModel.find_patient(patient_id) if patient_id is not None else PatientsModel.find_patient(name=name, last_name=last_name)
        if patient:
            return patient.json()
        return {'message': 'Patient not found.'}, 404 # not found

    @staticmethod
    @jwt_required
    def post(patient_id):

        if PatientsModel.find_patient(patient_id):
            return {"message": "Patient is exist."}, 400

        dados = Patient.atributos.parse_args()
        patient = PatientsModel(**dados)
        try:
            patient.save_patient()
        except:
            return {'message': 'An error ocurred trying to create patient.'}, 500
        return patient.json()

    @staticmethod
    @jwt_required
    def delete(patient_id):
        patient = PatientsModel.find_patient(patient_id)
        if patient:
            patient.delete_patient()
            return {'message': 'Patient deleted.'}
        return {'message': 'Patient not found.'}, 404


    @staticmethod
    @jwt_required
    def put(patient_id=None, name=None, last_name=None):
        dados = Patient.atributos.parse_args()
        patient = PatientsModel(**dados)

        patient_found = PatientsModel.find_patient(patient_id, name, last_name)
        if patient_found:
            patient_found.update_patient(**dados)
            patient_found.save_patient()
            return patient_found.json(), 200
        patient.save_patient()
        return patient.json(), 201
