from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func



app = Flask(__name__)

# Database Setup
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.sqlite'
# db = SQLAlchemy(app)

engine = create_engine("sqlite:///db/data.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)
#Save references to each table
Recipe = Base.classes.recipes
Ingredient = Base.classes.ingredient

session = Session(engine)

# class recipes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), nullable=False)
#     ingredients = db.Column(db.Text, nullable=False)
#     time = db.Column(db.Float, nullable=False)
#     portion = db.Column(db.Float, nullable=False)
#     calories = db.Column(db.Float, nullable=False)
#     direction = db.Column(db.Text, nullable=False)
#     link = db.Column(db.Text, nullable=False)
    

# class ingredient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     recipes = db.Column(db.String(80), nullable=False)
#     ingredient = db.Column(db.Text, nullable=False)
#     cost = db.Column(db.Float, nullable=False)
#     sale = db.Column(db.Float, nullable=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/recipes")
def recipes():
    engine = create_engine("sqlite:///db/data.sqlite")

    # Reflect an existing database into a new model
    Base = automap_base()
    # Reflect the tables
    Base.prepare(engine, reflect=True)
    #Save references to each table
    Recipe = Base.classes.recipes
    Ingredient = Base.classes.ingredient

    session = Session(engine)

    recps = session.query(Recipe).filter(Recipe.name == 'Broccoli salad').all()
    ingres = session.query(Ingredient).filter(Ingredient.recipes == 'Broccoli salad').all()
    return render_template("recipe.html", recps=recps, ingres=ingres, title="Recipe")

if __name__ == "__main__":
    app.run(debug=True)