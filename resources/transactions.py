import datetime

from flask_restful import Resource, reqparse
from models.transactions import TransactionsModel
from models.patients import PatientsModel
from models.pharmacies import PharmaciesModel
from flask_jwt_extended import jwt_required

path_params = reqparse.RequestParser()
path_params.add_argument('patient_id', type=int)
path_params.add_argument('pharmacie_id', type=int)
path_params.add_argument('amount', type=int)
path_params.add_argument('date_transaction', type=datetime)

class Transactions(Resource):

    @staticmethod
    def get():
        return {'transaction': [transaction.json() for transaction in TransactionsModel.query.all()]}

class Transaction(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('patient_id', type=int, required=True, help="The field 'patient_id' cannot be left blank.")
    atributos.add_argument('pharmacie_id', type=int, required=True, help="The field 'pharmacie_id' cannot be left blank.")
    atributos.add_argument('amount', type=int, required=True, help="The field 'amount' cannot be left blank.")
    atributos.add_argument('date_transaction', type=datetime, required=False, help="The field 'transaction_date' cannot be left blank.")

    @staticmethod
    def get(transaction_id):

        if transaction_id is None:
            return {'message': 'Transaction not found.'}, 404

        transaction = TransactionsModel.find_transaction(transaction_id)
        if transaction:
            return transaction.json()
        return {'message': 'Transaction not found.'}, 404 # not found

    @staticmethod
    @jwt_required
    def post(transaction_id):

        if TransactionsModel.find_transaction(transaction_id):
            return {"message": "Transaction is exist."}, 400

        dados = Transaction.atributos.parse_args()
        dados.date_transaction = datetime.datetime.now()
        transaction = TransactionsModel(**dados)

        try:
            transaction.save_transaction()
        except:
            return {'message': 'An error ocurred trying to create transaction.'}, 500

        patient = PatientsModel.find_patient(transaction.patient_id)
        pharmacie = PharmaciesModel.find_pharmacie((transaction.pharmacie_id))

        transaction = {
            'Patient': patient.json(),
            'Pharmacie': pharmacie.json(),
            'Transaction': transaction.json()
        }
        return transaction

    @staticmethod
    @jwt_required
    def put(transaction_id=None):
        dados = Transaction.atributos.parse_args()
        dados.date_transaction = datetime.datetime.now()
        transaction = TransactionsModel(**dados)

        if transaction is None:
            return {'message': 'Transaction not found.'}, 404

        transaction_found = TransactionsModel.find_transaction(transaction_id)
        transaction_found.date_transaction = datetime.datetime.now()

        if transaction_found:
            transaction_found.update_transaction(**dados)
            transaction_found.save_transaction()

            patient = PatientsModel.find_patient(transaction_found.patient_id)
            pharmacie = PharmaciesModel.find_pharmacie(transaction_found.pharmacie_id)

            transaction_found = {
                'Patient': patient.json(),
                'Pharmacie': pharmacie.json(),
                'Transaction': transaction_found.json()
            }
            return transaction_found, 200

        transaction.save_transaction()
        return transaction.json(), 201

    @staticmethod
    @jwt_required
    def delete(transaction_id):
        transaction = TransactionsModel.find_transaction(transaction_id)
        if transaction:
            transaction.delete_transaction()
            return {'message': 'Transaction deleted.'}
        return {'message': 'Transaction not found.'}, 404
