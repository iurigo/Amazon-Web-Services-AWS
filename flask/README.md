

# Intro to Flask Apps


## Introduction

Flask is a fast, lightweight way to connect your Python scripts to a server. It's a simple and robust framework that can do small tasks (create a microblog, stand up a simple API) or complex ones (Pinterest's API, create a twitter clone).

Let's jump in with a simple example. Then, we'll expand it to show what it can do with your models. But first you may need to:

```bash
$ pip install Flask
```

## Hello, world.
Create a new file called `hello.py` . Type in this code line by line. No copy pasting!

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Turings"

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)

```

To run your app, open a terminal window and launch from the folder which contains `hello.py`.

```python
python hello.py
 * Running on http://127.0.0.1:4000/ (Press CTRL+C to quit)
 ```

To see your app, open a browser and go to http://localhost:4000/.

We did a few things here:
- initialize the app (specifying a port)
- use built-in decorators to define what happens on a page
- launch the app

To close the app, hit `CTRL+C`.

## Passing an argument from the address

Add the below route after the `hello` function, but before you run the app.
```python
@app.route('/greet/<name>')
def greet(name):
    '''Say hello to your first parameter'''
    return "Hello, %s!" %name
```

Save and relaunch the app. Now navigate to http://localhost:4000/greet/phil. Your function should respond to that input!

## Basic styling with html

Since the `return` statement sends the output to an html page, you can style it directly with html tags if you want.

```python
@app.route("/")
def hello():
    return '''
    <body>
    <h2> Hello World! <h2>
    </body>
    '''
```

## Adding in machine learning!!

We can use Flask as a way to share and host our machine learning predictions.

Let's say you've built a model to predict survival on the Titanic.  In order to generate predictions, a user needs either to interact with your script in the terminal or a jupter notebook.  No fun.  Let's create a more user friendly way.

Create a new directory called `titanic_app`.  In the `titanic_app` folder, create a new file `titanic_app.py`. Import and initialize the flask app, and launch the server at the bottom. Leave room in the middle to add in your model and routes later on.

```python
from flask import Flask
app = Flask(__name__)

#-------- MODEL GOES HERE -----------#

#-------- ROUTES GO HERE -----------#

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'

    app.run(HOST, PORT)

```
## Build and train a model

We're going to add code to train a random forest.  

```python
#-------- MODEL GOES HERE -----------#
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv('../data/titanic.csv')
include = ['Pclass', 'Sex', 'Age', 'Fare', 'SibSp', 'Survived']

# Create dummies and drop NaNs
df['Sex'] = df['Sex'].apply(lambda x: 0 if x == 'male' else 1)
df = df[include].dropna()

X = df[['Pclass', 'Sex', 'Age', 'Fare', 'SibSp']]
y = df['Survived']

PREDICTOR = RandomForestClassifier(n_estimators=25).fit(X, y)
```

You could also train and test your model in a Jupyter notebook and pickle the fitted model. In that case your code would look something like this:

```python
with open('picked_model.pkl', 'r') as picklefile:
    PREDICTOR = pickle.load(picklefile)
```

## Make a simple API

Here's the fun part. Now that we have a PREDICTOR, we need to get some values to make our predictions.

One way to do this is to get information from the URL parameters. These are the part of a URL that come after the ? and are matched by key:value pairs. For example, if you navigate to: http://localhost:4000/predict?pclass=1&sex=1&age=18&fare=500&sibsp=0 Flask can retrieve that data for you.

Let's write a route to do just that:

```python
#-------- ROUTES GO HERE -----------#

@app.route('/predict', methods=["GET"])
def predict():
    pclass = request.args['pclass']
    sex = request.args['sex']
    age = request.args['age']
    fare = request.args['fare']
    sibsp = request.args['sibsp']

    item = [pclass, sex, age, fare, sibsp]
    score = PREDICTOR.predict_proba(item)
    results = {'survival chances': score[0,1], 'death chances': score[0,0]}
    return jsonify(results)

