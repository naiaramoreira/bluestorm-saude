from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'users'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.Text, nullable=False, unique=True)
    password = banco.Column(banco.Text, nullable=False)

    def __init__(self, login, password):
        self.login = login
        self.password = password

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login
            }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).one_or_none()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
