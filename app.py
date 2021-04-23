# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iAxCWG6KFy__iY_277BYQemE4sKwqust
"""

import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('sample.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    if request.method == 'POST':
        sqft = int(request.form['sqft'])
        bath = int(request.form['bathrooms'])
        bhk = int(request.form['bedrooms'])
        location = request.form['location']

        model_list = [sqft, bath, bhk, location]
        x_col = model.get_booster().feature_names
        model_input = []

        model_input.append(model_list[0])
        model_input.append(model_list[1])
        model_input.append(model_list[2])
        for col in x_col[3:]:
          if col == model_list[3]:
            model_input.append(1)
          else:
            model_input.append(0)
        data = np.array([model_input])
        my_prediction = model.predict(data)
        output = round(my_prediction[0], 3)

    return render_template('sample.html', prediction_text='Price of the property would be around $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
