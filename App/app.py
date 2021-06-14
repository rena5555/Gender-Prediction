import pickle
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, jsonify, flash, redirect
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing import image
import tensorflow as tf
Xception_Model = tf.keras.models.load_model('../Models/Xception_model.h5')
app = Flask(__name__)  
app.config['UPLOAD_FOLDER'] = 'static'

@app.route('/')  
def upload():  

    return render_template("upload.html")  
 
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(os.path.join('static/image', f.filename))
        images = os.listdir('static/image')
        images.sort()
     
        print(images)
        img_ = images[-1]
        
        #for file in os.listdir('static/image'):
        temp_path = 'static/image/'
        ext = img_.split('.')[-1]
      #  print(temp_path+image)
        if ext == 'jpeg' or ext == 'jpg' or ext =='png':
            img = image.load_img(temp_path + img_, target_size=(299, 299))
            img_batch = np.expand_dims(img, axis=0)
            prediction = np.argmax(Xception_Model.predict(img_batch), axis = 1)[0] 
              #  print(prediction)
            if prediction == 0:
                prediction = 'Female'
                return render_template("female.html", name = f.filename, prediction = prediction, img = img_)  
                  # lst.append(prediction)
            else:
                prediction = 'Male'
                return render_template("male.html", name = f.filename, prediction = prediction, img = img_)  
                 #  lst.append(prediction)  
             
            #return  str(np.argmax(Xception_Model.predict(img_batch), axis = 1)[0])
    else:
        return "Please upload jpg, jpeg, or png file"
        #return render_template("success.html", name = f.filename, prediction = prediction, img = file)  

@app.route('/uploads')  
def uploads():  
    return render_template("upload.html")  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=8084, debug = True) 

# pull skeleton from index.html
#@app.route('/', methods=['GET'])
#def main_page():
 #   return render_template("main_page.html")

#@app.route('/predict_gender', methods=['POST'])
##   text = str(request.form['text'])
  


#if __name__ == '__main__':
 
    

 #   app.run(host='0.0.0.0', port=8081, debug=True)