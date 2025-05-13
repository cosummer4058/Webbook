import sqlalchemy
from sqlalchemy import orm
from data.db_session import SqlAlchemyBase


class OrderItem(SqlAlchemyBase):
    __tablename__ = 'order_items'

    order_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('orders.id'), primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('products.id'), primary_key=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    product_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    order = orm.relationship("Order", back_populates="items")
