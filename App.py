from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "Secret Key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.app_context().push()


class data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    quantity = db.Column(db.String(10))
    price = db.Column(db.String(10))

    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price


@app.route('/')
def base():
    return render_template('base.html')


@app.route('/rewards_shop')
def rshop():
    all_data = data.query.all()
    name_data = data.query.get(request.form.get('name'))
    return render_template("rshop.html",all_data=all_data,name_data=name_data)


@app.route('/manage_rewards')
def rmanage():
    all_data = data.query.all()
    return render_template('rmanage.html',  all_data=all_data)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']

        my_data = data(name, quantity, price)
        db.session.add(my_data)
        db.session.commit()
        flash("Product Added Successfully")
        return redirect(url_for('rmanage'))


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = data.query.get(request.form.get('id'))
        my_data.name = request.form['name']
        my_data.quantity = request.form['quantity']
        my_data.price = request.form['price']
        db.session.commit()
        flash("Product Updated Successfully")
        return redirect(url_for('rmanage'))


@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    my_data = data.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Product Deleted Successfully")
    return redirect(url_for('rmanage'))


if __name__ == "__main__":
    app.run(debug=True)
