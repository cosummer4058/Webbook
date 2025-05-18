import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from data.db_session import SqlAlchemyBase

from werkzeug.security import generate_password_hash, check_password_hash


class Product(SqlAlchemyBase):
    __tablename__ = 'products'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                          primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String(100), nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text)

    order_items = orm.relationship('OrderItem', back_populates='product')


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                          primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                             unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    orders = orm.relationship('Order', back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


class Order(SqlAlchemyBase):
    __tablename__ = 'orders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    status = sqlalchemy.Column(sqlalchemy.Enum('pending', 'paid', 'shipped', 'cancelled'), default='pending')
    total = sqlalchemy.Column(sqlalchemy.Numeric(10, 2), nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))

    user = orm.relationship('User', back_populates='orders')
    items = orm.relationship('OrderItem', back_populates='order')


class OrderItem(SqlAlchemyBase):
    __tablename__ = 'order_items'

    order_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey('orders.id'),
                               primary_key=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer,
                                 sqlalchemy.ForeignKey('products.id'),
                                 primary_key=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    product_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)

    order = orm.relationship('Order', back_populates='items')
    product = orm.relationship('Product', back_populates='order_items')
