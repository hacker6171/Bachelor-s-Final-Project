from flask import Flask, render_template, request, send_from_directory
import os
import tensorflow as tf
import numpy as np
from keras.preprocessing import image

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/')
def homepage():
    return render_template('front.html')

@app.route('/', methods=['POST'])
def upload():
    if request.method == 'POST':
        # Handle file upload
        f = request.files['file']
        f.save(f.filename)
        fname = f.filename
        
        # Load the pre-trained model
        json_file = open('model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = tf.keras.models.model_from_json(loaded_model_json)
        loaded_model.load_weights("model1.h5")
        print("Loaded model from disk")

        # Preprocess the image for prediction
        test_image = image.load_img(fname, target_size=(300, 300, 3))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        # Predict the bird species
        result = loaded_model.predict(test_image)
        if result[0][0] == 1.0:
            res = "gull"
        elif result[0][1] == 1.0:
            res = "oriole"
        else:
            res = "sparrow"

        image_names = os.path.join('C:/Users/Win10/Desktop/myproject/images/final.jpg')
        return render_template('front.html', image_names=image_names, value=res)

@app.route('/<filename>')
def send_image(filename):
    return send_from_directory('final', filename)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
