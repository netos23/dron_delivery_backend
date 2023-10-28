import os
import cv2
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import numpy as np
from flask import Flask, request, jsonify
from keras.models import load_model
import urllib
from threading import Lock
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


class Classifier:
    def __init__(self):
        print("load model")
        self.cnn_model = load_model("model.h5")
        self.labels = ['fire', 'nofire']
        self.lock = Lock()

    def predict(self, img):
        im = self.preprocess_input(img)
        self.lock.acquire()
        ans = self.cnn_model.predict(im)
        self.lock.release()
        inn = np.argmax(ans)
        return inn

    def preprocess_input(self, image, im_size=350):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        res = cv2.resize(image, dsize=(im_size, im_size), interpolation=cv2.INTER_CUBIC) / 255
        res = np.expand_dims(res, axis=-1)
        return np.expand_dims(res, axis=0)

    def process_image(self, img):
        inn = self.predict(img)
        return self.labels[inn]


app = Flask(__name__)
classifier = Classifier()


@app.route('/classify', methods=['POST'])
def classify():
    global classifier
    jdata = request.get_json()
    urls = jdata
    ans = []
    for url in urls:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        res = opener.open(url)
        arr = np.asarray(bytearray(res.read()), dtype=np.uint8)
        img = cv2.imdecode(arr, -1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = np.asarray(img)
        print("Get image with shape: ", img.shape)
        ans.append(classifier.process_image(img))
    return jsonify(ans)

app.run(host='0.0.0.0', port=5000, debug=True)