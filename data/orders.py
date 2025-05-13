import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.Enum('pending', 'paid', 'shipped', 'cancelled'), default='pending')
    total = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)

    user_id = orm.relationship('User', back_populates='orders')
    items = orm.relationship('OrderItem', back_populates='order')