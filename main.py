from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data import db_session
from data.models import Product, Order
from flask import session


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your-secret-key'
db = SQLAlchemy(app)


def calculate_total(products):
    total = 0
    for product in products:
        total += int(product.price)
    return total

@app.before_request
def before_request():
    if 'cart' not in session:
        session['cart'] = {}


@app.route('/')
def index():
    from data.models import Product
    db_sess = db_session.create_session()
    products = db_sess.query(Product).all()
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    from data.models import Product
    db_sess = db_session.create_session()
    product = db_sess.query(Product).get(product_id)

    return render_template('product_details.html', product=product)


@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    product = db_sess.query(Product).get(product_id)

    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart

    db.session.commit()
    flash(f'Товар "{product.name}" добавлен в корзину', 'success')
    return redirect(request.referrer or url_for('index'))


@app.route('/cart')
def view_cart():
    cart_items = []
    total = 0

    cart = session.get('cart', {})
    products = db_sess.query(Product).filter(Product.id.in_(cart.keys())).all()

    for product in products:
        quantity = cart[str(product.id)]
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total += product.price * quantity

    return render_template('cart.html', cart_items=cart_items, total=total)


@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    cart_items = db_sess.query(Product).filter(Product.id.in_(cart.keys())).all()

    if not cart_items:
        flash('Ваша корзина пуста!', 'warning')
        return redirect(url_for('view_cart'))

    return render_template('checkout.html', cart_items=cart_items)


@app.route('/process_checkout', methods=['POST'])
def process_checkout():
    order = Order(
        user_id= None,
        total=calculate_total(session.get('cart')),
        status='pending',
        customer_name=request.form['name'],
        address=request.form['address'],
        phone=request.form['phone']
    )

    db.session.add(order)
    db.session.commit()

    session.pop('cart', None)

    db.session.commit()
    flash('Ваш заказ успешно оформлен!', 'success')
    return redirect(url_for('order_confirmation', order_id=order.id))


@app.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart

    flash('Товар удалён из корзины', 'info')
    return redirect(url_for('view_cart'))


@app.route('/cart/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    quantity = request.form.get('quantity', type=int)

    if not quantity or quantity < 1:
        flash('Некорректное количество', 'error')
        return redirect(url_for('view_cart'))

    cart = session.get('cart', {})
    if str(product_id) in cart:
        cart[str(product_id)] = quantity
        session['cart'] = cart
    else:
        flash('Товар не найден в корзине', 'error')
        return redirect(url_for('view_cart'))

    db.session.commit()
    flash('Количество обновлено', 'success')
    return redirect(url_for('view_cart'))


@app.route('/cart')
def cart():
    from data.models import Product
    cart = eval(request.cookies.get('cart', '{}'))
    products = []
    total = 0
    for product_id, quantity in cart.items():
        product = Product.query.get(product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total += product.price * quantity
    return render_template('cart.html', products=products, total=total)


if __name__ == '__main__':
    db_session.global_init('database.db')
    db_sess = db_session.create_session()
    app.run(port=8080, host='127.0.0.1', debug=True)
