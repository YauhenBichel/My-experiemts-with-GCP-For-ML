import pandas as pd
from flask import Flask, jsonify,request
import tensorflow as tf
import pre_process
import post_process


app = Flask(__name__)

model = tf.keras.models.load_model('model')

@app.route('/predict',methods=['POST','GET'])
def predict():
    req = request.json.get('instances')
    
    input_data = req[0]['email']

    #preprocessing
    text = pre_process.preprocess(input_data)
    vector = pre_process.preprocess_tokenizing(text)

    

    #predict
    prediction = model.predict(vector)

    #postprocessing
    value = post_process.postprocess(list(prediction[0])) 
    output = {
                'predictions':
                [{
                    'label' : value
                }]
            }
    return jsonify(output)

@app.route('/healthz')
def healthz():
    return "OK"


if __name__=='__main__':
    app.run(host='0.0.0.0')
