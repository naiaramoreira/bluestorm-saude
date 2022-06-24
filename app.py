from flask import Flask, jsonify
from flask_restful import Api
from resources.users import User, UserRegister, UserLogin, UserLogout
from resources.patients import Patient, Patients
from resources.pharmacies import Pharmacie, Pharmacies
from resources.transactions import Transaction, Transactions
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'DontTellAnyone'
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

api = Api(app)
jwt = JWTManager(app)

@app.before_first_request
def cria_banco():
    banco.create_all()

@jwt.revoked_token_loader
def token_access_invalid():
    return jsonify({'message': 'You have been logged out.'}), 401 # unauthorized


api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(Patients, '/patients')
api.add_resource(Patient, '/patient/<string:patient_id>')
api.add_resource(Pharmacies, '/pharmacies')
api.add_resource(Pharmacie, '/pharmacie/<string:pharmacie_id>')
api.add_resource(Transactions, '/transactions')
api.add_resource(Transaction, '/transaction/<string:transaction_id>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
