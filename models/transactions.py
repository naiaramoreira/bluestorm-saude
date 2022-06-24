# Author: Naiara Lemos Moreira
# Resumo: Classe responsável para criar a tabela de pacientes,
# assim como fazer inserção e deleção do mesmo

from sql_alchemy import banco

class TransactionsModel(banco.Model):
    __tablename__ = 'transactions'

    transaction_id = banco.Column(banco.Integer, primary_key=True)
    patient_id = banco.Column(banco.Integer, banco.ForeignKey('patients.patient_id'))
    pharmacie_id = banco.Column(banco.Integer, banco.ForeignKey('pharmacies.pharmacie_id'))
    amount = banco.Column(banco.Float(precision=4))
    date_transaction = banco.Column(banco.DateTime)

    def __init__(self, patient_id, pharmacie_id, amount, date_transaction=None):
        self.patient_id = patient_id
        self.pharmacie_id = pharmacie_id
        self.amount = amount
        self.date_transaction = date_transaction

    def json(self):
        return {
            'transaction_id': self.transaction_id,
            'patient_id': self.patient_id,
            'pharmacie_id': self.pharmacie_id,
            'amount': self.amount,
            'date_transaction': str(self.date_transaction)
        }

    @classmethod
    def find_transaction(cls, transaction_id):
        transaction = cls.query.filter_by(transaction_id=transaction_id).first()
        if transaction:
            return transaction
        return None

    def save_transaction(self):
        banco.session.add(self)
        banco.session.commit()

    def update_transaction(self, patient_id, pharmacie_id, amount, date_transaction):
        self.patient_id = patient_id
        self.pharmacie_id = pharmacie_id
        self.amount = amount
        self.date_transaction = date_transaction

    def delete_transaction(self):
        banco.session.delete(self)
        banco.session.commit()
