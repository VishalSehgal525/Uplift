import numpy as np
import os
from flask import Flask, request, render_template
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing import image

from werkzeug.utils import secure_filename

app = Flask(__name__)

MODEL_PATH = "./emotion_model.json"
json_file = open(MODEL_PATH, 'r')
loaded_model_json = json_file.read()
json_file.close()
emotion_model = model_from_json(loaded_model_json)
emotion_model.load_weights("./emotion_model.h5")

print('Model loaded...')

def model_predict(img_path, model):
    emotion_dict = {
        0: "Angry", 
        1: "Disgusted", 
        2: "Fearful", 
        3: "Happy", 
        4: "Neutral", 
        5: "Sad", 
        6: "Surprised"
    }
    img = image.load_img(img_path, target_size=(48, 48), color_mode='grayscale')
    img_array = image.img_to_array(img)
    img_batch = np.expand_dims(img_array, axis=0)
    key = emotion_model.predict(img_batch)
    key = np.argmax(key)
    return emotion_dict[key]

@app.route("/", methods=['GET'])
def index():
    return render_template('home.html')

@app.route("/mood", methods=['GET', 'POST'])
def mood():
    return render_template('mood.html')

@app.route('/predict', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename)
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        preds = model_predict(file_path, emotion_model)
        return preds
    return None

if __name__=="__main__":
    app.run(debug=True)