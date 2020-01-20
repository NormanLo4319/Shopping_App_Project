# Shopping App Project
Utilizig machine learning models to create application for shopping recommendation.

## Background:
Our team wants to make grocery shopping more convenient. Because sometimes we go to grocery to purchase food to cook lunches or dinners, we don’t know what to purchase or what types of food to cook. Sometimes even we have an idea what to cook. It will end to miss purchase certain types of ingredients or not purchase enough amounts of food, then we couldn’t even cook the completed cuisines. 

The idea of this app allows for people to upload images of their desired food and check different recipes with comprehensive ingredients, instruction, cook time and calories by using their photos. According to people’s register information, the app can predict whether the person is in high or low obesity group. If she/he is in high obesity group, the app will recommend her/him a ranking of recipes by low calories to high calories. 

For each recipe, we also show each ingredient’s cost at amazon. People can compare costs from regular grocery with amazon.  


## How to use the app:
* Register/login
* Upload the food Images 
* View recipes
* Select the desired recipe to check what ingredients need and how to cook in detail

## Technologies:
*  Loaded data to database
*  Created flask 
*  Used Xception model and VGG19 model to predict   images
*  Built web pages HTML5
*  Used Javascript to upload and diplay images

### Home Page:
![home](README_images/home.png)

### Upload Food Image to Predict Page: 
![upload](README_images/upload.png)
![broccoli](README_images/broccoli.png)

### Recommend Recipes:
![recipes](README_images/recipes.png)

### Check A Desired Recipe:
![pancake](README_images/pancake.png)

### Fill Out Register Form to Predict Risk of Obesity
![register](README_images/register.png)

### Prediction Result of Risk of Obesity and BMI
![result](README_images/obesity_prediction.png)
