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

from flask import Flask, request, redirect, url_for, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'food_test/test_images'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/data.db'


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
    broccoli_pancakes = recipes.query.filter_by(name="Savory Broccoli Pancakes").first()
    ingredients = broccoli_pancakes.ingredients
    time = broccoli_pancakes.time
    instruction = broccoli_pancakes.direction
    broccoli_pancakes_cost = ingredient.query.filter_by(name="Savory Broccoli Pancakes").first()
    cost = broccoli_pancakes_cost.cost

    return render_template("broccoli_pancakes.html", ingredients=ingredients , instruction=instruction, time=time , cost=broccoli_pancakes_cost)


@app.route('/register')
def register():
    return render_template("register.html")


@app.route('/team')
def team():
    return render_template("team.html")

@app.route('/recipes')
def recipes():
     return render_template("recipes.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/upload_img')
def upload_img():
     return render_template("upload_img.html")

@app.route('/broccoli_high')
def broccoli_high():
    return render_template("broccoli_high.html")

@app.route('/broccoli_low')
def broccoli_low():
    return render_template("broccoli_low.html")

@app.route('/cucumber_high')
def cucumber_high():
    return render_template("cucumber_high.html")

@app.route('/cucumber_low')
def cucumber_low():
    return render_template("cucumber_low.html")

@app.route('/butternut_squash_high')
def butternut_squash_high():
    return render_template("butternut_squash_high.html")

@app.route('/butternut_squash_low')
def butternut_squash_low():
    return render_template("butternut_squash_low.html")


@app.route('/broccoli_salad')
def broccoli_salad():
    return render_template("broccoli_salad.html")

@app.route('/broccoli_soup')
def broccoli_soup():
    return render_template("broccoli_soup.html")

@app.route('/butternut_squash_beef')
def butternut_squash_beef():
    return render_template("butternut_squash_beef.html")

@app.route('/butternut_squash_pizza')
def butternut_squash_pizza():
    return render_template("butternut_squash_pizza.html")

@app.route('/butternut_squash_soup')
def butternut_squash_soup():
    return render_template("butternut_squash_soup.html")

@app.route('/chicken_cucumber')
def chicken_cucumber():
    return render_template("chicken_cucumber.html")

@app.route('/cucumber_salad')
def cucumber_salad():
    return render_template("cucumber_salad.html")


@app.route('/watermelon_cucumber')
def watermelon_cucumber():
    return render_template("watermelon_cucumber.html")



if __name__ == "__main__":
    app.run(debug=True)
