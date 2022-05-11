"""
Модуль для работы с БД.
"""
import sqlalchemy as db
from sqlalchemy import func


class UserModel:
    """
    Класс для работы с БД.
    """
    def __init__(self):
        self.engine = db.create_engine('sqlite:///game_of_life.db')
        self.connection = self.engine.connect()
        self.metadata = db.MetaData()
        self.users = db.Table('users', self.metadata, autoload=True, autoload_with=self.engine)

    # print(forum.columns.keys()) # заголовки столбцов

    def get_by_email(self, email):
        query = db.select([self.users.columns.id, self.users.columns.email, self.users.columns.password]).where(self.users.columns.email == email)
        result = self.connection.execute(query).fetchone()
        return result

    def create(self, data):
        query = self.users.insert().values(email=data['email'], password=data['password'])
        self.connection.execute(query)
        result = self.get_by_email(data['email'])
        return result['id']

    def get_by_id(self, user_id):
        query = db.select([self.users.columns.email, self.users.columns.password]).where(self.users.columns.id == user_id)
        result = self.connection.execute(query).fetchone()
        return result[0]
