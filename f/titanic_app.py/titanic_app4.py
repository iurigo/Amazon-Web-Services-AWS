from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

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
       surv = score[0,1]
       if surv>=0.5:
           surv2="You are alive!  Well done."
           pict = '/static/rose.jpg'
       else:
           surv2="Uh oh.  You are dead."
           pict = '/static/jack.png'

       return render_template(
          'results.html', surv = surv, surv2 = surv2, pict=pict)

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST, PORT)
