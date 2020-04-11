import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    dataURI = sqlalchemy.Column(sqlalchemy.String, nullable=True)


