# Author: Naiara Lemos Moreira
# Resumo: Classe responsável para criar a tabela de pacientes,
# assim como fazer inserção e deleção do mesmo

from sql_alchemy import banco

class PharmaciesModel(banco.Model):
    __tablename__ = 'pharmacies'

    pharmacie_id = banco.Column(banco.Integer, primary_key=True)
    name = banco.Column(banco.String(40))
    city = banco.Column(banco.String(40))

    def __init__(self, name, city):
        self.name = name
        self.city = city

    def json(self):
        return {
            'pharmacie_id': self.pharmacie_id,
            'name': self.name,
            'city': self.city
        }

    @classmethod
    def find_pharmacie(cls, pharmacie_id=None, name=None, city=None):
        if pharmacie_id is not None:
            pharmacie = cls.query.filter_by(pharmacie_id=pharmacie_id).first()
        else:
            if name is not None and city is None:
                pharmacie = cls.query.filter_by(name=name).all()
            elif name is None and city is not None:
                pharmacie = cls.query.filter_by(city=city).all()
            else:
                pharmacie = cls.query.filter_by(name=name, city=city).all()

        if pharmacie:
            return pharmacie
        return None

    def save_pharmacie(self):
        banco.session.add(self)
        banco.session.commit()

    def update_pharmacie(self, name, city):
        self.name = name
        self.city = city

    def delete_pharmacie(self):
        banco.session.delete(self)
        banco.session.commit()
