import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)

    item = orm.relationship('OrderItem', back_populates='product_id')