```
In order to have this run, you need to add `import` statements to import `request` and `jsonify` from `flask`.

And... voila! Save the file. Launch your app. You now have a simple API for your model.

Play with the parameters in the URL. You should get the predicted probability of death and survival.

For now, we're sending our results as a json (a file type that speaks really well with other web-stuff).

## Make a simple webform.

Well that was exciting. But it doesn't look very nice. Let's create a simple webform to read in the inputs.

We are going to use `render_template` to view this file.  Flask requires a very specific file structure for this.

Create a directory in the same folder as your app called `templates`.  

Create a file `page.html` in that directory.

```html
<!doctype html>
<html>
  <head>
    <title> Titanic Survivor-O-Matic </title>
  </head>
   <body>

      <form action = "http://localhost:4000/result" method = "POST">
         <p>Class <input type = "int" name = "pclass" /></p>
         <p>Sex <input type = "int" name = "sex" /></p>
         <p>Age <input type = "int" name = "age" /></p>
         <p>Fare <input type ="int" name = "fare" /></p>
         <p># of siblings <input type ="text" name = "sibsp" /></p>

         <p><input type = "submit" value = "submit" /></p>
      </form>

   </body>
</html>
```


Flask knows how to read form tags in an HTML file that have been POSTed to the server.

Add two new decorators in below your first one.  You also need to import `render_template` from `flask`.

```python
#---------- CREATING AN API, METHOD 2 ----------------#

# This method takes input via an HTML page
@app.route('/page')
def page():
   return render_template('page.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if request.method == 'POST':

       inputs = request.form

       pclass = int(inputs['pclass'])
       sex = int(inputs['sex'])
       age = int(inputs['age'])
       fare = int(inputs['fare'])
       sibsp = int(inputs['sibsp'])

       item = np.array([pclass, sex, age, fare, sibsp])
       score = PREDICTOR.predict_proba(item)
       results = {'survival chances': score[0,1], 'death chances': score[0,0]}
       return jsonify(results)

```
Save, close, and relaunch the app. Go to http://localhost:4000/page and type in your inputs.

Both methods should still be there. You can either play with the URL parameters at /predict or enter them at /page.


## Making a prettier output

That `render_template` function can also be used for the output.  And we can pass arguments to it.

In your `templates` folder, create a new file `results.html`.

```html
<html>
  <head>
    <title> Titanic Survivor-O-Matic </title>
  </head>
   <body>

     <h2>Hi there.  You have a {{surv}} chance of survival.<h2><br>
{{surv2}}
<br>
     <img src={{pict}}>
<br>
     <a href="http://localhost:4000/page">Try a new one.</a>

   </body>
</html>
```

Everywhere you see `{{}}`, we are going to pass arguments from our flask app.  

We are going to pass images to our page too.  Again, flask has a very specific file structure.  On the same level as `templates`, create a directory `static`.  Place the images there.

Update your app as follows:

```python


@app.route('/result', methods=['POST', 'GET'])
def result():
    '''Gets prediction using the HTML form'''
    if request.method == 'POST':
       inputs = request.form
       pclass = int(inputs['pclass'])
       sex = int(inputs['sex'])
       age = int(inputs['age'])
       fare = int(inputs['fare'])
       sibsp = int(inputs['sibsp'])

       item = np.array([pclass, sex, age, fare, sibsp])
       score = PREDICTOR.predict_proba(item)
       surv = score[0,1]
       if surv>=0.5:
           surv2="You are alive!  Well done."
           pict = '/static/rose.jpg'
       else:
           surv2="Uh oh.  You are dead."
           pict = '/static/jack.png'

       return render_template(
          'results.html', surv = surv, surv2 = surv2, pict=pict)

```



## Independent Practice
See if you can customize and play around with the app you just built. Try the following things:
- Create the model in jupyter / pycharm, pickle it, and import it into your flask app.  Play around with the features used, change the model (try logistic regression)
- Make the app look nicer by playing with the HTML.  Can you use dropdowns?  Buttons?
- See if you can return more values to the page, like the predicted category, or the model's parameters.


## Examples
Here are some examples of Flask apps in action. Fork and clone the apps you like so you can play with them and edit them on your local machine.

Two apps using scikit-learn:
- [Visualizing the Iris dataset using Flask and Angular JS](https://github.com/ColCarroll/flask_angular_example)
- [Using Neural Nets to recognize images](https://github.com/mdlai/digit_recognition)

More websites built in Flask:
- [The Flask Website itself!](http://flask.pocoo.org/)
- [A reddit clone](https://github.com/codelucas/flask_reddit)

## Additional Resources

- [The Flask Documentation](http://flask.pocoo.org/docs/0.11/)
- [A Flask tutorial to follow along with](https://github.com/miguelgrinberg/flask-pycon2014)
- [The Flask mega tutorial](http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates)
