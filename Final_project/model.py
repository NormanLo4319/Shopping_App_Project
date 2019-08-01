''' Predict vegitables code here '''
#imports
import os
import io
import numpy as np

import keras
from keras.preprocessing import image
from keras.preprocessing.image import img_to_array
from keras.applications.xception import (
    Xception, preprocess_input, decode_predictions)
from keras import backend as K

from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pickle
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'food_test/test_images'

logit_model = pickle.load(open('./model/logit_model.pkl', 'rb'))
reg_model = pickle.load(open('./model/reg_model.pkl', 'rb'))


model = None
graph = None


def load_model():
    global model
    global graph
    model = Xception(weights="imagenet")
    graph = K.get_session().graph


load_model()


def prepare_image(img):
    img = img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    # return the processed image
    return img

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload_img', methods=['GET', 'POST'])
def upload_file():
    data = {"success": False}
    if request.method == 'POST':
        # if request.files.get('file'):
        if request.files.get('file'):
            # read the file
            file = request.files['file']

            # read the filename
            filename = file.filename

            # create a path to the uploads folder
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(filepath)

            # Load the saved image using Keras and resize it to the Xception
            # format of 299x299 pixels
            image_size = (299, 299)
            im = keras.preprocessing.image.load_img(filepath,
                                                    target_size=image_size,
                                                    grayscale=False)

            # preprocess the image and prepare it for classification
            image = prepare_image(im)


            global graph
            with graph.as_default():
                preds = model.predict(image)
                print(preds)
                results = decode_predictions(preds)
                print(results)

                prediction = []

                # loop over the results and add them to the list of
                # returned predictions
                for (imagenetID, label, prob) in results[0]:
                    prediction.append(label)
                
                page = []
                if prediction[0] == "broccoli":
                    page.append("broccoli_low.html")
                elif prediction[0] == "cucumber":
                    page.append("cucumber_low.html")
                else:
                    page.append("butternut_squash_low.html")
        return render_template(page)
    return render_template("upload_img.html")


@app.route('/broccoli_pancakes')
def broccoli_pancakes():
    return render_template("broccoli_pancakes.html", ingredients=ingredients , instruction=instruction, time=time , cost=broccoli_pancakes_cost)


@app.route('/register', methods=['GET', 'POST'])
def register():
   highsch = 1
   college = 0
   income = 20
   strenuous = 1
   read = 0
   highread = 0
   collegeread = 0

   if request.method == "POST":
       age = float(request.form["age"])
       age2 = (age)**2
       if request.form["gender"] == "male":
           male = 1
       else:
           male = 0
       if request.form["origin"] == "white":
           white = 1
           black = 0
           asian = 0
       elif request.form["origin"] == "black":
           white = 0
           black = 1
           asian = 0
       elif request.form["origin"] == "others":
           white = 0
           black = 1
           asian = 0
       else:
           white = 0
           black = 0
           asian = 1

       # data = request.form["age"]

       data = [age, age2, male, highsch, college, income, white, black, asian, strenuous, read, highread, collegeread]
       data = np.array([data])

       prediction1 = logit_model.predict(data)
       prediction2 = reg_model.predict(data)
       prediction2 = np.array(prediction2)

       if prediction1 == 0:
           result = "You are not at risk!"
       else:
           result = "You are at risk!"

       return render_template("prediction.html", data=data, result=result, title="Health Evaluation", BMI=prediction2)
   return render_template("register.html")

@app.route('/team')
def team():
    return render_template("team.html")


@app.route("/recipes", methods=[ "GET","POST"])
def recipes():
   recps = []
   ingres = []

   engine = create_engine("sqlite:///db/data.sqlite")
   # Reflect an existing database into a new model
   Base = automap_base()
   # Reflect the tables
   Base.prepare(engine, reflect=True)
   # Save references to each table
   Recipe = Base.classes.recipes
   Ingredient = Base.classes.ingredient
   # Create session for query
   session = Session(engine)

   if request.method == "POST":
       result = request.form["recipe"]

       recps = session.query(Recipe).filter(Recipe.name == result).all()
       ingres = session.query(Ingredient).filter(Ingredient.recipes == result).all()
       total = session.query(func.sum(Ingredient.cost)).filter(Ingredient.recipes == result).all()
       print(ingres)
       
       return render_template("recipe.html", recps=recps, ingres=ingres, total=total, title="Recipe")

   return render_template("broccoli_low.html")



@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/upload_img')
def upload_img():
     return render_template("upload_img.html")



if __name__ == "__main__":
    app.run(debug=True)
