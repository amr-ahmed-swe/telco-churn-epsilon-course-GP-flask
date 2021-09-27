import os
import pandas as pd 
import numpy as np 
import flask
import pickle
from flask import Flask, render_template, request

app=Flask(__name__)

@app.route("/", methods=['GET'])
def index():
    return flask.render_template("index_1.html")

def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1,-1)
    loaded_model = pickle.load(open("model.pkl","rb"))
    result = loaded_model.predict(to_predict)
    return result[0]
test_data = []
@app.route('/predict',methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        test_data = [0,3,1,1,1,1,0,3,8,1,0]
        test_data[0] = to_predict_list[0] # Dependents
        test_data[1] = to_predict_list[1] # tenure
        test_data[2] = to_predict_list[2] # OnlineSecurity
        test_data[3] = to_predict_list[3] # OnlineBackup
        test_data[4] = to_predict_list[4] # DeviceProtection
        test_data[5] = to_predict_list[5] # TechSupport
        if test_data[2] == 1:
            test_data[6] = 0 # PaperlessBilling
        else:
            test_data[6] = 1
        test_data[7] = to_predict_list[6] # MONTHLY CHARGES
        test_data[8] = float(test_data[1]) * float(test_data[7]) # TOTAL CHARGES
        test_data[9] = to_predict_list[7] # Contract_1
        if test_data[9] ==  0:
            test_data[10] = 1 # Contract_2
        else:
            test_data[10] = 0 # Contract_2 
        to_predict_list = test_data
        to_predict_list = list(map(float, to_predict_list))
        result = ValuePredictor(to_predict_list)
        prediction = str(result)
        return render_template("predict.html",prediction=prediction)
if __name__ == "__main__":
    app.run(debug=True)