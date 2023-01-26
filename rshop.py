from flask import Flask, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#Create a Flask Instance
app = Flask(__name__)
#Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rshop.db"
#Secret Key
app.config["SECRET_KEY"] = "s"
#initialise the Database
db = SQLAlchemy(app)

app.app_context().push()


# Create Model
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # Create a string
    def __repr__(self):
        return "<Name %r> <Price %r>" % self.name, self.price
# Add items form
class AddItemForm(FlaskForm):
    name=StringField("Name: ", validators=[DataRequired()])
    price=StringField("Price: ", validators=[DataRequired()])
    add = SubmitField("Add")

# create db
db.create_all()

@app.route("/")
def index():
    our_items = Items.query.order_by(Items.date_added)
    return render_template("rshop.html",our_items=our_items)

@app.route("/additem.html", methods=["GET","POST"])
def add_user():
    name = None
    price = None
    addform = AddItemForm()
    if addform.validate_on_submit():
        item = Items.query.filter_by(name=addform.name.data).first()
        if item is None:
            item = Items(name=addform.name.data,price=addform.price.data + " points")
            db.session.add(item)
            db.session.commit()
        name = addform.name.data
        addform.name.data = ""
        addform.price.data = ""
    return render_template("additem.html",addform=addform,name=name,price=price)


if __name__ == "__main__":
    app.run(debug=True)
