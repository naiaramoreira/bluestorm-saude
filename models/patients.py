# Author: Naiara Lemos Moreira
# Resumo: Classe responsável para criar a tabela de pacientes,
# assim como fazer inserção e deleção do mesmo

import datetime
from sql_alchemy import banco

class PatientsModel(banco.Model):
    __tablename__ = 'patients'

    patient_id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(40))
    last_name = banco.Column(banco.String(40))
    birth_date = banco.Column(banco.Date)

    def __init__(self, name, last_name, birth_date):
        self.name = name
        self.last_name = last_name
        self.birth_date = datetime.date(int(birth_date[0:4]), int(birth_date[6:7]), int(birth_date[9:10]))

    def json(self):
        return {
            'patient_id': self.patient_id,
            'name': self.name,
            'last_name': self.last_name,
            'birth_date': str(self.birth_date)
        }

    @classmethod
    def find_patient(cls, patient_id=None, name=None, last_name=None):
        if patient_id is not None:
            patients = cls.query.filter_by(patient_id=patient_id).first()
        else:
            patients = cls.query.filter_by(name=name, last_name=last_name).first() if last_name is not None else cls.query.filter_by(name=name).first()

        if patients:
            return patients
        return None

    def save_patient(self):
        banco.session.add(self)
        banco.session.commit()

    def update_patient(self, name, last_name, birth_date):
        self.name = name
        self.last_name = last_name
        self.birth_date = datetime.date(int(birth_date[0:4]), int(birth_date[6:7]), int(birth_date[9:10]))

    def delete_patient(self):
        banco.session.delete(self)
        banco.session.commit()
