import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase

from sqlalchemy import orm


class Photo(SqlAlchemyBase):
    __tablename__ = 'photos'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.vk_id"))
    dataURI = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user = orm.relation('User')


