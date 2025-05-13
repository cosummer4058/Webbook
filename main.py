from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired

from data import db_session
from data.products import Product

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/')
def index():
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    return render_template('index.html', products=products)